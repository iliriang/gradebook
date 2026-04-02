"""Core domain models for the gradebook application."""

from dataclasses import dataclass, field

from .validators import parse_grade


@dataclass
class Student:
    """Represents a student entity."""

    id: int
    name: str

    def __post_init__(self) -> None:
        if not isinstance(self.id, int) or self.id < 1:
            raise ValueError("Student id must be a positive integer.")
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Student name cannot be empty.")
        self.name = self.name.strip()

    def __str__(self) -> str:
        return f"Student(id={self.id}, name='{self.name}')"


@dataclass
class Course:
    """Represents a course entity."""

    code: str
    title: str

    def __post_init__(self) -> None:
        if not isinstance(self.code, str) or not self.code.strip():
            raise ValueError("Course code cannot be empty.")
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("Course title cannot be empty.")
        self.code = self.code.strip().upper()
        self.title = self.title.strip()

    def __str__(self) -> str:
        return f"Course(code='{self.code}', title='{self.title}')"


@dataclass
class Enrollment:
    """Represents a student-course enrollment with grades."""

    student_id: int
    course_code: str
    grades: list[float] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.student_id, int) or self.student_id < 1:
            raise ValueError("student_id must be a positive integer.")
        if not isinstance(self.course_code, str) or not self.course_code.strip():
            raise ValueError("course_code cannot be empty.")
        self.course_code = self.course_code.strip().upper()

        if not isinstance(self.grades, list):
            raise ValueError("grades must be a list.")
        self.grades = [parse_grade(g) for g in self.grades]

    def __str__(self) -> str:
        return (
            "Enrollment("
            f"student_id={self.student_id}, "
            f"course_code='{self.course_code}', "
            f"grades={self.grades}"
            ")"
        )
