"""Unit tests for gradebook service logic."""

import unittest

from gradebook.service import add_grade, add_student, compute_average, enroll


class TestService(unittest.TestCase):
    """Service function tests."""

    def setUp(self) -> None:
        self.data = {
            "students": [],
            "courses": [{"code": "CS101", "title": "Intro to CS"}],
            "enrollments": [],
            "next_student_id": 1,
        }

    def test_add_student_returns_new_id(self) -> None:
        """add_student should create a student and increment id."""
        new_id = add_student(self.data, "Alice")

        self.assertEqual(new_id, 1)
        self.assertEqual(self.data["students"][0]["name"], "Alice")
        self.assertEqual(self.data["next_student_id"], 2)

    def test_add_grade_happy_path(self) -> None:
        """add_grade should append a valid grade for an enrollment."""
        student_id = add_student(self.data, "Ilirian Gerxhaliu")
        enroll(self.data, student_id, "CS101")

        add_grade(self.data, student_id, "CS101", 95)

        self.assertEqual(self.data["enrollments"][0]["grades"], [95.0])

    def test_compute_average_happy_path(self) -> None:
        """compute_average should return mean grade for one course."""
        student_id = add_student(self.data, "Bexhet")
        enroll(self.data, student_id, "CS101")
        add_grade(self.data, student_id, "CS101", 80)
        add_grade(self.data, student_id, "CS101", 100)

        result = compute_average(self.data, student_id, "CS101")

        self.assertEqual(result, 90.0)

    def test_compute_average_raises_for_unenrolled(self) -> None:
        """compute_average should fail for unknown enrollment."""
        student_id = add_student(self.data, "Berat")

        with self.assertRaises(ValueError):
            compute_average(self.data, student_id, "CS101")


if __name__ == "__main__":
    unittest.main()
