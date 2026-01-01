# Flip: Validating Mixed-Integer Programming Solvers

**Flip** is a fuzzing framework for mixed-integer programming (MIP) solvers.
It systematically generates random MIP instances that are guaranteed by
construction to be either feasible or infeasible, with the goal of
uncovering correctness bugs in solver implementations.
Flip was first introduced in the research paper
[Validating Mixed-Integer Programming Solvers]()
published at ICSE 2026.