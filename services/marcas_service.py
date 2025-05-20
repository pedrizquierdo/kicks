from sqlalchemy.orm import Session
from entities.marcas import Marca

class MarcaService:
    def __init__(self, db: Session):
        self.db = db

    def get_marcas(self):
        return self.db.query(Marca).all()

    def get_marca_by_id(self, marca_id: int):
        return self.db.query(Marca).filter(Marca.marca_id == marca_id).first()

    def create_marca(self, marca_data: dict):
        marca = Marca(**marca_data)
        self.db.add(marca)
        self.db.commit()
        self.db.refresh(marca)
        return marca

    def update_marca(self, marca_id: int, marca_data: dict):
        marca = self.db.query(Marca).filter(Marca.marca_id == marca_id).first()
        if marca:
            for key, value in marca_data.items():
                setattr(marca, key, value)
            self.db.commit()
            return marca
        return None

    def delete_marca(self, marca_id: int):
        marca = self.db.query(Marca).filter(Marca.marca_id == marca_id).first()
        if marca:
            self.db.delete(marca)
            self.db.commit()
            return True
        return False
