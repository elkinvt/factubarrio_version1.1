from sqlalchemy import Boolean, Column, Integer, String
 
from src.models import Base, SessionLocal, to_dict
from src.models.mixins import RoleMixin
class Clientes(Base,RoleMixin):
    __tablename__ = 'clientes'
    
    idclientes = Column(Integer, primary_key=True, autoincrement=True)
    tipo_documento = Column(String(10), nullable=False)
    numero_documento = Column(String(20), unique=True, nullable=False)
    nombres_cliente = Column(String(100), nullable=False)
    telefono = Column(String(15))
    direccion = Column(String(255))
    email = Column(String(100))
    is_deleted = Column(Boolean, default=False)  # Campo de eliminación lógica
    is_active = Column(Boolean, default=True)  # Campo de activación

    def __init__(self, tipo_documento, numero_documento, nombres_cliente, telefono, direccion, email, is_active=True, is_deleted=False):
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento
        self.nombres_cliente = nombres_cliente
        self.telefono = telefono
        self.direccion = direccion
        self.email = email
        self.is_active = is_active  # Ahora acepta is_active
        self.is_deleted = is_deleted  # Ahora acepta is_deleted
        
    def __repr__(self):
        return f'<Cliente {self.nombres_cliente}>'
    
    # Método para obtener los clientes no eliminados
    @staticmethod
    def obtener_clientes():
        """Obtener todos los clientes no eliminados."""
        session = SessionLocal()
        try:
            clientes = session.query(Clientes).filter_by(is_deleted=False).all()

            return [to_dict(cliente) for cliente in clientes] 
        finally:
            session.close()
    
    #--------

    # Método estático para agregar un cliente      
    @staticmethod
    def agregar_cliente(cliente):
        session = SessionLocal()
        try:
            session.add(cliente)
            session.commit()  # Confirma los cambios
            return cliente
        finally:
            session.close()
    
    #----------

    # Método estático para buscar un cliente usando una sesión existente
    @staticmethod
    def buscar_cliente_por_documento(numero_documento):
        session = SessionLocal()
        try:
            cliente = session.query(Clientes).filter_by(
                 numero_documento = numero_documento).first()
            
            return to_dict(cliente) if cliente else None
        finally:
            session.close()

    #---------

    # Método estático para actualizar un cliente     
    @staticmethod
    def actualizar_cliente(cliente_id, datos_actualizados):
        session = SessionLocal()
        try:
            cliente = session.query(Clientes).filter_by(idclientes=cliente_id).first()

            if not cliente:
                raise ValueError("cliente no encontrado")

            # Actualizar los datos
            for key, value in datos_actualizados.items():
                setattr(cliente, key, value)

            session.commit()  # Confirma los cambios en la base de datos
            return cliente
        finally:
            session.close()
    #--------------

    # Método estático para actualizar estado del cliente 
    @staticmethod
    def actualizar_estado(cliente_id):
        """Toggle de estado de cliente"""
        session = SessionLocal()
        try:
            cliente = session.query(Clientes).filter_by(idclientes=cliente_id).first()
            
            if cliente:
                 # Cambiar el estado activo/inactivo
                cliente.is_active = not cliente.is_active
                session.commit()
                return cliente.is_active
            return None
        finally:
            session.close()
    #--------

    # Método estático para eliminar un cliente 
    @staticmethod
    def eliminar_cliente_logicamente(cliente_id):
        session = SessionLocal()
        try:
            cliente = session.query(Clientes).filter_by(idclientes= cliente_id).first()

            if cliente and not cliente.is_deleted:
                cliente.is_deleted = True
                session.commit()
                return True
            return False
        finally:
            session.close()
        
    #------------

    # Método estático para buscar el cliente en la factura
    @staticmethod
    def buscar_clientes(query, incluir_inactivos=False, incluir_eliminados=False):
        """Buscar clientes según filtros dinámicos"""
        session = SessionLocal()
        try:
            # Condiciones base para la consulta
            condiciones = [Clientes.numero_documento.ilike(f"%{query}%")]
            
            if not incluir_inactivos:
                condiciones.append(Clientes.is_active == True)
            
            if not incluir_eliminados:
                condiciones.append(Clientes.is_deleted == False)
            
            return [
            {
                'id': cliente.idclientes,
                'tipo_documento': cliente.tipo_documento,
                'numero_documento': cliente.numero_documento,
                'nombre': cliente.nombres_cliente,
                'telefono': cliente.telefono,
                'direccion': cliente.direccion,
                'email': cliente.email,
                'is_active': cliente.is_active,
                'is_deleted': cliente.is_deleted
            }
            for cliente in session.query(Clientes).filter(*condiciones).all()

        ]
        finally:
            session.close()
    #---------------------------

    # Método estático para validar duplicaciones del cliente
    @staticmethod
    def validar_datos(numero_documento=None, email=None, cliente_id=None):
        session = SessionLocal()
        try:
            errores = {}
            
            # Validar duplicado de número de documento, excluyendo el cliente actual si cliente_id está presente
            if numero_documento:
                cliente_doc = session.query(Clientes).filter_by(numero_documento=numero_documento).first()
                if cliente_doc and (cliente_id is None or cliente_doc.idclientes != int(cliente_id)):
                    errores['numeroDocumento'] = 'Este número de documento ya está registrado.'

            # Validar duplicado de email, excluyendo el cliente actual si cliente_id está presente
            if email:
                cliente_email = session.query(Clientes).filter_by(email=email).first()
                if cliente_email and (cliente_id is None or cliente_email.idclientes != int(cliente_id)):
                    errores['emailCliente'] = 'Este correo electrónico ya está registrado.'

            return errores
        finally:
            session.close()
        
    #--------

