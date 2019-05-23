#!/usr/bin/python3
# codesort.py - jeffgreenca 2019
from git import Repo

from collections import Counter
from itertools import combinations
import argparse
import time

# Temporary hack to suppress networkit stdout "warnings"
# thanks https://codingdose.info/2018/03/22/supress-print-output-in-python/
# TODO fix after patch to networkit lands switching to system warnings lib
import io
from contextlib import redirect_stdout

null = io.StringIO()
with redirect_stdout(null):
    from networkit import graph, centrality


def iter_files_per_commit(r, limit=None):
    """Iterate over lists of files per commit, by calling git log"""
    sep = "<|>"
    kwargs = {"name_only": True, "format": "format:%s" % sep}
    if limit:
        args["max_count"] = limit
    log = r.git.log(**kwargs)
    for commit in log.split(sep + "\n"):
        files = [f.strip() for f in commit.split("\n") if f.strip()]
        if files:
            yield files


# verbose display of runtime durations
def start(x):
    if verbose:
        print("%s..." % x, end="", flush=True)
    return time.time()


def finish(s):
    if verbose:
        print("ok (%ss)" % round(time.time() - s, 2), flush=True)


def _top_x_hits(bb, x, raw=False):
    """Return nicely formatted list of scores by file"""
    if not raw:
        total = sum((score for _, score in bb))
    for node, score in sorted(bb, key=lambda x: x[1], reverse=True)[:x]:
        if raw:
            yield ("%8.6f" % round(score, 6), node)
        else:
            yield ("%5.1f%%" % (score * 100 / total), node)


def main(
    repo_path,
    count,
    limit,
    bare=False,
    single=False,
    export=None,
    show_raw_scores=False,
):
    """List most "important" files in a git repo.

    Implements Aron Lurie's method, see details at:
        https://bit.ly/2v6M3X0
    """
    repo = Repo(repo_path)

    s = start("counting togetherness")
    togetherness = Counter()
    file_to_id = dict()
    id_to_file = dict()
    i = 0
    for related_files in iter_files_per_commit(repo, limit):
        related_files_by_id = []
        for f in related_files:
            try:
                related_files_by_id.append(file_to_id[f])
            except KeyError:
                related_files_by_id.append(i)
                file_to_id[f] = i
                id_to_file[i] = f
                i += 1
        for edge in combinations(related_files_by_id, 2):
            togetherness[edge] += 1
    finish(s)

    s = start("building networkit graph")
    g = graph.Graph(weighted=True)
    for i in range(len(file_to_id)):
        g.addNode()

    for e, t in togetherness.items():
        g.addEdge(e[0], e[1], 1 / t)
    finish(s)

    s = start("computing betweenness")
    # accurate, slow calculation
    b = centrality.Betweenness(g, normalized=True)
    # TODO - maybe allow toggling between accurate and estimate methods
    # faster but not as precise (10x better in a benchmark test)
    # b = networkit.centrality.EstimateBetweenness(g, 128, normalized=True, parallel=True)
    b.run()
    bb = b.ranking()
    finish(s)

    if export:
        raise NotImplementedError("Not implemented for networkit")
        # TODO implement networkit based export
        #  consider need for node id to filename conversion
        # s = start("saving graph to %s" % export)
        # networkx.set_node_attributes(graph, values=bb, name="betweenness")
        # networkx.write_graphml(graph, export)
        # finish(s)

    for hit in _top_x_hits(bb, count, show_raw_scores):
        if bare:
            print(f"{id_to_file[hit[1]]}")
        else:
            print(f"{hit[0]}\t{id_to_file[hit[1]]}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("-v", "--verbose", action="store_true", help="Show timings")
    parser.add_argument(
        "-n",
        "--num-results",
        default=24,
        type=int,
        metavar="N",
        help="Return only top N results",
    )
    parser.add_argument(
        "-c",
        "--commits",
        default=None,
        type=int,
        metavar="N",
        help="Max number of commits to traverse",
    )
    parser.add_argument(
        "-b",
        "--bare",
        action="store_true",
        help="Return sorted filenames (without scores)",
    )
    # TODO implement networkit based export
    # parser.add_argument(
    #    "-e", "--export", type=str, metavar="FILE", help="Save graph in GraphML format"
    # )
    parser.add_argument(
        "-r",
        "--raw",
        action="store_true",
        help="Show raw scores (default is percentage rank)",
    )
    parser.add_argument("repo", help="Path to target repository")
    args = parser.parse_args()
    verbose = args.verbose
    main(
        args.repo,
        count=args.num_results,
        limit=args.commits,
        bare=args.bare,
        single=args.single,
        export=args.export,
        show_raw_scores=args.raw,
    )
