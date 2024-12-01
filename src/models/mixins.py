class RoleMixin:
    """Clase base para modelos con roles."""
    def has_role(self, role):
        return self.rol == role
