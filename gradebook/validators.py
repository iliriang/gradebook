"""Input validation helpers for the gradebook package."""


def parse_grade(value: object) -> float:
    """Parse and validate a grade in the inclusive range [0, 100]."""
    try:
        grade = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Grade must be numeric.") from exc

    if not 0 <= grade <= 100:
        raise ValueError("Grade must be between 0 and 100.")
    return grade
