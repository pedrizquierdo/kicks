from sqlalchemy.orm import Session
from entities.categoria import Categoria

class CategoriaService:
    def __init__(self, db: Session):
        self.db = db

    def get_categorias(self):
        return self.db.query(Categoria).all()

    def get_categoria_by_id(self, categoria_id: int):
        return self.db.query(Categoria).filter(Categoria.categoria_id == categoria_id).first()

    def create_categoria(self, categoria_data: dict):
        categoria = Categoria(**categoria_data)
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def update_categoria(self, categoria_id: int, categoria_data: dict):
        categoria = self.db.query(Categoria).filter(Categoria.categoria_id == categoria_id).first()
        if categoria:
            for key, value in categoria_data.items():
                setattr(categoria, key, value)
            self.db.commit()
            return categoria
        return None

    def delete_categoria(self, categoria_id: int):
        categoria = self.db.query(Categoria).filter(Categoria.categoria_id == categoria_id).first()
        if categoria:
            self.db.delete(categoria)
            self.db.commit()
            return True
        return False
