import nlopt
import numpy as np


def test_nlopt():
    def obj_func(x, grad):
        if grad.size > 0:
            grad[0] = 0.0
            grad[1] = 0.5 / np.sqrt(x[1])
        return np.sqrt(x[1])

    def constraint(x, grad, a, b):
        if grad.size > 0:
            grad[0] = 3 * a * (a * x[0] + b) ** 2
            grad[1] = -1.0
        return (a * x[0] + b) ** 3 - x[1]

    opt = nlopt.opt(nlopt.LD_MMA, 2)
    opt.set_lower_bounds([-float('inf'), 0])
    opt.set_min_objective(obj_func)
    opt.add_inequality_constraint(lambda x, grad: constraint(x, grad, 2, 0), 1e-8)
    opt.add_inequality_constraint(lambda x, grad: constraint(x, grad, -1, 1), 1e-8)
    opt.set_xtol_rel(1e-4)
    x = opt.optimize([1.234, 5.678])
    minf = opt.last_optimum_value()

    assert opt.last_optimize_result() == 4
    assert np.isclose(x[0], 0.3333333346933468)
    assert np.isclose(x[1], 0.29629628940318486)
    assert np.isclose(minf, 0.5443310476200902)

    print('Passed: optimizer interface test')
