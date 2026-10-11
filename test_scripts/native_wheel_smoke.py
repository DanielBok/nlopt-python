"""Installed-wheel numerical and native Windows ARM64 regression checks."""
import argparse
import json
import struct
import sys
import sysconfig
from pathlib import Path

import nlopt
import nlopt._nlopt
import numpy as np


def pe_machine(path):
    data = Path(path).read_bytes()
    assert data[:2] == b"MZ", path
    offset = struct.unpack_from("<I", data, 0x3C)[0]
    assert data[offset:offset + 4] == b"PE\0\0", path
    return struct.unpack_from("<H", data, offset + 4)[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-arm64", action="store_true")
    args = parser.parse_args()
    # Convex quadratic: the unique minimizer is known independently of NLopt.
    target = np.array([1.25, -2.5, 0.75])
    calls = [0]

    def objective(x, grad):
        assert isinstance(x, np.ndarray)
        calls[0] += 1
        if grad.size:
            grad[:] = 2 * (x - target)
        return float(np.dot(x - target, x - target))

    opt = nlopt.opt(nlopt.LD_LBFGS, 3)
    opt.set_min_objective(objective)
    opt.set_xtol_rel(1e-10)
    opt.set_maxeval(200)
    result = opt.optimize(np.array([8.0, 3.0, -7.0]))
    np.testing.assert_allclose(result, target, atol=1e-7, rtol=0)
    assert opt.last_optimum_value() < 1e-12
    assert opt.last_optimize_result() > 0
    assert calls[0] > 1

    # A derivative-free bound-constrained problem exercises another algorithm.
    bounded = nlopt.opt(nlopt.LN_COBYLA, 3)
    bounded.set_lower_bounds([0.0, 0.0, 0.0])
    bounded.set_min_objective(objective)
    bounded.set_xtol_rel(1e-9)
    bounded.set_maxeval(1000)
    bounded_result = bounded.optimize([4.0, 3.0, 2.0])
    np.testing.assert_allclose(bounded_result, [1.25, 0.0, 0.75], atol=1e-5, rtol=0)
    assert abs(bounded.last_optimum_value() - 6.25) < 1e-8
    assert bounded.last_optimize_result() > 0

    binaries = {}
    if args.require_arm64:
        assert sysconfig.get_platform() == "win-arm64", sysconfig.get_platform()
        paths = [Path(sys.executable), Path(nlopt._nlopt.__file__)]
        paths += list(Path(np.__file__).parent.rglob("*.pyd"))
        assert len(paths) > 2, "NumPy extensions not found"
        for path in paths:
            machine = pe_machine(path)
            assert machine == 0xAA64, (path, hex(machine))
            binaries[path.name] = hex(machine)
    print(json.dumps({"python": sys.version, "platform": sysconfig.get_platform(),
                      "nlopt": nlopt.__version__, "numpy": np.__version__,
                      "quadratic": result.tolist(), "bounded": bounded_result.tolist(),
                      "objective_calls": calls[0], "pe_machine": binaries}))


if __name__ == "__main__":
    main()
