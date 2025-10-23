#!/usr/bin/env python3
from flask import Flask, render_template, url_for
import platform
import sys
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

# Menu items (disabled ones are potentially harmful and therefore not executable from the web)
menu_items = [
    {"id":"howto","label":"How to Use","description":"Guía interactiva sobre el uso de Kitty Tools","enabled":True},
    {"id":"info","label":"Information","description":"Créditos, licencia e información adicional","enabled":True},
    {"id":"flood","label":"Kahoot Flooder","description":"(DESHABILITADO) Utilidad de flooding para Kahoot","enabled":False},
    {"id":"answers","label":"Answer Hack","description":"(DESHABILITADO) Obtener respuestas para quizzes de Kahoot","enabled":False},
    {"id":"graphical","label":"GUI","description":"(DESHABILITADO) Interfaz gráfica","enabled":False},
    {"id":"exit","label":"Exit","description":"Salir de la aplicación (no aplica en web)","enabled":True},
]

howto_text = (
    "KITTY TOOLS es una suite de utilidades relacionadas con Kahoot.\n\n"
    "Características accesibles desde esta interfaz web (solo lectura):\n"
    "- Información del proyecto y contribuyentes.\n"
    "- Guía de uso y notas de seguridad.\n\n"
    "Por motivos de seguridad y de cumplimiento no se ejecutan desde la web las funcionalidades que puedan facilitar abuso "
    "(por ejemplo: flooders o herramientas para obtener respuestas). Si necesita ejecutar esas herramientas localmente, "
    "solo hágalo en redes de pruebas y con permiso explícito."
)

info_text = (
    "KITTY TOOLS v36.2 Enhanced\n"
    "Desarrollado por CPScript.\n\n"
    "Contribuidores:\n"
    "- @Ccode-lang\n"
    "- @xTobyPlayZ\n"
    "- @cheepling\n"
    "- @Zacky2613\n"
    "- @KiraKenjiro\n\n"
    "Licencia: software para fines educativos. Use bajo su responsabilidad."
)

@app.route('/')
def index():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    src_available = os.path.isdir(os.path.join(repo_root, 'src'))
    return render_template('index.html', menu_items=menu_items, src_available=src_available)

@app.route('/howto')
def howto():
    return render_template('howto.html', howto_text=howto_text)

@app.route('/info')
def info():
    return render_template('info.html', info_text=info_text)

@app.route('/status')
def status():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    src_available = os.path.isdir(os.path.join(repo_root, 'src'))
    data = {
        'platform': platform.system(),
        'platform_detail': platform.platform(),
        'python_version': sys.version,
        'src_available': src_available,
    }
    return render_template('status.html', data=data)

@app.route('/dependencies')
def dependencies():
    checks = {}
    for pkg in ('colorama', 'pystyle', 'PyQt5'):
        try:
            __import__(pkg)
            checks[pkg] = True
        except Exception:
            checks[pkg] = False
    return render_template('dependencies.html', checks=checks)

@app.route('/read_main')
def read_main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    main_path = os.path.join(repo_root, 'main.py')
    try:
        with open(main_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        content = f'No se pudo leer main.py: {e}'
    return render_template('read_main.html', content=content)

if __name__ == '__main__':
    # Run in debug mode by default for local testing. Do not expose in production without proper hardening.
    app.run(host='0.0.0.0', port=5000, debug=True)
