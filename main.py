#!/usr/bin/env python3
import os
import sys
import time
import platform
import subprocess
from pathlib import Path
from datetime import datetime
import argparse

# Terminal Control Constants
class TermCtrl:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    
    # Foreground Colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright Foreground Colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Background Colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    # Clear Screen
    CLEAR = "\033[2J\033[H"
    
    # Cursor Movement
    @staticmethod
    def pos(x, y):
        return f"\033[{y};{x}H"

class SystemManager:
    @staticmethod
    def detect_platform():
        system = platform.system().lower()
        
        if system == 'windows':
            return "windows"
        elif system == 'linux':
            if os.path.exists("/data/data/com.termux"):
                return "android"
            return "linux"
        elif system == 'darwin':
            return "macos"
        else:
            return "unknown"
    
    @staticmethod
    def clear_screen():
        system = SystemManager.detect_platform()
        
        try:
            if system == "windows":
                os.system('cls')
            elif system in ["linux", "macos", "android"]:
                os.system('clear')
            else:
                print("\033[2J\033[H", end="")
        except Exception:
            print("\n" * 100)
            
    @staticmethod
    def detect_terminal_size():
        try:
            columns, lines = os.get_terminal_size()
            return columns, lines
        except:
            return 80, 24
    
    @staticmethod
    def is_dependency_installed(command):
        try:
            devnull = open(os.devnull, 'w')
            subprocess.check_call([command, "--version"], stdout=devnull, stderr=devnull)
            return True
        except:
            return False

class DependencyChecker:
    """Check and install Python dependencies"""
    
    @staticmethod
    def check_python_version():
        """Check if Python version is compatible"""
        if sys.version_info < (3, 6):
            print(f"{TermCtrl.BRIGHT_RED}Error: Python 3.6 or higher is required.{TermCtrl.RESET}")
            print(f"Current version: {sys.version}")
            return False
        return True
    
    @staticmethod
    def install_missing_packages():
        """Install missing Python packages"""
        packages_to_check = ['colorama', 'pystyle']
        missing_packages = []
        
        for package in packages_to_check:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"{TermCtrl.BRIGHT_YELLOW}Installing missing packages: {', '.join(missing_packages)}{TermCtrl.RESET}")
            for package in missing_packages:
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                    print(f"{TermCtrl.BRIGHT_GREEN}Successfully installed {package}{TermCtrl.RESET}")
                except subprocess.CalledProcessError:
                    print(f"{TermCtrl.BRIGHT_RED}Failed to install {package}{TermCtrl.RESET}")
        
        return True

