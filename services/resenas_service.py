from sqlalchemy.orm import Session
from entities.resenas import Resena

class ResenaService:
    def __init__(self, db: Session):
        self.db = db

    def get_resenas(self):
        return self.db.query(Resena).all()

    def get_resena_by_id(self, resena_id: int):
        return self.db.query(Resena).filter(Resena.resena_id == resena_id).first()

    def create_resena(self, resena_data: dict):
        resena = Resena(**resena_data)
        self.db.add(resena)
        self.db.commit()
        self.db.refresh(resena)
        return resena

    def update_resena(self, resena_id: int, resena_data: dict):
        resena = self.db.query(Resena).filter(Resena.resena_id == resena_id).first()
        if resena:
            for key, value in resena_data.items():
                setattr(resena, key, value)
            self.db.commit()
            return resena
        return None

    def delete_resena(self, resena_id: int):
        resena = self.db.query(Resena).filter(Resena.resena_id == resena_id).first()
        if resena:
            self.db.delete(resena)
            self.db.commit()
            return True
        return False
