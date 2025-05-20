from sqlalchemy.orm import Session
from entities.empleados import Empleado

class EmpleadoService:
    def __init__(self, db: Session):
        self.db = db

    def get_empleados(self):
        return self.db.query(Empleado).all()

    def get_empleado_by_id(self, empleado_id: int):
        return self.db.query(Empleado).filter(Empleado.empleado_id == empleado_id).first()

    def create_empleado(self, empleado_data: dict):
        empleado = Empleado(**empleado_data)
        self.db.add(empleado)
        self.db.commit()
        self.db.refresh(empleado)
        return empleado

    def update_empleado(self, empleado_id: int, empleado_data: dict):
        empleado = self.db.query(Empleado).filter(Empleado.empleado_id == empleado_id).first()
        if empleado:
            for key, value in empleado_data.items():
                setattr(empleado, key, value)
            self.db.commit()
            return empleado
        return None

    def delete_empleado(self, empleado_id: int):
        empleado = self.db.query(Empleado).filter(Empleado.empleado_id == empleado_id).first()
        if empleado:
            self.db.delete(empleado)
            self.db.commit()
            return True
        return False