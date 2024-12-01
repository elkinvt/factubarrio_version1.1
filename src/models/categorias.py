from sqlalchemy import Column, Integer, String

from src.models import Base, SessionLocal, to_dict
class Categoria(Base):
    __tablename__ = 'categoria'
    
    idcategoria = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    
    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return f'<Categoria {self.nombre}>'
    
    
    #Metodo estatico para obtener las categorias
    @staticmethod
    def obtener_todas():
        session = SessionLocal()
        try:
            try:
                categorias = session.query(Categoria).all()
                # Convertimos cada categoría en un diccionario para no depender de la sesión
                categorias_dict = [to_dict(c) for c in categorias]
                return categorias_dict
            except KeyError as e:
                print(f"Error: Clave faltante en obtener_todas - {e}")
                return []
            except Exception as e:
                print(f"Error en obtener_todas: {e}")  # Log de error para depuración
                return []  # Retorna una lista vacía en caso de error
        finally:
            session.close()
                   
    #-------------------
    
    # Método para verificar categoria existe del producto
    @staticmethod
    def existe_categoria(id_categoria):
        session = SessionLocal()
        try:
            try:
                # Verifica si la categoría existe en la base de datos
                categoria_existe = session.query(Categoria).filter_by(idcategoria=id_categoria).first() is not None
                return categoria_existe
            except Exception as e:
                raise e
        finally:
            session.close()
            
    #-----------