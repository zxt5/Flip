import random
from pulp.pulp import COIN_CMD

params = {
    # "agg": ("int_choice", [-1, 1, 2, 3, 4, 5], True),
    # "bkpivot": ("int", range(0, 6), True),
    # "bkclqext": ("int", range(0, 5), True),
    # "depth": ("int_choice", [-1, -2, -12, -3, -999, 1], True),
    # "diveO": ("int_choice", [-1, 3, 4, 5, 6, 7], True), # cbc crashes with value > 10
    # "hOp": ("int_choice", [0, 1, 2, 4, 8], True),
    # "hot": ("int", range(0, 200), True),
    # "slow": ("int", range(-1, 15), True),
    # "oddwext": ("int_choice", [0, 1, 2], True),
    # "randomC": ("int", range(-1, 2147483647), True),
    # "passC": ("int", range(-200, 200), True),
    # "strong": ("int", range(0, 20), True),
    # *** Keyword parameters: ***
    # "clique": ("str_choice", ["on", "off", "root", "ifmove", "forceon", "onglobal"], True),
    # "cuts": ("str_choice", ["on", "off", "root", "ifmove", "forceon"], True),
    # "flow": ("str_choice", ["on", "off", "root", "ifmove", "forceon", "onglobal"], True),
    # "GMI": ("str_choice", ["on", "off", "root", "ifmove", "forceon", "endonly", "long", "longroot", "longifmove", "forcelongon", "longendonly"], True),
    # "gomory": ("str_choice", ["on", "off", "root", "ifmove", "forceon", "forceandglobal", "forcelongon", "onglobal", "longer", "shorter"], True),
    # "knapsack": ("str_choice", ["on", "off", "root", "ifmove", "forceon", "forceandglobal", "onglobal"], True),
    # "lagomory": ("str_choice", ["off", "root", "endonly", "endonlyroot", "endclean", "endcleanroot", "endboth", "onlyaswell", "onlyaswellroot", "cleanaswell", "cleanaswellroot", "bothaswell", "bothaswellroot", "onlyinstead", "cleaninstead", "bothinstead"], True),
    # "lift": ("str_choice", ["on", "off", "root", "ifmove", "forceon", "iflongon"], True),
    # "latwomir": ("str_choice", ["off", "endonly", "endonlyroot", "endclean", "endcleanroot", "endboth", "onlyaswell", "cleanaswell", "bothaswell", "onlyinstead", "cleaninstead", "bothinstead"], True),
    # "mixed": ("str_choice", ["on", "off", "root", "ifmove", "forceon", "onglobal"], True),
    # "oddwheel": ("str_choice", ["on", "off", "root", "ifmove", "forceon", "onglobal"], True),
    # "probing": ("str_choice", ["on", "off", "root", "ifmove", "forceon", "forceonbut", "forceonbutstrong", "forceonglobal", "forceonstrong", "onglobal", "strongroot"], True),
    # "reduceAndSplitCuts": ("str_choice", ["on", "off", "root", "ifmove", "forceon"], True),
    # "reduce2AndSplitCuts": ("str_choice", ["on", "off", "root", "longon", "longroot"], True),
    # "residual": ("str_choice", ["on", "off", "root", "ifmove", "forceon"], True),
    # "two": ("str_choice", ["on", "off", "root", "ifmove", "forceon", "forceandglobal", "forcelongon", "onglobal"], True),
    # "zero": ("str_choice", ["on", "off", "root", "ifmove", "forceon", "onglobal"], True),
    # "combineSolutions": ("str_choice", ["on", "off", "both", "before", "onequick", "bothquick", "beforequick"], True),
    # "combine2Solutions": ("str_choice", ["on", "off"], True),
    # "feas": ("str_choice", ["on", "off", "both", "before"], True),
    # "greedy": ("str_choice", ["on", "off", "both", "before"], True),
    # "local": ("str_choice", ["on", "off", "10", "100", "300"], True),
    # "pivotAndF": ("str_choice", ["on", "off", "both", "before"], True),
    # "Rins": ("str_choice", ["on", "off", "both", "before", "often"], True),
    # "round": ("str_choice", ["on", "off", "both", "before"], True),
    # "Vnd": ("str_choice", ["on", "off", "both", "before", "intree"], True),
    # "clqstr": ("str_choice", ["off", "before", "after"], True),
    # "constraint": ("str_choice", ["on", "off", "variable", "forcevariable", "conflict"], True),
    # "Orbit": ("str_choice", ["on", "off", "slowish", "strong", "force", "simple", "lightweight", "moreprinting", "cuts", "cutslight"], True),
    # "sosP": ("str_choice", ["off", "high", "low", "orderhigh", "orderlow"], True),
    # "cgraph": ("str_choice", ["on", "off", "clq"], True),

    ### Clp options
    # "KKT": ("str_choice", ["on", "off"], True),
    # "cross": ("str_choice", ["on", "off", "maybe", "presolve"], True),
    # "gamma": ("str_choice", ["on", "off", "gamma", "delta", "onstrong", "gammastrong", "deltastrong"], True),
    # "scal": ("str_choice", ["off", "equi", "geo", "auto", "dynamic", "rows"], True),
    # "vector": ("str_choice", ["on", "off"], True),

    "presolve": ("str_choice", ["on", "off"], True),
    "preprocess": ("str_choice", ["on", "off"], True),
}

def generate_cbc(env = None, msg: bool = True, time_limit: int = 60):
        
    params_list = []
    params_list.append("allow 0")
    params_list.append("ratio 0")
    params_list.append("integerT 1e-9")

    for param_name, (param_type, candidates, default_enabled) in params.items():
        if default_enabled:
            use_option = (random.random() < 0.95)
        else:
            use_option = (random.random() < 0.5)

        if not use_option:
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

        params_list.append(f"{param_name} {val}")
        
    return COIN_CMD(
        options=params_list,
        env=env,
        msg=msg,
        timeLimit=time_limit,
    )

if __name__ == "__main__":
    solver = generate_cbc()

