#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0111

# @author: Harsh Bhatt
# The main purpose of this file is to make it easier to run the
# program checking the results of the algorithm. One launch
# of this file will run the algorthm real time on a GUI.
# Much of the work done on this research topic was done in the
# algorithms portion of the code.

import argparse

from snake.game import Game, GameConf, GameMode

dict_solver = {
    "hamilton": "HamiltonSolver",
}

dict_mode = {
    "normal": GameMode.NORMAL,
}

parser = argparse.ArgumentParser(description="Run snake game agent.")
parser.add_argument("-s", default="hamilton", choices=dict_solver.keys(),
                    help="name of the solver to direct the snake (default: hamilton)")
parser.add_argument("-m", default="normal", choices=dict_mode.keys(),
                    help="game mode (default: normal)")
args = parser.parse_args()

conf = GameConf()
conf.solver_name = dict_solver[args.s]
conf.mode = dict_mode[args.m]
print("Solver: %s    Mode: %s" % (conf.solver_name, conf.mode))

Game(conf).run()
