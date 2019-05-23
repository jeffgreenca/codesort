# codesort

Given a git repository, identify the most "central" source files based on
commit history.

```
$ docker run --rm -v /path/to/your/repo:/repo:ro jeffgreenca/codesort:latest
```

When approaching an unknown code base, for example as a maintenance programmer,
this provides a clue about which source files to examine first.

![annotated graph via Cytoscape](graph.png)
> Example graph rendered via [Cytoscape](https://cytoscape.org/) from codesort
> output

## summary and credits
This follows [Aron Lurie's method
@medium](https://medium.com/@a.lurie_78598/using-graph-theory-to-decide-where-to-start-reading-source-code-74a1e2ddf72).
In short, compute [betweenness
centrality](https://en.wikipedia.org/wiki/Betweenness_centrality) on a graph
constructed from reading commit history.

Vertices of the graph represent individual files in the repository, and edges
are added between vertices (u, v) when files u and v appear in the same commit.
Edge weights are assigned based on the inverse count of commits wherein the two
vertices appear together (so, files that are highly correlated have a low edge
weight).

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

The output format is `score<TAB>filepath` per line where `score` is the ranking
of betweenness centrality score, descending.

## advanced usage

```
$ docker run --rm jeffgreenca/codesort --help
usage: codesort.py [-h] [-v] [-n N] [-c N] [-b] [-r] repo

List most "important" files in a git repo. Implements Aron Lurie's method, see
details at: https://bit.ly/2v6M3X0

positional arguments:
  repo                  Path to target repository

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Show timings
  -n N, --num-results N
                        Return only top N results
  -c N, --commits N     Max number of commits to traverse
  -b, --bare            Return sorted filenames (without scores)
  -r, --raw             Show raw scores (default is percentage rank)
```

> NOTE: when using the docker image, arg `repo` is already specified for you.

## about `networkit`

Initially, I used the friendly, approachable
[networkx](http://networkx.github.io/) package.  It has an excellent API and
installs easily.

Unfortunately, my `networkx` based implementation was painfully slow for large
repositories.

I switched to [networkit](https://networkit.github.io/) for a significant speed
boost.  This came at the cost of more development time to get the install
working, and slightly more complex code due to additional record-keeping
requirements, but pays off when running `codesort` on large repositories (and
frankly, if the repository isn't large, why bother using this tool anyway?).

## contributing

Contributions welcome.  Please apply [black](https://github.com/python/black).

## code of conduct

Be kind.
