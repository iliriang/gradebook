"""Command-line interface for the Gradebook mini-project."""

import argparse
from typing import Any

from gradebook.logging_config import get_logger
from gradebook.service import (
    add_course,
    add_grade,
    add_student,
    compute_average,
    compute_gpa,
    enroll,
    list_courses,
    list_enrollments,
    list_students,
)
from gradebook.storgate import load_data, save_data
from gradebook.validators import parse_grade

LOGGER = get_logger(__name__)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Gradebook CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_student_parser = subparsers.add_parser("add-student", help="Add a student")
    add_student_parser.add_argument("--name", required=True, help="Student full name")

    add_course_parser = subparsers.add_parser("add-course", help="Add a course")
    add_course_parser.add_argument("--code", required=True, help="Course code, e.g. CS101")
    add_course_parser.add_argument("--title", required=True, help="Course title")

    enroll_parser = subparsers.add_parser("enroll", help="Enroll a student in a course")
    enroll_parser.add_argument("--student-id", type=int, required=True)
    enroll_parser.add_argument("--course", required=True)

    add_grade_parser = subparsers.add_parser("add-grade", help="Add grade for enrollment")
    add_grade_parser.add_argument("--student-id", type=int, required=True)
    add_grade_parser.add_argument("--course", required=True)
    add_grade_parser.add_argument("--grade", required=True)

    list_parser = subparsers.add_parser("list", help="List records")
    list_parser.add_argument("entity", choices=["students", "courses", "enrollments"])
    list_parser.add_argument("--sort", choices=["name", "code", "id", "title"], default=None)

    avg_parser = subparsers.add_parser("avg", help="Compute course average")
    avg_parser.add_argument("--student-id", type=int, required=True)
    avg_parser.add_argument("--course", required=True)

    gpa_parser = subparsers.add_parser("gpa", help="Compute student GPA")
    gpa_parser.add_argument("--student-id", type=int, required=True)

    return parser


def _print_list(entity: str, items: list[dict]) -> None:
    if not items:
        print(f"No {entity} found.")
        return

    if entity == "students":
        for student in items:
            print(f"id={student['id']} | name={student['name']}")
    elif entity == "courses":
        for course in items:
            print(f"code={course['code']} | title={course['title']}")
    else:
        for enrollment_item in items:
            print(
                "student_id="
                f"{enrollment_item['student_id']} | "
                f"course={enrollment_item['course_code']} | "
                f"grades={enrollment_item['grades']}"
            )


def run_cli(args: list[str] | None = None) -> int:
    """Run CLI commands and return process-style exit code."""
    parser = _build_parser()
    parsed = parser.parse_args(args)

    try:
        data = load_data()

        if parsed.command == "add-student":
            student_id = add_student(data, parsed.name)
            save_data(data)
            print(f"Student added successfully with id={student_id}.")

        elif parsed.command == "add-course":
            add_course(data, parsed.code, parsed.title)
            save_data(data)
            print(f"Course {parsed.code.strip().upper()} added successfully.")

        elif parsed.command == "enroll":
            enroll(data, parsed.student_id, parsed.course)
            save_data(data)
            print("Enrollment created successfully.")

        elif parsed.command == "add-grade":
            grade = parse_grade(parsed.grade)
            add_grade(data, parsed.student_id, parsed.course, grade)
            save_data(data)
            print("Grade added successfully.")

        elif parsed.command == "list":
            if parsed.entity == "students":
                results = list_students(data, parsed.sort or "name")
            elif parsed.entity == "courses":
                results = list_courses(data, parsed.sort or "code")
            else:
                results = list_enrollments(data)
            _print_list(parsed.entity, results)

        elif parsed.command == "avg":
            avg_score = compute_average(data, parsed.student_id, parsed.course)
            print(
                f"Average for student {parsed.student_id} in "
                f"{parsed.course.strip().upper()}: {avg_score:.2f}"
            )

        elif parsed.command == "gpa":
            gpa_score = compute_gpa(data, parsed.student_id)
            print(f"GPA for student {parsed.student_id}: {gpa_score:.2f}")

        return 0

    except ValueError as exc:
        LOGGER.error("Validation or domain error: %s", exc)
        print(f"Error: {exc}")
        return 1
    except RuntimeError as exc:
        LOGGER.error("Storage error: %s", exc)
        print(f"Error: {exc}")
        return 1
    except Exception as exc:  # pragma: no cover
        LOGGER.error("Unexpected error: %s", exc)
        print("An unexpected error occurred. Check logs/app.log for details.")
        return 1


def main() -> None:
    """CLI entrypoint."""
    raise SystemExit(run_cli())


if __name__ == "__main__":
    main()
