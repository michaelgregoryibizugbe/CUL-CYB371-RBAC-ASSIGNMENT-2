"""
CYB 371 - Assignment
Role-Based Access Control (RBAC) Demonstration in Python
=========================================================

This program demonstrates the basic idea of Role-Based Access Control (RBAC)
using fictional users and permissions.

RBAC core idea:
    Users are NOT granted permissions directly.
    Instead, permissions are assigned to ROLES, and users are assigned to roles.
    A user's access is determined by the permissions of the role(s) they hold.

    User ---> Role ---> Permission

This file covers the three assignment tasks:
    1) Define user roles and permissions.
    2) Create a function to check permissions.
    3) Test the access control system (see the __main__ block and test_rbac.py).
"""

# ---------------------------------------------------------------------------
# 1) DEFINE USER ROLES AND PERMISSIONS
# ---------------------------------------------------------------------------

# Each role maps to a set of permissions it is allowed to perform.
ROLE_PERMISSIONS = {
    "admin": {
        "create_user",
        "delete_user",
        "edit_data",
        "view_reports",
        "manage_roles",
    },
    "manager": {
        "edit_data",
        "view_reports",
        "approve_requests",
    },
    "analyst": {
        "view_reports",
    },
    "guest": set(),  # No permissions at all
}

# Fictional users, each assigned exactly one role.
USERS = {
    "alice": "admin",
    "bob": "manager",
    "carol": "analyst",
    "dave": "guest",
}


class PermissionDeniedError(Exception):
    """Raised when a user tries to perform an action they are not allowed to."""


def get_user_role(username):
    """Return the role assigned to a user, or None if the user does not exist."""
    return USERS.get(username)


def get_role_permissions(role):
    """Return the set of permissions for a role (empty set for unknown roles)."""
    return ROLE_PERMISSIONS.get(role, set())


# ---------------------------------------------------------------------------
# 2) FUNCTION TO CHECK PERMISSIONS
# ---------------------------------------------------------------------------

def has_permission(username, permission):
    """
    Check whether a user is allowed to perform an action.

    Returns True if the user's role includes the permission, False otherwise.
    Unknown users and unknown permissions always return False (deny by default).
    """
    role = get_user_role(username)
    if role is None:
        return False  # Unknown user: deny access
    return permission in get_role_permissions(role)


def check_permission(username, permission):
    """
    Check a user's permission and raise PermissionDeniedError if not allowed.

    This is the "enforcement" version of has_permission(): it either allows
    the action to proceed or blocks it with a clear error.
    """
    if has_permission(username, permission):
        print(f"[ALLOWED]   {username} can '{permission}' "
              f"(role: {get_user_role(username)})")
        return True
    print(f"[DENIED]    {username} CANNOT '{permission}' "
          f"(role: {get_user_role(username)})")
    raise PermissionDeniedError(
        f"User '{username}' does not have permission '{permission}'."
    )


# ---------------------------------------------------------------------------
# 3) TEST THE ACCESS CONTROL SYSTEM
# ---------------------------------------------------------------------------

def run_access_tests():
    """Run a small suite of access checks and print the results."""
    print("=" * 60)
    print("RBAC ACCESS CONTROL TESTS")
    print("=" * 60)

    # Test cases: (username, permission, expected_result)
    test_cases = [
        # Admin should have full access
        ("alice", "create_user", True),
        ("alice", "delete_user", True),
        ("alice", "view_reports", True),
        # Manager: can edit data and view reports, but not delete users
        ("bob", "edit_data", True),
        ("bob", "view_reports", True),
        ("bob", "delete_user", False),
        # Analyst: read-only
        ("carol", "view_reports", True),
        ("carol", "edit_data", False),
        # Guest: no permissions at all
        ("dave", "view_reports", False),
        # Unknown user and unknown permission: deny by default
        ("mallory", "view_reports", False),
        ("alice", "launch_missiles", False),
    ]

    passed = 0
    for username, permission, expected in test_cases:
        result = has_permission(username, permission)
        status = "PASS" if result == expected else "FAIL"
        if result == expected:
            passed += 1
        print(f"[{status}] {username:>8} | {permission:<16} | "
              f"allowed={result} (expected {expected})")

    print("-" * 60)
    print(f"{passed}/{len(test_cases)} tests passed.")

    # Demonstrate the enforcement function (check_permission)
    print()
    print("Demonstrating check_permission() enforcement:")
    check_permission("alice", "delete_user")   # Should succeed

    try:
        check_permission("dave", "edit_data")  # Should be denied
    except PermissionDeniedError as error:
        print(f"[BLOCKED]   Exception raised as expected: {error}")

    print("=" * 60)


if __name__ == "__main__":
    run_access_tests()
