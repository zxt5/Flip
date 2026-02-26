# Flip: Validating Mixed-Integer Programming Solvers

**Flip** is a fuzzing framework for validating mixed-integer programming (MIP) solvers.

Flip is introduced in the ICSE'26 research paper
[*"Validating Mixed-Integer Programming Solvers"*](https://zxt5.github.io/papers/flip-icse26.pdf).

## Setup

Build the open-source solvers (SCIP, CBC, HiGHS) from source and configure paths:

```bash
source scripts/setup.sh
```

This compiles solver binaries into `third_party/`, creates symlinks in `bin/`, and sets `PATH`/`PYTHONPATH`. For commercial solvers (Gurobi, MOSEK), please install them separately following their official documentation if you want to fuzz them or use them as reference solvers.

Install Python dependencies:

```bash
uv sync
```

## Usage

Run the fuzzer with `flip` to start a fuzzing campaign with default settings. The output would be something like:

```bash
$ flip
[     INFO] [2026-02-25 23:56:06] Time to run: 24 hours
[     INFO] [2026-02-25 23:56:06] Number of jobs in parallel: 1
[     INFO] [2026-02-25 23:56:06] Output directory: /path/to/output/out-20260225-235606-feasible
[     INFO] [2026-02-25 23:56:06] Solvers under test: ['SCIP_CMD', 'COIN_CMD', 'HiGHS_CMD']
[     INFO] [2026-02-25 23:56:06] Reference solver: GUROBI_CMD
[     INFO] [2026-02-25 23:56:06] Mode: MIP
[     INFO] [2026-02-25 23:56:06] Feasibility: feasible
...
```

### Common examples

Fuzz for 2 hours using 4 parallel workers:

```bash
$ flip -t 2 -j 4
```

Fuzz only HiGHS and SCIP, generating both feasible and infeasible instances:

```bash
$ flip --solvers_under_test HiGHS_CMD SCIP_CMD --feasibility random
```

Use HiGHS as the reference solver (e.g., when Gurobi is unavailable), generating infeasible instances:

```bash
$ flip --reference_solver HiGHS_CMD --feasibility infeasible
```

### All options

| Flag | Default | Description |
|---|---|---|
| `-t`, `--time_to_run` | `24` | Hours to run |
| `-j`, `--jobs` | `1` | Parallel worker processes |
| `-o`, `--output_dir` | auto-named | Output directory |
| `-m`, `--mode` | `MIP` | Problem type: `MIP`, `LP`, or `IP` |
| `-f`, `--feasibility` | `feasible` | Seed type: `feasible`, `infeasible`, `random`, or `blind` |
| `--solvers_under_test` | `SCIP_CMD COIN_CMD HiGHS_CMD` | Solvers to test (space-separated) |
| `--reference_solver` | `GUROBI_CMD` | Reference solver used to generate infeasible instances |
| `--save_instances` | `false` | Save all generated `.mps` files |
| `-minv`, `--min_vars_num` | `2` | Min variables per instance |
| `-maxv`, `--max_vars_num` | `10` | Max variables per instance |
| `-mincr`, `--min_cons_ratio` | `2` | Min constraints-to-variables ratio |
| `-maxcr`, `--max_cons_ratio` | `5` | Max constraints-to-variables ratio |
| `-minsp`, `--min_sparsity` | `0.8` | Min fraction of non-zero coefficients |
| `-maxsp`, `--max_sparsity` | `1.0` | Max fraction of non-zero coefficients |

## Output

```
out_dir/
├── bugs/
│   ├── crash-HiGHS_CMD-0/       # solver crashed
│   │   ├── small.mps
│   │   └── small.lp
│   ├── feasibility-SCIP_CMD-1/  # feasibility disagreement
│   └── wrong-COIN_CMD-2/        # wrong objective value
└── instances/                   # only if --save_instances true
    ├── 0.mps
    └── ...
```

Three bug types are reported:
- **crash** — solver returned an error or threw an exception
- **feasibility** — One or more solvers report Infeasible while others report Feasible, or vice versa
- **wrong** — all solvers report Optimal but objective values differ by more than 2.0

## Configuration (`flip/config.py`)

| Variable | Description |
|---|---|
| `SOLVERS` | All recognized solver names that can be passed to `--solvers_under_test` or `--reference_solver` |
| `DEFAULT_SOLVER_UNDER_TEST` | Default solvers tested when `--solvers_under_test` is not specified (`SCIP_CMD`, `COIN_CMD`, `HiGHS_CMD`) |
| `DEFAULT_REFERENCE_SOLVER` | Default reference solver for generating infeasible instances (`GUROBI_CMD`) |
| `DUPLICATES` | List of output substrings that identify known/duplicate issues; any result matching these strings is silently skipped to avoid re-reporting known bugs |

To suppress a newly identified false positive or known duplicate, add a unique substring from its solver output to `DUPLICATES`.

Although some of these parameters can be overridden via command-line parameters, modifying this file
permanently changes Flip's default behavior.

## Supporting New Solvers

Flip is built on top of [PuLP](https://github.com/coin-or/pulp.git), which already supports most major MIP solvers. Adding a new solver to Flip is straightforward:

1. Create `flip/solvers/<name>.py` with a `generate_<name>()` function that constructs and returns a configured `LpSolver` instance. See the existing files in `flip/solvers/` for reference.
2. Register the solver in `flip/solvers/solver.py` by adding a branch to `generate_solver()`.
3. Add the solver name to `SOLVERS` in `flip/config.py` to make it recognizable by the CLI.
