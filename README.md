# Railway Problem

This repo contains materials for a school project I'm working on which is about the classification of *railway systems*. A railway system is a mathematically defined structure. For a detailed formulation of the problem, see [`frage_formulierung.pdf`](https://github.com/lutalli/RailwayProblem/blob/main/frage_formulierung.pdf) (written in German).

The Python script [`eisenbahn_brutal.py`](https://github.com/lutalli/RailwayProblem/blob/main/eisenbahn_brutal.py) is a brutal force solver for the problem that simply lists out all connection possiblities of given switches and classify them. Usage:

```
> python eisenbahn_brutal.py -d <dimension> -f <path>
```

| Argument | Explanation |
| --- | --- |
| `-d`, `--dimension` | The dimension of the railway systems to classify. Must be an even number. |
| `-f`, `--file` | The path to the file which the result should be saved into. If not specified, the result will be saved to `./result` by default. |
