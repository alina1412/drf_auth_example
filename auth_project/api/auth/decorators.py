from api.auth.schemas import UserRole


def require_basic_role(view_class):
    view_class.require_role = UserRole.BASIC
    return view_class


def require_manager_role(view_class):
    view_class.require_role = UserRole.MANAGER
    return view_class


def require_admin_role(view_class):
    view_class.require_role = UserRole.ADMIN
    return view_class
