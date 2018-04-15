# Snake

[![][badge-travis]][build-travis] [![][badge-appveyor]][build-appveyor] ![][badge-python]

This project focuses on the artificial intelligence of the [Snake][wiki-snake] game. The snake's goal is to eat the food continuously and fill the map with its bodies. Huge thanks to [Chuyang Liu][Chuyang-Liu] for his implementation of the game on python3. This is being tweaked to add implementations of the "almighty move" and random moves in order to make the snake more effeicient. 

***[Algorithm Research >][doc-algorithms]***

## Experiments

I used two metrics to evaluate the performance of an AI:

1. **Average Length:** Average length the snake has grown to (*max:* 64).
2. **Average Steps:** Average steps the snake has moved.

Test results (averaged over 100 episodes):

| Solver | Demo (optimal) | Average Length | Average Steps |
| :----: | :------------: | :------------: | :-----------: |
|[Hamilton][doc-hamilton]|![][demo-hamilton]|60|700|

## Installation

Requirements: Python 3.5+ (64-bit) with [Tkinter][doc-tkinter] installed.

```
$ pip3 install -r requirements.txt

# Run the algorithm in real time
$ python3 run.py 
```

## License

See the [LICENSE](./LICENSE) file for license rights and limitations.


[snake-proj-old]: https://github.com/chuyangliu/Snake/tree/7227f5e0f3185b07e9e3de1ac5c19a17b9de3e3c

[build-travis]: https://travis-ci.org/chuyangliu/Snake
[build-appveyor]: https://ci.appveyor.com/project/chuyangliu/snake/branch/master
[badge-travis]: https://travis-ci.org/chuyangliu/Snake.svg?branch=dev_refactor
[badge-appveyor]: https://ci.appveyor.com/api/projects/status/d4agff8ef7d9tfxh/branch/master?svg=true
[badge-python]: https://img.shields.io/badge/python-3.5%2C%203.6-blue.svg

[wiki-snake]: https://en.wikipedia.org/wiki/Snake_(video_game)
[doc-tkinter]: https://docs.python.org/3.6/library/tkinter.html
[doc-algorithms]: https://drive.google.com/file/d/1FH6NLQPb8pSsNYN9Uz0NCItUayFHZlZu/view?usp=sharing
[doc-greedy]: ./docs/algorithms.md#greedy-solver
[doc-hamilton]: ./docs/algorithms.md#hamilton-solver
[doc-dqn]: ./docs/algorithms.md#dqn-solver

[demo-hamilton]: ./images/solver_hamilton.gif
[Chuyang-Liu]: https://github.com/chuyangliu
