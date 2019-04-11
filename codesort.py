from git import Repo
from collections import Counter
from itertools import combinations
from pprint import pprint
from graph_tool.all import *
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

    file_to_id = dict()
    id_to_file = dict()

    s = start("counting togetherness")
    togetherness = Counter()
    index = 0
    for related_files in iter_files_per_commit(repo):
        #print("related files: ", related_files)
        for fname in related_files:
            file_to_id[fname] = index
            id_to_file[index] = fname
            index += 1
        for edge in combinations(related_files, 2):
            togetherness[edge] += 1
    finish(s)

    s = start("building graph-tool graph")
    graph = Graph(directed=False)
    e_dist = graph.new_edge_property("float")
    for e, t in togetherness.items():
        edge = graph.add_edge(file_to_id[e[0]], file_to_id[e[1]])
        e_dist[edge] = 1/t
    finish(s)

    s = start("computing betweenness")
    vprop_result, _ = graph_tool.centrality.betweenness(graph, weight=e_dist)
    finish(s)

    nodes = { id_to_file[v]: vprop_result[v] for v in graph.vertices() }

    for hit in _top_x_hits(nodes, count):
        print("%s\t%s" % hit)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("-v", "--verbose", action="store_true", help="Show timings")
    parser.add_argument("-c", "--count", default=10, type=int, metavar='N', help="Maximum files to return")
    parser.add_argument("repo", help="Path to target repository")
    args = parser.parse_args()
    verbose = args.verbose
    main(args.repo, args.count)

