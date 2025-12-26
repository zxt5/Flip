from flip.solvers.scip import generate_scip
from flip.solvers.cbc import generate_cbc
from flip.solvers.highs import generate_highs
from flip.solvers.mosek import generate_mosek
from flip.solvers.gurobi import generate_gurobi
from pulp.pulp import LpSolver

def generate_solver(
        name: str,
        env=None,
        msg: bool = False,
        time_limit: int = 30) -> LpSolver:
    if name == "SCIP_CMD":
        return generate_scip(env=env, msg=msg, time_limit=time_limit)
    elif name == "COIN_CMD":
        return generate_cbc(env=env, msg=msg, time_limit=time_limit)
    elif name == "HiGHS_CMD":
        return generate_highs(env=env, msg=msg, time_limit=time_limit)
    elif name == "GUROBI_CMD":
        return generate_gurobi(env=env, msg=msg, time_limit=time_limit)
    elif name == "MOSEK":
        return generate_mosek(env=env, msg=msg, time_limit=time_limit)
    else:
        raise ValueError(f"Unsupported solver: {name}")


if __name__ == "__main__":
    pass