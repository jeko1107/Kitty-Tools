#!/usr/bin/env python3
from flask import Flask, render_template, url_for
from flask import request, redirect, session, flash, send_file, jsonify
from functools import wraps
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sys
import platform
import json
import subprocess
import threading
import queue
import signal
import time
import secrets

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

# Cola global para jobs en ejecución
running_jobs = {}
job_queues = {}

# Decorator para proteger rutas que requieren login
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Debe iniciar sesión para acceder', 'warning')
            return redirect(url_for('login'))
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
@login_required
def index():
    # Cargar todos los jobs
    jobs = []
    for fname in sorted(os.listdir(JOBS_DIR), reverse=True):
        if fname.endswith('.json'):
            path = os.path.join(JOBS_DIR, fname)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    job = json.load(f)
                    jobs.append(job)
            except Exception:
                pass
    
    return render_template('index.html', jobs=jobs, csrf_token=get_csrf_token())

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
    main_path = os.path.join(repo_root, 'main.py')
    warning = "Esta herramienta debe usarse solo con permiso explícito."
    
    return render_template('flood.html', 
                         cmd=f"{sys.executable} {main_path} --mode flood", 
                         warning=warning, 
                         src_available=src_available,
                         csrf_token=get_csrf_token())

@app.route('/answers')
@login_required
def answers():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    src_available = os.path.isdir(os.path.join(repo_root, 'src'))
    main_path = os.path.join(repo_root, 'main.py')
    warning = "Esta herramienta debe usarse solo con permiso explícito."
    
    return render_template('answers.html', 
                         cmd=f"{sys.executable} {main_path} --mode answers", 
                         warning=warning, 
                         src_available=src_available,
                         csrf_token=get_csrf_token())

