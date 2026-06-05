"""Multi-node (SLURM) edition of the L3 zero-mode percolation campaign.

Same per-unit physics as ``l3_campaign.py`` (imported, not duplicated), with:

  * **Work sharding** across SLURM tasks: each global rank computes the units
    whose deterministic index ≡ rank (mod ntasks).  Seeds depend only on
    (level/window, p, realization), so results are rank-independent and
    identical to the single-node run.
  * **Per-rank JSONL shards** ``l3_campaign.rank{NNN}.jsonl`` — no cross-node
    append contention.  Resume globs all shards (plus the single-node file).
  * **Optional GPU eigh** (the dominant cost): set ``HATSOFF_GPU=1`` to run the
    dense symmetric eigendecomposition on CUDA via PyTorch (fp64), one GPU
    bound per task.  Gallai–Edmonds matching stays on CPU.

Env knobs (all optional):
  HATSOFF_GPU=1                 use CUDA eigh if torch+GPU available
  HATSOFF_STAGE_A_MAX_R=300     raise the Stage A realization cap
  HATSOFF_STAGE_B_MAX_R=600     raise the Stage B realization cap
  HATSOFF_STAGE_A_HOURS / _B_HOURS   per-rank wall-clock budgets (see base)

Launch (see experiments/submit_l3.sbatch): one task per A100, e.g.
  srun --ntasks=3 --gpus-per-task=1 python experiments/l3_campaign_cluster.py
Run repeatedly / after a requeue — it resumes from the shards.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

import l3_campaign as base  # noqa: E402
from hatsoff import support  # noqa: E402


def rank_world() -> tuple[int, int]:
    """Global task rank and task count from SLURM (fallback 0/1 locally)."""
    rank = int(os.environ.get("SLURM_PROCID", os.environ.get("RANK", "0")))
    world = int(os.environ.get("SLURM_NTASKS", os.environ.get("WORLD_SIZE", "1")))
    return rank, max(1, world)


def maybe_enable_gpu() -> str:
    """Bind one GPU per task and route dense eigh through CUDA if requested.

    Returns a short backend description for logging.
    """
    if os.environ.get("HATSOFF_GPU") != "1":
        return "cpu"
    import torch  # noqa: PLC0415 - optional cluster-only dependency

    if not torch.cuda.is_available():
        return "cpu (no CUDA)"
    local = int(os.environ.get("SLURM_LOCALID", "0"))
    device = torch.device(f"cuda:{local % torch.cuda.device_count()}")
    torch.cuda.set_device(device)

    def gpu_eigh(dense: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        t = torch.from_numpy(np.ascontiguousarray(dense)).to(device, torch.float64)
        evals, evecs = torch.linalg.eigh(t)
        return evals.cpu().numpy(), evecs.cpu().numpy()

    support.set_dense_eigh(gpu_eigh)
    return f"cuda:{device.index} ({torch.cuda.get_device_name(device)})"


def load_done_all() -> set[str]:
    """Union of completed keys across every shard and the single-node file."""
    done: set[str] = set()
    for path in sorted(base.EXP_DIR.glob("l3_campaign*.jsonl")):
        done |= base.load_done(path)
    return done


def env_int(name: str, default: int) -> int:
    return int(os.environ.get(name, str(default)))


def safe_record(out_path: Path, compute, key: str, stage: str,
                done: set[str]) -> None:
    """Run one unit, append it to this rank's shard; isolate per-unit failures.

    A stochastic numerical failure (e.g. a LAPACK non-convergence) must not
    abort the rank.  The key is marked done either way so a requeue does not
    re-hit a deterministic failure.
    """
    try:
        rec = compute()
    except Exception as exc:  # noqa: BLE001 - isolate any per-unit failure
        rec = {"stage": stage, "error": repr(exc)}
        print(f"UNIT FAILED {key}: {exc!r}", flush=True)
    rec["key"] = key
    base.append_record(out_path, rec)
    done.add(key)


def stage_a_specs(max_r: int):
    for r in range(max_r):
        for level in base.STAGE_A_LEVELS:
            for p in base.P_GRID:
                if p == 0.0 and r > 0:
                    continue
                yield (level, p, r)


def stage_b_specs(max_r: int):
    for r in range(max_r):
        for frac in base.STAGE_B_FRACTIONS:
            for p in base.P_GRID:
                if p == 0.0 and r > 0:
                    continue
                yield (frac, p, r)


def main() -> None:
    rank, world = rank_world()
    backend = maybe_enable_gpu()
    out_path = base.EXP_DIR / f"l3_campaign.rank{rank:03d}.jsonl"
    log = lambda m: print(f"[rank {rank}/{world}] {m}", flush=True)  # noqa: E731

    t0 = time.time()
    graphs = {lvl: base.build_tb_graph(base.generate_tiling(lvl))
              for lvl in (2, 3)}
    log(f"graphs built in {time.time() - t0:.1f}s; eigh backend = {backend}")

    done = load_done_all()
    log(f"resume: {len(done)} units already done across all shards")

    a_max = env_int("HATSOFF_STAGE_A_MAX_R", base.STAGE_A_MAX_R)
    b_max = env_int("HATSOFF_STAGE_B_MAX_R", base.STAGE_B_MAX_R)

    # ----- Stage A (full L2/L3 graphs) -----
    started = time.time()
    budget = base.STAGE_A_HOURS * 3600
    n = 0
    for idx, (level, p, seed) in enumerate(stage_a_specs(a_max)):
        if idx % world != rank:
            continue
        key = base.make_key("A", level, "full", p, seed)
        if key in done:
            continue
        safe_record(out_path, lambda lv=level, pp=p, sd=seed:
                    base.stage_a_unit(lv, graphs, pp, sd), key, "A", done)
        n += 1
        if n % 10 == 0:
            log(f"stage A: {n} units, {(time.time() - started) / 3600:.2f}h")
        if time.time() - started > budget:
            log("stage A budget reached")
            break

    # ----- Stage B (support spanning on crop windows) -----
    verts, adj = graphs[base.STAGE_B_LEVEL]
    graphlike = SimpleNamespace(nodes=verts,
                                neighbors=base.neighbors_from_adj(adj))
    extent = float(min(np.ptp(verts[:, 0]), np.ptp(verts[:, 1])))
    windows = {f: base.crop_square(graphlike, L=f * extent,
                                   boundary_thickness=base.BOUNDARY_THICKNESS)
               for f in base.STAGE_B_FRACTIONS}
    started = time.time()
    budget = base.STAGE_B_HOURS * 3600
    n = 0
    for idx, (frac, p, seed) in enumerate(stage_b_specs(b_max)):
        if idx % world != rank:
            continue
        key = base.make_key("B", base.STAGE_B_LEVEL, frac, p, seed)
        if key in done:
            continue
        safe_record(out_path, lambda fr=frac, pp=p, sd=seed:
                    base.stage_b_unit(windows[fr], fr, pp, sd), key, "B", done)
        n += 1
        if n % 10 == 0:
            log(f"stage B: {n} units, {(time.time() - started) / 3600:.2f}h")
        if time.time() - started > budget:
            log("stage B budget reached")
            break

    log(f"done; shard -> {out_path.name}")


if __name__ == "__main__":
    main()
