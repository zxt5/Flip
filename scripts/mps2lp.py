#!/usr/bin/env python3
import os
import sys
from pulp.pulp import LpProblem

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./mps2lp.py <mps_file>")
        exit(1)

    mps_file = sys.argv[1]
    path = os.path.dirname(mps_file)
    lp_path = os.path.splitext(mps_file)[0] + ".lp"

    vars, prob = LpProblem.fromMPS(mps_file)

    prob.writeLP(lp_path)
    print(f"{lp_path} is generated in {path}")