@app.route('/graphical')
@login_required
def graphical():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    main_path = os.path.join(repo_root, 'main.py')
    has_gui = os.path.isfile(main_path)
    note = "La interfaz gráfica requiere un entorno con display X11."
    
    return render_template('graphical.html', 
                         cmd=f"{sys.executable} {main_path} --mode graphical", 
                         note=note, 
                         has_gui=has_gui,
                         csrf_token=get_csrf_token())

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
            flash('Token CSRF inválido', 'danger')
            return redirect(url_for('login'))

        if attempts >= 10:
            flash('Demasiados intentos fallidos. Intente más tarde.', 'danger')
            return redirect(url_for('login'))

        user = request.form.get('username')
        pwd = request.form.get('password')

        if user == ADMIN_USER and check_password_hash(ADMIN_PASS_HASH, pwd):
            session['logged_in'] = True
            session['user'] = user
            session['login_attempts'] = 0
            flash('Sesión iniciada correctamente', 'success')
            return redirect(url_for('admin'))
        else:
            session['login_attempts'] = attempts + 1
            session['login_last_attempt'] = time.time()
            flash('Credenciales incorrectas', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', csrf_token=get_csrf_token())

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    jobs = []
    for fname in sorted(os.listdir(JOBS_DIR), reverse=True):
        if fname.endswith('.json'):
            path = os.path.join(JOBS_DIR, fname)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    job = json.load(f)
                    jobs.append(job)
            except Exception:
                pass
    return render_template('admin.html', jobs=jobs, csrf_token=get_csrf_token())

@app.route('/admin/create_job', methods=['POST'])
@login_required
def create_job():
    form_csrf = request.form.get('_csrf')
    if not validate_csrf(form_csrf):
        flash('Token CSRF inválido', 'danger')
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
        with open(path, 'r', encoding='utf-8') as f:
            job = json.load(f)
        return render_template('view_job.html', job=job, csrf_token=get_csrf_token())
    flash('Job no encontrado', 'danger')
    return redirect(url_for('admin'))

def execute_job_in_background(job_id, job_type, params):
    """Ejecuta un job en background y actualiza su estado"""
    job_path = os.path.join(JOBS_DIR, f"{job_id}.json")
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    main_path = os.path.join(repo_root, 'main.py')
    
    job_queues[job_id] = queue.Queue()
    output_lines = []
    
    try:
        cmd = [sys.executable, main_path]
        
        if job_type == 'flood':
            cmd.extend(['--mode', 'flood'])
            if params.get('pin'):
                cmd.extend(['--pin', str(params['pin'])])
            if params.get('n'):
                cmd.extend(['--n', str(params['n'])])
            if params.get('minlat'):
                cmd.extend(['--minlat', str(params['minlat'])])
            if params.get('maxlat'):
                cmd.extend(['--maxlat', str(params['maxlat'])])
            if params.get('name'):
                cmd.extend(['--name', str(params['name'])])
                
        elif job_type == 'answers':
            cmd.extend(['--mode', 'answers'])
            if params.get('pin'):
                cmd.extend(['--pin', str(params['pin'])])
            if params.get('quiz_id'):
                cmd.extend(['--quiz-id', str(params['quiz_id'])])
            if params.get('q'):
                cmd.extend(['--q', str(params['q'])])
            if params.get('acc'):
                cmd.extend(['--acc', str(params['acc'])])
                
        elif job_type == 'gui':
            cmd.extend(['--mode', 'graphical'])
            if params.get('pin'):
                cmd.extend(['--pin', str(params['pin'])])
            if params.get('e'):
                cmd.extend(['--e', str(params['e'])])
        
        # Log del comando para debug
        cmd_str = ' '.join(cmd)
        output_lines.append(f"[DEBUG] Ejecutando: {cmd_str}")
        output_lines.append(f"[DEBUG] Working directory: {repo_root}")
        print(f"[JOB {job_id}] Ejecutando: {cmd_str}")
        
        # Actualizar job con el comando
        with open(job_path, 'r', encoding='utf-8') as f:
            job_data = json.load(f)
        job_data['result']['output'] = '\n'.join(output_lines) + '\n'
        job_data['result']['command'] = cmd_str
        with open(job_path, 'w', encoding='utf-8') as f:
            json.dump(job_data, f, indent=2)
        
        # Ejecutar proceso con variables de entorno heredadas
        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=0,  # Sin buffer
            universal_newlines=True,
            cwd=repo_root,  # Ejecutar desde el directorio raíz del proyecto
            env=env,
            preexec_fn=os.setsid if platform.system() != 'Windows' else None
        )
        
        running_jobs[job_id] = process
        
        # Leer output en tiempo real
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                line = line.rstrip()
                output_lines.append(line)
                job_queues[job_id].put(line)
                print(f"[JOB {job_id}] {line}")
                
                # Actualizar job periódicamente
                if len(output_lines) % 5 == 0:
                    try:
                        with open(job_path, 'r', encoding='utf-8') as f:
                            job_data = json.load(f)
                        job_data['result']['output'] = '\n'.join(output_lines)
                        with open(job_path, 'w', encoding='utf-8') as f:
                            json.dump(job_data, f, indent=2)
                    except Exception as e:
                        print(f"[JOB {job_id}] Error actualizando: {e}")
        
        process.wait(timeout=300)
        
        print(f"[JOB {job_id}] Proceso terminado con código: {process.returncode}")
        
        with open(job_path, 'r', encoding='utf-8') as f:
            job_data = json.load(f)
        
        job_data['status'] = 'completed' if process.returncode == 0 else 'failed'
        job_data['result']['output'] = '\n'.join(output_lines)
        job_data['result']['exit_code'] = process.returncode
        job_data['completed_at'] = datetime.utcnow().isoformat() + 'Z'
        
        # No agregar métricas simuladas, dejar que el output real lo muestre
        
        with open(job_path, 'w', encoding='utf-8') as f:
            json.dump(job_data, f, indent=2)
            
    except subprocess.TimeoutExpired:
        print(f"[JOB {job_id}] TIMEOUT")
        process.kill()
        with open(job_path, 'r', encoding='utf-8') as f:
            job_data = json.load(f)
        job_data['status'] = 'timeout'
        job_data['result']['output'] = '\n'.join(output_lines) + '\n\n[TIMEOUT: Proceso excedió 5 minutos]'
        with open(job_path, 'w', encoding='utf-8') as f:
            json.dump(job_data, f, indent=2)
            
    except Exception as e:
        print(f"[JOB {job_id}] ERROR: {e}")
        import traceback
        traceback.print_exc()
        with open(job_path, 'r', encoding='utf-8') as f:
            job_data = json.load(f)
        job_data['status'] = 'error'
        job_data['result']['output'] = '\n'.join(output_lines) + f"\n\n[ERROR: {str(e)}]"
        with open(job_path, 'w', encoding='utf-8') as f:
            json.dump(job_data, f, indent=2)
    
    finally:
        if job_id in running_jobs:
            del running_jobs[job_id]
        if job_id in job_queues:
            del job_queues[job_id]

