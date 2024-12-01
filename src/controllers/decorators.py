from functools import wraps

from flask import abort
from flask_login import current_user


def role_required(roles):
    """Decorador para validar roles antes de acceder a una ruta."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return abort(401)  # No autenticado
            if current_user.rol not in roles:  # Validar el rol
                return abort(403)  # Acceso denegado
            return func(*args, **kwargs)
        return wrapper
    return decorator
