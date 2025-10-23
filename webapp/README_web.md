Kitty Tools - Interfaz web segura (solo lectura)\n\nEste pequeño proyecto expone una interfaz web que muestra información de `main.py` y del repositorio sin ejecutar las funcionalidades potencialmente dañinas (p. ej. flooders o herramientas para obtener respuestas).\n\nRequisitos:\n- Python 3.8+\n- Instalar dependencias: `pip install -r requirements.txt`\n\nEjecutar en desarrollo (desde `/webapp`):\n\n```bash
python app.py
```
\nLa app escuchará en http://0.0.0.0:5000 y es para uso local o en entornos de desarrollo solamente. No lo exponga a Internet sin medidas de seguridad adicionales (autenticación, HTTPS, etc.).
