# evaluator.py

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
    total_match_pct: float


def check_constraint(facts: Dict, field: str, op: str, expected: Any, message: str) -> RequirementCheck:
    actual = facts.get(field)

    if op == "bool":
        passed = bool(actual) == bool(expected)
    elif op == "min":
        try:
            passed = float(actual) >= float(expected)
        except (TypeError, ValueError):
            passed = False
    elif op == "max":
        try:
            passed = float(actual) <= float(expected)
        except (TypeError, ValueError):
            passed = False
    else:
        passed = False

    return RequirementCheck(
        passed=passed,
        message=message,
        expected=expected,
        actual=actual,
        field=field,
        operator=op,
    )


def evaluate_position(facts: Dict, position: Dict) -> PositionResult:
    required_checks = [
        check_constraint(facts, field, op, val, msg)
        for (field, op, val, msg) in position.get("required", [])
    ]

    required_failed = [c for c in required_checks if not c.passed]
    required_passed = [c for c in required_checks if c.passed]
    required_match_pct = (len(required_passed) / len(required_checks)) * 100 if required_checks else 0.0

    desired_checks = [
        check_constraint(facts, field, op, val, msg)
        for (field, op, val, msg) in position.get("desired", [])
    ]
    desired_missing = [c for c in desired_checks if not c.passed]
    desired_met = [c for c in desired_checks if c.passed]
    desired_match_pct = (len(desired_met) / len(desired_checks)) * 100 if desired_checks else 0.0

    total_checks = len(required_checks) + len(desired_checks)
    total_passed = len(required_passed) + len(desired_met)
    total_match_pct = (total_passed / total_checks) * 100 if total_checks else 0.0

    return PositionResult(
        name=position["name"],
        qualified=len(required_failed) == 0,
        required_passed=required_passed,
        required_failed=required_failed,
        required_match_pct=required_match_pct,
        desired_met=desired_met,
        desired_missing=desired_missing,
        desired_match_pct=desired_match_pct,
        total_match_pct=total_match_pct,
    )


def evaluate_all(facts: Dict, positions: List[Dict]) -> List[PositionResult]:
    return [evaluate_position(facts, p) for p in positions]


class InferenceEngine:
    def __init__(self):
        self.trace = []

    def reset_trace(self):
        self.trace = []

    def evaluate_with_trace(self, facts: Dict, positions: List[Dict]) -> List[PositionResult]:
        self.reset_trace()

        self.trace.append("=" * 60)
        self.trace.append("INFERENCE ENGINE TRACE")
        self.trace.append("=" * 60)
        self.trace.append(f"Facts provided: {len(facts)}")

        for position in positions:
            self.trace.append("")
            self.trace.append("-" * 40)
            self.trace.append(f"Evaluating: {position['name']}")
            self.trace.append("-" * 40)

            self.trace.append("REQUIRED:")
            for (field, op, val, msg) in position.get("required", []):
                check = check_constraint(facts, field, op, val, msg)
                status = "PASS" if check.passed else "FAIL"
                self.trace.append(f"  {status} | {msg} | expected={val} op={op} actual={facts.get(field)}")

            if position.get("desired"):
                self.trace.append("DESIRED:")
                for (field, op, val, msg) in position.get("desired", []):
                    check = check_constraint(facts, field, op, val, msg)
                    status = "MET" if check.passed else "NOT MET"
                    self.trace.append(f"  {status} | {msg} | expected={val} op={op} actual={facts.get(field)}")

        self.trace.append("=" * 60)

        return evaluate_all(facts, positions)