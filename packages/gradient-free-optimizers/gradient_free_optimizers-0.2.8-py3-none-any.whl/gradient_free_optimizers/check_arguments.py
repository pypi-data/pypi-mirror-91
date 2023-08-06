# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import numbers
import collections
import pandas as pd


def check_search_space(search_space):
    if not isinstance(search_space, dict):
        raise ValueError("search_space must be of type dictionary")


def check_initialize(initialize):
    if not isinstance(initialize, dict):
        raise ValueError("initialize must be of type dictionary")


def check_objective_function(objective_function):
    if not isinstance(objective_function, collections.Callable):
        raise ValueError("objective_function must be callable")


def check_n_iter(n_iter):
    if not isinstance(n_iter, int):
        raise ValueError("n_iter must be of type int")


def check_max_time(max_time):
    if not isinstance(max_time, (numbers.Number, type(None))):
        raise ValueError("max_time must be of type float, int or None")


def check_max_score(max_score):
    if not isinstance(max_score, (numbers.Number, type(None))):
        raise ValueError("max_score must be of type float, int or None")


def check_memory(memory):
    if not isinstance(memory, bool):
        raise ValueError("memory must be of type bool")


def check_memory_warm_start(memory_warm_start):
    if not isinstance(memory_warm_start, (pd.DataFrame, type(None))):
        raise ValueError(
            "memory_warm_start must be of type pandas dataframe or None"
        )


def check_verbosity(verbosity):
    if not isinstance(verbosity, list):
        raise ValueError("verbosity must be of type list")


def check_random_state(random_state):
    if not isinstance(random_state, (int, type(None))):
        raise ValueError("random_state must be of type int or None")

