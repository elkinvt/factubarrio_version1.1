from sqlalchemy import Boolean, Column,ForeignKey, Integer, String 
from sqlalchemy.orm import relationship

from src.models import Base, SessionLocal, to_dict
from src.models.mixins import RoleMixin
from src.models.usuarios import Usuarios



class Vendedores(Base, RoleMixin):
    __tablename__ = 'vendedores'
    
    idvendedores = Column(Integer, primary_key=True, autoincrement=True)
    tipo_documento = Column(String(10), nullable=False)
    numero_documento = Column(String(20), unique=True, nullable=False)
    nombres_vendedor = Column(String(100), nullable=False)
    telefono = Column(String(15))
    direccion = Column(String(255))  
    email = Column(String(100))
    is_deleted = Column(Boolean, default=False)  # Campo de eliminación lógica
    usuario_id = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)  # Clave foránea para asociar al usuario

    # Relación para acceder al usuario desde un vendedor
    usuario = relationship('Usuarios', backref='vendedores')

    def __init__(self, tipo_documento, numero_documento, nombres_vendedor, telefono, direccion, email, usuario_id, is_deleted=False):
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento
        self.nombres_vendedor = nombres_vendedor
        self.telefono = telefono
        self.direccion = direccion
        self.email = email
        self.usuario_id = usuario_id
        self.is_deleted = is_deleted  # Ahora acepta is_deleted

    def __repr__(self):
        return f'<Vendedor {self.nombres_vendedor}>'
    
    
    # Método para obtener los vendedores no eliminados
    @staticmethod
    def obtener_vendedores():
        session = SessionLocal()
        try: 
            vendedores = session.query(Vendedores, Usuarios).join(
                Usuarios, Vendedores.usuario_id  == Usuarios.id_usuario).filter(Vendedores.is_deleted==False).all()
            
            vendedores_dict =[
                {
                    'vendedor': to_dict(vendedor),
                    'usuario': to_dict(usuario)
                }
                for vendedor, usuario in vendedores
            ]
            return vendedores_dict
        finally:
            session.close()

    #------------     

    # Método estático para agregar un vendedor      
    @staticmethod
    def agregar_vendedor(vendedor):
        session = SessionLocal()
        try:
            session.add(vendedor)
            session.commit()  # Confirma los cambios
            return vendedor
        finally:
            session.close()
        
    #------------------
    
    # Método estático para buscar un vendedor usando una sesión existente
    @staticmethod
    def buscar_vendedor_por_documento(numero_documento):
        session = SessionLocal()
        try:
            vendedor = session.query(Vendedores).filter_by(
            numero_documento=numero_documento).first()

            return to_dict(vendedor) if vendedor else None
        finally:
            session.close()

    #---------
    
    # Método estático para actualizar un vendedor     
    @staticmethod
    def actualizar_vendedor(vendedor_id, datos_actualizados):
        session = SessionLocal()
        try:
            vendedor = session.query(Vendedores).filter_by(idvendedores=vendedor_id).first()

            if not vendedor:
                raise ValueError("Vendedor no encontrado")

            # Actualizar los datos
            for key, value in datos_actualizados.items():
                setattr(vendedor, key, value)

            session.commit()  # Confirma los cambios en la base de datos
            return vendedor
        finally:
            session.close()
        
    #--------------

    #Metodo estatico para buscar vendedor por id
    @staticmethod
    def buscar_vendedor_por_id(vendedor_id):
        session = SessionLocal()
        try:
            return session.query(Vendedores).filter_by(idvendedores=vendedor_id).first()
        finally:
            session.close()
    
    #-----------------
    
    # Método estático para eliminar un vendedor 
    @staticmethod
    def eliminar_vendedor_logicamente(vendedor_id):
        session = SessionLocal()
        try:
            vendedor = session.query(Vendedores).filter_by(idvendedores=vendedor_id). first()
            vendedor.is_deleted = True  # Marcamos el vendedor como eliminado
            session.commit()  # Guardamos los cambios en la base de datos
            return True
        finally:
            session.close()

    #------------    

    # Método de validación en Vendedores
    @staticmethod
    def validar_datos(numero_documento=None, email=None,vendedor_id=None):
        session = SessionLocal()
        try:
            errores = {}

            #print(f'Validando: numero_documento={numero_documento}, email={email}, vendedor_id={vendedor_id}')

            # Validar duplicado de número de documento, excluyendo el vendedor actual si vendedor_id está presente
            if numero_documento:
                vendedor_doc= session.query(Vendedores).filter_by(numero_documento=numero_documento).first()
                #print(f'Vendedor encontrado por número de documento: {vendedor_doc}')
                if vendedor_doc and (vendedor_id is None or vendedor_doc.idvendedores != int(vendedor_id)):
                    errores['numeroDocumento'] = 'Este número de documento ya está registrado.'


            # Validar duplicado de email, excluyendo el vendedor actual si vendedor_id está presente   
            if email:
                vendedor_email = session.query(Vendedores).filter_by(email=email).first()
                #print(f'Vendedor encontrado por email: {vendedor_email}')
                if vendedor_email and (vendedor_id is None or vendedor_email.idvendedores != int(vendedor_id)):
                    errores['emailVendedor'] = 'Este correo electrónico ya está registrado.'

            #print(f'Errores detectados: {errores}')      
            return errores
        finally:
            session.close()

    #---------

    #Metodo estatico para acceder al vendedodor por id de usuario
    @staticmethod
    def obtener_vendedor_por_usuario(usuario_id):
        """Obtiene el vendedor asociado a un usuario dado."""
        session = SessionLocal()
        try:
            vendedor = session.query(Vendedores).filter_by(usuario_id=usuario_id, is_deleted=False).first()
            if not vendedor:
                raise ValueError('No se encontró un vendedor asociado al usuario.')
            return vendedor
        finally:
            session.close()
            
    #-----------------
    

