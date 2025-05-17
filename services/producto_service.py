from sqlalchemy.orm import Session
from entities.producto import Producto

class ProductoService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_productos(self):
        return self.db.query(Producto).all()
    
    def get_producto_by_id(self, producto_id: int):
        return self.db.query(Producto).filter(Producto.producto_id == producto_id).first()
    
    def create_producto(self, producto_data: dict):
        producto = Producto(**producto_data)
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto
    
    def update_producto(self, producto_id: int, producto_data: dict):
        producto = self.db.query(Producto).filter(Producto.producto_id == producto_id).first()
        if producto:
            for key, value in producto_data.items():
                setattr(producto, key, value)
            self.db.commit()
            return producto
        return None
    
    def delete_producto(self, producto_id: int):
        producto = self.db.query(Producto).filter(Producto.producto_id == producto_id).first()
        if producto:
            self.db.delete(producto)
            self.db.commit()
            return True
        return False