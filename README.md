# codesort

Given a git repository, determine the most "important" files in the repository, as determined by [Aron Lurie's method](http://redd.it/bb7qst).

The idea is when approaching an unknown code base, look at the highest-ranked files as a starting place for understanding the system.

## usage

With `pipenv` available:

```
$ pipenv install
$ pipenv run python codesort.py /path/to/repository
0.33939	app/file1.py
0.2707	app/lib/__init__.py
0.15025	tox.ini
0.11347	Dockerfile
```

The output is in format `score<TAB>filepath` per line where `score` is the betweenness centrality score, sorted descending by score.
