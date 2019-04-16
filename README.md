# codesort

Given a git repository, identify the most "central" source files based on commit history.

```
$ docker run --rm -v /path/to/your/repo:/repo:ro jeffgreenca/codesort:latest
```

When approaching an unknown code base, for example as a maintenance programmer, this provides a clue about which source files to examine first.

## summary and credits
This follows [Aron Lurie's method](http://redd.it/bb7qst).  In short, compute [betweenness centrality](https://en.wikipedia.org/wiki/Betweenness_centrality) on a graph constructed from reading commit history.

Vertices of the graph represent individual files in the repository, and edges are added between vertices (u, v) when files u and v appear in the same commit.  Edge weights are assigned based on the inverse count of commits wherein the two vertices appear together (so, files that are highly correlated have a low edge weight).
 
## usage example

### run with docker
Mount your repository to `/repo` and run the container:
```
$ docker run --rm -v /path/to/your/repo:/repo:ro jeffgreenca/codesort
25.00%	app/file1.py
 8.00%	app/lib/__init__.py
 4.00%	tox.ini
 2.00%	Dockerfile
...
``` 

### run with pipenv
Requires [pipenv](https://pipenv.readthedocs.io/en/latest/).  Setup:
```
$ git clone https://github.com/jeffgreenca/codesort.git
$ cd codesort && pipenv install
```

Run with path to your repository:
```
$ pipenv run python codesort.py /path/to/repository
25.00%	app/file1.py
 8.00%	app/lib/__init__.py
 4.00%	tox.ini
 2.00%	Dockerfile
...
```

The output is in format `score<TAB>filepath` per line where `score` is the ranking of betweenness centrality score, descending.

## advanced usage

```
$ ./codesort.py -h
usage: codesort.py [-h] [-v] [-n N] [-c N] [-b] [-s] [-e EXPORT] [-r] repo

List most "important" files in a git repo. Implements Aron Lurie's method, see
details at: http://redd.it/bb7qst

positional arguments:
  repo                  Path to target repository

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Show timings
  -n N, --num-results N
                        Return only top N results
  -c N, --commits N     Max number of commits to traverse
  -b, --bare            Return sorted filenames (without scores)
  -s, --single          Disable parallel processing of betweenness score
                        (might be needed for very small repositories)
  -e EXPORT, --export EXPORT
                        Save graph in GraphML format
  -r, --raw             Show raw scores (instead of percentage rank)
```

## contributing

Contributions welcome - bug reports, feature requests, pull requests.

## code of conduct

Be kind.
