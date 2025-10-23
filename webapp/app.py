#!/usr/bin/env python3
from flask import Flask, render_template, url_for
from flask import request, redirect, session, flash, send_file
from functools import wraps
import threading
import platform
import sys
import os
import json
from datetime import datetime
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
import subprocess

app = Flask(__name__, template_folder="templates", static_folder="static")
# Secret key for session (for demo only). In production, use a secure random key.
app.secret_key = os.environ.get('KITTY_WEB_SECRET', 'dev-secret-key')

# Simple auth config (change in env for production)
ADMIN_USER = os.environ.get('KITTY_WEB_USER', 'admin')
# Support either providing a plain password or a precomputed hash via env.
env_pass = os.environ.get('KITTY_WEB_PASS', None)
env_pass_hash = os.environ.get('KITTY_WEB_PASS_HASH', None)
if env_pass_hash:
    ADMIN_PASS_HASH = env_pass_hash
else:
    if env_pass:
        ADMIN_PASS_HASH = generate_password_hash(env_pass)
    else:
        # default password: 'admin' (user authorized). Override via env strongly recommended.
        ADMIN_PASS_HASH = generate_password_hash('admin')

# Jobs directory
JOBS_DIR = os.path.join(os.path.dirname(__file__), 'jobs')
os.makedirs(JOBS_DIR, exist_ok=True)

# Menu items (disabled ones are potentially harmful but now executable with caution)
menu_items = [
    {"id":"howto","label":"How to Use","description":"Guía interactiva sobre el uso de Kitty Tools","enabled":True},
    {"id":"info","label":"Information","description":"Créditos, licencia e información adicional","enabled":True},
    {"id":"flood","label":"Kahoot Flooder","description":"Kahoot Flooder (ejecutable con permiso)","enabled":True},
    {"id":"answers","label":"Answer Hack","description":"Answer Hack (ejecutable con permiso)","enabled":True},
    {"id":"graphical","label":"GUI","description":"Interfaz gráfica (ejecutable con permiso)","enabled":True},
    {"id":"logout","label":"Exit","description":"Salir de la aplicación","enabled":True},
]

