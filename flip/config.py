SOLVERS = [
    "SCIP_CMD",
    "COIN_CMD",
    "HiGHS_CMD",
    # "MOSEK",
    # "GUROBI_CMD",
]

DUPLICATES = [
    "Assertion `lb_consistent' failed", # HiGHS-2174
    "Assertion `ub_consistent' failed", # HiGHS-2178 (duplicate of HiGHS-2174)
    "fabs(checkefficacy) >= 1e30",
    "unresolved numerical troubles", # scip: numerical issue, not a bug
    "possible tolerance issue", # cbc: tolerance issue, not a bug
]