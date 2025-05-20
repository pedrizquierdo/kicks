from sqlalchemy.orm import Session
from entities.ventas import Venta

class VentaService:
    def __init__(self, db: Session):
        self.db = db

    def get_ventas(self):
        return self.db.query(Venta).all()

    def get_venta_by_id(self, venta_id: int):
        return self.db.query(Venta).filter(Venta.venta_id == venta_id).first()

    def create_venta(self, venta_data: dict):
        venta = Venta(**venta_data)
        self.db.add(venta)
        self.db.commit()
        self.db.refresh(venta)
        return venta

    def update_venta(self, venta_id: int, venta_data: dict):
        venta = self.db.query(Venta).filter(Venta.venta_id == venta_id).first()
        if venta:
            for key, value in venta_data.items():
                setattr(venta, key, value)
            self.db.commit()
            return venta
        return None

    def delete_venta(self, venta_id: int):
        venta = self.db.query(Venta).filter(Venta.venta_id == venta_id).first()
        if venta:
            self.db.delete(venta)
            self.db.commit()
            return True
        return False
