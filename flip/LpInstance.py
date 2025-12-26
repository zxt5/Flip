import os
import json
from pulp.pulp import LpProblem
from flip.utils import warning
from pathlib import Path

class LpInstance:
    def __init__(self, prob: LpProblem, feasibility: bool, solution: dict):
        self.prob = prob
        self.num_vars = len(prob.variables())
        self.num_cons = len(prob.constraints)
        self.feasibility = feasibility
        self.solution = solution

    def __str__(self):
        str = ""
        str += f"{self.prob}\n"
        str += "=" * 10 + " info " + "=" * 10 + "\n"
        str += f"num_vars: {self.num_vars}\n"
        str += f"num_cons: {self.num_cons}\n"
        str += f"feasibility: {self.feasibility}\n"
        str += f"solution: {self.solution}\n"
        return str

    def save(self, mps_file_path: Path, dump_json_file: bool = True, dump_lp_file: bool = False):
        mps_file_path = Path(mps_file_path)
        if dump_lp_file:
            lp_file_path = mps_file_path.with_suffix(".lp")
            self.prob.writeLP(lp_file_path)
        self.prob.writeMPS(mps_file_path)
        if dump_json_file:
            json_file_path = mps_file_path.with_suffix(".json")
            self.toJSON(json_file_path)

    def toJSON(self, json_file: Path):
        """
        Serialize the instance to a JSON file,
        ignoring the unserializable prob attribute
        """
        serializable_dict = {}
        
        for key, value in self.__dict__.items():
            if key == 'prob':
                continue
            
            try:
                json.dumps(value)
                serializable_dict[key] = value
            except (TypeError, OverflowError):
                if hasattr(value, '__str__'):
                    serializable_dict[key] = str(value)
                else:
                    warning(f"Skipping non-serializable attribute '{key}' with value: {value}")
        
        with open(json_file, "w") as f:
            json.dump(serializable_dict, f, indent=2, ensure_ascii=False)

    @classmethod
    def loadInstance(cls, mps_file: str, json_file: str) -> 'LpInstance':
        assert os.path.exists(mps_file), f"MPS file {mps_file} not found"
        assert os.path.exists(json_file), f"JSON file {json_file} not found"
        
        vars, prob = LpProblem.fromMPS(mps_file)
        
        with open(json_file, "r") as f:
            json_dict = json.load(f)
        
        instance = LpInstance(
            prob,
            json_dict['feasibility'],
            json_dict['solution'],
        )

        return instance

    @classmethod
    def fromJSON(cls, json_file: Path) -> 'LpInstance':
        json_file = Path(json_file)
        mps_file = json_file.with_suffix(".mps")
        if not os.path.exists(mps_file):
            raise FileNotFoundError(f"MPS file {mps_file} not found")

        return cls.loadInstance(mps_file, json_file)

    @classmethod
    def fromMPS(cls, mps_file: Path) -> 'LpInstance':
        mps_file = Path(mps_file)
        json_file = mps_file.with_suffix(".json")
        if not os.path.exists(json_file):
            raise FileNotFoundError(f"JSON file {json_file} not found")
        
        return cls.loadInstance(mps_file, json_file)
        