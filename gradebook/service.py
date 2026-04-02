"""Business logic for managing gradebook entities and calculations."""

from statistics import mean

from .models import Course, Enrollment, Student
from .validators import parse_grade


def _ensure_student_exists(data: dict, student_id: int) -> None:
    if not any(student["id"] == student_id for student in data["students"]):
        raise ValueError(f"Unknown student_id: {student_id}")


def _ensure_course_exists(data: dict, course_code: str) -> str:
    code = course_code.strip().upper()
    if not any(course["code"] == code for course in data["courses"]):
        raise ValueError(f"Unknown course code: {code}")
    return code


def add_student(data: dict, name: str) -> int:
    """Add a student and return the generated student id."""
    student = Student(id=data["next_student_id"], name=name)
    data["students"].append({"id": student.id, "name": student.name})
    data["next_student_id"] += 1
    return student.id


def add_course(data: dict, code: str, title: str) -> None:
    """Add a new course if the course code is unique."""
    course = Course(code=code, title=title)

    if any(existing["code"] == course.code for existing in data["courses"]):
        raise ValueError(f"Course {course.code} already exists.")

    data["courses"].append({"code": course.code, "title": course.title})


def enroll(data: dict, student_id: int, course_code: str) -> None:
    """Enroll a student in a course."""
    _ensure_student_exists(data, student_id)
    normalized_code = _ensure_course_exists(data, course_code)

    already_enrolled = any(
        enrollment["student_id"] == student_id
        and enrollment["course_code"] == normalized_code
        for enrollment in data["enrollments"]
    )
    if already_enrolled:
        raise ValueError("Student is already enrolled in this course.")

    enrollment_obj = Enrollment(student_id=student_id, course_code=normalized_code)
    data["enrollments"].append(
        {
            "student_id": enrollment_obj.student_id,
            "course_code": enrollment_obj.course_code,
            "grades": enrollment_obj.grades,
        }
    )


def add_grade(data: dict, student_id: int, course_code: str, grade: float) -> None:
    """Add a validated grade for an enrolled student-course pair."""
    normalized_code = course_code.strip().upper()
    validated_grade = parse_grade(grade)

    for enrollment_item in data["enrollments"]:
        if (
            enrollment_item["student_id"] == student_id
            and enrollment_item["course_code"] == normalized_code
        ):
            enrollment_item["grades"].append(validated_grade)
            return

    raise ValueError("Student is not enrolled in the specified course.")


def list_students(data: dict, sort_by: str = "name") -> list[dict]:
    """Return students sorted by name or id."""
    valid_sort = sort_by if sort_by in {"name", "id"} else "name"
    return sorted(
        [student.copy() for student in data["students"]], key=lambda item: item[valid_sort]
    )


def list_courses(data: dict, sort_by: str = "code") -> list[dict]:
    """Return courses sorted by code or title."""
    valid_sort = sort_by if sort_by in {"code", "title"} else "code"
    return sorted(
        [course.copy() for course in data["courses"]], key=lambda item: item[valid_sort]
    )


def list_enrollments(data: dict) -> list[dict]:
    """Return enrollments sorted by student id then course code."""
    enrollments = [
        {
            "student_id": item["student_id"],
            "course_code": item["course_code"],
            "grades": list(item["grades"]),
        }
        for item in data["enrollments"]
    ]
    return sorted(enrollments, key=lambda item: (item["student_id"], item["course_code"]))


def compute_average(data: dict, student_id: int, course_code: str) -> float:
    """Compute the average grade for a student in one course."""
    normalized_code = course_code.strip().upper()

    for enrollment_item in data["enrollments"]:
        if (
            enrollment_item["student_id"] == student_id
            and enrollment_item["course_code"] == normalized_code
        ):
            if not enrollment_item["grades"]:
                raise ValueError("No grades available for this enrollment.")
            return float(mean(enrollment_item["grades"]))

    raise ValueError("Student is not enrolled in the specified course.")


def compute_gpa(data: dict, student_id: int) -> float:
    """Compute GPA as the mean of each course average for a student."""
    student_enrollments = [
        item
        for item in data["enrollments"]
        if item["student_id"] == student_id and item["grades"]
    ]

    if not student_enrollments:
        raise ValueError("No graded enrollments found for this student.")

    course_averages = [mean(item["grades"]) for item in student_enrollments]
    return float(mean(course_averages))
