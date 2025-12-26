import sys
import os
import datetime
import time
from dataclasses import dataclass
from pulp.pulp import LpProblem, LpSolver, LpStatus, value

@dataclass
class SolveResult:
    solver: str
    status: str
    objective: float
    solution_map: dict
    elapsed_time: float
    error_message: str = None
    output_pipe: object = None

    def __del__(self):
        if self.output_pipe and self.output_pipe.name and os.path.exists(self.output_pipe.name):
            self.output_pipe.close()
            os.remove(self.output_pipe.name)

########################################################################################
### solver an MIP problem with the given solver
########################################################################################
def solve(
    prob: LpProblem,
    solver: LpSolver,
) -> SolveResult:
    try:
        start_time = time.time()
        status, pipe = prob.solve(solver)
        end_time = time.time()
        elapsed_time = end_time - start_time
        status = LpStatus.get(status, "unknown")
        try:
            objective = value(prob.objective)
        except Exception as e:
            objective = None

        try:
            solution_map = [
                {"name": v.name, "value": v.varValue} for v in prob.variables()
            ]
        except Exception as e:
            solution_map = None

        # double check to close the pipe
        if pipe:
            pipe.close()

        return SolveResult(
            solver=solver.name,
            status=status,
            objective=objective,
            solution_map=solution_map,
            elapsed_time=elapsed_time,
            output_pipe=pipe,
        )
    except Exception as e:
        warning(f"Unexpected error when solving the problem: {e}")
        return SolveResult(
            solver=solver.name,
            status="UnexpectedError",
            error_message=str(e),
            objective=None,
            solution_map=None,
            elapsed_time=None,
            output_pipe=None,
        )

### read the content from the pipe
def read_pipe(pipe):
    if pipe is None or pipe.name is None or not os.path.exists(pipe.name):
        return []
    output = []
    with open(pipe.name, "r") as f:
        for line in f:
            output.append(line.strip())
    return output

########################################################################################
### printing fancy messages
########################################################################################
def _fmt(level):
    colors = {
        "DEBUG": "\033[34m",   # Blue
        "INFO": "\033[32m",    # Green
        "NOTICE": "\033[32m",  # Green
        "WARNING": "\033[33m", # Orange (Yellow)
        "ERROR": "\033[31m"    # Red
    }
    color_reset = "\033[0m"  # Reset color

    color = colors.get(level, "\033[31m")  # Default to red for unknown levels

    # Check terminal compatibility
    if not os.getenv("TERM", "").startswith("xterm") or not sys.stdout.isatty():
        color = ""
        color_reset = ""

    return f"{color}[{level:>9}]{color_reset}"

def log_message(level, message):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_level = _fmt(level)
    print(f"{formatted_level} [{time}] {message}", file=sys.stderr)

def error(*args):
    log_message("ERROR", " ".join(map(str, args)))

def warning(*args):
    log_message("WARNING", " ".join(map(str, args)))

def info(*args):
    log_message("INFO", " ".join(map(str, args)))

def debug(*args):
    log_message("DEBUG", " ".join(map(str, args)))


if __name__ == "__main__":
    error("This is an error message")
    warning("This is a warning message")
    info("This is an info message")
    debug("This is a debug message")
