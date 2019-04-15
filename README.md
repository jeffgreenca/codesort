# codesort

Given a git repository, identify the most "central" source files based on commit history.

When approaching an unknown code base, for example as a maintenance programmer, this provides a clue about which source files to examine first.

## summary and credits
This follows the method described by [Aron Lurie's method](http://redd.it/bb7qst).

In short, compute [betweenness centrality](https://en.wikipedia.org/wiki/Betweenness_centrality) on a graph constructed from reading commit history.

Vertices of the graph represent individual files in the repository, and edges are added between vertices (u, v) when files u and v appear in the same commit.  Edge weights are assigned based on the inverse count of commits two vertices appear together (so files that are highly correlated have a low weight).

## usage example

### run with docker
Mount your repository to `/repo` and run the container:
```
$ docker run --rm -v /path/to/your/repo:/repo:ro jeffgreenca/codesort
0.33939	app/file1.py
0.2707	app/lib/__init__.py
0.15025	tox.ini
0.11347	Dockerfile
...
``` 

### run with pipenv
Setup with [pipenv](https://pipenv.readthedocs.io/en/latest/):
```
$ pipenv install
```

Provide full path to your repository:
```
$ pipenv run python codesort.py /path/to/repository
0.33939	app/file1.py
0.2707	app/lib/__init__.py
0.15025	tox.ini
0.11347	Dockerfile
...
```

The output is in format `score<TAB>filepath` per line where `score` is the betweenness centrality score, sorted descending by score.

## advanced usage example

See `codesort.py -h` for all options.

For example, show timings and limit number of commits to last 100 from HEAD of kubernetes repo:
```
$ python codesort.py ~/repos/kubernetes/ -v -c 100
counting togetherness...ok (3.1s)
building networkx graph...ok (0.45s)
computing betweenness...ok (87.59s)
0.05958 staging/src/k8s.io/apiextensions-apiserver/go.mod
0.05456 staging/src/k8s.io/kube-aggregator/go.mod
0.01911 go.mod
0.01911 go.sum
0.01911 vendor/modules.txt
0.01416 staging/src/k8s.io/sample-apiserver/go.mod
0.01363 staging/src/k8s.io/apiextensions-apiserver/go.sum
0.01244 staging/src/k8s.io/kube-aggregator/go.sum
0.01244 staging/src/k8s.io/sample-apiserver/go.sum
0.00936 staging/src/k8s.io/metrics/go.mod
0.00936 staging/src/k8s.io/node-api/go.mod
0.00936 staging/src/k8s.io/sample-controller/go.mod
```
