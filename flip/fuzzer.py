#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import random
import signal
import multiprocessing as mp
from pathlib import Path
from typing import Dict, List, Optional
from pulp.pulp import LpSolver

from flip.argument_parser import parse_arguments
from flip.solvers.solver import generate_solver
from flip.LpInstance import LpInstance
from flip.InstanceGenerator import InstanceGenerator
from flip.utils import solve, SolveResult
from flip.utils import info, read_pipe
from flip.config import DUPLICATES

def ensure_dir(path: Path) -> None:
    """
        Structure of output directory:
        out_dir/
         ├── bugs/
         │   ├── crash-1/
         │   ├── crash-2/
         │   ├── wrong-1/
         │   ├── wrong-2/
         │   └── ...
         └── instances/ (only if --save_instances is true)
             ├── 1.mps
             ├── 2.mps
             └── ...
    """
    bugs = path / "bugs"
    inst = path / "instances"
    for d in [path, bugs, inst]:
        d.mkdir(parents=True, exist_ok=True)

def run_fuzzer_worker(
    worker_id: int,
    inst_generator: InstanceGenerator,
    end_time: float,
    stop_event: mp.Event,
    args, # command line arguments
):
    random.seed(os.getpid() ^ int(time.time()))
    SUT = args.solvers_under_test
    out_dir = Path(args.output_dir).resolve()
    bug_dir = out_dir / "bugs"
    inst_dir = out_dir / "instances"
    save_instances = args.save_instances.lower() == "true"
    worker_count = args.jobs
    feasibility = args.feasibility
    cnt = worker_id

    def get_new_seed() -> LpInstance:
        if feasibility == "feasible":
            return inst_generator.generate_feasible_instance()
        elif feasibility == "infeasible":
            return inst_generator.generate_infeasible_instance()
        elif feasibility == "random":
            if random.random() < 0.5:
                return inst_generator.generate_feasible_instance()
            else:
                return inst_generator.generate_infeasible_instance()
        elif feasibility == "blind":
            return inst_generator.generate_random_instance()
        else:
            raise ValueError(f"Unknown feasibility option: {feasibility}")

    def deduplicate_and_save_bug(
            bug_type: str,
            seed: LpInstance,
            solvers: List[LpSolver] = None,
            bad_solver: Optional[LpSolver] = None,
            bad_result: Optional[SolveResult] = None,
            results: Optional[Dict[LpSolver, SolveResult]] = None
    ):
        for s, res in (results or {}).items():
            if res.elapsed_time and res.elapsed_time >= 29:
                info(f"Skip timeout cases")
                return
            if res.output_pipe:
                output = read_pipe(res.output_pipe)
                for line in reversed(output):
                    for dup in DUPLICATES:
                        if dup in line:
                            info(f"Duplicate bug found in solver {s.name}: {dup}")
                            return

        bug_name = f"{bug_type}-{bad_solver.name}-{cnt}" if bad_solver else f"{bug_type}-{cnt}"
        new_bug_dir = bug_dir / bug_name
        os.makedirs(new_bug_dir)
        mps_file = new_bug_dir / "small.mps"
        seed.save(mps_file, dump_lp_file=True)

        def write_config(solver: LpSolver):
            config_file = new_bug_dir / (solver.name + (".set" if solver.name == "SCIP_CMD" else ".txt"))
            with open(config_file, "w") as f:
                if solver.name == "MOSEK":
                    for k, v in solver.options.items():
                        f.write(f"{k}={v}\n")
                else:
                    for opt in solver.options:
                        f.write(f"{opt}\n")

        if solvers:
            for s in solvers:
                write_config(s)

    def save_instance(inst: LpInstance, idx: int):
        filename = f"{idx}.mps"
        inst_file_dir = inst_dir / filename
        inst.save(inst_file_dir, dump_json_file=False, dump_lp_file=False)

    try:
        while not stop_event.is_set() and time.time() < end_time:
            seed = get_new_seed()
            results: Dict[LpSolver, SolveResult] = {}
            found_bug = False
            bug_type = None
            bad_solver = None
            bad_result = None
            solvers = []

            # solve with solvers under test
            for s in SUT:
                env = os.environ.copy()
                # if s == "COIN_CMD":
                #     env["LD_LIBRARY_PATH"] = CBC_LIB_PATH + (":" + env["LD_LIBRARY_PATH"] if "LD_LIBRARY_PATH" in env else "")
                solver = generate_solver(s, env=env)
                solvers.append(solver)
                if not solver.available():
                    raise ValueError(f"Solver {s} is not available.")
                result: SolveResult = solve(seed.prob, solver)
                results[solver] = result

            # check for bugs
            has_optimal = any(res.status == "Optimal" for res in results.values())
            for s, res in results.items():
                if res.status in ["Error", "UnexpectedError"]:
                    found_bug = True
                    bug_type = "crash"
                    bad_solver = s
                    bad_result = res
                    break
                if has_optimal and res.status != "Optimal":
                    found_bug = True
                    bug_type = "feasibility"
                    bad_solver = s
                    bad_result = res
                    break
            if not found_bug and has_optimal and len(results) > 1:
                tol = 2.0
                ref_obj = next(iter(results.values())).objective
                if ref_obj is None:
                    found_bug = True
                    bug_type = "wrong"
                for s, res in results.items():
                    assert res.status == "Optimal"
                    if res.objective is None or abs(res.objective - ref_obj) > tol:
                        found_bug = True
                        bug_type = "wrong"
                        break
            
            # save bug if found
            if found_bug:
                deduplicate_and_save_bug(
                    bug_type=bug_type,
                    seed=seed,
                    solvers=solvers,
                    bad_solver=bad_solver,
                    bad_result=bad_result,
                    results=results
                )

            if save_instances:
                save_instance(seed, cnt)

            cnt += worker_count

    except Exception as e:
        raise e

def run_fuzzer_master(args):
    out_dir = Path(args.output_dir).resolve()
    ensure_dir(out_dir)

    inst_generator = InstanceGenerator(
        min_num_vars=args.min_vars_num,
        max_num_vars=args.max_vars_num,
        min_cons_ratio=args.min_cons_ratio,
        max_cons_ratio=args.max_cons_ratio,
        min_sparsity=args.min_sparsity,
        max_sparsity=args.max_sparsity,
        mode=args.mode,
    )

    start_time = time.time()
    end_time = start_time + args.time_to_run * 3600

    manager = mp.Manager()
    stop_event = manager.Event()

    # start workers
    workers = []
    for w_id in range(args.jobs):
        proc = mp.Process(
            target=run_fuzzer_worker,
            args=(
                w_id,
                inst_generator,
                end_time,
                stop_event,
                args,
            ),
            daemon=True
        )
        workers.append(proc)
        proc.start()

    try:
        while time.time() < end_time:
            time.sleep(5)
    except KeyboardInterrupt:
        info(f"Keyboard interrupt received. Stopping fuzzer.")
    finally:
        stop_event.set()
        for worker in workers:
            worker.join()

    info(f"Fuzzer finished. Total time: {time.time() - start_time:.2f} seconds.")

def main():
    args = parse_arguments()
    info(f"Solver under test: {args.solvers_under_test}")
    run_fuzzer_master(args)


if __name__ == "__main__":
    main()  