import random
from pulp.pulp import HiGHS_CMD

# option_name: (opt_type, candidates, default_enabled)
params = {
    "presolve": ("str_choice", ["off", "on"], True),
    # "run_crossover": ("str_choice", ["off", "on", "choose"], True),
    # "ranging": ("str_choice", ["off", "on"], True),
    # "random_seed": ("int", range(0, 2147483647), True),
    # "simplex_strategy": ("int_choice", [0, 1, 2, 3], True), 
    # "simplex_scale_strategy": ("int_choice", [0, 1, 2, 3, 4], True),
    # "mip_detect_symmetry": ("str_choice", ["true", "false"], True),
    # "mip_allow_restart": ("str_choice", ["true", "false"], True),
    # "mip_lp_age_limit": ("int_choice", [0, 1, 10, 20, 50, 100], True),
    # "mip_pool_age_limit": ("int_choice", [0, 1, 10, 20, 30,  50, 100], True),
    # "mip_pscost_minreliable": ("int_choice", [0, 1, 5, 8, 10], True),
    # "mip_heuristic_effort": ("float", (0.0, 1.0), True),
}

def generate_highs(env=None, msg: bool = True, time_limit: int = 60):
    params_list = []
    params_list.append("mip_rel_gap=0")
    params_list.append("mip_abs_gap=0")
    params_list.append("primal_feasibility_tolerance=1e-9") # [1e-10, inf]
    # params_list.append("dual_feasibility_tolerance=1e-9") # [1e-10, inf]
    # params_list.append("ipm_optimality_tolerance=1e-9") # [1e-12, inf]
    # params_list.append("primal_residual_tolerance=1e-9") # [1e-10, inf]
    # params_list.append("dual_residual_tolerance=1e-9") # [1e-10, inf]

    for param_name, (param_type, candidates, default_enabled) in params.items():
        if default_enabled:
            use_param = (random.random() < 0.95)
        else:
            use_param = (random.random() < 0.5)

        if not use_param:
            continue

        if param_type == "int":
            if isinstance(candidates, range):
                min, max = candidates.start, candidates.stop
                val = random.randint(min, max)
            else:
                val = random.choice(candidates)
        elif param_type == "float":
            min_val, max_val = candidates
            val = random.uniform(min_val, max_val)
        elif param_type == "int_choice":
            val = random.choice(candidates)
        elif param_type == "str_choice":
            val = random.choice(candidates)
        else:
            raise ValueError(f"Unknown parameter type: {param_type}")
        
        params_list.append(f"{param_name}={val}")

    return HiGHS_CMD(
        options=params_list,
        env=env,
        msg=msg,
        timeLimit=time_limit,
    )
        

if __name__ == "__main__":
    solver = generate_highs()
