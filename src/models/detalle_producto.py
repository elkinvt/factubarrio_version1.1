from sqlalchemy import Column,ForeignKey, Integer, Numeric
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship

from src.models import Base,SessionLocal
from src.models.productos import Productos
class DetalleProducto(Base):
    __tablename__ = 'detalle_producto'
    
    factura_idfactura = Column(Integer, ForeignKey('factura.id'), primary_key=True)
    productos_idproductos = Column(Integer, ForeignKey('productos.idproductos'), primary_key=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    total_precio = Column(Numeric(10, 2), nullable=False)

     # Relación con la tabla de productos
    producto = relationship('Productos')

    def __init__(self, factura_idfactura, productos_idproductos, cantidad, precio_unitario, total_precio):
        self.factura_idfactura = factura_idfactura
        self.productos_idproductos = productos_idproductos
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.total_precio = total_precio

    def __repr__(self):
        return f'<DetalleProducto Factura {self.factura_id} Producto {self.productos_idproductos}>'
    
    # Método estático para agregar productos al detalle de la factura
    @staticmethod
    def agregar_detalles(factura_id, productos):
        session = SessionLocal()
        try:
            try:
                for producto in productos:
                    # Verificar que el producto existe y tiene suficiente stock
                    producto_db = session.query(Productos).filter_by(idproductos=producto['id']).first()
                    if not producto_db:
                        raise ValueError(f"El producto con ID {producto['id']} no existe.")
                    
                    if producto_db.cantidad_stock < producto['cantidad']:
                        raise ValueError(f"El producto {producto_db.nombre} no tiene suficiente stock para cubrir la venta.")
                    
                    # Reducir el stock del producto
                    producto_db.cantidad_stock -= producto['cantidad']

                    # Crear el detalle de la factura
                    detalle = DetalleProducto(
                        factura_idfactura=factura_id,
                        productos_idproductos=producto['id'],
                        cantidad=producto['cantidad'],
                        precio_unitario=producto['precio'],
                        total_precio=producto['subtotal']
                    )
                    session.add(detalle)

                # Confirmar las operaciones de detalle y reducción de stock
                session.commit()
                return True
            except (SQLAlchemyError, ValueError) as e:
                print(f"Error al agregar detalles: {str(e)}")
                return False
        finally:
            session.close()
           
    #----------

   