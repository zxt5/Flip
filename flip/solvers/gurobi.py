import random
from pulp.pulp import GUROBI_CMD

OPTIONS = {
    "Seed": ("int", range(0, 200000000), True),
    "Aggregate": ("int_choice", [0, 1, 2], True),
    "DualReductions": ("int_choice", [0, 1], True),
    "PrePasses": ("int_choice", [-1, 0, 1, 5, 10, 100, 500], True),
    "Presolve": ("int_choice", [-1, 0, 1, 2], True),
    "NumericFocus": ("int_choice", [0, 1, 2, 3], True),
    "IntegralityFocus": ("int_choice", [0, 1], True),
    "MIPFocus": ("int_choice", [0, 1, 2, 3], True),
    "Symmetry": ("int_choice", [-1, 0, 1, 2], True),
    # "AggFill": ("int_choice", [-1, 0, 1, 10, 100, 500], True),
    # "PreCrush": ("int_choice", [0, 1], True),
    # "PreDepRow": ("int_choice", [-1, 0, 1], True),
    # "PreDual": ("int_choice", [-1, 0, 1, 2], True),
    # "PreSparsify": ("int_choice", [-1, 0, 1, 2], True),
    # "PreSOS1Encoding": ("int_choice", [-1, 0, 1, 2, 3], True),
    # "PreSOS2Encoding": ("int_choice", [-1, 0, 1, 2, 3], True),
    # "Method": ("int_choice", [-1, 0, 1, 2, 3, 4, 5], True),
    # "Sifting": ("int_choice", [-1, 0, 1, 2], True),
    # "SiftMethod": ("int_choice", [-1, 0, 1, 2], True),
    # "SimplexPricing": ("int_choice", [-1, 0, 1, 2, 3], True),

    # barrier
    # "BarConvTol": ("float_choice", [1e-9, 1e-8, 1e-7], True),
    # "BarCorrectors": ("int_choice", [-1, 0, 1, 10, 100, 500], True),
    # "BarHomogeneous": ("int_choice", [-1, 0, 1], True),
    # "BarOrder": ("int_choice", [-1, 0, 1], True),
    # "Crossover": ("int_choice", [-1, 0, 1, 2, 3, 4], True), # disable for now until fixed in Gurobi
    # "CrossoverBasis": ("int_choice", [-1, 0, 1], True),

    # scale
    # "ScaleFlag": ("int_choice", [-1, 0, 1, 2, 3], True), # disable for now until fixed in Gurobi

    # MIP
    # "BranchDir": ("int_choice", [-1, 0, 1], True),
    # "Disconnected": ("int_choice", [-1, 0, 1, 2], True),
    # "Heuristics": ("float", (0, 0.6), True),
    # "OBBT": ("int_choice", [-1, 0, 1, 2, 3], True),
    # "PartitionPlace": ("int", range(0, 31), True),
    # "VarBranch": ("int_choice", [-1, 0, 1, 2, 3], True),
    # "NodeMethod": ("int_choice", [-1, 0, 1, 2], True), # disable for now until fixed in Gurobi
    # "IISMethod": ("int_choice", [-1, 0, 1, 2, 3], True),

    # MIP cuts
    # "Cuts": ("int_choice", [-1, 0, 1, 2, 3], True),
    # "BQPCuts": ("int_choice", [-1, 0, 1, 2], True),
    # "CliqueCuts": ("int_choice", [-1, 0, 1, 2], True),
    # "CoverCuts": ("int_choice", [-1, 0, 1, 2], True),
    # "CutAggPasses": ("int_choice", [-1, 0, 1, 10, 100], True),
    # "CutPasses": ("int_choice", [-1, 0, 1, 10, 100], True),
    # "DualImpliedCuts": ("int_choice", [-1, 0, 1, 2], True),
    # "FlowCoverCuts": ("int_choice", [-1, 0, 1, 2], True),
    # "FlowPathCuts": ("int_choice", [-1, 0, 1, 2], True),
    # "GomoryPasses": ("int_choice", [-1, 0, 1, 10, 100], True),
    # "GUBCoverCuts": ("int_choice", [-1, 0, 1, 2], True),
    # "ImpliedCuts": ("int_choice", [-1, 0, 1, 2], True),
    # "InfProofCuts": ("int_choice", [-1, 0, 1, 2], True),
    # "LiftProjectCuts": ("int_choice", [-1, 0, 1, 2], True),
    # "MIPSepCuts": ("int_choice", [-1, 0, 1, 2], True),
    # "MIRCuts": ("int_choice", [-1, 0, 1, 2], True),
    # "MixingCuts": ("int_choice", [-1, 0, 1, 2], True),
    # "ModKCuts": ("int_choice", [-1, 0, 1, 2], True),
    # "NetworkCuts": ("int_choice", [-1, 0, 1, 2], True),
    # "ProjImpliedCuts": ("int_choice", [-1, 0, 1, 2], True),
    # "PSDCuts": ("int_choice", [-1, 0, 1, 2], True),
    # "RelaxLiftCuts": ("int_choice", [-1, 0, 1, 2], True),
    # "RLTCuts": ("int_choice", [-1, 0, 1, 2], True),
    # "StrongCGCuts": ("int_choice", [-1, 0, 1, 2], True),
    # "SubMIPCuts": ("int_choice", [-1, 0, 1, 2], True),
    # "ZeroHalfCuts": ("int_choice", [-1, 0, 1, 2], True),
}



def generate_gurobi(env=None, msg=True, time_limit=60):

    options = []
    options.append(("FeasibilityTol", 1e-9))
    options.append(("IntFeasTol", 1e-9))
    options.append(("IntegralityFocus", 1))
    options.append(("MIPGap", 0))
    options.append(("MIPGapAbs", 0))

    for option_name, (opt_type, candidates, default_enabled) in OPTIONS.items():
        if default_enabled:
            use_option = (random.random() < 0.9)
        else:
            use_option = (random.random() < 0.5)

        if not use_option:
            continue

        if opt_type == "int":
            if isinstance(candidates, range):
                min, max = candidates.start, candidates.stop
                val = random.randint(min, max)
            else:
                val = random.choice(candidates)
        elif opt_type == "float":
            min_val, max_val = candidates
            val = random.uniform(min_val, max_val)
        elif opt_type == "int_choice":
            val = random.choice(candidates)
        elif opt_type == "float_choice":
            val = random.choice(candidates)
        elif opt_type == "str_choice":
            val = random.choice(candidates)
        else:
            raise ValueError(f"Unknown option type: {opt_type}")
    
        options.append((option_name, val))

    return GUROBI_CMD(
        options=options,
        env=env,
        timeLimit=time_limit,
        msg=msg
    )


if __name__ == "__main__":
    solver = generate_gurobi()