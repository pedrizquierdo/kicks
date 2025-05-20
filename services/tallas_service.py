from sqlalchemy.orm import Session
from entities.tallas import Talla

class TallaService:
    def __init__(self, db: Session):
        self.db = db

    def get_tallas(self):
        return self.db.query(Talla).all()

    def get_talla_by_id(self, talla_id: int):
        return self.db.query(Talla).filter(Talla.talla_id == talla_id).first()

    def create_talla(self, talla_data: dict):
        talla = Talla(**talla_data)
        self.db.add(talla)
        self.db.commit()
        self.db.refresh(talla)
        return talla

    def update_talla(self, talla_id: int, talla_data: dict):
        talla = self.db.query(Talla).filter(Talla.talla_id == talla_id).first()
        if talla:
            for key, value in talla_data.items():
                setattr(talla, key, value)
            self.db.commit()
            return talla
        return None

    def delete_talla(self, talla_id: int):
        talla = self.db.query(Talla).filter(Talla.talla_id == talla_id).first()
        if talla:
            self.db.delete(talla)
            self.db.commit()
            return True
        return False
