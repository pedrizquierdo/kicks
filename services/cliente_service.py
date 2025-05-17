from sqlalchemy.orm import Session
from entities.cliente import Cliente

class ClienteService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_clientes(self):
        return self.db.query(Cliente).all()
    
    def get_cliente_by_id(self, cliente_id: int):
        return self.db.query(Cliente).filter(Cliente.cliente_id == cliente_id).first()
    
    def create_cliente(self, cliente_data: dict):
        cliente = Cliente(**cliente_data)
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente
    
    def update_cliente(self, cliente_id: int, cliente_data: dict):
        cliente = self.db.query(Cliente).filter(Cliente.cliente_id == cliente_id).first()
        if cliente:
            for key, value in cliente_data.items():
                setattr(cliente, key, value)
            self.db.commit()
            return cliente
        return None
    
    def delete_cliente(self, cliente_id: int):
        cliente = self.db.query(Cliente).filter(Cliente.cliente_id == cliente_id).first()
        if cliente:
            self.db.delete(cliente)
            self.db.commit()
            return True
        return False