howto_text = (
    "KITTY TOOLS es una suite de utilidades relacionadas con Kahoot.\n\n"
    "Características accesibles desde esta interfaz web:\n"
    "- Información del proyecto y contribuyentes.\n"
    "- Guía de uso y notas de seguridad.\n"
    "- Ejecución controlada de herramientas (requiere autenticación).\n\n"
    "ATENCIÓN: Ejecute estas herramientas solo en entornos de prueba con permiso explícito."
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

# Decorator para proteger rutas que requieren login
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return wrapper

def get_csrf_token():
    token = session.get('_csrf_token')
    if not token:
        token = secrets.token_urlsafe(16)
        session['_csrf_token'] = token
    return token

def validate_csrf(form_token):
    session_token = session.get('_csrf_token')
    return session_token and session_token == form_token

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
@login_required
def flood():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    src_available = os.path.isdir(os.path.join(repo_root, 'src'))
    main_path = os.path.join(repo_root, 'src', 'main.py') if src_available else os.path.join(repo_root, 'Kitty', 'Flood', 'main.py')
    warning = None
    try:
        result = subprocess.run([sys.executable, main_path, '--mode', 'flood'], capture_output=True, text=True, timeout=60)
        output = result.stdout + result.stderr
        status = 'success' if result.returncode == 0 else 'error'
    except subprocess.TimeoutExpired:
        output = "Error: La ejecución excedió el tiempo límite de 60 segundos."
        status = 'error'
    except Exception as e:
        output = f"Error al ejecutar main.py: {str(e)}"
        status = 'error'
    job = {
        'id': datetime.utcnow().strftime('%Y%m%d%H%M%S%f'),
        'type': 'flood',
        'params': {'mode': 'flood'},
        'user': session.get('user'),
        'created_at': datetime.utcnow().isoformat() + 'Z',
        'status': status,
        'result': {'output': output}
    }
    out = os.path.join(JOBS_DIR, f"{job['id']}.json")
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(job, fh, indent=2)
    return render_template('flood.html', cmd=f"{sys.executable} {main_path} --mode flood", warning=warning, src_available=src_available, output=output, status=status)

@app.route('/answers')
@login_required
def answers():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    src_available = os.path.isdir(os.path.join(repo_root, 'src'))
    main_path = os.path.join(repo_root, 'src', 'main.py') if src_available else os.path.join(repo_root, 'Kitty', 'client.py')
    warning = None
    try:
        result = subprocess.run([sys.executable, main_path, '--mode', 'answers'], capture_output=True, text=True, timeout=60)
        output = result.stdout + result.stderr
        status = 'success' if result.returncode == 0 else 'error'
    except subprocess.TimeoutExpired:
        output = "Error: La ejecución excedió el tiempo límite de 60 segundos."
        status = 'error'
    except Exception as e:
        output = f"Error al ejecutar main.py: {str(e)}"
        status = 'error'
    job = {
        'id': datetime.utcnow().strftime('%Y%m%d%H%M%S%f'),
        'type': 'answers',
        'params': {'mode': 'answers'},
        'user': session.get('user'),
        'created_at': datetime.utcnow().isoformat() + 'Z',
        'status': status,
        'result': {'output': output}
    }
    out = os.path.join(JOBS_DIR, f"{job['id']}.json")
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(job, fh, indent=2)
    return render_template('answers.html', cmd=f"{sys.executable} {main_path} --mode answers", warning=warning, src_available=src_available, output=output, status=status)

@app.route('/graphical')
@login_required
def graphical():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    gui_path = os.path.join(repo_root, 'src', 'main.py')
    alt_path = os.path.join(repo_root, 'Kitty', 'client.py')
    main_path = gui_path if os.path.isfile(gui_path) else alt_path
    has_gui = os.path.isfile(main_path)
    note = None
    try:
        result = subprocess.run([sys.executable, main_path, '--mode', 'graphical'], capture_output=True, text=True, timeout=60)
        output = result.stdout + result.stderr
        status = 'success' if result.returncode == 0 else 'error'
    except subprocess.TimeoutExpired:
        output = "Error: La ejecución excedió el tiempo límite de 60 segundos."
        status = 'error'
    except Exception as e:
        output = f"Error al ejecutar main.py: {str(e)}"
        status = 'error'
    job = {
        'id': datetime.utcnow().strftime('%Y%m%d%H%M%S%f'),
        'type': 'graphical',
        'params': {'mode': 'graphical'},
        'user': session.get('user'),
        'created_at': datetime.utcnow().isoformat() + 'Z',
        'status': status,
        'result': {'output': output}
    }
    out = os.path.join(JOBS_DIR, f"{job['id']}.json")
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(job, fh, indent=2)
    return render_template('graphical.html', cmd=f"{sys.executable} {main_path} --mode graphical", note=note, has_gui=has_gui, output=output, status=status)

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    attempts = session.get('login_attempts', 0)
    last_attempt = session.get('login_last_attempt', 0)
    if request.method == 'POST':
        form_csrf = request.form.get('_csrf')
        if not validate_csrf(form_csrf):
            flash('CSRF token inválido', 'danger')
            return render_template('login.html', csrf_token=get_csrf_token())

        if attempts >= 10:
            flash('Demasiados intentos. Espere un momento.', 'danger')
            return render_template('login.html', csrf_token=get_csrf_token())

        user = request.form.get('username')
        pwd = request.form.get('password')
        if user == ADMIN_USER and check_password_hash(ADMIN_PASS_HASH, pwd):
            session['logged_in'] = True
            session['user'] = user
            session['login_attempts'] = 0
            flash('Sesión iniciada', 'success')
            nxt = request.args.get('next') or url_for('admin')
            return redirect(nxt)
        else:
            attempts += 1
            session['login_attempts'] = attempts
            session['login_last_attempt'] = int(datetime.utcnow().timestamp())
            flash('Credenciales incorrectas', 'danger')
    return render_template('login.html', csrf_token=get_csrf_token())

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    jobs = []
    for fname in sorted(os.listdir(JOBS_DIR), reverse=True):
        if fname.endswith('.json'):
            path = os.path.join(JOBS_DIR, fname)
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    jobs.append(json.load(fh))
            except Exception:
                continue
    return render_template('admin.html', jobs=jobs, csrf_token=get_csrf_token())

@app.route('/admin/create_job', methods=['POST'])
@login_required
def create_job():
    form_csrf = request.form.get('_csrf')
    if not validate_csrf(form_csrf):
        flash('CSRF token inválido', 'danger')
        return redirect(url_for('admin'))

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

@app.route('/admin/view_job/<jobid>')
@login_required
def view_job(jobid):
    path = os.path.join(JOBS_DIR, f"{jobid}.json")
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as fh:
            job = json.load(fh)
        return render_template('view_job.html', job=job)
    flash('Job no encontrado', 'danger')
    return redirect(url_for('admin'))

@app.route('/admin/simulate', methods=['POST'])
@login_required
def admin_simulate():
    form_csrf = request.form.get('_csrf')
    if not validate_csrf(form_csrf):
        flash('CSRF token inválido', 'danger')
        return redirect(url_for('admin'))

    sim_type = request.form.get('sim_type')
    
    # Recolectar parámetros de los campos individuales
    params = {}
    
    # Número (puede ser bots o eventos)
    if request.form.get('param_n'):
        params['n'] = request.form.get('param_n')
    
    # PIN del juego
    if request.form.get('param_pin'):
        params['pin'] = request.form.get('param_pin')
    
    # Latencias
    if request.form.get('param_minlat'):
        params['minlat'] = request.form.get('param_minlat')
    if request.form.get('param_maxlat'):
        params['maxlat'] = request.form.get('param_maxlat')
    
    # Preguntas y precisión (para answers)
    if request.form.get('param_q'):
        params['q'] = request.form.get('param_q')
    if request.form.get('param_acc'):
        params['acc'] = request.form.get('param_acc')

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # SIEMPRE usar el main.py del directorio raíz (no el de src)
    main_path = os.path.join(repo_root, 'main.py')

    # Crear job en estado running y lanzar proceso en background
    job = {
        'id': datetime.utcnow().strftime('%Y%m%d%H%M%S%f'),
        'type': sim_type,
        'params': params,
        'user': session.get('user'),
        'created_at': datetime.utcnow().isoformat() + 'Z',
        'status': 'running',
        'result': {'output': ''}
    }

    # Guardar job inicial
    out = os.path.join(JOBS_DIR, f"{job['id']}.json")
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(job, fh, indent=2)

    # Preparar comando
    cmd = [sys.executable, main_path, '--mode', sim_type]
    for k, v in params.items():
        cmd.extend([f'--{k}', v])

    log_path = os.path.join(JOBS_DIR, f"{job['id']}.log")

    try:
        # Iniciar proceso en background y redirigir salida a archivo
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=repo_root)

        # Worker que hace streaming del stdout al log y actualiza el JSON del job
        def stream_and_finalize(proc, log_path, job_json_path, jobid):
            try:
                with open(log_path, 'w', encoding='utf-8') as logf:
                    if proc.stdout:
                        for line in iter(proc.stdout.readline, ''):
                            if line == '':
                                break
                            logf.write(line)
                            logf.flush()
                            # actualización parcial del job
                            try:
                                with open(job_json_path, 'r', encoding='utf-8') as jf:
                                    j = json.load(jf)
                            except Exception:
                                j = None
                            if j is not None:
                                prev = j.get('result', {}).get('output', '')
                                j.setdefault('result', {})['output'] = prev + line
                                with open(job_json_path, 'w', encoding='utf-8') as jf:
                                    json.dump(j, jf, indent=2)

                ret = proc.wait()
                with open(log_path, 'r', encoding='utf-8') as logf2:
                    output = logf2.read()
                status_final = 'success' if ret == 0 else 'error'
            except Exception as e:
                output = f"Error during execution: {e}"
                status_final = 'error'

            # Actualizar job final
            try:
                with open(job_json_path, 'r', encoding='utf-8') as jf:
                    j = json.load(jf)
            except Exception:
                j = {}
            j['status'] = status_final
            j['result'] = {'output': output, 'log': os.path.basename(log_path)}
            with open(job_json_path, 'w', encoding='utf-8') as jf:
                json.dump(j, jf, indent=2)

        # Lanzar worker daemon para no bloquear la petición
        t = threading.Thread(target=stream_and_finalize, args=(proc, log_path, out, job['id']), daemon=True)
        t.start()

    except Exception as e:
        output = f"Error al iniciar proceso en background: {str(e)}"
        job['status'] = 'error'
        job['result'] = {'output': output}
        with open(out, 'w', encoding='utf-8') as fh:
            json.dump(job, fh, indent=2)

        flash('Error al iniciar la ejecución', 'danger')
        return redirect(url_for('admin'))

    flash('Ejecución iniciada y registrada (ver historial para salida)', 'success')
    return redirect(url_for('view_job', jobid=job['id']))


@app.route('/admin/download_log/<jobid>')
@login_required
def download_log(jobid):
    path = os.path.join(JOBS_DIR, f"{jobid}.log")
    if os.path.isfile(path):
        return send_file(path, as_attachment=True)
    flash('Log no encontrado', 'danger')
    return redirect(url_for('view_job', jobid=jobid))

@app.route('/admin/job_status/<jobid>')
@login_required
def job_status(jobid):
    """Endpoint para polling: devuelve estado actual del job y salida del log"""
    job_path = os.path.join(JOBS_DIR, f"{jobid}.json")
    log_path = os.path.join(JOBS_DIR, f"{jobid}.log")
    
    if not os.path.isfile(job_path):
        return {'error': 'Job no encontrado'}, 404
    
    with open(job_path, 'r', encoding='utf-8') as fh:
        job = json.load(fh)
    
    # Leer log actual si existe
    output = ''
    if os.path.isfile(log_path):
        with open(log_path, 'r', encoding='utf-8') as logf:
            output = logf.read()
    
    return {
        'id': job.get('id'),
        'status': job.get('status', 'unknown'),
        'output': output,
        'result': job.get('result', {})
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)