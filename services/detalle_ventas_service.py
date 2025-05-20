from sqlalchemy.orm import Session
from entities.detalle_ventas import DetalleVenta

class DetalleVentaService:
    def __init__(self, db: Session):
        self.db = db

    def get_detalles_venta(self):
        return self.db.query(DetalleVenta).all()

    def get_detalle_venta_by_id(self, detalle_id: int):
        return self.db.query(DetalleVenta).filter(DetalleVenta.detalle_id == detalle_id).first()

    def create_detalle_venta(self, detalle_data: dict):
        detalle = DetalleVenta(**detalle_data)
        self.db.add(detalle)
        self.db.commit()
        self.db.refresh(detalle)
        return detalle

    def update_detalle_venta(self, detalle_id: int, detalle_data: dict):
        detalle = self.db.query(DetalleVenta).filter(DetalleVenta.detalle_id == detalle_id).first()
        if detalle:
            for key, value in detalle_data.items():
                setattr(detalle, key, value)
            self.db.commit()
            return detalle
        return None

    def delete_detalle_venta(self, detalle_id: int):
        detalle = self.db.query(DetalleVenta).filter(DetalleVenta.detalle_id == detalle_id).first()
        if detalle:
            self.db.delete(detalle)
            self.db.commit()
            return True
        return False
