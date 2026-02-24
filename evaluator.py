# evaluator.py

import operator
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class RequirementCheck:
    passed: bool
    message: str
    expected: Any
    actual: Any
    field: str
    operator: str

@dataclass
class PositionResult:
    name: str
    qualified: bool
    required_passed: List[RequirementCheck]
    required_failed: List[RequirementCheck]
    required_match_pct: float
    desired_met: List[RequirementCheck]
    desired_missing: List[RequirementCheck]
    desired_match_pct: float

# Operator mapping for scalability
OPS = {
    "bool": lambda a, e: bool(a) == bool(e),
    "min": lambda a, e: float(a or 0) >= float(e),
    "max": lambda a, e: float(a or 0) <= float(e),
    "eq": lambda a, e: a == e
}

def check_constraint(facts: Dict, field: str, op: str, expected: Any, message: str) -> RequirementCheck:
    actual = facts.get(field)
    try:
        passed = OPS[op](actual, expected)
    except (ValueError, TypeError, KeyError):
        passed = False

    return RequirementCheck(passed, message, expected, actual, field, op)

def evaluate_position(facts: Dict, position: Dict) -> PositionResult:
    req_checks = [check_constraint(facts, f, o, v, m) for (f, o, v, m) in position["required"]]
    req_failed = [c for c in req_checks if not c.passed]
    req_passed = [c for c in req_checks if c.passed]
    req_pct = (len(req_passed) / len(req_checks)) * 100 if req_checks else 0
    
    des_checks = [check_constraint(facts, f, o, v, m) for (f, o, v, m) in position.get("desired", [])]
    des_met = [c for c in des_checks if c.passed]
    des_missing = [c for c in des_checks if not c.passed]
    des_pct = (len(des_met) / len(des_checks)) * 100 if des_checks else 0

    return PositionResult(position["name"], len(req_failed) == 0, req_passed, req_failed, req_pct, des_met, des_missing, des_pct)

class InferenceEngine:
    def __init__(self):
        self.trace = []

    def evaluate_with_trace(self, facts: Dict, positions: List[Dict]) -> List[PositionResult]:
        self.trace = ["="*60, "INFERENCE ENGINE TRACE", "="*60, f"\nFacts: {len(facts)}"]
        for k, v in facts.items():
            if not isinstance(v, (list, dict)): self.trace.append(f"  - {k}: {v}")
        
        results = []
        for pos in positions:
            self.trace.append(f"\nEvaluating: {pos['name']}")
            res = evaluate_position(facts, pos)
            results.append(res)
            self.trace.append(f"  RESULT: {'QUALIFIED' if res.qualified else 'NOT QUALIFIED'}")
        return results