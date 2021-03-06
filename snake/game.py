#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0111,W0201,W0703

# @author: Harsh Bhatt
# The main purpose of the file is to be a base layout for our game.
# It will configure what type of algorithm is running on the game.
# This makes it easier for future implementations of different
# algorithms to be run on the same board for experimental results.
# I have added useful features such as pausing the game to play it 
# on your own with the arrow keys.
# Much of my work was done on the alogirthm portion as that is where the
# key reaserching was done. 

import errno
import os
import traceback
from enum import Enum, unique

from snake.base import Direc, Map, PointType, Pos, Snake
from snake.gui import GameWindow
from snake.solver import  HamiltonSolver


@unique
class GameMode(Enum):
    NORMAL = 0         # AI with GUI
    BENCHMARK = 1      # Run benchmarks without GUI

class GameConf:

    def __init__(self):
        """Initialize a default configuration."""

        # Game mode
        self.mode = GameMode.NORMAL

        # Solver
        self.solver_name = 'Hamiltonian Solver with Shortcuts'  # Class name of the solver

        # Size
        self.map_rows = 8
        self.map_cols = self.map_rows
        self.map_width = 160  # pixels
        self.map_height = self.map_width
        self.info_panel_width = 155  # pixels
        self.window_width = self.map_width + self.info_panel_width
        self.window_height = self.map_height
        self.grid_pad_ratio = 0.25

        # Switch
        self.show_grid_line = False
        self.show_info_panel = True

        # Delay
        self.interval_draw = 50       # ms
        self.interval_draw_max = 200  # ms

        # Color
        self.color_bg = '#FFFFFF'
        self.color_txt = '#000000'
        self.color_line = '#000000'
        self.color_wall = '#F5F5F5'
        self.color_food = '#A800B5'
        self.color_head = '#FF0000'
        self.color_body = '#000000'

        # Initial snake
        self.init_direc = Direc.RIGHT
        self.init_bodies = [Pos(1, 4), Pos(1, 3), Pos(1, 2), Pos(1, 1)]
        self.init_types = [PointType.HEAD_R] + [PointType.BODY_HOR] * 3

        # Font
        self.font_info = ('Arial', 9)

        # Info
        self.info_str = (
            "<w/a/s/d>: snake direction\n"
            "<space>: pause/resume\n"
            "<r>: restart    <esc>: exit\n"
            "-----------------------------------\n"
            "status: %s\n"
            "episode: %d   step: %d\n"
            "length: %d/%d (" + str(self.map_rows) + "x" + str(self.map_cols) + ")\n"
            "-----------------------------------"
        )
        self.info_status = ['eating', 'dead', 'full']

class Game:

    def __init__(self, conf):
        self._conf = conf
        self._map = Map(conf.map_rows + 2, conf.map_cols + 2)
        self._snake = Snake(self._map, conf.init_direc,
                            conf.init_bodies, conf.init_types)
        self._pause = False
        self._solver = globals()[self._conf.solver_name](self._snake)
        self._episode = 1
        self._init_log_file()

    @property
    def snake(self):
        return self._snake

    @property
    def episode(self):
        return self._episode

    def run(self):
        window = GameWindow("Snake", self._conf, self._map, self, self._on_exit, (
            ('<w>', lambda e: self._update_direc(Direc.UP)),
            ('<a>', lambda e: self._update_direc(Direc.LEFT)),
            ('<s>', lambda e: self._update_direc(Direc.DOWN)),
            ('<d>', lambda e: self._update_direc(Direc.RIGHT)),
            ('<r>', lambda e: self._reset()),
            ('<space>', lambda e: self._toggle_pause())
        ))
        if self._conf.mode == GameMode.NORMAL:
            window.show(self._game_main_normal)
        elif self._conf.mode == GameMode.TRAIN_DQN_GUI:
            window.show(self._game_main_dqn_train)
            self._plot_history()

    def _game_main_normal(self):
        if not self._map.has_food():
            self._map.create_rand_food()

        if self._pause or self._is_episode_end():
            return

        self._update_direc(self._solver.next_direc())

        if self._conf.mode == GameMode.NORMAL and self._snake.direc_next != Direc.NONE:
            self._write_logs()

        self._snake.move()

        if self._is_episode_end():
            self._write_logs()  # Write the last step

    def _plot_history(self):
        self._solver.plot()

    def _update_direc(self, new_direc):
        self._snake.direc_next = new_direc
        if self._pause:
            self._snake.move()

    def _toggle_pause(self):
        self._pause = not self._pause

    def _is_episode_end(self):
        return self._snake.dead or self._map.is_full()

    def _reset(self):
        self._snake.reset()
        self._episode += 1

    def _on_exit(self):
        if self._log_file:
            self._log_file.close()
        if self._solver:
            self._solver.close()

    def _init_log_file(self):
        try:
            os.makedirs("logs")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        try:
            self._log_file = None
            self._log_file = open('logs/snake.log', 'w')
        except FileNotFoundError:
            if self._log_file:
                self._log_file.close()

    def _write_logs(self):
        self._log_file.write("[ Episode %d / Step %d ]\n" % \
                             (self._episode, self._snake.steps))
        for i in range(self._map.num_rows):
            for j in range(self._map.num_cols):
                pos = Pos(i, j)
                t = self._map.point(pos).type
                if t == PointType.EMPTY:
                    self._log_file.write("  ")
                elif t == PointType.WALL:
                    self._log_file.write("# ")
                elif t == PointType.FOOD:
                    self._log_file.write("F ")
                elif t == PointType.HEAD_L or t == PointType.HEAD_U or \
                    t == PointType.HEAD_R or t == PointType.HEAD_D:
                    self._log_file.write("H ")
                elif pos == self._snake.tail():
                    self._log_file.write("T ")
                else:
                    self._log_file.write("B ")
            self._log_file.write("\n")
        self._log_file.write("[ last/next direc: %s/%s ]\n" % \
                              (self._snake.direc, self._snake.direc_next))
        self._log_file.write("\n")
