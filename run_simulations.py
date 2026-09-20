"""Random dynamic-evacuation simulations.

For every non-exit node, a random number (at least 2) of random nodes are blocked and the
shortest route to the nearest reachable exit is plotted.

Usage:
    python run_simulations.py                       # one run per node
    python run_simulations.py --seed 1 --max-blocked 8 --runs 3

Images go to simulations/<source>_to_<exit>_blocked_<nodes>.png and a summary
is written to simulations/summary.csv.
"""
import argparse
import csv
import os
import random

import matplotlib
matplotlib.use("Agg")

from dijkstra import dijkstra, path_length
from graph import build_graph, EXIT_NODES
from graph_data import ABComplex_data


def nearest_exit(source, blocked):
    """Return (exit, path, length) for the closest reachable exit, or None."""
    best = None
    for exit_node in EXIT_NODES:
        path = dijkstra(ABComplex_data, source, exit_node, blocked)
        if path is None:
            continue
        length = path_length(ABComplex_data, path)
        if best is None or length < best[2]:
            best = (exit_node, path, length)
    return best


def random_scenario(source, rng, min_blocked, max_blocked):
    """Pick a random blocked set that still leaves some exit reachable."""
    candidates = [n for n in ABComplex_data if not n.startswith("E") and n != source]
    while True:
        blocked = set(rng.sample(candidates, rng.randint(min_blocked, max_blocked)))
        result = nearest_exit(source, blocked)
        if result:
            return blocked, result


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--seed", type=int, default=None, help="random seed for repeatable runs")
    parser.add_argument("--min-blocked", type=int, default=2, help="minimum blocked nodes per run")
    parser.add_argument("--max-blocked", type=int, default=6, help="maximum blocked nodes per run")
    parser.add_argument("--runs", type=int, default=1, help="scenarios per source node")
    parser.add_argument("--out", default="simulations", help="output directory")
    args = parser.parse_args()

    if not 1 <= args.min_blocked <= args.max_blocked:
        parser.error("--min-blocked must be at least 1 and no more than --max-blocked")

    rng = random.Random(args.seed)
    os.makedirs(args.out, exist_ok=True)
    sources = [n for n in ABComplex_data if not n.startswith("E")]

    rows = []
    for source in sources:
        for run in range(args.runs):
            blocked, (exit_node, path, length) = random_scenario(source, rng, args.min_blocked, args.max_blocked)
            blocked_names = "_".join(sorted(blocked, key=int))
            name = f"{source}_to_{exit_node}_blocked_{blocked_names}"
            if args.runs > 1:
                name += f"_run{run + 1}"
            build_graph(source, exit_node, blocked, save_path=os.path.join(args.out, name + ".png"))
            rows.append([source, exit_node, len(blocked), " ".join(sorted(blocked, key=int)),
                         "-".join(path), length])

    with open(os.path.join(args.out, "summary.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "exit", "num_blocked", "blocked", "path", "distance_m"])
        writer.writerows(rows)
    print(f"Saved {len(rows)} images and summary.csv to {args.out}/")


if __name__ == "__main__":
    main()
