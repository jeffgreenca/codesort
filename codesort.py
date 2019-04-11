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

def _top_x_hits(nodes, x):
    for k in sorted(nodes, key=nodes.get, reverse=True)[:x]:
        yield (round(nodes[k], 5), k)

def main(repo_path, count, limit, bare=False, single=False):
    """List most "important" files in a git repo.

    Implements Aron Lurie's method, see details at:
        http://redd.it/bb7qst
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
        graph.add_edge(e[0], e[1], distance=1/t)
    finish(s)

    if single:
        s = start("computing betweenness")
        nodes = networkx.betweenness_centrality(graph, weight='distance')
    else:
        s = start("computing betweenness (via parallel processes)")
        nodes = multi.betweenness_centrality_parallel(graph, weight='distance')
    finish(s)

    for hit in _top_x_hits(nodes, count):
        if bare:
            print("%s" % hit[1])
        else:
            print("%s\t%s" % hit)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("-v", "--verbose", action="store_true", help="Show timings")
    parser.add_argument("-n", "--num-results", default=12, type=int, metavar='N', help="Return only top N results")
    parser.add_argument("-c", "--commits", default=None, type=int, metavar='N', help="Max number of commits to traverse")
    parser.add_argument("-b", "--bare", action="store_true", help="Return sorted filenames (without scores)")
    parser.add_argument("-s", "--single", action="store_true", help="Disable parallel processing of betweenness score (might be needed for very small repositories)")
    parser.add_argument("repo", help="Path to target repository")
    args = parser.parse_args()
    verbose = args.verbose
    main(args.repo, count=args.num_results, limit=args.commits, bare=args.bare, single=args.single)

