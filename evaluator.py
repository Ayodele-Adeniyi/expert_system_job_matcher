# evaluator.py

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class RequirementCheck:
    """Represents a single requirement check result."""
    passed: bool
    message: str
    expected: Any
    actual: Any
    field: str
    operator: str


@dataclass
class PositionResult:
    """Represents the evaluation result for a single position."""
    name: str
    qualified: bool
    required_passed: List[RequirementCheck]
    required_failed: List[RequirementCheck]
    required_match_pct: float
    desired_met: List[RequirementCheck]
    desired_missing: List[RequirementCheck]
    desired_match_pct: float


def check_constraint(facts: Dict, field: str, op: str, expected: Any, message: str) -> RequirementCheck:
    """
    Check a single constraint against the facts.
    
    Args:
        facts: Dictionary of user-provided facts
        field: The field to check
        op: Operator (bool, min, max, etc.)
        expected: Expected value
        message: Human-readable message
    
    Returns:
        RequirementCheck object with results
    """
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
        operator=op
    )


def evaluate_position(facts: Dict, position: Dict) -> PositionResult:
    """
    Evaluate a single position against the facts.
    
    Args:
        facts: Dictionary of user-provided facts
        position: Position dictionary with required/desired skills
    
    Returns:
        PositionResult object
    """
    # Check required skills
    required_checks = [
        check_constraint(facts, field, op, val, msg)
        for (field, op, val, msg) in position["required"]
    ]
    
    required_failed = [c for c in required_checks if not c.passed]
    required_passed = [c for c in required_checks if c.passed]
    required_match_pct = (len(required_passed) / len(required_checks)) * 100 if required_checks else 0
    
    # Check desired skills if they exist
    desired_checks = []
    if "desired" in position and position["desired"]:
        desired_checks = [
            check_constraint(facts, field, op, val, msg)
            for (field, op, val, msg) in position["desired"]
        ]
    
    desired_missing = [c for c in desired_checks if not c.passed]
    desired_met = [c for c in desired_checks if c.passed]
    desired_match_pct = (len(desired_met) / len(desired_checks)) * 100 if desired_checks else 0

    return PositionResult(
        name=position["name"],
        qualified=len(required_failed) == 0,
        required_passed=required_passed,
        required_failed=required_failed,
        required_match_pct=required_match_pct,
        desired_met=desired_met,
        desired_missing=desired_missing,
        desired_match_pct=desired_match_pct,
    )


def evaluate_all(facts: Dict, positions: List[Dict]) -> List[PositionResult]:
    """
    Evaluate all positions against the facts.
    
    Args:
        facts: Dictionary of user-provided facts
        positions: List of position dictionaries
    
    Returns:
        List of PositionResult objects
    """
    return [evaluate_position(facts, p) for p in positions]


class InferenceEngine:
    """
    Inference engine with tracing capability for debugging.
    """
    
    def __init__(self):
        self.trace = []
        self.reset_trace()
    
    def reset_trace(self):
        """Clear the trace log."""
        self.trace = []
    
    def evaluate_with_trace(self, facts: Dict, positions: List[Dict]) -> List[PositionResult]:
        """
        Evaluate positions with detailed tracing.
        
        Args:
            facts: Dictionary of user-provided facts
            positions: List of position dictionaries
        
        Returns:
            List of PositionResult objects
        """
        self.reset_trace()
        results = []
        
        self.trace.append("=" * 60)
        self.trace.append("INFERENCE ENGINE TRACE")
        self.trace.append("=" * 60)
        self.trace.append(f"\nFacts provided: {len(facts)}")
        for key, value in facts.items():
            if not key.startswith('_') and not isinstance(value, (list, dict)):
                self.trace.append(f"  - {key}: {value}")
        
        for position in positions:
            self.trace.append(f"\n{'-' * 40}")
            self.trace.append(f"Evaluating: {position['name']}")
            self.trace.append(f"{'-' * 40}")
            
            # Check required skills
            self.trace.append("\n  REQUIRED SKILLS:")
            required_checks = []
            for (field, op, val, msg) in position["required"]:
                actual = facts.get(field)
                check = check_constraint(facts, field, op, val, msg)
                required_checks.append(check)
                
                status = "✅ PASS" if check.passed else "❌ FAIL"
                self.trace.append(f"    {status} - {msg}")
                self.trace.append(f"        Expected: {val} {op}, Actual: {actual}")
            
            # Check desired skills
            if "desired" in position and position["desired"]:
                self.trace.append("\n  DESIRED SKILLS:")
                for (field, op, val, msg) in position["desired"]:
                    actual = facts.get(field)
                    check = check_constraint(facts, field, op, val, msg)
                    
                    status = "✅ MET" if check.passed else "⭐ NOT MET"
                    self.trace.append(f"    {status} - {msg}")
                    self.trace.append(f"        Expected: {val} {op}, Actual: {actual}")
            
            # Calculate result
            failed = [c for c in required_checks if not c.passed]
            qualified = len(failed) == 0
            
            self.trace.append(f"\n  RESULT: {'QUALIFIED' if qualified else 'NOT QUALIFIED'}")
            if not qualified:
                self.trace.append(f"    Missing {len(failed)} required skills")
        
        self.trace.append("\n" + "=" * 60)
        
        # Return normal evaluation results
        return evaluate_all(facts, positions)