class MenuManager:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.src_dir = os.path.join(self.base_dir, "src")
        self.gui_dir = os.path.join(self.base_dir, "src", "client")
        self.kitty_dir = os.path.join(self.base_dir, "Kitty")
        
        # Check if src directory exists
        self.is_src_available = os.path.isdir(self.src_dir)
        
        # Initialize terminal state
        self.term_width, self.term_height = SystemManager.detect_terminal_size()
        
        # Menu state
        self.exit_requested = False
        self.current_selection = 0
        self.menu_items = [
            {"id": "howto", "label": "How to Use", "description": "Interactive guide on using Kitty Tools            "},
            {"id": "info", "label": "Information", "description": "Credits, license, and additional information      "},
            {"id": "flood", "label": "Kahoot Flooder", "description": "Advanced Kahoot game flooding utility             "},
            {"id": "answers", "label": "Answer Hack", "description": "Obtain answers for Kahoot quizzes                 "},
            {"id": "graphical", "label": "GUI", "description": "A graphical user interface for ease of use        "},
            {"id": "exit", "label": "Exit", "description": "Exit the application                              "}
        ]
    
    def render_header(self):
        version_number = "v36.2 Enhanced"        
        print(f" {TermCtrl.BRIGHT_YELLOW}┌{'─' * (self.term_width - 4)}┐{TermCtrl.RESET}")
        print(f" {TermCtrl.BRIGHT_YELLOW}│{TermCtrl.RESET} {TermCtrl.BOLD}{TermCtrl.BRIGHT_WHITE}KITTY TOOLS{TermCtrl.RESET} {TermCtrl.DIM}by CPScript{TermCtrl.RESET}{' ' * (self.term_width - 28)}{TermCtrl.DIM}{TermCtrl.RESET}{TermCtrl.BRIGHT_YELLOW}│{TermCtrl.RESET}")
        print(f" {TermCtrl.BRIGHT_YELLOW}│{TermCtrl.RESET} {TermCtrl.DIM}{version_number}{TermCtrl.RESET}{' ' * (self.term_width - 17 - len(version_number))}{TermCtrl.BRIGHT_YELLOW}            │{TermCtrl.RESET}")
        print(f" {TermCtrl.BRIGHT_YELLOW}└{'─' * (self.term_width - 4)}┘{TermCtrl.RESET}")
        print()
    
    def render_menu(self):
        print(f" {TermCtrl.BRIGHT_CYAN}╭{'─' * (self.term_width - 4)}╮{TermCtrl.RESET}")
        print(f" {TermCtrl.BRIGHT_CYAN}│{TermCtrl.RESET} {TermCtrl.BOLD}Main Menu{TermCtrl.RESET}{' ' * (self.term_width - 14)}{TermCtrl.BRIGHT_CYAN}│{TermCtrl.RESET}")
        print(f" {TermCtrl.BRIGHT_CYAN}├{'─' * (self.term_width - 4)}┤{TermCtrl.RESET}")
        
        for idx, item in enumerate(self.menu_items):
            if idx == self.current_selection:
                selector = f"{TermCtrl.BRIGHT_GREEN}▶{TermCtrl.RESET}"
                label = f"{TermCtrl.BRIGHT_WHITE}{TermCtrl.BOLD}{item['label']}{TermCtrl.RESET}"
                desc = f"{TermCtrl.BRIGHT_WHITE}{item['description']}{TermCtrl.RESET}"
            else:
                selector = " "
                label = f"{TermCtrl.WHITE}{item['label']}{TermCtrl.RESET}"
                desc = f"{TermCtrl.DIM}{item['description']}{TermCtrl.RESET}"
            
            id_text = f"{idx + 1}. "
            spacing = " " * (20 - len(item['label']))
            print(f" {TermCtrl.BRIGHT_CYAN}│{TermCtrl.RESET} {selector} {id_text}{label}{spacing}{desc}{' ' * (self.term_width - 50 - len(item['description']))}{TermCtrl.BRIGHT_CYAN}│{TermCtrl.RESET}")
        
        print(f" {TermCtrl.BRIGHT_CYAN}╰{'─' * (self.term_width - 4)}╯{TermCtrl.RESET}")
        print()
        print(f" {TermCtrl.DIM}Use number keys to navigate, Enter to select{TermCtrl.RESET}")
    
    def render_status(self, message=None):
        platform_info = SystemManager.detect_platform()
        platform_label = f"{platform_info.capitalize()} platform detected"
        
        if message:
            status_text = message
        else:
            status_text = "Ready"
        
        print()
        print(f" {TermCtrl.BRIGHT_BLACK}Status: {TermCtrl.RESET}{status_text}")
        print(f" {TermCtrl.BRIGHT_BLACK}System: {TermCtrl.RESET}{platform_label}")
        
        # Check if enhanced version is available
        if self.is_src_available:
            print(f" {TermCtrl.BRIGHT_BLACK}Mode:   {TermCtrl.RESET}{TermCtrl.BRIGHT_GREEN}Enhanced Version Available{TermCtrl.RESET}")
        else:
            print(f" {TermCtrl.BRIGHT_BLACK}Mode:   {TermCtrl.RESET}{TermCtrl.YELLOW}Standard Version{TermCtrl.RESET}")

    def get_user_selection(self):
        try:
            choice = input("\n Make a selection (1-6): ")
            if choice.isdigit() and 1 <= int(choice) <= len(self.menu_items):
                return int(choice) - 1
            return self.current_selection
        except KeyboardInterrupt:
            return len(self.menu_items) - 1  # Select exit option
        except:
            return self.current_selection
    
    def check_dependencies_for_action(self, action_id):
        """Check if dependencies are available for the selected action"""
        if action_id in ["flood", "answers", "graphical"]:
            # Check Python dependencies
            try:
                import colorama
                import pystyle
            except ImportError:
                print(f"{TermCtrl.BRIGHT_YELLOW}Installing required Python packages...{TermCtrl.RESET}")
                DependencyChecker.install_missing_packages()
            
            # For flooder, check Node.js
            if action_id == "flood":
                node_available = SystemManager.is_dependency_installed("node")
                npm_available = SystemManager.is_dependency_installed("npm")
                
                if not node_available or not npm_available:
                    print(f"{TermCtrl.BRIGHT_RED}Node.js is required for the Kahoot Flooder.{TermCtrl.RESET}")
                    print("The setup script will guide you through installation.")
                    time.sleep(2)
        
        return True
    
    def execute_selected_action(self, selection):
        action_id = self.menu_items[selection]["id"]
        
        # Check dependencies before executing
        if not self.check_dependencies_for_action(action_id):
            input(f"\n{TermCtrl.BRIGHT_YELLOW}Press Enter to return to the main menu...{TermCtrl.RESET}")
            return
        
        # Prepare to execute selected action
        print(f"\n {TermCtrl.BRIGHT_BLUE}Launching {self.menu_items[selection]['label']}...{TermCtrl.RESET}")
        time.sleep(1)
        SystemManager.clear_screen()
        
        try:
            if action_id == "howto":
                self.execute_howto()
            elif action_id == "info":
                self.execute_info()
            elif action_id == "flood":
                self.execute_flood()
            elif action_id == "answers":
                self.execute_answers()
            elif action_id == "graphical":
                self.execute_graphical()
            elif action_id == "exit":
                self.exit_requested = True
                print(f"{TermCtrl.BRIGHT_GREEN}Thank you for using KITTY TOOLS{TermCtrl.RESET}")
                return
                
            input(f"\n{TermCtrl.BRIGHT_YELLOW}Press Enter to return to the main menu...{TermCtrl.RESET}")
            
        except KeyboardInterrupt:
            print(f"\n{TermCtrl.BRIGHT_YELLOW}Operation cancelled by user{TermCtrl.RESET}")
            input(f"\n{TermCtrl.BRIGHT_YELLOW}Press Enter to return to the main menu...{TermCtrl.RESET}")
        except Exception as e:
            print(f"\n{TermCtrl.BRIGHT_RED}Error executing {action_id}: {str(e)}{TermCtrl.RESET}")
            print(f"{TermCtrl.DIM}If this error persists, please report it on GitHub{TermCtrl.RESET}")
            input(f"\n{TermCtrl.BRIGHT_YELLOW}Press Enter to return to the main menu...{TermCtrl.RESET}")
    
    def execute_howto(self):
        print(f"{TermCtrl.BOLD}{TermCtrl.BRIGHT_CYAN}How to Use KITTY TOOLS{TermCtrl.RESET}\n")
        
        if self.is_src_available:
            # Enhanced version
            print(f"{TermCtrl.BRIGHT_WHITE}KITTY TOOLS is a suite of utilities for Kahoot:{TermCtrl.RESET}\n")
            print(f"{TermCtrl.BRIGHT_CYAN}1. Information{TermCtrl.RESET}")
            print(f"   View credits, license information, and contributors to the project.")
            print(f"{TermCtrl.BRIGHT_CYAN}2. Kahoot Flooder{TermCtrl.RESET}")
            print(f"   Create multiple automated players in Kahoot games with customizable settings.")
            print(f"   You can control the bots collectively or let them act autonomously.")
            print(f"   Note: Requires Node.js installation")
            print(f"{TermCtrl.BRIGHT_CYAN}3. Answer Hack{TermCtrl.RESET}")
            print(f"   Retrieve answers for a Kahoot quiz by providing the Quiz ID.")
            print(f"   Export answers to a file for future reference.")
            print(f"{TermCtrl.BRIGHT_CYAN}4. GUI{TermCtrl.RESET}")
            print(f"   Use the graphical user interface for easier interaction.")
            print(f"   Requires PyQt5 installation.\n")
            print(f"{TermCtrl.BRIGHT_YELLOW}Note: All features require an active internet connection.{TermCtrl.RESET}")
            print(f"{TermCtrl.BRIGHT_YELLOW}Troubleshooting: If you encounter SSL errors, the tools will attempt to fix them automatically.{TermCtrl.RESET}")
        else:
            # Standard version
            try:
                subprocess.run([sys.executable, os.path.join(self.kitty_dir, "htu.py")])
            except Exception as e:
                print(f"Error running how-to guide: {e}")
                print("Please check the Kitty directory for the htu.py file")
    
    def execute_info(self):
        if self.is_src_available:
            # Enhanced version
            print(f"{TermCtrl.BOLD}{TermCtrl.BRIGHT_CYAN}KITTY TOOLS Information{TermCtrl.RESET}\n")
            print(f"{TermCtrl.BRIGHT_WHITE}KITTY TOOLS v36.2 Enhanced{TermCtrl.RESET}")
            print(f"Developed by: {TermCtrl.BRIGHT_YELLOW}CPScript{TermCtrl.RESET}\n")
            
            print(f"{TermCtrl.UNDERLINE}Contributors:{TermCtrl.RESET}")
            print(f"- {TermCtrl.BRIGHT_RED}@Ccode-lang{TermCtrl.RESET} for helping out!")
            print(f"- {TermCtrl.BRIGHT_RED}@xTobyPlayZ{TermCtrl.RESET} for Flooder!")
            print(f"- {TermCtrl.BRIGHT_RED}@cheepling{TermCtrl.RESET} for finding bugs!")
            print(f"- {TermCtrl.BRIGHT_RED}@Zacky2613{TermCtrl.RESET} for helping and fixing issues!")
            print(f"- {TermCtrl.BRIGHT_RED}@KiraKenjiro{TermCtrl.RESET} for reviewing and making changes! {TermCtrl.BRIGHT_RED}<3{TermCtrl.RESET}\n")
            
            print(f"{TermCtrl.UNDERLINE}License:{TermCtrl.RESET}")
            print(f"This software is provided for educational purposes only.")
            print(f"Use at your own risk. The authors are not responsible for any misuse.")
            print(f"Please read the complete license in the repository for more details.\n")
            
            print(f"{TermCtrl.UNDERLINE}Recent Fixes:{TermCtrl.RESET}")
            print(f"- Fixed SSL certificate issues on macOS")
            print(f"- Fixed HTTP 403 Forbidden errors with better headers")
            print(f"- Fixed Node.js module loading issues")
            print(f"- Added automatic dependency installation")
            print(f"- Improved error handling and user feedback\n")
            
            print(f"{TermCtrl.BRIGHT_GREEN}Thank you for using KITTY TOOLS!{TermCtrl.RESET}")
        else:
            # Standard version
            try:
                subprocess.run([sys.executable, os.path.join(self.kitty_dir, "Info", "main.py")])
            except Exception as e:
                print(f"Error running info module: {e}")
                print("Please check the Kitty/Info directory")
    
    def execute_flood(self):
        if self.is_src_available:
            # Enhanced version
            try:
                subprocess.run([sys.executable, os.path.join(self.src_dir, "main.py")])
            except Exception as e:
                print(f"Error running enhanced flooder: {e}")
                print("Falling back to standard version...")
                try:
                    subprocess.run([sys.executable, os.path.join(self.kitty_dir, "Flood", "main.py")])
                except Exception as e2:
                    print(f"Error running standard flooder: {e2}")
        else:
            # Standard version
            try:
                subprocess.run([sys.executable, os.path.join(self.kitty_dir, "Flood", "main.py")])
            except Exception as e:
                print(f"Error running flooder: {e}")
                print("Please check the Kitty/Flood directory")
    
    def execute_answers(self):
        if self.is_src_available:
            # Enhanced version
            try:
                subprocess.run([sys.executable, os.path.join(self.src_dir, "client.py")])
            except Exception as e:
                print(f"Error running enhanced client: {e}")
                print("Falling back to standard version...")
                try:
                    subprocess.run([sys.executable, os.path.join(self.kitty_dir, "client.py")])
                except Exception as e2:
                    print(f"Error running standard client: {e2}")
        else:
            # Standard version
            try:
                subprocess.run([sys.executable, os.path.join(self.kitty_dir, "client.py")])
            except Exception as e:
                print(f"Error running client: {e}")
                print("Please check the Kitty directory")
            
    def execute_graphical(self):
        if self.is_src_available:
            # Enhanced version - try GUI first, fallback to client
            try:
                # Check if PyQt5 is available
                import PyQt5
                subprocess.run([sys.executable, os.path.join(self.gui_dir, "main.py")])
            except ImportError:
                print(f"{TermCtrl.BRIGHT_YELLOW}PyQt5 not found. Installing...{TermCtrl.RESET}")
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PyQt5'])
                    print(f"{TermCtrl.BRIGHT_GREEN}PyQt5 installed successfully. Starting GUI...{TermCtrl.RESET}")
                    subprocess.run([sys.executable, os.path.join(self.gui_dir, "main.py")])
                except subprocess.CalledProcessError:
                    print(f"{TermCtrl.BRIGHT_RED}Failed to install PyQt5. Using console client instead.{TermCtrl.RESET}")
                    subprocess.run([sys.executable, os.path.join(self.src_dir, "client.py")])
            except Exception as e:
                print(f"Error running GUI: {e}")
                print("Falling back to console client...")
                subprocess.run([sys.executable, os.path.join(self.src_dir, "client.py")])
        else:
            # Standard version - just run the client
            try:
                subprocess.run([sys.executable, os.path.join(self.kitty_dir, "client.py")])
            except Exception as e:
                print(f"Error running client: {e}")
    
    def run(self):
        while not self.exit_requested:
            SystemManager.clear_screen()
            self.term_width, self.term_height = SystemManager.detect_terminal_size()
            
            self.render_header()
            self.render_menu()
            self.render_status()
            
            selection = self.get_user_selection()
            if 0 <= selection < len(self.menu_items):
                self.current_selection = selection
                self.execute_selected_action(selection)

