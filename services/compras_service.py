from sqlalchemy.orm import Session
from entities.compras import Compra

class CompraService:
    def __init__(self, db: Session):
        self.db = db

    def get_compras(self):
        return self.db.query(Compra).all()

    def get_compra_by_id(self, compra_id: int):
        return self.db.query(Compra).filter(Compra.compra_id == compra_id).first()

    def create_compra(self, compra_data: dict):
        compra = Compra(**compra_data)
        self.db.add(compra)
        self.db.commit()
        self.db.refresh(compra)
        return compra

    def update_compra(self, compra_id: int, compra_data: dict):
        compra = self.db.query(Compra).filter(Compra.compra_id == compra_id).first()
        if compra:
            for key, value in compra_data.items():
                setattr(compra, key, value)
            self.db.commit()
            return compra
        return None

    def delete_compra(self, compra_id: int):
        compra = self.db.query(Compra).filter(Compra.compra_id == compra_id).first()
        if compra:
            self.db.delete(compra)
            self.db.commit()
            return True
        return False
