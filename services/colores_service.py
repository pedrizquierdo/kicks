from sqlalchemy.orm import Session
from entities.colores import Color

class ColorService:
    def __init__(self, db: Session):
        self.db = db

    def get_colores(self):
        return self.db.query(Color).all()

    def get_color_by_id(self, color_id: int):
        return self.db.query(Color).filter(Color.color_id == color_id).first()

    def create_color(self, color_data: dict):
        color = Color(**color_data)
        self.db.add(color)
        self.db.commit()
        self.db.refresh(color)
        return color

    def update_color(self, color_id: int, color_data: dict):
        color = self.db.query(Color).filter(Color.color_id == color_id).first()
        if color:
            for key, value in color_data.items():
                setattr(color, key, value)
            self.db.commit()
            return color
        return None

    def delete_color(self, color_id: int):
        color = self.db.query(Color).filter(Color.color_id == color_id).first()
        if color:
            self.db.delete(color)
            self.db.commit()
            return True
        return False