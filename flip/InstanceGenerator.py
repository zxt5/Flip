import random
from pulp.pulp import GUROBI_CMD, SCIP_CMD, COIN_CMD, HiGHS_CMD, MOSEK
from pulp.pulp import LpMinimize, LpProblem, LpInteger, LpContinuous, LpVariable, lpSum, LpConstraint, LpConstraintLE
from flip.LpInstance import LpInstance
from flip.utils import solve
from pulp.pulp import LpMinimize, LpProblem, LpContinuous, LpInteger, LpVariable, lpSum

class InstanceGenerator:
    '''
    A class to generate feasible and infeasible instances.
    '''
    def __init__(self,
                 min_num_vars: int = 2,
                 max_num_vars: int = 10,
                 min_cons_ratio: float = 2,
                 max_cons_ratio: float = 5,
                 min_sparsity: float = 0.8,
                 max_sparsity: float = 1.0,
                 min_integer_ratio: float = 0.0,
                 max_integer_ratio: float = 1.0,
                 min_bound_radius: int = 20,
                 max_bound_radius: int = 100,
                 mode: str = 'MIP',
                 reference_solver: str = "GUROBI_CMD",
                ):
        self.min_num_vars = min_num_vars
        self.max_num_vars = max_num_vars
        self.min_cons_ratio = min_cons_ratio
        self.max_cons_ratio = max_cons_ratio
        self.min_sparsity = min_sparsity
        self.max_sparsity = max_sparsity
        self.min_integer_ratio = min_integer_ratio
        self.max_integer_ratio = max_integer_ratio
        self.min_bound_radius = min_bound_radius
        self.max_bound_radius = max_bound_radius
        self.mode = mode
        self.reference_solver = reference_solver

    def generate_feasible_solution(self,
                                   num_vars: int,
                                   lower_bound: int = -100,
                                   upper_bound: int = 100,
                                   ):
        return [random.randint(lower_bound, upper_bound) for _ in range(num_vars)]

    def generate_variables(self,
                           num_vars: int,
                           mode: str = 'MIP',
                           lower_bound: int = -100,
                           upper_bound: int = 100,
                           ):
        var_list = []
        cats = []

        if mode == "IP":
            cats = [LpInteger] * num_vars
        elif mode == "LP":
            cats = [LpContinuous] * num_vars
        else:
            assert mode == "MIP", "mode should be either 'IP', 'LP', or 'MIP'"
            num_ints = int(num_vars * random.uniform(self.min_integer_ratio, self.max_integer_ratio))
            int_indices = random.sample(range(num_vars), num_ints)
            cats = [LpInteger if i in int_indices else LpContinuous for i in range(num_vars)]

        for i in range(num_vars):
            var_list.append(LpVariable(f'x{i}', lowBound=lower_bound, upBound=upper_bound, cat=cats[i]))
        return var_list

    def get_density(self):
        return 1.0 if random.random() < 0.2 else random.uniform(self.min_sparsity, self.max_sparsity)

    def generate_coeff_matrix(self,
                              num_vars: int,
                              num_cons: int,
                              sparsity: float = 0.8,
                              coeff_range = (-100.0, 100.0),
                              ):
        coeff_matrix = []
        for _ in range(num_cons):
            coeffs = [round(random.uniform(*coeff_range), 2) if random.random() < sparsity else 0 for _ in range(num_vars)]
            # ensure at least one non-zero coefficient
            if all(c == 0 for c in coeffs):
                idx = random.randint(0, num_vars - 1)
                c = 0
                while c == 0:
                    c = round(random.uniform(*coeff_range), 2)
                coeffs[idx] = c
            coeff_matrix.append(coeffs)
        return coeff_matrix

    def generate_objective_function(self, vars: list, coeff_range = (-500.0, 500.0)):
        coeffs = []
        for _ in vars:
            coeffs.append(round(random.uniform(*coeff_range), 2))
        return lpSum([coeffs[i] * vars[i] for i in range(len(vars))])

    def get_reference_solver(self):
        if self.reference_solver == "GUROBI_CMD":
            return GUROBI_CMD(gapRel=0, gapAbs=0, msg=False, timeLimit=10)
        elif self.reference_solver == "SCIP_CMD":
            return SCIP_CMD(gapRel=0, gapAbs=0, msg=False, timeLimit=10)
        elif self.reference_solver == "COIN_CMD":
            return COIN_CMD(gapRel=0, gapAbs=0, msg=False, timeLimit=10)
        elif self.reference_solver == "HiGHS_CMD":
            return HiGHS_CMD(gapRel=0, gapAbs=0, msg=False, timeLimit=10)
        elif self.reference_solver == "MOSEK":
            return MOSEK(options={"MSK_DPAR_MIO_TOL_ABS_GAP": 0.0, "MSK_DPAR_MIO_TOL_REL_GAP": 0.0}, msg=False, timeLimit=10)
        else:
            raise ValueError(f"Invalid reference solver: {self.reference_solver}")

    def generate_feasibility_breaking_constraint(self, prob: LpProblem) -> LpConstraint:
        reference_solver = self.get_reference_solver()
        result = solve(prob, reference_solver)
        if result.status != "Optimal":
            return None
        objective = result.objective
        if objective is None:
            raise ValueError("Cannot extract objective value from the solved problem.")
        objective_function = prob.objective
        epsilon = random.uniform(0.05, 0.2) # configurable
        fbc = lpSum([var * coef for var, coef in objective_function.items()]) <= objective - epsilon
        feasibility_breaking_constraint = LpConstraint(e=fbc, sense=LpConstraintLE, name="fbc")
        return feasibility_breaking_constraint

    def generate_feasible_instance(self) -> LpInstance:
        sense = LpMinimize
        num_vars = random.randint(self.min_num_vars, self.max_num_vars)
        num_cons = random.randint(int(num_vars * self.min_cons_ratio), int(num_vars * self.max_cons_ratio))
        sparsity = self.get_density()
        feasible_solution = self.generate_feasible_solution(num_vars)
        vars = self.generate_variables(num_vars, self.mode)
        coeff_matrix = self.generate_coeff_matrix(num_vars, num_cons, sparsity)
        prob = LpProblem("feasible", sense)
        rhs_bound = random.randint(1, 2500)

        for i in range(num_cons):
            coeffs = coeff_matrix[i]
            assert not all(c == 0 for c in coeffs), "All coefficients cannot be zero"
            lhs_value = sum(coeffs[j] * feasible_solution[j] for j in range(num_vars))
            r = random.randint(2, 4)
            rhs = round(random.uniform(- rhs_bound, rhs_bound), r)
            if lhs_value <= rhs:
                prob += (lpSum([coeffs[j] * vars[j] for j in range(num_vars)]) <= rhs, f"c{i}")
            else:
                prob += (lpSum([coeffs[j] * vars[j] for j in range(num_vars)]) >= rhs, f"c{i}")
        
        prob += self.generate_objective_function(vars)
        
        solution_map = {f'x{i}': feasible_solution[i] for i in range(num_vars)}
        feasible_instance = LpInstance(prob, True, solution=solution_map)
        return feasible_instance

    def generate_infeasible_instance(self) -> LpInstance:
        sense = LpMinimize
        base_instance = self.generate_feasible_instance()
        infeasible_prob = LpProblem("infeasible", sense)

        for cons in base_instance.prob.constraints:
            cons = base_instance.prob.constraints[cons]
            infeasible_prob += cons
        
        vars = base_instance.prob.variables()
        fbc = self.generate_feasibility_breaking_constraint(base_instance.prob)
        infeasible_prob += fbc
        infeasible_prob += self.generate_objective_function(vars)

        infeasible_instance = LpInstance(
            infeasible_prob,
            False,
            solution=base_instance.solution,
        )

        return infeasible_instance
        

    def generate_random_instance(self) -> LpInstance:
        sense = LpMinimize
        num_vars = random.randint(self.min_num_vars, self.max_num_vars)
        num_cons = random.randint(int(num_vars * self.min_cons_ratio), num_vars * self.max_cons_ratio)
        sparsity = self.get_density()
        vars = self.generate_variables(num_vars, self.mode)
        coeff_matrix = self.generate_coeff_matrix(num_vars, num_cons, sparsity)        
        prob = LpProblem("random", sense)

        rhs_bound = random.randint(1, 2500)

        for i in range(num_cons):
            coeffs = coeff_matrix[i]
            r = random.randint(2, 4)
            rhs = round(random.uniform(-rhs_bound, rhs_bound), r)
            if random.random() < 0.5:
                prob += (lpSum([coeffs[j] * vars[j] for j in range(num_vars)]) <= rhs, f"c{i}")
            else:
                prob += (lpSum([coeffs[j] * vars[j] for j in range(num_vars)]) >= rhs, f"c{i}")

        prob += self.generate_objective_function(vars)

        random_instance = LpInstance(prob, None, None)

        return random_instance

if __name__ == "__main__":
    pass