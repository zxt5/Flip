import random
from pulp.pulp import MOSEK

OPTIONS = {
    "MSK_IPAR_PRESOLVE_USE": ("int_choice", [0, 1, 2], True),
    # ...
}

def generate_mosek(env=None, msg=True, time_limit=60):
    options = {} # dict
    options["MSK_DPAR_MIO_TOL_ABS_GAP"] = 0.0
    options["MSK_DPAR_MIO_TOL_REL_GAP"] = 0.0
    options["MSK_DPAR_MIO_TOL_ABS_RELAX_INT"] = 1e-9
    options["MSK_DPAR_MIO_TOL_FEAS"] = 1e-9

    for option_name, (opt_type, candidates, default_enabled) in OPTIONS.items():
        if default_enabled:
            use_option = (random.random() < 0.95)
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
        elif opt_type == "str_choice":
            val = random.choice(candidates)
        else:
            raise ValueError(f"Unknown option type: {opt_type}")
        
        options[option_name] = val

    return MOSEK(options=options, timeLimit=time_limit, msg=msg)

if __name__ == "__main__":
    solver = generate_mosek(msg=True)