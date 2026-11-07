import csv
from decimal import Decimal
from datetime import datetime
from typing import List, Dict, Any

class CSVDataLoader:
    def __init__(self, data_folder: str = "data"):
        self.data_folder = data_folder

    def _read_csv(self, filename: str) -> List[Dict[str, str]]:
        filepath = f"{self.data_folder}/{filename}"
        with open(filepath, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            return [dict(row) for row in reader]

    def cargar_actores(self) -> List[Dict[str, Any]]:
        filas = self._read_csv("actores.csv")
        actores = []
        for f in filas:
            actores.append({
                "actor_id": f.get("id") or f.get("actor_id"),
                "nombre": f.get("nombre"),
                "tipo": f.get("tipo"),
                "activo": f.get("activo", "true").lower() in ("true", "1", "si")
            })
        return actores

    def cargar_catalogo(self) -> List[Dict[str, Any]]:
        filas = self._read_csv("catalogo.csv")
        servicios = []
        for f in filas:
            servicios.append({
                "recurso_id": f.get("id") or f.get("recurso_id"),
                "nombre": f.get("nombre"),
                "precio_mxn": Decimal(f.get("precio_mxn", "0.00")),
                "duracion_minutos": int(f.get("duracion_minutos", 30))
            })
        return servicios

    def cargar_operaciones(self) -> List[Dict[str, Any]]:
        operaciones_filas = self._read_csv("operaciones.csv")
        detalles_filas = self._read_csv("detalle_operaciones.csv")

        detalles_map: Dict[str, List[Dict[str, Any]]] = {}
        for d in detalles_filas:
            op_id = d.get("operacion_id")
            if op_id not in detalles_map:
                detalles_map[op_id] = []
            
            detalles_map[op_id].append({
                "recurso_id": d.get("recurso_id"),
                "cantidad": int(d.get("cantidad", 1)),
                "precio_unitario": Decimal(d.get("precio_mxn", "0.00"))
            })

        operaciones = []
        for op in operaciones_filas:
            op_id = op.get("id") or op.get("operacion_id")
            lineas = detalles_map.get(op_id, [])
            
            total_calculado = sum(
                linea["precio_unitario"] * linea["cantidad"] for linea in lineas
            ) if lineas else Decimal(op.get("total_mxn", "0.00"))

            operaciones.append({
                "operacion_id": op_id,
                "actor_id": op.get("actor_id"),
                "fecha_hora": datetime.fromisoformat(op.get("fecha_iso")),
                "estado_inicial": op.get("estado", "SOLICITADA"),
                "detalles": lineas,
                "total_mxn": total_calculado
            })
        return operaciones