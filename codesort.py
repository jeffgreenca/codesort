import networkx
from git import Repo
import argparse

def iter_files_per_commit(r):
    """Iterate over lists of files per commit"""
    for commit in r.iter_commits():
        # files = [b.name for b in commit.tree.diff("HEAD~1").traverse()]
        #print(commit, files)
        #for diff in commit.diff("HEAD~1"):
        #    print(help(diff))
        file_list = r.git.diff("%s~1..%s" % (commit, commit), name_only=True)
        yield file_list.split("\n")

def main(repo_path):
    repo = Repo(repo_path)

    graph = networkx.Graph()
    for related_files in iter_files_per_commit(repo):
        print("related files: ", related_files)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", help="Path to target repository")
    args = parser.parse_args()
    if args.repo:
        main(args.repo)

