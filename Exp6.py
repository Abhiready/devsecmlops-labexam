# Experiment 6: ML Pipeline with Role-Based Access Control (RBAC)
from functools import wraps
from datetime import datetime

# ---- Role definitions: role -> set of allowed permissions ----
ROLES = {
    "data_engineer":  {"extract", "transform"},
    "data_scientist": {"transform", "train", "evaluate"},
    "ml_engineer":    {"train", "evaluate", "deploy"},
    "admin":          {"extract", "transform", "train", "evaluate", "deploy"},
    "viewer":         {"view"},
}

AUDIT_LOG = []


class AccessDenied(Exception):
    """Raised when a role attempts an action it is not permitted to perform."""


def audit(role, permission, allowed):
    entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "role": role,
        "action": permission,
        "result": "ALLOW" if allowed else "DENY",
    }
    AUDIT_LOG.append(entry)


def require(permission):
    """Decorator that enforces RBAC for a pipeline stage."""
    def decorator(func):
        @wraps(func)
        def wrapper(user_role, *args, **kwargs):
            allowed = permission in ROLES.get(user_role, set())
            audit(user_role, permission, allowed)
            if not allowed:
                raise AccessDenied(
                    f"Role '{user_role}' is NOT authorized for '{permission}'")
            print(f"[AUTH OK ] {user_role:15s} -> {permission}")
            return func(user_role, *args, **kwargs)
        return wrapper
    return decorator


@require("extract")
def extract(role):
    return "raw_data"

@require("train")
def train(role):
    return "trained_model"

@require("deploy")
def deploy(role):
    return "deployed"


def try_action(fn, role):
    try:
        fn(role)
    except AccessDenied as e:
        print(f"[DENIED  ] {e}")


if __name__ == "__main__":
    print("=== ML Pipeline Access Control ===")
    # Admin is allowed to run every stage
    extract("admin"); train("admin"); deploy("admin")
    # These should be blocked
    try_action(deploy, "data_scientist")
    try_action(train, "viewer")
    try_action(extract, "ml_engineer")

    print("\n=== Audit Log ===")
    for e in AUDIT_LOG:
        print(f"{e['time']}  {e['role']:15s} {e['action']:10s} {e['result']}")