@app.route('/admin/simulate', methods=['POST'])
@login_required
def admin_simulate():
    if not validate_csrf(request.form.get('csrf_token')):
        flash('Token CSRF inválido', 'error')
        return redirect(url_for('index'))
    
    sim_type = request.form.get('sim_type', 'flood')
    params = {}
    
    if request.form.get('pin'):
        params['pin'] = request.form.get('pin')
    if request.form.get('param_n'):
        params['n'] = int(request.form.get('param_n'))
    if request.form.get('param_minlat'):
        params['minlat'] = int(request.form.get('param_minlat'))
    if request.form.get('param_maxlat'):
        params['maxlat'] = int(request.form.get('param_maxlat'))
    if request.form.get('param_name'):
        params['name'] = request.form.get('param_name')
    if request.form.get('param_q'):
        params['q'] = int(request.form.get('param_q'))
    if request.form.get('param_acc'):
        params['acc'] = float(request.form.get('param_acc'))
    if request.form.get('param_e'):
        params['e'] = int(request.form.get('param_e'))
    if request.form.get('param_pin_answers'):
        params['pin'] = request.form.get('param_pin_answers')
    if request.form.get('param_quiz_id'):
        params['quiz_id'] = request.form.get('param_quiz_id')

    job = {
        'id': datetime.utcnow().strftime('%Y%m%d%H%M%S%f'),
        'type': sim_type,
        'params': params,
        'user': session.get('user'),
        'created_at': datetime.utcnow().isoformat() + 'Z',
        'status': 'running',
        'result': {'output': 'Iniciando ejecución...\n'}
    }

    out = os.path.join(JOBS_DIR, f"{job['id']}.json")
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(job, fh, indent=2)

    thread = threading.Thread(
        target=execute_job_in_background,
        args=(job['id'], sim_type, params),
        daemon=True
    )
    thread.start()

    flash(f'Job {job["id"]} iniciado en segundo plano', 'success')
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
    job_path = os.path.join(JOBS_DIR, f"{jobid}.json")
    if not os.path.isfile(job_path):
        return jsonify({'error': 'Job no encontrado'}), 404
    
    try:
        with open(job_path, 'r', encoding='utf-8') as f:
            job = json.load(f)
        
        new_lines = []
        if jobid in job_queues:
            try:
                while True:
                    line = job_queues[jobid].get_nowait()
                    new_lines.append(line)
            except queue.Empty:
                pass
        
        return jsonify({
            'status': job.get('status', 'unknown'),
            'output': job.get('result', {}).get('output', ''),
            'new_lines': new_lines,
            'is_running': jobid in running_jobs
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/stop_job/<jobid>', methods=['POST'])
@login_required
def stop_job(jobid):
    if not validate_csrf(request.form.get('csrf_token')):
        return jsonify({'error': 'CSRF inválido'}), 403
    
    if jobid not in running_jobs:
        return jsonify({'error': 'Job no está corriendo'}), 400
    
    try:
        process = running_jobs[jobid]
        if platform.system() == 'Windows':
            process.terminate()
        else:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        
        time.sleep(1)
        
        if process.poll() is None:
            process.kill()
        
        job_path = os.path.join(JOBS_DIR, f"{jobid}.json")
        with open(job_path, 'r', encoding='utf-8') as f:
            job = json.load(f)
        
        job['status'] = 'stopped'
        job['result']['output'] += '\n\n[DETENIDO POR EL USUARIO]'
        
        with open(job_path, 'w', encoding='utf-8') as f:
            json.dump(job, f, indent=2)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Iniciando Kitty Tools Web Interface...")
    print(f"📂 Directorio de jobs: {JOBS_DIR}")
    print(f"👤 Usuario admin: {ADMIN_USER}")
    print("🌐 Servidor disponible en: https://localhost:5000")
    print("⚠️  Credenciales por defecto: admin/admin (¡cámbielas en producción!)")
    
    # Para GitHub Codespaces, usar el puerto forwarding correctamente con SSL
    port = int(os.environ.get('PORT', 5000))
    
    # Verificar si existen certificados SSL
    cert_path = os.path.join(os.path.dirname(__file__), 'cert.pem')
    key_path = os.path.join(os.path.dirname(__file__), 'key.pem')
    
    if os.path.exists(cert_path) and os.path.exists(key_path):
        context = (cert_path, key_path)
        print("🔒 SSL habilitado")
        app.run(host='0.0.0.0', port=port, debug=True, threaded=True, ssl_context=context)
    else:
        print("⚠️  SSL no disponible, ejecutando en HTTP")
        app.run(host='0.0.0.0', port=port, debug=True, threaded=True)