from git import Repo
from collections import Counter
from itertools import combinations
from pprint import pprint
import networkx
import argparse
import time

def iter_files_per_commit(r):
    """Iterate over lists of files per commit"""

    # TODO include all branches?
    for commit in r.iter_commits():
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

def main(repo_path, count=10):
    """List most "important" files in a git repo.

    Implements Aron Lurie's method, see details at:
        http://redd.it/bb7qst
    """
    repo = Repo(repo_path)

    s = start("counting togetherness")
    togetherness = Counter()
    for related_files in iter_files_per_commit(repo):
        #print("related files: ", related_files)
        for edge in combinations(related_files, 2):
            togetherness[edge] += 1
    finish(s)

    s = start("building networkx graph")
    graph = networkx.Graph()
    for e, t in togetherness.items():
        graph.add_edge(e[0], e[1], distance=1/t)
    finish(s)

    s = start("computing betweenness")
    nodes = networkx.betweenness_centrality(graph, weight='distance')
    finish(s)

    for hit in _top_x_hits(nodes, count):
        print("%s\t%s" % hit)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("-v", "--verbose", action="store_true", help="Show timings")
    parser.add_argument("-c", "--count", default=10, help="Maximum files to return")
    parser.add_argument("repo", help="Path to target repository")
    args = parser.parse_args()
    verbose = args.verbose
    main(args.repo, args.count)

