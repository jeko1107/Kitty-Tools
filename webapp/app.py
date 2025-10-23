#!/usr/bin/env python3
from flask import Flask, render_template, url_for
from flask import request, redirect, session, flash, send_file
import platform
import sys
import os
import json
from datetime import datetime

app = Flask(__name__, template_folder="templates", static_folder="static")
# Secret key for session (for demo only). In production, use a secure random key.
app.secret_key = os.environ.get('KITTY_WEB_SECRET', 'dev-secret-key')

# Simple auth config (change in env for production)
ADMIN_USER = os.environ.get('KITTY_WEB_USER', 'admin')
ADMIN_PASS = os.environ.get('KITTY_WEB_PASS', 'changeme')

# Jobs directory
JOBS_DIR = os.path.join(os.path.dirname(__file__), 'jobs')
os.makedirs(JOBS_DIR, exist_ok=True)

# Menu items (disabled ones are potentially harmful and therefore not executable from the web)
menu_items = [
    {"id":"howto","label":"How to Use","description":"Guía interactiva sobre el uso de Kitty Tools","enabled":True},
    {"id":"info","label":"Information","description":"Créditos, licencia e información adicional","enabled":True},
    # Estas entradas aparecen habilitadas en la UI pero las rutas web son 'stubs' seguros
    {"id":"flood","label":"Kahoot Flooder","description":"Kahoot Flooder (habilitado en UI: ver comandos seguros)","enabled":True},
    {"id":"answers","label":"Answer Hack","description":"Answer Hack (habilitado en UI: ver comandos seguros)","enabled":True},
    {"id":"graphical","label":"GUI","description":"Interfaz gráfica (habilitado en UI: ver comandos seguros)","enabled":True},
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


@app.route('/flood')
def flood():
    # Esta ruta NO ejecuta el flooder; muestra cómo ejecutarlo localmente y advertencias.
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    src_available = os.path.isdir(os.path.join(repo_root, 'src'))
    if src_available:
        cmd = f"{sys.executable} {os.path.join(repo_root, 'src', 'main.py')}"
    else:
        cmd = f"{sys.executable} {os.path.join(repo_root, 'Kitty', 'Flood', 'main.py')}"
    warning = (
        "ATENCIÓN: El uso de flooders puede ser ilegal o violar las condiciones de servicio. "
        "Nunca ejecute estas herramientas contra servicios o redes sin permiso explícito."
    )
    return render_template('flood.html', cmd=cmd, warning=warning, src_available=src_available)


@app.route('/answers')
def answers():
    # Ruta segura que muestra cómo ejecutar localmente la herramienta de cliente
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    src_available = os.path.isdir(os.path.join(repo_root, 'src'))
    if src_available:
        cmd = f"{sys.executable} {os.path.join(repo_root, 'src', 'client.py')}"
    else:
        cmd = f"{sys.executable} {os.path.join(repo_root, 'Kitty', 'client.py')}"
    warning = (
        "ATENCIÓN: Obtener respuestas de quizzes sin permiso puede ser considerado cheating. "
        "Use estas utilidades sólo en entornos de pruebas o con autorización."
    )
    return render_template('answers.html', cmd=cmd, warning=warning, src_available=src_available)


@app.route('/graphical')
def graphical():
    # Mostrar instrucciones para ejecutar la GUI localmente
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    gui_path = os.path.join(repo_root, 'src', 'client', 'main.py')
    alt_path = os.path.join(repo_root, 'Kitty', 'client.py')
    if os.path.isfile(gui_path):
        cmd = f"{sys.executable} {gui_path}"
        has_gui = True
    else:
        cmd = f"{sys.executable} {alt_path}"
        has_gui = os.path.isfile(alt_path)
    note = (
        "Nota: la GUI requiere PyQt5 u otro framework gráfico. Estos pasos son para ejecución "
        "local en su máquina de desarrollo."
    )
    return render_template('graphical.html', cmd=cmd, note=note, has_gui=has_gui)

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


def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return wrapper


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            session['logged_in'] = True
            session['user'] = user
            flash('Sesión iniciada', 'success')
            nxt = request.args.get('next') or url_for('admin')
            return redirect(nxt)
        else:
            flash('Credenciales incorrectas', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
def admin():
    # List jobs
    jobs = []
    for fname in sorted(os.listdir(JOBS_DIR)):
        if fname.endswith('.json'):
            path = os.path.join(JOBS_DIR, fname)
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    jobs.append(json.load(fh))
            except Exception:
                continue
    return render_template('admin.html', jobs=jobs)


@app.route('/admin/create_job', methods=['POST'])
@login_required
def create_job():
    # Accepts a job type (flood/answers/graphical) and parameters, but does NOT execute.
    jtype = request.form.get('type')
    params = request.form.get('params') or ''
    job = {
        'id': datetime.utcnow().strftime('%Y%m%d%H%M%S%f'),
        'type': jtype,
        'params': params,
        'user': session.get('user'),
        'created_at': datetime.utcnow().isoformat() + 'Z',
        'status': 'created'
    }
    out = os.path.join(JOBS_DIR, f"{job['id']}.json")
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(job, fh, indent=2)
    flash('Job creado (no ejecutado) y registrado localmente', 'success')
    return redirect(url_for('admin'))


@app.route('/admin/download_job/<jobid>')
@login_required
def download_job(jobid):
    path = os.path.join(JOBS_DIR, f"{jobid}.json")
    if os.path.isfile(path):
        return send_file(path, as_attachment=True)
    flash('Job no encontrado', 'danger')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    # Run in debug mode by default for local testing. Do not expose in production without proper hardening.
    app.run(host='0.0.0.0', port=5000, debug=True)
