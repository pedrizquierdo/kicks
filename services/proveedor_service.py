from sqlalchemy.orm import Session
from entities.proveedores import Proveedor

class ProveedorService:
    def __init__(self, db: Session):
        self.db = db

    def get_proveedores(self):
        return self.db.query(Proveedor).all()

    def get_proveedor_by_id(self, proveedor_id: int):
        return self.db.query(Proveedor).filter(Proveedor.proveedor_id == proveedor_id).first()

    def create_proveedor(self, proveedor_data: dict):
        proveedor = Proveedor(**proveedor_data)
        self.db.add(proveedor)
        self.db.commit()
        self.db.refresh(proveedor)
        return proveedor

    def update_proveedor(self, proveedor_id: int, proveedor_data: dict):
        proveedor = self.db.query(Proveedor).filter(Proveedor.proveedor_id == proveedor_id).first()
        if proveedor:
            for key, value in proveedor_data.items():
                setattr(proveedor, key, value)
            self.db.commit()
            return proveedor
        return None

    def delete_proveedor(self, proveedor_id: int):
        proveedor = self.db.query(Proveedor).filter(Proveedor.proveedor_id == proveedor_id).first()
        if proveedor:
            self.db.delete(proveedor)
            self.db.commit()
            return True
        return False