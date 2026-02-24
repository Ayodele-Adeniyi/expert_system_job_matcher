# evaluator.py

from dataclasses import dataclass


@dataclass
class PositionResult:
    name: str
    qualified: bool
    required_passed: list
    required_failed: list
    required_match_pct: float


def check_constraint(facts, field, op, expected, message):
    actual = facts.get(field)

    if op == "bool":
        passed = bool(actual) == bool(expected)
    elif op == "min":
        try:
            passed = float(actual) >= float(expected)
        except:
            passed = False
    else:
        passed = False

    return {
        "passed": passed,
        "message": message,
        "expected": expected,
        "actual": actual,
    }


def evaluate_position(facts, position):
    checks = [
        check_constraint(facts, f, op, val, msg)
        for (f, op, val, msg) in position["required"]
    ]

    failed = [c for c in checks if not c["passed"]]
    passed = [c for c in checks if c["passed"]]

    return PositionResult(
        name=position["name"],
        qualified=len(failed) == 0,
        required_passed=passed,
        required_failed=failed,
        required_match_pct=(len(passed) / len(checks)) * 100,
    )


def evaluate_all(facts, positions):
    return [evaluate_position(facts, p) for p in positions]