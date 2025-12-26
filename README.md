# Flip: Validating Mixed-Integer Programming Solvers

**Flip** is a fuzzer designed for mixed-integer programming (MIP) solvers.
Flip generates random MIP instances which are feasible/infeasible by construction,
to expose bugs in MIP solvers. Flip is originally described in the research paper
[Validating Mixed-Integer Programming Solvers]() published in ICSE 2026.



```
$ flip --help
usage: flip [-h] [--time_to_run TIME_TO_RUN] [--jobs JOBS] [--save_instances {true,false}] [--output_dir OUTPUT_DIR] [--mode {MIP,LP,IP}] [--feasibility {feasible,infeasible,random,blind}] [--min_vars_num MIN_VARS_NUM] [--max_vars_num MAX_VARS_NUM] [--min_cons_ratio MIN_CONS_RATIO]
            [--max_cons_ratio MAX_CONS_RATIO] [--min_sparsity MIN_SPARSITY] [--max_sparsity MAX_SPARSITY] [--solvers_under_test {SCIP_CMD,COIN_CMD,HiGHS_CMD} [{SCIP_CMD,COIN_CMD,HiGHS_CMD} ...]]

Flip: Fuzzing Mixed Integer Programming Solvers

options:
  -h, --help            show this help message and exit
  --time_to_run, -t TIME_TO_RUN
                        Number of hours to run fuzzing (default: 24)
  --jobs, -j JOBS       Number of jobs to run in parallel (default: 1)
  --save_instances, -si {true,false}
                        Save all the test instances generated during fuzzing (true or false) (default: false)
  --output_dir, -o OUTPUT_DIR
                        Directory of the output (default: None)
  --mode, -m {MIP,LP,IP}
                        Mode: MIP (Mixed Integer Programming), LP (Linear Programming), IP (Integer Programming) (default: MIP)
  --feasibility, -f {feasible,infeasible,random,blind}
                        Feasibility of the generated seeds for testing: feasible, infeasible, random (feasible or infeasible), blind (fully random generation, mainly used for evaluation) (default: feasible)
  --min_vars_num, -minv MIN_VARS_NUM
                        Minimum number of variables in the generated seeds (default: 2)
  --max_vars_num, -maxv MAX_VARS_NUM
                        Maximum number of variables in the generated seeds (default: 10)
  --min_cons_ratio, -mincr MIN_CONS_RATIO
                        Minimum ratio of constraints to variables in the generated seeds (default: 2)
  --max_cons_ratio, -maxcr MAX_CONS_RATIO
                        Maximum ratio of constraints to variables in the generated seeds (default: 5)
  --min_sparsity, -minsp MIN_SPARSITY
                        Minimum sparsity of the generated seeds (fraction of non-zero coefficients) (default: 0.8)
  --max_sparsity, -maxsp MAX_SPARSITY
                        Maximum sparsity of the generated seeds (fraction of non-zero coefficients) (default: 1.0)
  --solvers_under_test, -sut {SCIP_CMD,COIN_CMD,HiGHS_CMD} [{SCIP_CMD,COIN_CMD,HiGHS_CMD} ...]
                        Solvers under test: SCIP_CMD, COIN_CMD, HiGHS_CMD (default: ['SCIP_CMD', 'COIN_CMD', 'HiGHS_CMD'])
```
