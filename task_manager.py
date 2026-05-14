import json
import os
from datetime import datetime

class TaskFlowApp:
    def __init__(self, archivo_datos='tareas.json'):
        self.archivo_datos = os.path.abspath(archivo_datos)
        self.tareas = self.cargar_tareas()

    def cargar_tareas(self):
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except: return []
        return []

    def guardar_tareas(self):
        with open(self.archivo_datos, 'w', encoding='utf-8') as f:
            json.dump(self.tareas, f, indent=4)

    def crear_tarea(self, titulo, descripcion):
        nueva_tarea = {
            "titulo": titulo,
            "descripcion": descripcion,
            "estado": "Pendiente",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.tareas.append(nueva_tarea)
        self.guardar_tareas()
        print(f"\n✅ Tarea '{titulo}' creada.")

    def consultar_tareas(self):
        print("\n--- 📋 LISTA DE TAREAS ---")
        if not self.tareas:
            print("📭 No hay tareas.")
        else:
            for i, t in enumerate(self.tareas):
                print(f"{i}. [{t['estado']}] {t['titulo']}")

    def marcar_completada(self, indice):
        if 0 <= indice < len(self.tareas):
            self.tareas[indice]['estado'] = "Completada"
            self.guardar_tareas()
            print(f"✔️ Tarea '{self.tareas[indice]['titulo']}' completada.")
        else:
            print("❌ Número de tarea no válido.")

    def eliminar_tarea(self, indice):
        """Elimina una tarea específica por su número"""
        if 0 <= indice < len(self.tareas):
            eliminada = self.tareas.pop(indice)
            self.guardar_tareas()
            print(f"🗑️ Tarea '{eliminada['titulo']}' eliminada para siempre.")
        else:
            print("❌ Número de tarea no válido.")

    def limpiar_completadas(self):
        """Borra todas las tareas que ya estén en estado 'Completada'"""
        tareas_antes = len(self.tareas)
        self.tareas = [t for t in self.tareas if t['estado'] != "Completada"]
        tareas_despues = len(self.tareas)
        
        self.guardar_tareas()
        print(f"🧹 Limpieza terminada. Se borraron {tareas_antes - tareas_despues} tareas.")

    def generar_reporte(self):
        total = len(self.tareas)
        completadas = sum(1 for t in self.tareas if t['estado'] == "Completada")
        print("\n" + "="*30)
        print(f"📊 REPORTE ACTUAL\nTotal: {total}\n✅ Hechas: {completadas}\n⏳ Pendientes: {total - completadas}")
        print("="*30)

if __name__ == "__main__":
    app = TaskFlowApp()
    while True:
        print("\n--- 🚀 TASKFLOW SOLUTIONS ---")
        print("1. Crear | 2. Ver | 3. Completar | 4. Reporte")
        print("5. Eliminar una | 6. Limpiar todas las completadas | 7. Salir")
        
        opcion = input("\nSelecciona: ")
        
        if opcion == "1":
            app.crear_tarea(input("Título: "), input("Descripción: "))
        elif opcion == "2":
            app.consultar_tareas()
        elif opcion == "3":
            app.consultar_tareas()
            try:
                app.marcar_completada(int(input("Número a completar: ")))
            except: print("Error: Ingresa un número.")
        elif opcion == "4":
            app.generar_reporte()
        elif opcion == "5":
            app.consultar_tareas()
            try:
                app.eliminar_tarea(int(input("Número a eliminar: ")))
            except: print("Error: Ingresa un número.")
        elif opcion == "6":
            app.limpiar_completadas()
        elif opcion == "7":
            print("¡Adiós!")
            break