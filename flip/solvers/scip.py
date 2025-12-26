import random
from pulp.pulp import SCIP_CMD

params = {
    "lp/presolving": ("str_choice", ["TRUE", "FALSE"], True),
    # ...
}

def generate_scip(env=None, msg: bool = True, time_limit: int = 60):
    params_list = []
    params_list.append("limits/gap=0")
    params_list.append("limits/absgap=0")
    params_list.append("numerics/feastol = 1e-9")
    params_list.append("numerics/epsilon = 1e-9")
    params_list.append("numerics/sumepsilon = 1e-9")
    # params_list.append("numerics/dualfeastol = 1e-9")

    # if random.random() < 0.3:
    #     params_list.append("presolving/maxrounds = 0")
    # else:
    #     if random.random() < 0.5:
    #         params_list.append("presolving/maxrounds = -1")
    #     else:
    #         maxrounds = random.randint(1, 1000)
    #         params_list.append(f"presolving/maxrounds = {maxrounds}")

    for param_name, (param_type, candidates, default_enabled) in params.items():
        if default_enabled:
            use_param = random.random() < 0.9
        else:
            use_param = random.random() < 0.5

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
            raise ValueError(f"Unsupported parameter type: {param_type}")

        params_list.append(f"{param_name} = {val}")

    return SCIP_CMD(
        options=params_list,
        env=env,
        msg=msg,
        timeLimit=time_limit,
    )


if __name__ == "__main__":
    solver = generate_scip()