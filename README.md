# CYB 371 - Role-Based Access Control (RBAC) Demo

A Python demonstration of the basic idea of **Role-Based Access Control (RBAC)**
using fictional users and permissions.

## Core RBAC Idea

Users are never granted permissions directly. Instead:

```
User ---> Role ---> Permission
```

Permissions are attached to **roles**, and users are assigned **roles**.
A user's access is determined entirely by the permissions of the role they hold.

## Files

| File | Purpose |
|------|---------|
| `rbac.py` | Main program: roles, permissions, permission checks, and tests |
| `test_rbac.py` | Automated test suite (runs with plain Python or pytest) |

## How It Works

### 1) Define user roles and permissions

`ROLE_PERMISSIONS` maps each role to the set of actions it may perform:

| Role | Permissions |
|------|-------------|
| `admin` | create_user, delete_user, edit_data, view_reports, manage_roles |
| `manager` | edit_data, view_reports, approve_requests |
| `analyst` | view_reports |
| `guest` | *(none)* |

`USERS` assigns each fictional user a role: alice (admin), bob (manager),
carol (analyst), dave (guest).

### 2) Permission-checking functions

- `has_permission(username, permission)` returns `True`/`False`.
  Unknown users and unknown permissions are **denied by default**.
- `check_permission(username, permission)` enforces the rule and raises
  `PermissionDeniedError` when access is not allowed.

### 3) Testing the access control system

- `python rbac.py` runs a built-in suite of 11 access checks covering every
  role, plus unknown users and unknown permissions, and prints PASS/FAIL.
- `python test_rbac.py` runs 11 assert-based unit tests (also works with
  `pytest test_rbac.py`).

## Running It

```bash
python rbac.py        # demo + access tests
python test_rbac.py   # unit tests
```

Sample output:

```
[PASS]     alice | create_user      | allowed=True (expected True)
[PASS]        bob | delete_user      | allowed=False (expected False)
[PASS]      carol | edit_data        | allowed=False (expected False)
[PASS]       dave | view_reports     | allowed=False (expected False)
...
11/11 tests passed.
```

## Author

Michael Gregory Ibizugbe - CYB 371
