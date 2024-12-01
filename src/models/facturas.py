from sqlalchemy import Column, Date, ForeignKey, Integer,  Numeric, Time
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship

from src.models import Base, SessionLocal, to_dict
from src.models.mixins import RoleMixin
class Factura(Base,RoleMixin):
    __tablename__ = 'factura'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    clientes_idclientes = Column(Integer, ForeignKey('clientes.idclientes'), nullable=False)  # Apunta correctamente a 'idclientes'
    vendedores_idvendedores = Column(Integer, ForeignKey('vendedores.idvendedores'), nullable=False)  # Apunta correctamente a 'idvendedores'
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    total_valor = Column(Numeric(10, 2), nullable=False)
    impuesto = Column(Numeric(10, 2), nullable=False)
    descuento = Column(Numeric(10, 2), nullable=True)
    monto_pagado = Column(Numeric(10, 2), nullable=False)
    cambio = Column(Numeric(10, 2), nullable=True)

    # Relación con el cliente
    cliente = relationship('Clientes', backref='facturas')

    # Relación con el vendedor
    vendedor = relationship('Vendedores', backref='facturas')

    #Relacion con detalle_producto
    detalles = relationship('DetalleProducto', backref='factura')

    def __init__(self, clientes_idclientes, vendedores_idvendedores, fecha, hora, total_valor, impuesto, descuento=None, monto_pagado=None, cambio=None):
        self.clientes_idclientes = clientes_idclientes
        self.vendedores_idvendedores = vendedores_idvendedores
        self.fecha = fecha
        self.hora = hora
        self.total_valor = total_valor
        self.impuesto = impuesto
        self.descuento = descuento
        self.monto_pagado = monto_pagado
        self.cambio = cambio

    def __repr__(self):
        return f'<Factura {self.id}>'
    
    # Método para crear una factura
    @staticmethod
    def crear_factura(clientes_idclientes, vendedores_idvendedores, fecha, hora, total_valor, impuesto, descuento, monto_pagado, cambio):
        session = SessionLocal()
        try:
            try:
                nueva_factura =Factura(
                    clientes_idclientes=clientes_idclientes,
                    vendedores_idvendedores=vendedores_idvendedores,
                    fecha=fecha,
                    hora=hora,
                    total_valor=total_valor,
                    impuesto=impuesto,
                    descuento=descuento,
                    monto_pagado=monto_pagado,
                    cambio=cambio
                )
                session.add(nueva_factura)
                session.commit()

                # Refresca la instancia desde la base de datos
                session.refresh(nueva_factura)

                return to_dict(nueva_factura) if nueva_factura else None
            except SQLAlchemyError as e:
                print(f"Error al crear la factura: {str(e)}")
                return None
        finally:
            session.close()
           
    #--------------------------

    #Metodo para búsqueda de facturas por fecha
    @staticmethod
    def buscar_por_fecha(fecha):
        session = SessionLocal()
        try:
            try:
                # Buscar facturas por la fecha proporcionada
                facturas = session.query(Factura).filter(Factura.fecha == fecha).all()

                if facturas:

                

                    # Serializar los datos de las facturas
                    facturas_data = [{
                        'id': factura.id,
                        'fecha': factura.fecha.strftime('%d/%m/%Y'),  # Formato amigable dd/mm/yyyy
                        'hora': factura.hora.strftime('%H:%M:%S'),    # Formato 24 horas HH:MM:SS
                        'cliente': factura.cliente.nombres_cliente,  # Asegúrate de que este campo exista
                        'total': float(factura.total_valor)
                    } for factura in facturas]
                    return facturas_data
                else:
                    return None  # Si no hay facturas
            except Exception as e:
                print(f"Error al buscar facturas: {e}")
                return None
        finally:
            session.close()

    #----------------

    #Metodo para obtener los detalles de la factura
    @staticmethod
    def obtener_detalles(id_factura):
        session = SessionLocal()
        try:
            try:
                # Buscar la factura por id
                factura = session.query(Factura).filter_by(id=id_factura).first()

                if factura:

                    # Serializar los datos de la factura
                    factura_data = {
                        'id': factura.id,
                        'fecha': factura.fecha.strftime('%d/%m/%Y'),  # Formato amigable dd/mm/yyyy
                        'hora': factura.hora.strftime('%H:%M:%S'),    # Hora formateada
                        'cliente': factura.cliente.nombres_cliente,  # Asegúrate de que este campo exista
                        'vendedor': factura.vendedor.nombres_vendedor, 
                        'impuesto':float(factura.impuesto),  # Asegúrate de que este campo exista
                        'total': float(factura.total_valor),
                        'montoPagado': float(factura.monto_pagado),
                        'cambio': float(factura.cambio),
                        'items': [{
                            'producto': item.producto.nombre,  # Asegúrate de que este campo exista en la relación Producto
                            'cantidad': item.cantidad,
                            'precioUnitario': float(item.precio_unitario),
                            'subtotal': float ( item.total_precio)
                        } for item in factura.detalles]
                    }
                    return factura_data
                else:
                    return None  # Si no se encuentra la factura
            except Exception as e:
                print(f"Error al obtener detalles de la factura: {e}")
                return None
        finally:
            session.close()
    
    #------------------
     
