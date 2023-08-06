import pytest
import numpy as np

from gradient_free_optimizers import RandomSearchOptimizer


def test_check_search_space():
    def objective_function(para):
        score = -para["x1"] * para["x1"]
        return score

    search_space = 1

    with pytest.raises(ValueError):
        opt = RandomSearchOptimizer(search_space)
        opt.search(objective_function, n_iter=30)


def test_check_initialize():
    def objective_function(para):
        score = -para["x1"] * para["x1"]
        return score

    search_space = {"x1": np.arange(-10, 10, 0.1)}

    initialize = 1

    with pytest.raises(ValueError):
        opt = RandomSearchOptimizer(search_space, initialize)
        opt.search(objective_function, n_iter=30)


def test_check_objective_function():
    objective_function = 1

    search_space = {"x1": np.arange(-10, 10, 0.1)}

    with pytest.raises(ValueError):
        opt = RandomSearchOptimizer(search_space)
        opt.search(objective_function, n_iter=30)


def test_check_n_iter():
    def objective_function(para):
        score = -para["x1"] * para["x1"]
        return score

    search_space = {"x1": np.arange(-10, 10, 0.1)}
    n_iter = 0.1

    with pytest.raises(ValueError):
        opt = RandomSearchOptimizer(search_space)
        opt.search(objective_function, n_iter=n_iter)


def test_check_max_time():
    def objective_function(para):
        score = -para["x1"] * para["x1"]
        return score

    search_space = {"x1": np.arange(-10, 10, 0.1)}
    max_time = "1"

    with pytest.raises(ValueError):
        opt = RandomSearchOptimizer(search_space)
        opt.search(objective_function, n_iter=30, max_time=max_time)


def test_check_max_score():
    def objective_function(para):
        score = -para["x1"] * para["x1"]
        return score

    search_space = {"x1": np.arange(-10, 10, 0.1)}
    max_score = "1"

    with pytest.raises(ValueError):
        opt = RandomSearchOptimizer(search_space)
        opt.search(objective_function, n_iter=30, max_score=max_score)


def test_check_memory():
    def objective_function(para):
        score = -para["x1"] * para["x1"]
        return score

    search_space = {"x1": np.arange(-10, 10, 0.1)}
    memory = "1"

    with pytest.raises(ValueError):
        opt = RandomSearchOptimizer(search_space)
        opt.search(objective_function, n_iter=30, memory=memory)


def test_check_memory_warm_start():
    def objective_function(para):
        score = -para["x1"] * para["x1"]
        return score

    search_space = {"x1": np.arange(-10, 10, 0.1)}
    memory_warm_start = "1"

    with pytest.raises(ValueError):
        opt = RandomSearchOptimizer(search_space)
        opt.search(
            objective_function, n_iter=30, memory_warm_start=memory_warm_start
        )


def test_check_memory_verbosity():
    def objective_function(para):
        score = -para["x1"] * para["x1"]
        return score

    search_space = {"x1": np.arange(-10, 10, 0.1)}
    verbosity = "1"

    with pytest.raises(ValueError):
        opt = RandomSearchOptimizer(search_space)
        opt.search(objective_function, n_iter=30, verbosity=verbosity)


def test_check_memory_random_state():
    def objective_function(para):
        score = -para["x1"] * para["x1"]
        return score

    search_space = {"x1": np.arange(-10, 10, 0.1)}
    random_state = "1"

    with pytest.raises(ValueError):
        opt = RandomSearchOptimizer(search_space)
        opt.search(objective_function, n_iter=30, random_state=random_state)

