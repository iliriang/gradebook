"""Seed script to populate sample gradebook data."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gradebook.service import add_course, add_grade, add_student, enroll
from gradebook.storgate import save_data


def seed() -> None:
    """Create sample students, courses, enrollments, and grades."""
    data = {
        "students": [],
        "courses": [],
        "enrollments": [],
        "next_student_id": 1,
    }

    add_course(data, "CS101", "Intro to CS")
    add_course(data, "MATH201", "Discrete Math")

    ilirian_id = add_student(data, "Ilirian Gerxhaliu")
    ardit_id = add_student(data, "Ardit Tahiri")
    elsa_id = add_student(data, "Elsa Hoxha")

    enroll(data, ilirian_id, "CS101")
    enroll(data, ilirian_id, "MATH201")
    enroll(data, ardit_id, "CS101")
    enroll(data, elsa_id, "MATH201")

    add_grade(data, ilirian_id, "CS101", 93)
    add_grade(data, ilirian_id, "CS101", 88)
    add_grade(data, ilirian_id, "MATH201", 91)
    add_grade(data, ardit_id, "CS101", 79)
    add_grade(data, elsa_id, "MATH201", 85)
    add_grade(data, elsa_id, "MATH201", 90)

    output_path = Path(__file__).resolve().parent.parent / "data" / "gradebook.json"
    save_data(data, output_path)
    print(f"Sample data written to {output_path}")


if __name__ == "__main__":
    seed()
