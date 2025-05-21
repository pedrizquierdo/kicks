from sqlalchemy.orm import Session
from entities.inventario import Inventario
from entities.producto import Producto
from typing import List, Optional

class InventarioService:
    def __init__(self, db: Session):
        self.db = db
    
    def obtener_todo_el_inventario(self) -> List[Inventario]:
        """Obtener todos los elementos del inventario"""
        return self.db.query(Inventario).all()
    
    def obtener_inventario_por_id(self, inventario_id: int) -> Optional[Inventario]:
        """Obtener un elemento del inventario por ID"""
        return self.db.query(Inventario).filter(Inventario.inventario_id == inventario_id).first()
    
    def obtener_inventario_por_producto(self, producto_id: int) -> List[Inventario]:
        """Obtener elementos del inventario para un producto específico"""
        return self.db.query(Inventario).filter(Inventario.producto_id == producto_id).all()
    
    def obtener_inventario_por_ubicacion(self, ubicacion: str) -> List[Inventario]:
        """Obtener elementos del inventario por ubicación de almacenamiento"""
        return self.db.query(Inventario).filter(Inventario.ubicacion_almacen == ubicacion).all()
    
    def obtener_stock_bajo(self, limite: int = 5) -> List[Inventario]:
        """Obtener elementos del inventario con stock por debajo del límite"""
        return self.db.query(Inventario).filter(Inventario.cantidad_disponible < limite).all()
    
    def crear_elemento_inventario(self, producto_id: int, talla: str, color: str, 
                                  cantidad: int, ubicacion: str) -> Inventario:
        """Crear un nuevo elemento de inventario"""
        item = Inventario(
            producto_id=producto_id,
            talla=talla,
            color=color,
            cantidad_disponible=cantidad,
            ubicacion_almacen=ubicacion
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def actualizar_elemento_inventario(self, inventario_id: int, cantidad: int = None, 
                                       ubicacion: str = None) -> Optional[Inventario]:
        """Actualizar un elemento del inventario"""
        item = self.obtener_inventario_por_id(inventario_id)
        if not item:
            return None
        
        if cantidad is not None:
            item.cantidad_disponible = cantidad
        if ubicacion is not None:
            item.ubicacion_almacen = ubicacion
            
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def agregar_stock(self, inventario_id: int, cantidad: int) -> Optional[Inventario]:
        """Agregar stock a un elemento del inventario"""
        item = self.obtener_inventario_por_id(inventario_id)
        if not item:
            return None
        
        item.cantidad_disponible += cantidad
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def quitar_stock(self, inventario_id: int, cantidad: int) -> Optional[Inventario]:
        """Quitar stock de un elemento del inventario"""
        item = self.obtener_inventario_por_id(inventario_id)
        if not item:
            return None
        
        if item.cantidad_disponible < cantidad:
            raise ValueError("No hay suficiente stock disponible")
        
        item.cantidad_disponible -= cantidad
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def eliminar_elemento_inventario(self, inventario_id: int) -> bool:
        """Eliminar un elemento del inventario"""
        item = self.obtener_inventario_por_id(inventario_id)
        if not item:
            return False
        
        self.db.delete(item)
        self.db.commit()
        return True
    
    def obtener_info_producto(self, producto_id: int) -> Optional[Producto]:
        """Obtener la información del producto asociado a un elemento del inventario"""
        return self.db.query(Producto).filter(Producto.producto_id == producto_id).first()
    
    def obtener_resumen_inventario(self) -> dict:
        """Obtener información resumida del inventario"""
        total_elementos = self.db.query(Inventario).count()
        total_productos = self.db.query(Producto).count()
        bajo_stock = len(self.obtener_stock_bajo())
        
        return {
            "total_elementos": total_elementos,
            "total_productos": total_productos,
            "elementos_con_stock_bajo": bajo_stock
        }
