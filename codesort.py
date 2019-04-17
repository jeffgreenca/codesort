from git import Repo
from collections import Counter
from itertools import combinations
from pprint import pprint
import networkx
import argparse
import time
import multi


def iter_files_per_commit(r, limit=None):
    """Iterate over lists of files per commit"""

    # TODO include all branches?
    count = 0
    for commit in r.iter_commits():
        count += 1
        if limit is not None and count > limit:
            return
        if not commit.parents:
            return
        file_list = r.git.diff("%s~1..%s" % (commit, commit), name_only=True)
        yield file_list.split("\n")


def start(x):
    if verbose:
        print("%s..." % x, end="", flush=True)
    return time.time()


def finish(s):
    if verbose:
        print("ok (%ss)" % round(time.time() - s, 2), flush=True)


def _top_x_hits(bb, x, raw=False):
    total = sum(bb.values())
    for k in sorted(bb, key=bb.get, reverse=True)[:x]:
        if raw:
            yield (round(bb[k], 6), k)
        else:
            yield ("%5.1f%%" % (bb[k] * 100 / total), k)


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
    for related_files in iter_files_per_commit(repo, limit):
        for edge in combinations(related_files, 2):
            togetherness[edge] += 1
    finish(s)

    s = start("building networkx graph")
    graph = networkx.Graph()
    for e, t in togetherness.items():
        graph.add_edge(e[0], e[1], distance=1 / t)
    finish(s)

    if single:
        s = start("computing betweenness")
        bb = networkx.betweenness_centrality(graph, weight="distance")
    else:
        # TODO if erro IndexError: list index out of range fallback
        s = start("computing betweenness (via parallel processes)")
        bb = multi.betweenness_centrality_parallel(graph, weight="distance")
    finish(s)

    if export:
        s = start("saving graph to %s" % export)
        networkx.set_node_attributes(graph, values=bb, name="betweenness")
        networkx.write_graphml(graph, export)
        finish(s)

    for hit in _top_x_hits(bb, count, show_raw_scores):
        if bare:
            print("%s" % hit[1])
        else:
            print("%s\t%s" % hit)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("-v", "--verbose", action="store_true", help="Show timings")
    parser.add_argument(
        "-n",
        "--num-results",
        default=12,
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
    parser.add_argument(
        "-s",
        "--single",
        action="store_true",
        help="Disable parallel processing of betweenness score (might be needed for very small repositories)",
    )
    parser.add_argument("-e", "--export", type=str, help="Save graph in GraphML format")
    parser.add_argument(
        "-r",
        "--raw",
        action="store_true",
        help="Show raw scores (instead of percentage rank)",
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
