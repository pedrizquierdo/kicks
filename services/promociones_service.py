from sqlalchemy.orm import Session
from entities.promociones import Promocion

class PromocionService:
    def __init__(self, db: Session):
        self.db = db

    def get_promociones(self):
        return self.db.query(Promocion).all()

    def get_promocion_by_id(self, promocion_id: int):
        return self.db.query(Promocion).filter(Promocion.promocion_id == promocion_id).first()

    def create_promocion(self, promocion_data: dict):
        promocion = Promocion(**promocion_data)
        self.db.add(promocion)
        self.db.commit()
        self.db.refresh(promocion)
        return promocion

    def update_promocion(self, promocion_id: int, promocion_data: dict):
        promocion = self.db.query(Promocion).filter(Promocion.promocion_id == promocion_id).first()
        if promocion:
            for key, value in promocion_data.items():
                setattr(promocion, key, value)
            self.db.commit()
            return promocion
        return None

    def delete_promocion(self, promocion_id: int):
        promocion = self.db.query(Promocion).filter(Promocion.promocion_id == promocion_id).first()
        if promocion:
            self.db.delete(promocion)
            self.db.commit()
            return True
        return False
