from sqlalchemy import Boolean, Column, Float,ForeignKey, Integer, String

from src.models import Base, SessionLocal, to_dict
from src.models.categorias import Categoria
from src.models.mixins import RoleMixin
from src.models.unidad_medida import UnidadMedida

class Productos(Base,RoleMixin):
    __tablename__ = 'productos'
    
    idproductos = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    categoria_idcategoria = Column(Integer, ForeignKey('categoria.idcategoria'), nullable=False)
    unidad_medida_idunidad_medida = Column(Integer, ForeignKey('unidad_medida.idunidad_medida'))
    presentacion = Column(String(50))
    cantidad_stock = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    is_deleted = Column(Boolean, default=False)  # Campo de eliminación lógica
    is_active = Column(Boolean, default=True)  # Campo de activación

    def __init__(self, codigo, nombre, descripcion, categoria_idcategoria, unidad_medida_idunidad_medida, presentacion, cantidad_stock, precio_unitario):
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria_idcategoria = categoria_idcategoria
        self.unidad_medida_idunidad_medida = unidad_medida_idunidad_medida
        self.presentacion = presentacion
        self.cantidad_stock = cantidad_stock
        self.precio_unitario = precio_unitario

    def __repr__(self):
        return f'<Producto {self.nombre}>'
    
    
    # Método estático para obtener los productos no eliminados con JOIN a categorías y unidades de medida
    @staticmethod
    def obtener_productos():
        session = SessionLocal()
        try: 
            # Realizamos el join entre productos, categorías y unidades de medida
            productos = session.query(Productos, Categoria, UnidadMedida).join(
                Categoria, Productos.categoria_idcategoria == Categoria.idcategoria  # Join con Categorías
            ).join(
                UnidadMedida, Productos.unidad_medida_idunidad_medida == UnidadMedida.idunidad_medida  # Join con Unidades de Medida
            ).filter(Productos.is_deleted == False).all()  # Filtramos solo productos no eliminados
            
            # Convertimos cada objeto en un diccionario utilizando la función to_dict
            productos_dict =[
                {
                    'producto': to_dict(producto),
                    'categoria': to_dict (categoria),
                    'unidad_medida': to_dict (unidad_medida)
                }
                for producto, categoria, unidad_medida in productos
            ]
            return productos_dict  # Retornamos la lista de productos con las relaciones
        finally:
            session.close()
       
    #------------
    
    # Método estático para agregar un producto
    @staticmethod
    def agregar_producto(producto):
        session = SessionLocal()
        try:    
            try:
                session.add(producto)
                session.commit()
                return producto
            except Exception as e:
                session.rollback()
                raise e
        finally:
            session.close()
            
    #--------

    # Método para buscar productos por código o nombre
    @staticmethod
    def buscar_por_codigo_o_nombre(termino):
        session = SessionLocal()
        try:
            try:
                productos = session.query(Productos).filter(
                    (Productos.codigo.ilike(f'%{termino}%')) |
                    (Productos.nombre.ilike(f'%{termino}%')),
                    Productos.is_deleted == False
                ).all()
                # Convertir el resultado en una lista de diccionarios
                productos_dict =[to_dict(producto) for producto in productos]
                return productos_dict
            except Exception as e:
                raise e
        finally:
            session.close()
           
    #---------
    
    # Método para obtener un producto por su ID
    @staticmethod
    def obtener_por_id(id):
       session = SessionLocal()
       try:
            try:
                producto = session.query(Productos).filter_by(idproductos=id, is_deleted=False).first()
                return to_dict(producto) if producto else None
            except Exception as e:
                raise e
       finally:
            session.close()
        
    #-----------
    
    # Método para actualizar los datos de un producto
    @staticmethod
    def actualizar_producto(id, datos_actualizados):
        session = SessionLocal()
        try:
            try:
                producto = session.query(Productos).get(id)
                if producto:
                    for key, value in datos_actualizados.items():
                        setattr(producto, key, value)
                    session.commit()
                    return producto
                else:
                    return None  # Retorna None si el producto no se encontró
            except Exception as e:
                raise e
        finally:
            session.close()
            
    #-------------
    
    # Método para actualizar el estado de un producto
    @staticmethod
    def toggle_estado(id):
        session = SessionLocal()
        try:
            try:
                # Buscar el producto por ID
                producto = session.query(Productos).filter_by(idproductos=id).first()
                if producto:
                    # Cambiar el estado de `is_active`
                    producto.is_active = not producto.is_active
                    session.commit()
                    return producto.is_active # Retornar el nuevo estado
                else:
                    return None  # Retornar None si el producto no se encuentra
            except Exception as e:
                raise e  # Propaga la excepción para que la ruta pueda manejarla
        finally:
            session.close()
            
    #--------------------

    # Método para eliminar(logica) el producto
    @staticmethod
    def eliminar_producto(id):
        session = SessionLocal()
        try:
            try:
                # Obtener el producto por su ID
                producto = session.query(Productos).filter_by(idproductos=id, is_deleted=False).first()
                if producto:
                    # Realizar eliminación lógica
                    producto.is_deleted = True
                    session.commit()
                    return True  # Indica que la eliminación fue exitosa
                else:
                    return False  # Indica que no se encontró el producto
            except Exception as e:
                raise e  # Propaga la excepción para que la ruta pueda manejarla
            
        finally:
            session.close()
        
    #-----------------
    
    # Método para buscar producto por nombre en la factura
    @staticmethod
    def buscar_productos_por_nombre(query):
        session = SessionLocal()
        try:
            try:
                productos = session.query(Productos).filter(
                    Productos.nombre.ilike(f'%{query}%'),
                    Productos.is_deleted == False
                ).all()
                # Retornamos la lista de productos en formato de diccionario
                return [
                    {
                        'id': producto.idproductos,
                        'codigo': producto.codigo,
                        'nombre': producto.nombre,
                        'descripcion': producto.descripcion,
                        'precio_unitario': float(producto.precio_unitario)
                    }
                    for producto in productos
                ]
            except Exception as e:
                raise e 
        finally:
            session.close()
    #---------------------

    # Método para verificar la cantidad de un producto
    @staticmethod
    def verificar_stock_producto(codigo, cantidad):
        session = SessionLocal()
        try:
            try:
                # Busca el producto por su código
                producto = session.query(Productos).filter_by(codigo=codigo).first()
                
                # Verifica si el producto existe y si tiene suficiente stock
                if not producto:
                    return {'error': 'Producto no encontrado', 'error_type': 'not_found'}
                elif producto.cantidad_stock < cantidad:
                    return {'error': 'Stock insuficiente para la cantidad solicitada', 'error_type': 'insufficient_stock'}
                else:
                    return {
                        'id': producto.idproductos,
                        'codigo': producto.codigo,
                        'nombre': producto.nombre,
                        'precio_unitario': producto.precio_unitario,
                        'cantidad_stock': producto.cantidad_stock
                    }
            
            except Exception as e:
                raise e
        finally:
            session.close()
    #-----------------

    # Método para verificar codigo existe del producto
    @staticmethod
    def existe_codigo(codigo):
        session = SessionLocal()
        try:
            try:
                # Realiza la consulta para verificar si el código existe
                producto_existe = session.query(Productos).filter_by(codigo=codigo).first() is not None
                return producto_existe  # Retorna True si existe, False si no
            except Exception as e:
                raise e  # Propaga la excepción para manejo externo
        finally:
            session.close()
            
    #-------------

    


    

