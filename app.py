from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DB_FILE = 'tareas.json'


# CARGAR TAREAS
def cargar_tareas():

    if os.path.exists(DB_FILE):

        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    return []


# GUARDAR TAREAS
def guardar_tareas(tareas):

    with open(DB_FILE, 'w', encoding='utf-8') as f:

        json.dump(
            tareas,
            f,
            indent=4,
            ensure_ascii=False
        )


# INICIO
@app.route('/')
def index():

    tareas = cargar_tareas()

    total = len(tareas)

    completadas = sum(
        1 for t in tareas
        if t['estado'] == "Completada"
    )

    pendientes = sum(
        1 for t in tareas
        if t['estado'] == "Pendiente"
    )

    return render_template(
        'index.html',
        tareas=tareas,
        total=total,
        completadas=completadas,
        pendientes=pendientes
    )


# AGREGAR TAREA
@app.route('/add', methods=['POST'])
def add():

    titulo = request.form.get('titulo')

    if titulo:

        tareas = cargar_tareas()

        nueva_tarea = {

            "titulo": titulo,

            "estado": "Pendiente"

        }

        tareas.append(nueva_tarea)

        guardar_tareas(tareas)

    return redirect(url_for('index'))


# COMPLETAR TAREA
@app.route('/complete/<int:index>')
def complete(index):

    tareas = cargar_tareas()

    if 0 <= index < len(tareas):

        tareas[index]['estado'] = "Completada"

        guardar_tareas(tareas)

    return redirect(url_for('index'))


# ELIMINAR TAREA
@app.route('/delete/<int:index>')
def delete(index):

    tareas = cargar_tareas()

    if 0 <= index < len(tareas):

        tareas.pop(index)

        guardar_tareas(tareas)

    return redirect(url_for('index'))


# LIMPIAR COMPLETADAS
@app.route('/clear_completed')
def clear_completed():

    tareas = cargar_tareas()

    tareas = [
        t for t in tareas
        if t['estado'] != "Completada"
    ]

    guardar_tareas(tareas)

    return redirect(url_for('index'))


# EJECUTAR
if __name__ == '__main__':

    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'

    app.run(host='0.0.0.0', port=port, debug=debug)