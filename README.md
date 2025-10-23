# Kitty-Tools - v36.2
> Please go check out my other repositories. there might be something you like <3

<div align="left">

[![Version](https://img.shields.io/badge/Version-36.2-orange.svg)](https://github.com/CPScript/Kitty-Tools)
[![License](https://img.shields.io/badge/License-CC0_1.0-blue.svg)](https://github.com/CPScript/Kitty-Tools/blob/main/LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows_|_Linux_|_Web_|_Android_|_IOS_|_MACos_|_Mobile-orange.svg)](https://github.com/CPScript/Kitty-Tools)

</div>

## Overview

Kitty-Tools is a comprehensive suite of utilities designed for enhancing and analyzing Kahoot quiz interactions. The toolkit provides powerful features for educators, students, and quiz enthusiasts, enabling advanced quiz analysis, answer retrieval, and automated participation capabilities.

<div align="center">
 
  ![Header Image](https://github.com/user-attachments/assets/329567e9-2de0-4cf8-92be-86b525365514)

</div>

## ✨ Key Features

- **Answer Retrieval System** - Obtain answers for any Kahoot quiz using Quiz ID or Game PIN
- **Multi-bot Participation** - Create multiple automated quiz participants with configurable behaviors **NOTE; YOU CAN NOT USE THIS OPTION IN GITHUB CODESPACE**
- **Cross-Platform Support** - Works on Windows, macOS, Linux, and Android (via Termux)
- **Modern GUI Interface** - Sleek, intuitive graphical user interface with dark theme
- **Export Functionality** - Save quiz answers in text format for future reference
- **Enhanced CLI Mode** - Full functionality available via command line for low-resource environments

<div align="center">
  <img src="https://github.com/user-attachments/assets/ab185a22-f7a3-41f5-a507-0cfcf6c453cd" width="80%" />
</div>

## 🚀 Installation Guide

### Prerequisites

- Python 3.6+ 
- Git 
- Node.js (for Flooder functionality)

### Installation by Platform

<details>
<summary><b>Windows</b></summary>

1. Install Python from [python.org/downloads](https://www.python.org/downloads/) (ensure "Add to PATH" is checked)
2. Install Git from [git-scm.com/download/win](https://git-scm.com/download/win)
3. Open Command Prompt and run:
   ```
   git clone https://github.com/CPScript/Kitty-Tools
   cd Kitty-Tools
   python main.py
   ```
</details>

<details>
<summary><b>Linux/macOS</b></summary>

1. Install required packages:
   ```bash
   # Ubuntu/Debian
   sudo apt install python3 python3-pip git
   
   # Fedora
   sudo dnf install python3 python3-pip git
   
   # macOS (with Homebrew)
   brew install python git
   ```

2. Clone and run:
   ```bash
   git clone https://github.com/CPScript/Kitty-Tools
   cd Kitty-Tools
   python3 main.py
   ```
</details>

<details>
<summary><b>Mobile</b></summary>

1. Install Termux by *F-Droid* **And** IOS using [iSH](https://ish.app/)
2. Install requirements:
   ```bash
   pkg install python git
   git clone https://github.com/CPScript/Kitty-Tools
   cd Kitty-Tools/LITE
   python lite.py
   ```
</details>

<details>
<summary><b>GitHub Codespace / Replit</b></summary>

#### Codespace
1. Create a new Codespace based on the repository
2. In the terminal, run:
   ```bash
   python main.py
   ```

#### Replit
1. Use this replit link
   ```bash
   https://replit.com/@Kitty-Tools/Kitty-Tools
   ```
</details>


## 📊 Usage Guide

Kitty-Tools now soporta tres modos principales:

### 1. CLI Mode (Terminal)

Interfaz textual mejorada, ideal para sistemas sin entorno gráfico.

Ejecuta:
```bash
python main.py --mode answers   # Modo respuestas Kahoot
python main.py --mode flood     # Modo flooder de bots
python main.py --mode graphical # Modo gráfico textual (no PyQt5)
```
Si ejecutas simplemente `python main.py`, aparecerá un menú interactivo en terminal.

### 2. Web Mode (Flask)

Interfaz web moderna y segura, con panel de control y login.

Desde la carpeta `webapp/` ejecuta:
```bash
cd webapp
python app.py
```
Luego abre [http://localhost:5000](http://localhost:5000) en tu navegador.

### 3. GUI Mode (PyQt5)

Interfaz gráfica real, moderna y futurista (requiere PyQt5 y entorno gráfico).

Ejecuta:
```bash
python main.py --mode pyqt
```
Si no tienes entorno gráfico (por ejemplo, en servidores o Codespaces), verás un error claro y seguro.

#### Notas sobre GUI (PyQt5):
- Si ves un error sobre `DISPLAY` o `PyQt5`, asegúrate de tener entorno gráfico y la librería instalada:
   ```bash
   pip install PyQt5
   ```
- El sistema intentará importar la GUI desde varias rutas y mostrará mensajes claros si hay problemas.

---

### Resumen de Modos

| Modo         | Comando                        | Requiere GUI | Notas                      |
|--------------|-------------------------------|--------------|----------------------------|
| CLI          | `python main.py --mode ...`   | No           | Menú textual, robusto      |
| Web (Flask)  | `python app.py` (en webapp/)  | No           | Navegador, login seguro    |
| GUI (PyQt5)  | `python main.py --mode pyqt`  | Sí           | Interfaz moderna, PyQt5    |

---

## 🖌️ Visual & UX Improvements

- Interfaz web y GUI con estilo futurista (glassmorphism, neon, responsive)
- Sin emojis de gatos ni botones innecesarios
- Panel de control y login integrados en la web
- CLI con salida formateada y símbolos auténticos Kahoot

## ⚠️ Troubleshooting

- **Falta PyQt5**: Instala con `pip install PyQt5`
- **No DISPLAY**: Solo puedes usar GUI en sistemas con entorno gráfico
- **Node.js requerido**: Para el flooder, instala Node.js si no está presente
- **Errores de dependencias**: El sistema intentará instalar `colorama` y `pystyle` automáticamente

## 🤝 Contributors

Ver sección original para lista completa de contribuyentes.

---

<p align="center">
   &copy; 2025 Kitty-Tools | All rights reserved
</p>

## 🔧 Advanced Configuration

Kitty-Tools supports various advanced configurations and custom settings:

- **Name Generation** - Generate random names or use custom prefixes
- **Anti-Detection Mode** - Implement techniques to avoid bot detection
- **Export Format Control** - Customize how answers are exported
- **Bot Behavior Patterns** - Configure response timing and answer selection

## ❓ Troubleshooting

**Common Issues:**

- **Module Not Found** - Run `pip install <module-name>` for any missing dependencies
- **Node.js Not Found** - Install Node.js for Flooder functionality
- **Game PIN Connection Fails** - Verify the PIN and ensure the Kahoot game is active
- **Performance Issues** - Use LITE version on low-resource systems

## 📜 Legal Disclaimer

Kitty-Tools is provided for **educational purposes only**. This software is designed to demonstrate educational platform vulnerabilities and to be used in controlled, ethical environments.

The developers do not endorse or encourage any use of this software that violates terms of service of educational platforms or disrupts educational activities. Use at your own risk and responsibility.

## 🤝 Contributors

A special thanks to all contributors who have helped make Kitty-Tools better:

- **@CPScript** - Lead Developer & Project Maintainer
- **@Ccode-lang** - Core Development & API Integration
- **@xTobyPlayZ** - Flooder Module Development
- **@cheepling** - Quality Assurance & Bug Reporting
- **@Zacky2613** - Technical Support & Issue Resolution
- **@KiraKenjiro** - Code Review & Optimization

## 📱 Mobile Support

For mobile devices, we provide Kitty-Tools LITE - a streamlined version designed specifically for Android via Termux:

```bash
cd Kitty-Tools/LITE
python lite.py
```

The LITE version offers core functionality with reduced resource requirements.

## 🌟 Star the Project

If you find Kitty-Tools useful, please consider giving it a star on GitHub to help others discover it!

---

<p align="center">
  &copy; 2025 Kitty-Tools | All rights reserved
</p>
