SOLVERS = [
    "SCIP_CMD",
    "COIN_CMD",
    "HiGHS_CMD",
    "MOSEK",
    "GUROBI_CMD",
]

DEFAULT_SOLVER_UNDER_TEST = [
    "SCIP_CMD",
    "COIN_CMD",
    "HiGHS_CMD",
]

DEFAULT_REFERENCE_SOLVER = "GUROBI_CMD"

DUPLICATES = [
    "Assertion `lb_consistent' failed", # HiGHS-2174
    "Assertion `ub_consistent' failed", # HiGHS-2178 (duplicate of HiGHS-2174)
    "fabs(checkefficacy) >= 1e30", # HiGHS
    "unresolved numerical troubles", # scip: numerical issue, not a bug
    "possible tolerance issue", # cbc: tolerance issue, not a bug
]