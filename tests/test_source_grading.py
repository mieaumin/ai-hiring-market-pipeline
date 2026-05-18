from src.registry.source_grading import (
    can_move_to_master,
    default_approval_status,
    requires_human_approval,
    validate_source_approval_fields,
)


def test_grade_a_can_pass_without_human_approval_when_automated_checks_pass():
    row = {
        "source_grade": "A",
        "human_approval_required": "false",
        "approval_status": "not_required",
    }

    assert can_move_to_master(row, automated_checks_passed=True)
    assert not can_move_to_master(row, automated_checks_passed=False)


def test_grades_b_c_require_approved_human_status():
    for grade in ["B", "C"]:
        pending = {"source_grade": grade, "approval_status": "pending"}
        approved = {"source_grade": grade, "approval_status": "approved"}

        assert requires_human_approval(grade)
        assert default_approval_status(grade) == "pending"
        assert not can_move_to_master(pending, automated_checks_passed=True)
        assert can_move_to_master(approved, automated_checks_passed=False)


def test_grade_d_requires_review_and_e_f_are_rejected():
    assert requires_human_approval("D")
    assert default_approval_status("D") == "pending"
    for grade in ["D", "E", "F"]:
        row = {"source_grade": grade, "approval_status": "approved"}

        assert not can_move_to_master(row, automated_checks_passed=True)


def test_validate_source_approval_fields_catches_mismatched_human_flag():
    row = {
        "source_grade": "B",
        "human_approval_required": "false",
        "approval_status": "pending",
    }

    valid, reason = validate_source_approval_fields(row)

    assert not valid
    assert reason == "human_approval_required_mismatch"
