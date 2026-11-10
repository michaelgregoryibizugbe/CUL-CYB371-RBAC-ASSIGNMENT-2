"""
Automated tests for the RBAC system in rbac.py.

Run with:  python test_rbac.py
(or with pytest:  pytest test_rbac.py)
"""

from rbac import (
    USERS,
    ROLE_PERMISSIONS,
    has_permission,
    check_permission,
    get_user_role,
    PermissionDeniedError,
)


def test_roles_and_permissions_defined():
    """Task 1: roles and permissions exist and are non-empty (guest is empty on purpose)."""
    assert "admin" in ROLE_PERMISSIONS
    assert "manager" in ROLE_PERMISSIONS
    assert "analyst" in ROLE_PERMISSIONS
    assert len(ROLE_PERMISSIONS["admin"]) > 0
    assert ROLE_PERMISSIONS["guest"] == set()


def test_users_are_assigned_roles():
    """Every fictional user maps to a valid role."""
    for username, role in USERS.items():
        assert role in ROLE_PERMISSIONS, f"{username} has unknown role {role}"


def test_admin_has_all_permissions():
    for permission in ("create_user", "delete_user", "edit_data", "view_reports"):
        assert has_permission("alice", permission) is True


def test_manager_cannot_delete_users():
    assert has_permission("bob", "edit_data") is True
    assert has_permission("bob", "delete_user") is False


def test_analyst_is_read_only():
    assert has_permission("carol", "view_reports") is True
    assert has_permission("carol", "edit_data") is False


def test_guest_has_no_access():
    assert has_permission("dave", "view_reports") is False


def test_unknown_user_denied():
    assert has_permission("mallory", "view_reports") is False


def test_unknown_permission_denied():
    assert has_permission("alice", "launch_missiles") is False


def test_check_permission_allows_valid_access():
    assert check_permission("alice", "view_reports") is True


def test_check_permission_raises_on_denial():
    try:
        check_permission("dave", "edit_data")
    except PermissionDeniedError:
        pass  # Expected
    else:
        raise AssertionError("check_permission should have raised PermissionDeniedError")


def test_get_user_role():
    assert get_user_role("alice") == "admin"
    assert get_user_role("nobody") is None


if __name__ == "__main__":
    # Simple runner when pytest is not installed
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for test in tests:
        try:
            test()
            print(f"[PASS] {test.__name__}")
        except AssertionError as error:
            failed += 1
            print(f"[FAIL] {test.__name__}: {error}")
    print(f"\n{len(tests) - failed}/{len(tests)} tests passed.")
    raise SystemExit(1 if failed else 0)
