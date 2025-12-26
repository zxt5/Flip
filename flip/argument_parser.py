import argparse
import os
import time

from flip.config import SOLVERS

def parse_arguments(target="fuzzer"):
    parser = argparse.ArgumentParser(
        description="Flip: Fuzzing Mixed Integer Programming Solvers",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--time_to_run",
        "-t",
        type=float,
        default=24,
        help="Number of hours to run fuzzing",
    )

    parser.add_argument(
        "--jobs",
        "-j",
        type=int,
        default=1,
        help="Number of jobs to run in parallel",
    )

    parser.add_argument(
        "--save_instances",
        "-si",
        type=str,
        default="false",
        choices=["true", "false"],
        help="Save all the test instances generated during fuzzing (true or false)",
    )

    parser.add_argument(
        "--output_dir",
        "-o",
        type=str,
        default=None,
        help="Directory of the output",
    )

    parser.add_argument(
        "--mode",
        "-m",
        type=str,
        default="MIP",
        choices=["MIP", "LP", "IP"],
        help="Mode: MIP (Mixed Integer Programming), LP (Linear Programming), IP (Integer Programming)",
    )

    parser.add_argument(
        "--feasibility",
        "-f",
        type=str,
        default="feasible",
        choices=["feasible", "infeasible", "random", "blind"],
        help="Feasibility of the generated seeds for testing: feasible, infeasible, random (feasible or infeasible), blind (fully random generation, mainly used for evaluation)",
    )

    parser.add_argument(
        "--min_vars_num",
        "-minv",
        type=int,
        default=2,
        help="Minimum number of variables in the generated seeds",
    )

    parser.add_argument(
        "--max_vars_num",
        "-maxv",
        type=int,
        default=10,
        help="Maximum number of variables in the generated seeds",
    )

    parser.add_argument(
        "--min_cons_ratio",
        "-mincr",
        type=int,
        default=2,
        help="Minimum ratio of constraints to variables in the generated seeds",
    )

    parser.add_argument(
        "--max_cons_ratio",
        "-maxcr",
        type=int,
        default=5,
        help="Maximum ratio of constraints to variables in the generated seeds",
    )

    parser.add_argument(
        "--min_sparsity",
        "-minsp",
        type=float,
        default=0.8,
        help="Minimum sparsity of the generated seeds (fraction of non-zero coefficients)",
    )

    parser.add_argument(
        "--max_sparsity",
        "-maxsp",
        type=float,
        default=1.0,
        help="Maximum sparsity of the generated seeds (fraction of non-zero coefficients)",
    )

    parser.add_argument(
        "--solvers_under_test",
        "-sut",
        type=str,
        nargs="+",
        default=SOLVERS,
        choices=SOLVERS,
        help=f"Solvers under test: {', '.join(SOLVERS)}",
    )

    args = parser.parse_args()

    # check arguments
    if args.time_to_run <= 0: 
        parser.error("time_to_run must be greater than 0")

    if args.jobs <= 0:
        parser.error("jobs must be greater than 0")

    if args.min_vars_num <= 0:
        parser.error("min_vars_num must be greater than 0")

    if args.max_vars_num <= 0:
        parser.error("max_vars_num must be greater than 0")

    if args.min_vars_num > args.max_vars_num:
        parser.error("min_vars_num must be less than or equal to max_vars_num")

    if args.min_cons_ratio <= 0:
        parser.error("min_cons_ratio must be greater than 0")

    if args.max_cons_ratio <= 0:
        parser.error("max_cons_ratio must be greater than 0")

    if args.min_cons_ratio > args.max_cons_ratio:
        parser.error("min_cons_ratio must be less than or equal to max_cons_ratio")

    if args.min_sparsity < 0 or args.max_sparsity > 1:
        parser.error("min_sparsity must be between 0 and 1")

    if args.min_sparsity > args.max_sparsity:
        parser.error("min_sparsity must be less than or equal to max_sparsity")

    if args.output_dir is None:
        cwd = os.getcwd()
        tf = time.strftime("%Y%m%d-%H%M%S")
        feasibility = args.feasibility
        args.output_dir = f"{cwd}/out-{tf}-{feasibility}"

    return args

if __name__ == "__main__":
    args = parse_arguments()