from sqlalchemy import Boolean, Column, Integer, String, func
from flask_login import UserMixin

from src.models import  Base, SessionLocal, to_dict
from src.models.mixins import RoleMixin
class Usuarios(Base, UserMixin,RoleMixin):
    __tablename__ = 'usuarios'

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombres_usuario = Column(String(100), nullable=False)
    email = Column(String(100),nullable=False, unique=True)
    contraseña = Column(String(128),nullable=False)
    rol = Column(String(100),nullable=False)
    is_deleted = Column(Boolean, default=False) 
    is_active = Column(Boolean, default=True)  # Campo de activación

    
    def __init__(self,nombre_usuario, email, contraseña, rol,is_active=True, is_deleted=False):
        self.nombres_usuario = nombre_usuario
        self.email = email
        self.contraseña = contraseña
        self.rol = rol
        self.is_active = is_active 
        self.is_deleted = is_deleted  

    def __repr__(self):
            return f'<Usuario {self.nombres_usuario}>'
    
    @property
    def can_login(self):
        """Permitir inicio de sesión solo si está activo y no eliminado."""
        return self.is_active and not self.is_deleted
    
    def flask_is_active(self):
        """Método usado por Flask-Login para validar si el usuario está activo."""
        return self.can_login


    def get_id(self):
        """Método requerido por Flask-Login para obtener el identificador único del usuario."""
        return str(self.id_usuario)
    
    # Método para obtener los usuarios no eliminados
    @staticmethod
    def obtener_usuarios():
        session = SessionLocal()
        try:
            usuarios = session.query(Usuarios).filter_by(is_deleted=False).all()
            return [to_dict(usuario) for usuario in usuarios]
        finally:
            session.close()
    #------------ 

    # Método estático para agregar un usuario      
    @staticmethod
    def agregar_usuario(usuario):
        session = SessionLocal()
        try:
            session.add(usuario)
            session.commit()  # Confirma los cambios
            return usuario
        finally:
            session.close()
    #------------------

    # Método estático para buscar usuario por nombre
    @staticmethod
    def buscar_usuario_por_nombre(nombre_usuario):
        session = SessionLocal()
        try:
            usuario =session.query(Usuarios).filter(func.lower(Usuarios.nombres_usuario)==nombre_usuario.lower().strip()).first()
            return to_dict(usuario) if usuario else None
        finally:
            session.close()

    #-----------------
    
    # Método estático para actualizar un usuario     
    @staticmethod
    def actualizar_usuario(usuario_id, datos_actualizados):
        session = SessionLocal()
        try:

            usuario = session.query(Usuarios).filter_by(id_usuario=usuario_id).first()
            if not usuario:
                raise ValueError("usuario no encontrado")

            # Actualizar los datos
            for key, value in datos_actualizados.items():
                setattr(usuario, key, value)

            session.commit()  # Confirma los cambios en la base de datos
            return usuario
        finally:
            session.close()
    #--------------

    # Método estático para actualizar estado del usuario
    @staticmethod
    def actualizar_estado(id_usuario):
        """Toggle de estado de usuario"""
        session = SessionLocal()    
        try:
            usuario = session.query(Usuarios).filter_by(id_usuario=id_usuario).first()
                    
            if usuario:
                    # Cambiar el estado activo/inactivo
                    usuario.is_active = not usuario.is_active
                    session.commit()
                    return usuario.is_active
            return None
        finally:
                    session.close()
    
    #--------

    # Método estático para eliminar un usuario
    @staticmethod
    def eliminar_usuario_logicamente(id_usuario):
        session = SessionLocal()
        try:
            usuario = session.query(Usuarios).filter(Usuarios.id_usuario == id_usuario).first()

            if not usuario:
                return False  # Usuario no encontrado
        
            if usuario.is_deleted:
                return False  # Ya eliminado
           
            usuario.is_deleted = True
            session.commit()
            return True
        
        finally:
            session.close()
          
    #------------

    # Método de validación en Usuarios
    @staticmethod
    def validar_datos(email=None, usuario_id=None):
        session = SessionLocal()
        try:
            errores = {}

            # Validar duplicado de email solo en Usuarios, excluyendo el usuario actual si usuario_id está presente
            if email:
                usuario_email = session.query(Usuarios).filter_by(email=email).first()
                if usuario_email and (usuario_id is None or usuario_email.id_usuario != int(usuario_id)):
                    errores['emailUsuario'] = 'Este correo electrónico ya está registrado en Usuarios.'

            return errores
        finally:
            session.close()
        
    #--------------

    # Método de para obtener usuarios en vendedores
    @staticmethod
    def obtener_usuarios_vendedores():
        session = SessionLocal()
        try: 
            usuarios = session.query(Usuarios).filter(
                Usuarios.rol == 'vendedor',
                Usuarios.is_deleted == False
            ).all()  
            usuarios_dict = [to_dict(usuario) for usuario in usuarios]  
            return usuarios_dict  # Retornar los datos ya procesados
        finally:
            session.close()
    
    #--------------------

    #Metodo estatico para validar usuario en el login
    @staticmethod
    def validar_usuario_login(nombre_usuario, contraseña):
        # Crea una sesión de base de datos explícita
        session = SessionLocal()
        try:
            usuario_valido = session.query(Usuarios).filter_by(nombres_usuario=nombre_usuario).first()
            if usuario_valido and usuario_valido.contraseña == contraseña:
                return usuario_valido  # Devuelve el objeto completo y conectado a la sesión
            return None
        finally:
            session.close()  # Cierra la sesión al finalizar

    #--------------

    
    # Método estático para obtener un usuario por ID
    @staticmethod
    def obtener_usuario_por_id(id_usuario):
        session = SessionLocal()
        try:
            return session.query(Usuarios).get(int(id_usuario))
        finally:
            session.close()
            
    #----------
  