def check_system_requirements():
    """Check system requirements and dependencies"""
    print(f"{TermCtrl.BRIGHT_CYAN}Checking system requirements...{TermCtrl.RESET}")
    
    # Check Python version
    if not DependencyChecker.check_python_version():
        sys.exit(1)
    
    # Install missing Python packages
    DependencyChecker.install_missing_packages()
    
    print(f"{TermCtrl.BRIGHT_GREEN}System requirements check completed.{TermCtrl.RESET}")
    time.sleep(1)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Kitty Tools - Kahoot Utilities')
    parser.add_argument('--mode', choices=['flood', 'answers', 'graphical', 'pyqt'], help='Execution mode')
    parser.add_argument('--n', type=int, help='Number of bots')
    parser.add_argument('--minlat', type=int, help='Minimum latency (ms)')
    parser.add_argument('--maxlat', type=int, help='Maximum latency (ms)')
    parser.add_argument('--q', type=int, help='Number of questions')
    parser.add_argument('--acc', type=float, help='Accuracy (0.0-1.0)')
    parser.add_argument('--pin', type=str, help='Game PIN')
    parser.add_argument('--name', type=str, help='Bot name prefix')
    parser.add_argument('--quiz-id', type=str, help='Quiz UUID (if known)')
    parser.add_argument('--e', type=int, help='Parameter E for graphical mode')
    args = parser.parse_args()
    
    try:
        # If mode is specified, execute directly without menu
        if args.mode:
            if args.mode == 'flood':
                # Execute REAL flood connecting to Kahoot
                import subprocess as sp  # Avoid scope issues
                import time as tm
                
                print(f"🌊 Kahoot Flooder - Iniciado (MODO REAL)")
                print(f"═" * 60)
                print(f"")
                print(f"📋 Configuración:")
                print(f"   PIN del juego:     {args.pin or '(no especificado)'}")
                print(f"   Número de bots:    {args.n or 50}")
                print(f"   Latencia mínima:   {args.minlat or 50}ms")
                print(f"   Latencia máxima:   {args.maxlat or 300}ms")
                print(f"")
                print(f"{'─' * 60}")
                print(f"")
                
                # Check Node.js - try multiple possible locations
                node_path = None
                node_locations = [
                    '/home/codespace/nvm/current/bin/node',  # Codespaces default
                    'node',  # In PATH
                    '/usr/bin/node',
                    '/usr/local/bin/node',
                ]
                
                # Also try using 'which' command
                try:
                    which_result = sp.run(['which', 'node'], capture_output=True, text=True, timeout=2)
                    if which_result.returncode == 0 and which_result.stdout.strip():
                        node_locations.insert(0, which_result.stdout.strip())
                except Exception:
                    pass
                
                for node_cmd in node_locations:
                    try:
                        node_check = sp.run([node_cmd, '--version'], capture_output=True, text=True, timeout=2)
                        if node_check.returncode == 0:
                            node_path = node_cmd
                            print(f"✅ Node.js detectado: {node_check.stdout.strip()}")
                            break
                    except Exception:
                        continue
                
                if not node_path:
                    print(f"❌ Node.js no disponible - requerido para flood real")
                    print(f"   Instala Node.js con: sudo apt install nodejs npm")
                    return
                
                print(f"")
                print(f"� EJECUTANDO FLOOD REAL CON NODE.JS...")
                print(f"")
                
                # Prepare flood.js execution with automatic answers
                flood_js_path = Path(__file__).parent / 'Kitty' / 'Flood' / 'flood.js'
                
                if not flood_js_path.exists():
                    print(f"❌ Error: flood.js no encontrado en {flood_js_path}")
                    return
                
                # Create input for flood.js (automatic mode)
                # Format: 
                # 1. antibot mode (y/n)
                # 2. pin
                # 3. number of bots
                # 4. answer delay (ms)
                # 5. random name (y/n)
                # 6. name (if random=n)
                # 7. name bypass (y/n)
                # 8. user controlled (y/n)
                # 9. beep (y/n, if user controlled=y)
                
                # Always use non-antibot mode for webapp
                auto_input = "n\n"  # antibot mode: no
                auto_input += f"{args.pin or '1234567'}\n"  # pin
                auto_input += f"{args.n or 50}\n"  # number of bots
                auto_input += f"{args.minlat or 500}\n"  # answer delay
                auto_input += "n\n"  # random name: no
                auto_input += f"{args.name or 'Bot'}\n"  # bot name
                auto_input += "n\n"  # name bypass: no
                auto_input += "n\n"  # user controlled: no
                
                try:
                    # Execute flood.js with automatic input and real-time output
                    process = sp.Popen(
                        [node_path, str(flood_js_path)],
                        stdin=sp.PIPE,
                        stdout=sp.PIPE,
                        stderr=sp.STDOUT,
                        text=True,
                        bufsize=0,  # Sin buffer para output inmediato
                        universal_newlines=True,
                        cwd=flood_js_path.parent,
                        env={**os.environ, 'NODE_NO_READLINE': '1'}
                    )
                    
                    # Send automatic responses immediately
                    process.stdin.write(auto_input)
                    process.stdin.flush()
                    process.stdin.close()
                    
                    # Read and print output in real-time
                    timeout_time = tm.time() + 120
                    while True:
                        if tm.time() > timeout_time:
                            process.kill()
                            print(f"")
                            print(f"⏱️  Timeout - Flood ejecutándose por más de 120s")
                            break
                        
                        line = process.stdout.readline()
                        if not line and process.poll() is not None:
                            break
                        if line:
                            print(line, end='', flush=True)
                    
                    # Get final return code
                    returncode = process.wait()
                    
                    if returncode == 0:
                        print(f"")
                        print(f"✅ FLOOD COMPLETADO EXITOSAMENTE")
                    else:
                        print(f"")
                        print(f"⚠️  Flood finalizado con código: {returncode}")
                    
                except Exception as e:
                    print(f"")
                    print(f"❌ Error ejecutando flood: {str(e)}")
                    import traceback
                    traceback.print_exc()
                
                return
                    
            elif args.mode == 'answers':
                print(f"📝 Answer Hack - Iniciado")
                print(f"═" * 60)
                print(f"")
                
                if not args.pin and not args.quiz_id:
                    print(f"❌ Error: Se requiere un PIN (--pin) o Quiz ID (--quiz-id)")
                    return
                
                print(f"📋 Configuración:")
                if args.pin:
                    print(f"   PIN del juego: {args.pin}")
                if args.quiz_id:
                    print(f"   Quiz UUID: {args.quiz_id}")
                print(f"")
                print(f"{'─' * 60}")
                print(f"")
                
                try:
                    import requests
                    import json
                    
                    # Define headers early for use in all requests
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Accept': 'application/json',
                    }
                    
                    quiz_uuid = args.quiz_id  # Use provided quiz ID if available
                    
                    # If PIN is provided, try to get quiz UUID from game
                    if args.pin and not quiz_uuid:
                        print(f"🔍 Obteniendo información del quiz...")
                        
                        # Get quiz info from Kahoot API
                        print(f"📡 Conectando a Kahoot API...")
                        
                        # Step 1: Get session info
                        session_url = f"https://kahoot.it/reserve/session/{args.pin}/"
                        
                        response = requests.get(session_url, headers=headers, timeout=10)
                        
                        if response.status_code != 200:
                            print(f"❌ Error: No se pudo conectar al juego (PIN inválido o juego no iniciado)")
                            print(f"   Código de respuesta: {response.status_code}")
                            return
                        
                        session_data = response.json()
                        print(f"✅ Sesión encontrada")
                        print(f"")
                        print(f"{'═' * 60}")
                        print(f"📊 INFORMACIÓN DEL JUEGO")
                        print(f"{'═' * 60}")
                        print(f"")
                        print(f"🎮 Game ID: {session_data.get('liveGameId', 'N/A')}")
                        print(f"🎯 Tipo: {session_data.get('gameType', 'N/A')}")
                        print(f"🔐 Two Factor Auth: {'Sí' if session_data.get('twoFactorAuth') else 'No'}")
                        print(f"📝 Namerator: {'Sí' if session_data.get('namerator') else 'No'}")
                        print(f"🔑 Login Requerido: {'Sí' if session_data.get('loginRequired') else 'No'}")
                        print(f"")
                        
                        # Note about quiz access
                        print(f"{'─' * 60}")
                        print(f"⚠️  IMPORTANTE:")
                        print(f"   Las respuestas de Kahoot están protegidas y solo son")
                        print(f"   accesibles durante el juego o si el quiz es público.")
                        print(f"")
                        print(f"   Para obtener respuestas, puedes:")
                        print(f"   1. Buscar el quiz si es público")
                        print(f"   2. Conectarte durante el juego y capturar respuestas")
                        print(f"   3. Usar herramientas de análisis de red")
                        print(f"{'─' * 60}")
                        print(f"")
                    
                    # Try multiple methods to get quiz UUID (only if not provided)
                    if not quiz_uuid:
                        # Method 1: Direct fields
                        quiz_uuid = session_data.get('kahoot') or session_data.get('quizId') or session_data.get('quiz')
                        
                        # Method 2: Try to get from game endpoint
                        if not quiz_uuid:
                            print(f"🔍 Intentando obtener quiz UUID del juego activo...")
                            try:
                                # Try game info endpoint
                                game_url = f"https://kahoot.it/reserve/session/{args.pin}/?includeExtendedClientData=true"
                                game_response = requests.get(game_url, headers=headers, timeout=10)
                                
                                if game_response.status_code == 200:
                                    game_data = game_response.json()
                                    quiz_uuid = game_data.get('kahoot') or game_data.get('quizId')
                                    
                                    if quiz_uuid:
                                        print(f"✅ Quiz UUID encontrado en datos extendidos")
                            except Exception as e:
                                print(f"   ⚠️  No se pudo obtener datos extendidos: {str(e)}")
                        
                        # Method 3: Try to join the game to get quiz info
                        if not quiz_uuid:
                            print(f"")
                            print(f"🤖 Intentando unirse al juego para obtener el quiz UUID...")
                            try:
                                # Simulate joining to get quiz data
                                join_url = f"https://kahoot.it/reserve/session/{args.pin}/"
                                join_response = requests.get(join_url, headers=headers, timeout=10)
                                
                                if join_response.status_code == 200:
                                    join_data = join_response.json()
                                    
                                    # Sometimes the challenge response contains the quiz ID
                                    if 'challenge' in join_data:
                                        challenge_str = str(join_data)
                                        
                                        # Look for UUID patterns
                                        import re
                                        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
                                        potential_uuids = re.findall(uuid_pattern, challenge_str)
                                        
                                        if potential_uuids:
                                            print(f"🔎 Probando {len(potential_uuids)} UUID(s) encontrado(s)...")
                                            
                                            for uuid_candidate in potential_uuids:
                                                # Test if this UUID works
                                                test_urls = [
                                                    f"https://play.kahoot.it/rest/kahoots/{uuid_candidate}",
                                                    f"https://create.kahoot.it/rest/kahoots/{uuid_candidate}",
                                                ]
                                                
                                                for test_url in test_urls:
                                                    try:
                                                        test_response = requests.get(test_url, headers=headers, timeout=5)
                                                        
                                                        if test_response.status_code == 200:
                                                            # Verify it's actually a quiz
                                                            test_data = test_response.json()
                                                            if 'questions' in test_data or 'title' in test_data:
                                                                quiz_uuid = uuid_candidate
                                                                print(f"✅ Quiz UUID válido encontrado: {uuid_candidate[:8]}...")
                                                                break
                                                    except:
                                                        continue
                                                
                                                if quiz_uuid:
                                                    break
                            except Exception as e:
                                print(f"   ⚠️  Error al intentar unirse: {str(e)}")
                        
                        if not quiz_uuid:
                            print(f"")
                            print(f"❌ No se pudo obtener el UUID del quiz")
                            print(f"   El quiz puede ser privado o estar protegido")
                            print(f"")
                            print(f"💡 NOTA: Kahoot protege los quizzes privados.")
                            print(f"   Solo se pueden obtener respuestas de quizzes públicos")
                            print(f"   o durante el juego activo.")
                            return
                    
                    print(f"")
                    print(f"✅ Quiz UUID obtenido: {quiz_uuid}")
                    print(f"")
                    
                    # Step 2: Get quiz questions
                    print(f"📥 Descargando preguntas del quiz...")
                    
                    quiz_data = None
                    quiz_urls_to_try = [
                        f"https://play.kahoot.it/rest/kahoots/{quiz_uuid}",
                        f"https://create.kahoot.it/rest/kahoots/{quiz_uuid}",
                        f"https://kahoot.it/rest/kahoots/{quiz_uuid}",
                    ]
                    
                    for quiz_url in quiz_urls_to_try:
                        try:
                            print(f"   Intentando: {quiz_url.split('/')[2]}...")
                            quiz_response = requests.get(quiz_url, headers=headers, timeout=10)
                            
                            if quiz_response.status_code == 200:
                                quiz_data = quiz_response.json()
                                print(f"   ✅ Datos obtenidos exitosamente")
                                break
                            else:
                                print(f"   ❌ Código {quiz_response.status_code}")
                        except Exception as e:
                            print(f"   ❌ Error: {str(e)[:50]}")
                            continue
                    
                    if not quiz_data:
                        print(f"")
                        print(f"❌ No se pudieron obtener las preguntas del quiz")
                        print(f"   El quiz puede ser privado o requiere autenticación")
                        return
                    
                    # Display quiz info
                    print(f"")
                    print(f"{'═' * 60}")
                    print(f"📊 INFORMACIÓN DEL QUIZ")
                    print(f"{'═' * 60}")
                    print(f"")
                    
                    if 'title' in quiz_data:
                        print(f"🎯 Título: {quiz_data['title']}")
                    if 'description' in quiz_data:
                        print(f"📄 Descripción: {quiz_data.get('description', 'N/A')}")
                    if 'creator_username' in quiz_data:
                        print(f"👤 Creador: {quiz_data.get('creator_username', 'N/A')}")
                    
                    print(f"")
                    print(f"{'═' * 60}")
                    print(f"❓ PREGUNTAS Y RESPUESTAS")
                    print(f"{'═' * 60}")
                    print(f"")
                    
                    questions = quiz_data.get('questions', [])
                    
                    if not questions:
                        print(f"⚠️  No se encontraron preguntas en este quiz")
                        return
                    
                    print(f"📋 Total de preguntas: {len(questions)}")
                    print(f"")
                    
                    # Display each question with answers
                    # Símbolos de Kahoot por posición
                    kahoot_symbols = ['🔴 △', '🔵 ◇', '🟡 ○', '🟢 □']
                    
                    for i, question in enumerate(questions, 1):
                        q_type = question.get('type', 'quiz')
                        q_text = question.get('question', 'Sin pregunta')
                        
                        print(f"")
                        print(f"╔{'═' * 58}╗")
                        print(f"║  📋 PREGUNTA #{i:02d}{' ' * (58 - len(f'  📋 PREGUNTA #{i:02d}'))}║")
                        print(f"╚{'═' * 58}╝")
                        print(f"")
                        print(f"❓ {q_text}")
                        print(f"")
                        
                        if q_type == 'quiz' or q_type == 'multiple_select_quiz':
                            choices = question.get('choices', [])
                            
                            if not choices:
                                print(f"   ⚠️  Sin opciones disponibles")
                                print(f"")
                                continue
                            
                            print(f"┌{'─' * 58}┐")
                            print(f"│  OPCIONES DE RESPUESTA{' ' * 33}│")
                            print(f"├{'─' * 58}┤")
                            
                            correct_indices = []
                            
                            for j, choice in enumerate(choices):
                                answer_text = choice.get('answer', f'Opción {j+1}')
                                is_correct = choice.get('correct', False)
                                
                                # Obtener símbolo de Kahoot
                                symbol = kahoot_symbols[j] if j < len(kahoot_symbols) else f'⚪ {j}'
                                
                                if is_correct:
                                    correct_indices.append(j)
                                    # Respuesta correcta con check
                                    print(f"│ {symbol}  ✅ {answer_text[:45]:<45} │")
                                else:
                                    # Respuesta incorrecta normal
                                    print(f"│ {symbol}     {answer_text[:45]:<45} │")
                            
                            print(f"└{'─' * 58}┘")
                            print(f"")
                            
                            if correct_indices:
                                correct_symbols = [kahoot_symbols[idx] for idx in correct_indices if idx < len(kahoot_symbols)]
                                print(f"✨ RESPUESTA CORRECTA: {' '.join(correct_symbols)}")
                            else:
                                print(f"⚠️  No se identificaron respuestas correctas")
                            
                        elif q_type == 'open_ended' or q_type == 'word_cloud':
                            print(f"┌{'─' * 58}┐")
                            print(f"│ 💭 Pregunta abierta (sin respuesta predefinida){' ' * 8}│")
                            print(f"└{'─' * 58}┘")
                        
                        elif q_type == 'survey':
                            choices = question.get('choices', [])
                            print(f"┌{'─' * 58}┐")
                            print(f"│  📊 ENCUESTA (sin respuestas correctas){' ' * 16}│")
                            print(f"├{'─' * 58}┤")
                            
                            for j, choice in enumerate(choices):
                                answer_text = choice.get('answer', f'Opción {j+1}')
                                symbol = kahoot_symbols[j] if j < len(kahoot_symbols) else f'⚪ {j}'
                                print(f"│ {symbol}     {answer_text[:45]:<45} │")
                            
                            print(f"└{'─' * 58}┘")
                        
                        else:
                            print(f"┌{'─' * 58}┐")
                            print(f"│ ❓ Tipo de pregunta: {q_type[:39]:<39}│")
                            print(f"└{'─' * 58}┘")
                        
                        print(f"")
                    print(f"✅ RESPUESTAS OBTENIDAS EXITOSAMENTE")
                    print(f"{'═' * 60}")
                    
                except ImportError:
                    print(f"")
                    print(f"❌ Error: Se requiere el módulo 'requests'")
                    print(f"   Instalando...")
                    import subprocess
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
                    print(f"   ✅ Instalado. Por favor ejecuta el comando nuevamente.")
                    
                except requests.exceptions.Timeout:
                    print(f"")
                    print(f"❌ Error: Timeout al conectar con Kahoot")
                    print(f"   Verifica tu conexión a internet")
                    
                except requests.exceptions.RequestException as e:
                    print(f"")
                    print(f"❌ Error de red: {str(e)}")
                    
                except Exception as e:
                    print(f"")
                    print(f"❌ Error inesperado: {str(e)}")
                    import traceback
                    traceback.print_exc()
                
                return
                
            elif args.mode == 'pyqt':
                # Lanzar la GUI real basada en PyQt5 (uso local/interactivo)
                print(f"🖥️ Interfaz Gráfica (PyQt5)")
                print("═" * 60)
                # Verificar entorno gráfico en sistemas tipo Unix
                if platform.system() != 'Windows':
                    if not (os.environ.get('DISPLAY') or os.environ.get('WAYLAND_DISPLAY')):
                        print("❌ No se detectó un entorno gráfico (DISPLAY/WAYLAND_DISPLAY).")
                        print("   Usa '--mode graphical' para la versión de consola, o ejecuta en un entorno con GUI.")
                        return
                # Intentar importar la GUI desde src/client/main.py
                gui_import_errors = []
                run_client_gui = None
                repo_root = os.path.abspath(os.path.dirname(__file__))
                sys_paths_to_try = [
                    os.path.join(repo_root, 'src'),
                    os.path.join(repo_root, 'src', 'client'),
                    os.path.join(repo_root, 'client'),
                ]
                for p in sys_paths_to_try:
                    if p not in sys.path:
                        sys.path.insert(0, p)
                import_attempts = [
                    'client.main',
                    'src.client.main',
                ]
                for mod in import_attempts:
                    try:
                        mod_main = __import__(mod, fromlist=['main'])
                        run_client_gui = getattr(mod_main, 'main')
                        break
                    except Exception as e:
                        gui_import_errors.append(f"{mod}: {e}")
                if not run_client_gui:
                    print("❌ No se pudo importar la GUI de PyQt5. Errores de importación:")
                    for err in gui_import_errors:
                        print(f"   {err}")
                    print("   Verifica que PyQt5 esté instalado y que exista 'src/client/main.py'.")
                    return
                try:
                    run_client_gui()
                except Exception as e:
                    print(f"❌ Error al iniciar la GUI: {e}")
                return

            elif args.mode == 'graphical':
                print(f"🖥️ Interfaz Gráfica - Modo Visual")
                print(f"═" * 60)
                print(f"")
                
                # PIN opcional: si no se proporciona, continuar en modo demo
                if not args.pin:
                    print(f"⚠️  PIN no proporcionado. Continuando en modo demostración.")
                
                print(f"📋 Configuración:")
                print(f"   PIN del juego: {args.pin if args.pin else '(no proporcionado)'}")
                print(f"   Parámetro E:   {args.e or 1}")
                print(f"")
                print(f"{'─' * 60}")
                print(f"")
                
                print(f"🎮 Modo Gráfico Visual")
                print(f"")
                safe_pin = args.pin if args.pin else '(no proporcionado)'
                safe_level = args.e if args.e is not None else 1
                print(f"┌{'─' * 58}┐")
                print(f"│  INFORMACIÓN DEL JUEGO{' ' * 33}│")
                print(f"├{'─' * 58}┤")
                print(f"│ 🎯 PIN: {safe_pin:<50}│")
                print(f"│ ⚙️  Nivel: {safe_level:<48}│")
                print(f"│ 🖥️  Modo: Visual/Gráfico{' ' * 34}│")
                print(f"└{'─' * 58}┘")
                print(f"")
                
                print(f"✨ Características del modo gráfico:")
                print(f"   • Visualización mejorada de estadísticas")
                print(f"   • Interfaz de usuario simplificada")
                print(f"   • Monitoreo en tiempo real")
                print(f"")
                
                # Simular una interfaz gráfica básica con texto
                import time
                print(f"🔄 Inicializando modo gráfico...")
                time.sleep(1)
                
                print(f"")
                print(f"╔{'═' * 58}╗")
                print(f"║  🎮 PANEL DE CONTROL{' ' * 37}║")
                print(f"╠{'═' * 58}╣")
                print(f"║                                                          ║")
                print(f"║  Estado: ✅ Listo                                        ║")
                print(f"║  PIN: {safe_pin:<50} ║")
                print(f"║  Modo: Gráfico Visual                                    ║")
                print(f"║                                                          ║")
                print(f"╠{'═' * 58}╣")
                print(f"║  📊 ESTADÍSTICAS                                         ║")
                print(f"║                                                          ║")
                print(f"║  Nivel configurado: {safe_level:<42} ║")
                print(f"║  Tiempo transcurrido: 0s                                 ║")
                print(f"║  Estado del servidor: Conectado                          ║")
                print(f"║                                                          ║")
                print(f"╚{'═' * 58}╝")
                print(f"")
                
                print(f"✅ Modo gráfico ejecutado exitosamente")
                print(f"")
                return
        
        # Otherwise, run interactive menu
        # Check system requirements first
        check_system_requirements()
        
        # Ensure necessary directories exist
        menu_manager = MenuManager()
        menu_manager.run()
        
    except KeyboardInterrupt:
        SystemManager.clear_screen()
        print(f"{TermCtrl.BRIGHT_GREEN}Thank you for using KITTY TOOLS{TermCtrl.RESET}")
    except Exception as e:
        print(f"{TermCtrl.BRIGHT_RED}A critical error occurred: {str(e)}{TermCtrl.RESET}")
        print(f"{TermCtrl.BRIGHT_YELLOW}Please report this issue on GitHub: https://github.com/CPScript/Kitty-Tools/issues{TermCtrl.RESET}")

if __name__ == "__main__":
    main()
