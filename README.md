# codesort

Given a git repository, determine the most "important" files in the repository, as determined by [Aron Lurie's method](http://redd.it/bb7qst).

The idea is when approaching an unknown code base, look at the highest-ranked files as a starting place for understanding the system.

## usage

Via Docker container:
```
$ docker run -v /path/to/your/repo:/repo:ro jeffgreenca/codesort
``` 

Without Docker, with `pipenv` available:

```
$ pipenv install
$ pipenv run python codesort.py /path/to/repository
0.33939	app/file1.py
0.2707	app/lib/__init__.py
0.15025	tox.ini
0.11347	Dockerfile
```

The output is in format `score<TAB>filepath` per line where `score` is the betweenness centrality score, sorted descending by score.

## advanced usage

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
