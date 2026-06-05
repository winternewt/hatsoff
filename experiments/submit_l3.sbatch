#!/bin/bash
#SBATCH --job-name=hatsoff-l3
#SBATCH --output=experiments/slurm-%j.out
#SBATCH --nodes=1                 # raise for multi-node; tasks shard the work
#SBATCH --ntasks=3               # one task per A100
#SBATCH --gpus-per-task=1        # binds one GPU per task (CUDA_VISIBLE_DEVICES)
#SBATCH --cpus-per-task=8        # CPU for the Gallai-Edmonds matching
#SBATCH --time=12:00:00
#SBATCH --mem-per-cpu=4G
#
# Multi-node SLURM launcher for the L3 zero-mode percolation campaign.
# Work is sharded by global task rank; each task writes its own JSONL shard
# (experiments/l3_campaign.rank###.jsonl) so there is no cross-node contention.
# Re-submitting (or --requeue) resumes from the shards. Aggregate with
#   uv run python experiments/aggregate_campaign.py   (reads all shards)
#
# Tune statistics / runtime:
#   HATSOFF_STAGE_A_MAX_R, HATSOFF_STAGE_B_MAX_R  realization caps
#   HATSOFF_STAGE_A_HOURS, HATSOFF_STAGE_B_HOURS  per-rank wall-clock budgets
#
# For >1 node, raise --nodes and --ntasks together (e.g. 3 nodes x 1 GPU =
# --nodes=3 --ntasks=3), or pack GPUs per node as the cluster allows.

set -euo pipefail
cd "${SLURM_SUBMIT_DIR:-.}"

export HATSOFF_GPU=1
export HATSOFF_STAGE_A_MAX_R=${HATSOFF_STAGE_A_MAX_R:-300}
export HATSOFF_STAGE_B_MAX_R=${HATSOFF_STAGE_B_MAX_R:-600}
export HATSOFF_STAGE_A_HOURS=${HATSOFF_STAGE_A_HOURS:-6}
export HATSOFF_STAGE_B_HOURS=${HATSOFF_STAGE_B_HOURS:-11}

# One Python process per SLURM task; SLURM sets SLURM_PROCID / SLURM_NTASKS /
# SLURM_LOCALID which the script reads for sharding and GPU binding.
srun uv run python experiments/l3_campaign_cluster.py

# Final aggregation once all tasks finish (single rank does it).
uv run python experiments/aggregate_campaign.py
