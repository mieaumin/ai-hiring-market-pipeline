from src.registry.source_grading import (
    can_move_to_master,
    default_approval_status,
    requires_human_approval,
)
from src.registry.source_registry import grade_source


def test_grade_a_is_only_directly_usable_after_automated_checks():
    row = {"source_grade": "A", "approval_status": "not_required"}

    assert default_approval_status("A") == "not_required"
    assert not requires_human_approval("A")
    assert not can_move_to_master(row, automated_checks_passed=False)
    assert can_move_to_master(row, automated_checks_passed=True)


def test_grades_b_c_require_human_approval_and_approved_status():
    for grade in ["B", "C"]:
        assert requires_human_approval(grade)
        assert default_approval_status(grade) == "pending"
        assert not can_move_to_master(
            {"source_grade": grade, "approval_status": "pending"},
            automated_checks_passed=True,
        )
        assert can_move_to_master(
            {"source_grade": grade, "approval_status": "approved"},
            automated_checks_passed=False,
        )


def test_grade_d_e_and_f_never_move_to_master_for_mvp():
    assert requires_human_approval("D")
    assert default_approval_status("D") == "pending"
    for grade in ["D", "E", "F"]:
        assert not can_move_to_master(
            {"source_grade": grade, "approval_status": "approved"},
            automated_checks_passed=True,
        )


def test_local_grade_source_helper_is_conservative_for_blockers():
    assert (
        grade_source(
            {
                "login_required": "true",
                "captcha_required": "false",
                "anti_bot_risk": "low",
                "robots_target_path_status": "allowed",
                "terms_collection_policy": "allowed",
            }
        )
        == "E"
    )
    assert (
        grade_source(
            {
                "api_required": "true",
                "robots_target_path_status": "allowed",
                "terms_collection_policy": "allowed",
            }
        )
        == "D"
    )
