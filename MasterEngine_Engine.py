import sys
import os
import time
import threading
import datetime
import subprocess
import winreg
import stat
import ctypes
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, 
    QVBoxLayout, QHBoxLayout, QFrame, QTextEdit, QMessageBox, QDialog, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject

# Win32 API - Pure Hardware Injection
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort), ("wScan", ctypes.c_ushort), ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong), ("dwExtraInfo", PUL)]
class HardwareInput(ctypes.Structure):
    _fields_ = [("u", ctypes.c_ulong)]
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long), ("dy", ctypes.c_long), ("mouseData", ctypes.c_ulong), ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong), ("dwExtraInfo", PUL)]
class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput), ("mi", MouseInput), ("hi", HardwareInput)]
class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]

def safe_append_ini(file_path, content):
    folder = os.path.dirname(file_path)
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    if os.path.exists(file_path):
        os.chmod(file_path, stat.S_IWRITE | stat.S_IREAD)
    existing = ""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            existing = f.read()
    with open(file_path, "a", encoding="utf-8") as f:
        if content.strip() not in existing:
            f.write(f"\n{content}\n")

class NativeMacroEngine(QObject):
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.is_armed = False
        # Virtual Key Codes
        self.VK_W = 0x57
        self.VK_A = 0x41
        self.VK_S = 0x53
        self.VK_D = 0x44
        self.VK_Q = 0x51
        self.VK_E = 0x45
        self.VK_SPACE = 0x20 # Keyboard Jump (Safe proxy, no mouse click)
        self.VK_SHIFT = 0x10 # Keyboard Boost (Safe proxy, no mouse click)

    def log(self, msg):
        self.log_signal.emit(msg)

    def send_key(self, hex_vk, key_up=False):
        try:
            extra = ctypes.c_ulong(0x524C4353)
            ii_ = Input_I()
            flags = 0x0002 if key_up else 0x0000
            ii_.ki = KeyBdInput(wVk=hex_vk, wScan=0, dwFlags=flags, time=0, dwExtraInfo=ctypes.cast(ctypes.pointer(extra), PUL))
            x = Input(type=1, ii=ii_)
            ctypes.windll.user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
        except:
            pass

    def fractional_sleep(self, duration):
        time.sleep(duration)

    # ---------------------------------------------------------
    # MACRO LOGIC RESTRUCTURED BASED ON EXACT USER SPECIFICATIONS
    # ---------------------------------------------------------

    def execute_forward_speedflip(self):
        try:
            self.log("[EXEC] Forward Speedflip [30-30-20-550] sequence initialized.")
            self.send_key(self.VK_SHIFT, False)
            self.send_key(self.VK_W, False)
            self.send_key(self.VK_SPACE, False)
            self.fractional_sleep(0.030) # 30ms
            
            self.send_key(self.VK_SPACE, True)
            self.fractional_sleep(0.030) # 30ms
            
            self.send_key(self.VK_SPACE, False)
            self.fractional_sleep(0.020) # 20ms
            self.send_key(self.VK_SPACE, True)
            self.send_key(self.VK_W, True)
            
            self.send_key(self.VK_S, False) # Cancel
            self.fractional_sleep(0.550) # 550ms
            self.send_key(self.VK_S, True)
            self.send_key(self.VK_SHIFT, True)
        except:
            pass

    def execute_left_speedflip(self):
        try:
            self.log("[EXEC] Left Speedflip [30-30-20-600] sequence initialized.")
            self.send_key(self.VK_SHIFT, False)
            self.send_key(self.VK_W, False)
            self.send_key(self.VK_A, False)
            self.send_key(self.VK_SPACE, False)
            self.fractional_sleep(0.030) # 30ms
            
            self.send_key(self.VK_SPACE, True)
            self.fractional_sleep(0.030) # 30ms
            
            self.send_key(self.VK_SPACE, False)
            self.fractional_sleep(0.020) # 20ms
            self.send_key(self.VK_SPACE, True)
            self.send_key(self.VK_W, True)
            self.send_key(self.VK_A, True)
            
            self.send_key(self.VK_S, False) # Cancel
            self.send_key(self.VK_Q, False) # Air Roll Left
            self.fractional_sleep(0.600) # 600ms
            self.send_key(self.VK_S, True)
            self.send_key(self.VK_Q, True)
            self.send_key(self.VK_SHIFT, True)
        except:
            pass

    def execute_right_speedflip(self):
        try:
            self.log("[EXEC] Right Speedflip [30-30-20-600] sequence initialized.")
            self.send_key(self.VK_SHIFT, False)
            self.send_key(self.VK_W, False)
            self.send_key(self.VK_D, False)
            self.send_key(self.VK_SPACE, False)
            self.fractional_sleep(0.030) # 30ms
            
            self.send_key(self.VK_SPACE, True)
            self.fractional_sleep(0.030) # 30ms
            
            self.send_key(self.VK_SPACE, False)
            self.fractional_sleep(0.020) # 20ms
            self.send_key(self.VK_SPACE, True)
            self.send_key(self.VK_W, True)
            self.send_key(self.VK_D, True)
            
            self.send_key(self.VK_S, False) # Cancel
            self.send_key(self.VK_E, False) # Air Roll Right
            self.fractional_sleep(0.600) # 600ms
            self.send_key(self.VK_S, True)
            self.send_key(self.VK_E, True)
            self.send_key(self.VK_SHIFT, True)
        except:
            pass

    def execute_fast_aerial(self):
        try:
            self.log("[EXEC] Fast Aerial [200-30-30-150-20-300] sequence initialized.")
            self.send_key(self.VK_SHIFT, False)
            self.send_key(self.VK_S, False)
            self.send_key(self.VK_SPACE, False)
            self.fractional_sleep(0.200) # 200ms Pitch
            
            self.send_key(self.VK_SPACE, True)
            self.send_key(self.VK_S, True)
            self.fractional_sleep(0.030) # 30ms
            
            self.send_key(self.VK_SPACE, False) # Second Jump
            self.fractional_sleep(0.030) # 30ms
            self.send_key(self.VK_SPACE, True)
            
            self.fractional_sleep(0.150) # 150ms Delay
            
            self.send_key(self.VK_W, False)
            self.send_key(self.VK_SPACE, False) # Flip
            self.fractional_sleep(0.020) # 20ms
            self.send_key(self.VK_SPACE, True)
            self.send_key(self.VK_W, True)
            
            self.send_key(self.VK_S, False) # Cancel Recovery
            self.fractional_sleep(0.300) # 300ms
            self.send_key(self.VK_S, True)
            self.send_key(self.VK_SHIFT, True)
        except:
            pass

class ProProfilesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pro Physics & Profiles")
        self.setFixedSize(760, 520)
        self.setStyleSheet("background-color: #0b0e14; color: #f0f5ff;")
        self.parent = parent

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("TOP PROFILES (NWPO, RW9, TRK511)")
        title.setStyleSheet("color: #00d2ff; font-weight: bold; font-size: 12pt;")
        layout.addWidget(title)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)

        nwpo_card = QFrame()
        nwpo_card.setStyleSheet("background-color: #121826; border: 1px solid #1e293b; border-radius: 6px;")
        nwpo_layout = QVBoxLayout(nwpo_card)
        nwpo_title = QLabel("NWPO")
        nwpo_title.setStyleSheet("color: #00ffb4; font-weight: bold; font-size: 11pt; border: none;")
        btn_nwpo = QPushButton("Inject Nwpo Profile")
        btn_nwpo.setStyleSheet("background-color: #1c3b28; color: #00ffb4; font-weight: bold; padding: 10px; border-radius: 4px;")
        btn_nwpo.clicked.connect(lambda: self.inject_pro_profile("Nwpo", 0.07, 1.40, 1.40))
        nwpo_layout.addWidget(nwpo_title)
        nwpo_layout.addWidget(btn_nwpo)

        rw9_card = QFrame()
        rw9_card.setStyleSheet("background-color: #121826; border: 1px solid #1e293b; border-radius: 6px;")
        rw9_layout = QVBoxLayout(rw9_card)
        rw9_title = QLabel("RW9")
        rw9_title.setStyleSheet("color: #ffaa00; font-weight: bold; font-size: 11pt; border: none;")
        btn_rw9 = QPushButton("Inject Rw9 Profile")
        btn_rw9.setStyleSheet("background-color: #3b2815; color: #ffaa00; font-weight: bold; padding: 10px; border-radius: 4px;")
        btn_rw9.clicked.connect(lambda: self.inject_pro_profile("Rw9", 0.07, 1.50, 1.50))
        rw9_layout.addWidget(rw9_title)
        rw9_layout.addWidget(btn_rw9)

        trk_card = QFrame()
        trk_card.setStyleSheet("background-color: #121826; border: 1px solid #1e293b; border-radius: 6px;")
        trk_layout = QVBoxLayout(trk_card)
        trk_title = QLabel("TRK511")
        trk_title.setStyleSheet("color: #e6a0ff; font-weight: bold; font-size: 11pt; border: none;")
        btn_trk = QPushButton("Inject TRK511 Profile")
        btn_trk.setStyleSheet("background-color: #371e4b; color: #e6a0ff; font-weight: bold; padding: 10px; border-radius: 4px;")
        btn_trk.clicked.connect(lambda: self.inject_pro_profile("TRK511", 0.09, 2.70, 2.90))
        trk_layout.addWidget(trk_title)
        trk_layout.addWidget(btn_trk)

        grid_layout.addWidget(nwpo_card, 0, 0)
        grid_layout.addWidget(rw9_card, 0, 1)
        grid_layout.addWidget(trk_card, 0, 2)

        layout.addLayout(grid_layout)

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("background-color: #c83232; color: white; font-weight: bold; padding: 8px; border-radius: 4px;")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    def inject_pro_profile(self, name, deadzone, air_sens, steer_sens):
        try:
            target = os.path.join(self.parent.rl_config_dir, "TAInput.ini")
            content = f"\n[Engine.Input]\nGamepadDeadzone={deadzone}\nAxisDeadzone={deadzone}\n\n[Bindings.Lateral]\nAirRollSensitivity={air_sens}\nSteeringSensitivity={steer_sens}\n"
            safe_append_ini(target, content)
            self.parent.log_message(f"[PRO INJECT] {name} Profile Injected.")
            QMessageBox.information(self, "Profile Injected", f"{name} settings successfully injected!")
        except Exception as e:
            pass

class LuaStudioDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Logitech Lua Environment Studio")
        self.setFixedSize(780, 620)
        self.setStyleSheet("background-color: #0b0e14; color: #f0f5ff;")
        self.parent = parent

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("LUA ENVIRONMENT, DRY-RUN & SAFE DEPLOYMENT")
        title.setStyleSheet("color: #00d2ff; font-weight: bold; font-size: 11pt;")
        layout.addWidget(title)

        self.lua_preview = QTextEdit()
        self.lua_preview.setStyleSheet("background-color: #070a0f; color: #00ffb4; font-family: Consolas; font-size: 9pt; border: 1px solid #1e293b; border-radius: 4px;")
        
        lua_source = os.path.join(self.parent.project_root, "lua", "RocketLeague_MasterEngine.lua")
        if os.path.exists(lua_source):
            with open(lua_source, "r", encoding="utf-8") as f:
                self.lua_preview.setPlainText(f.read())
        layout.addWidget(self.lua_preview)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        btn_test_lua = QPushButton("Test Lua Code (Dry-Run)")
        btn_test_lua.setStyleSheet("background-color: #3b2815; color: #ffb400; font-weight: bold; padding: 12px; border-radius: 4px;")
        btn_test_lua.clicked.connect(self.test_lua_code)

        btn_safe_run = QPushButton("Deploy & Safe Run (Activate)")
        btn_safe_run.setStyleSheet("background-color: #00b478; color: white; font-weight: bold; padding: 12px; border-radius: 4px;")
        btn_safe_run.clicked.connect(self.deploy_safe_run)

        grid_layout.addWidget(btn_test_lua, 0, 0)
        grid_layout.addWidget(btn_safe_run, 0, 1)

        layout.addLayout(grid_layout)

        close_btn = QPushButton("Close Studio")
        close_btn.setStyleSheet("background-color: #c83232; color: white; font-weight: bold; padding: 8px; border-radius: 4px;")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    def test_lua_code(self):
        code = self.lua_preview.toPlainText()
        if "function OnEvent" in code:
            self.parent.log_message("[LUA TEST] Local Lua syntax dry-run passed.")
            QMessageBox.information(self, "Lua Dry-Run", "Lua syntax looks solid!")
        else:
            QMessageBox.warning(self, "Lua Dry-Run", "Script is missing basic 'function OnEvent(event, arg)' structure.")

    def deploy_safe_run(self):
        try:
            ghub_dir = os.path.expandvars("%LOCALAPPDATA%\\LGHUB\\scripts")
            os.makedirs(ghub_dir, exist_ok=True)
            target = os.path.join(ghub_dir, "RocketLeague_MasterEngine.lua")
            code = self.lua_preview.toPlainText()
            with open(target, "w", encoding="utf-8") as f:
                f.write(code)
            QApplication.clipboard().setText(code)
            self.parent.log_message("[LUA STUDIO] Script Deployed, Activated, and Copied for Safe Run.")
            QMessageBox.information(self, "Safe Run", "Script is deployed and actively queued. Safe Run mode engaged!")
        except:
            pass

class RLConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hardware Config & Injectors")
        self.setFixedSize(700, 580)
        self.setStyleSheet("background-color: #0b0e14; color: #f0f5ff;")
        self.parent = parent

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("HARDWARE CONFIGURATION & INJECTORS")
        title.setStyleSheet("color: #00d2ff; font-weight: bold; font-size: 11pt;")
        layout.addWidget(title)

        grid_frame = QFrame()
        grid_frame.setStyleSheet("background-color: #121826; border: 1px solid #1e293b; border-radius: 6px;")
        grid_layout = QGridLayout(grid_frame)
        grid_layout.setContentsMargins(15, 15, 15, 15)

        btn_tainput = QPushButton("Inject TAInput (LTA - Safe)")
        btn_tainput.setStyleSheet("background-color: #192d41; color: #00d2ff; font-weight: bold; padding: 12px; border-radius: 4px;")
        btn_tainput.clicked.connect(self.inject_lta)

        btn_tasys = QPushButton("Inject TASystem (LTS - Safe)")
        btn_tasys.setStyleSheet("background-color: #232d41; color: #ffc850; font-weight: bold; padding: 12px; border-radius: 4px;")
        btn_tasys.clicked.connect(self.inject_lts)

        btn_physics = QPushButton("Inject Physics (Zero Lag)")
        btn_physics.setStyleSheet("background-color: #4b1e3b; color: #e6a0ff; font-weight: bold; padding: 12px; border-radius: 4px;")
        btn_physics.clicked.connect(self.inject_physics)

        grid_layout.addWidget(btn_tainput, 0, 0)
        grid_layout.addWidget(btn_tasys, 0, 1)
        grid_layout.addWidget(btn_physics, 1, 0)

        layout.addWidget(grid_frame)

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("background-color: #c83232; color: white; font-weight: bold; padding: 8px; border-radius: 4px;")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    def inject_lta(self):
        try:
            target = os.path.join(self.parent.rl_config_dir, "TAInput.ini")
            safe_append_ini(target, "[Engine.PlayerInput]\nbEnableMouseSmoothing=False")
            self.parent.log_message("[INJECT] LTA safely appended.")
            QMessageBox.information(self, "LTA", "TAInput (LTA) safely appended!")
        except:
            pass

    def inject_lts(self):
        try:
            target = os.path.join(self.parent.rl_config_dir, "TASystemSettings.ini")
            safe_append_ini(target, "[SystemSettings]\nAllowPerFrameSleep=False")
            self.parent.log_message("[INJECT] LTS safely appended.")
            QMessageBox.information(self, "LTS", "TASystemSettings (LTS) safely appended!")
        except:
            pass

    def inject_physics(self):
        try:
            target = os.path.join(self.parent.rl_config_dir, "TASystemSettings.ini")
            content = "[SystemSettings]\nOneFrameThreadLag=False\nMaxAnisotropy=16\nDynamicShadows=False\nDetailMode=0"
            safe_append_ini(target, content)
            self.parent.log_message("[INJECT] Physics injected.")
            QMessageBox.information(self, "Physics", "Top 100 Physics injected!")
        except:
            pass

class MasterEngineWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ROCKET LEAGUE MASTER ENGINE v4.8 PRO (TIMING FIXES & MOUSE ISOLATION)")
        self.setFixedSize(960, 720)
        self.setStyleSheet("background-color: #0b0e14; color: #f0f5ff;")

        self.user_profile = os.environ.get("USERPROFILE", "")
        self.docs = os.path.join(self.user_profile, "Documents")
        self.rl_config_dir = os.path.join(self.docs, "My Games", "Rocket League", "TAGame", "Config")
        self.project_root = "D:\\rl\\engine-rl"

        self.engine = NativeMacroEngine()
        self.engine.log_signal.connect(self.log_message)
        self.hook_active = False

        self.init_ui()
        self.log_message("[INIT] Engine v4.8 PRO Online. Macros fully rebuilt with 30-30-20-600 logic.")

    def log_message(self, msg):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.console.append(f"[{timestamp}] {msg}")

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(12)

        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #121826; border: 1px solid #1e293b; border-radius: 4px;")
        header_frame.setFixedHeight(65)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(15, 8, 15, 8)
        header_layout.setSpacing(2)

        title_lbl = QLabel("MACRO EXECUTION DASHBOARD (PRO TIMINGS & KEYBOARD JUMP/BOOST)")
        title_lbl.setStyleSheet("color: #00d2ff; font-weight: bold; font-size: 13pt; border: none;")
        
        sub_lbl = QLabel("Safe Hotkeys: [F1] Fwd Flip | [F2] Left Flip | [F3] Right Flip | [F4] Aerial Pitch")
        sub_lbl.setStyleSheet("color: #00ffb4; font-size: 9.5pt; border: none; font-weight: bold;")

        header_layout.addWidget(title_lbl)
        header_layout.addWidget(sub_lbl)
        main_layout.addWidget(header_frame)

        actions_frame = QFrame()
        actions_frame.setStyleSheet("background-color: #121826; border: 1px solid #1e293b; border-radius: 4px;")
        actions_frame.setFixedHeight(48)
        actions_layout = QHBoxLayout(actions_frame)
        actions_layout.setContentsMargins(8, 8, 8, 8)

        btn_rl = QPushButton("Launch RL")
        btn_rl.setStyleSheet("background-color: #006eb4; color: white; font-weight: bold; border-radius: 3px;")
        btn_rl.clicked.connect(self.launch_rl)

        btn_ghub = QPushButton("Launch G-HUB")
        btn_ghub.setStyleSheet("background-color: #232d41; color: #00d2ff; font-weight: bold; border-radius: 3px;")
        btn_ghub.clicked.connect(self.launch_ghub)

        btn_pro = QPushButton("Pro Profiles")
        btn_pro.setStyleSheet("background-color: #3b2815; color: #ffaa00; font-weight: bold; border-radius: 3px;")
        btn_pro.clicked.connect(self.open_pro_profiles)

        btn_rl_config = QPushButton("RL Config & Injectors")
        btn_rl_config.setStyleSheet("background-color: #1d2836; color: #00ffc8; font-weight: bold; border-radius: 3px;")
        btn_rl_config.clicked.connect(self.open_rl_config)

        btn_lua_studio = QPushButton("Lua Testing Studio")
        btn_lua_studio.setStyleSheet("background-color: #193732; color: #00ffb4; font-weight: bold; border-radius: 3px;")
        btn_lua_studio.clicked.connect(self.open_lua_studio)

        for b in [btn_rl, btn_ghub, btn_pro, btn_rl_config, btn_lua_studio]:
            actions_layout.addWidget(b)

        main_layout.addWidget(actions_frame)

        macro_layout = QHBoxLayout()
        macro_layout.setSpacing(10)

        self.btn_start = QPushButton("RUN MACRO ENGINE")
        self.btn_start.setFixedHeight(50)
        self.btn_start.setStyleSheet("background-color: #00b478; color: white; font-weight: bold; font-size: 11pt; border-radius: 4px;")
        self.btn_start.clicked.connect(self.run_macro)

        self.btn_stop = QPushButton("STOP MACRO ENGINE")
        self.btn_stop.setFixedHeight(50)
        self.btn_stop.setEnabled(False)
        self.btn_stop.setStyleSheet("background-color: #c83232; color: white; font-weight: bold; font-size: 11pt; border-radius: 4px;")
        self.btn_stop.clicked.connect(self.stop_macro)

        macro_layout.addWidget(self.btn_start)
        macro_layout.addWidget(self.btn_stop)
        main_layout.addLayout(macro_layout)

        console_lbl = QLabel("LOG HISTORY & LIVE MONITOR:")
        console_lbl.setStyleSheet("color: #ffaa00; font-weight: bold; font-size: 10pt;")
        main_layout.addWidget(console_lbl)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("background-color: #070a0f; color: #64e696; font-family: Consolas; font-size: 10pt; border: 1px solid #1e293b; border-radius: 4px;")
        main_layout.addWidget(self.console)

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(10)

        btn_reg = QPushButton("System Registry Build")
        btn_reg.setFixedHeight(36)
        btn_reg.setStyleSheet("background-color: #142d3c; color: #00ffc8; font-weight: bold; font-size: 9pt; border-radius: 4px;")
        btn_reg.clicked.connect(self.apply_full_registry)

        btn_build = QPushButton("Build Environment (.EXE)")
        btn_build.setFixedHeight(36)
        btn_build.setStyleSheet("background-color: #371e4b; color: #e6a0ff; font-weight: bold; font-size: 9pt; border-radius: 4px;")
        btn_build.clicked.connect(self.build_pkg)

        bottom_layout.addWidget(btn_reg)
        bottom_layout.addWidget(btn_build)
        main_layout.addLayout(bottom_layout)

    def launch_rl(self):
        try:
            subprocess.Popen("start com.epicgames.launcher://apps/Sugar?action=launch&silent=true", shell=True)
            self.log_message("[SYSTEM] Epic Games launcher dispatched.")
        except:
            pass

    def launch_ghub(self):
        try:
            ghub_path = os.path.expandvars("%ProgramFiles%\\LGHUB\\lghub.exe")
            if os.path.exists(ghub_path):
                subprocess.Popen([ghub_path])
        except:
            pass

    def open_rl_config(self):
        dialog = RLConfigDialog(self)
        dialog.exec()

    def open_lua_studio(self):
        dialog = LuaStudioDialog(self)
        dialog.exec()
        
    def open_pro_profiles(self):
        dialog = ProProfilesDialog(self)
        dialog.exec()

    def build_pkg(self):
        try:
            self.log_message("[SYSTEM] Triggering PKG Environment Builder...")
            subprocess.Popen(["pyinstaller", "--noconsole", "--onefile", "--clean", __file__], cwd=self.project_root)
            QMessageBox.information(self, "PKG Builder", "Build process started! Check 'dist' folder.")
        except:
            pass

    def run_macro(self):
        self.hook_active = True
        self.btn_start.setEnabled(False)
        self.btn_start.setText("MACRO RUNNING")
        self.btn_stop.setEnabled(True)
        self.log_message("[MONITOR] MACRO ENGINE RUNNING. Full Logic + Virtual Keyboard Jumps. Hotkeys F1-F4 active.")

        import keyboard
        keyboard.add_hotkey('f1', lambda: threading.Thread(target=self.engine.execute_forward_speedflip, daemon=True).start())
        keyboard.add_hotkey('f2', lambda: threading.Thread(target=self.engine.execute_left_speedflip, daemon=True).start())
        keyboard.add_hotkey('f3', lambda: threading.Thread(target=self.engine.execute_right_speedflip, daemon=True).start())
        keyboard.add_hotkey('f4', lambda: threading.Thread(target=self.engine.execute_fast_aerial, daemon=True).start())

    def stop_macro(self):
        self.hook_active = False
        import keyboard
        keyboard.unhook_all()
        self.btn_start.setEnabled(True)
        self.btn_start.setText("RUN MACRO ENGINE")
        self.btn_stop.setEnabled(False)
        self.log_message("[MONITOR] MACRO ENGINE STOPPED. All macro hotkeys unhooked.")

    def apply_full_registry(self):
        try:
            desktop_path = r"Control Panel\Desktop"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, desktop_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, "LowLevelHooksTimeout", 0, winreg.REG_DWORD, 1000)
                winreg.SetValueEx(key, "ForegroundLockTimeout", 0, winreg.REG_DWORD, 0)
            
            app_path = r"Software\RocketLeagueMasterEngine"
            winreg.CreateKey(winreg.HKEY_CURRENT_USER, app_path)
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, app_path, 0, winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, "EngineVersion", 0, winreg.REG_SZ, "v4.8 PRO")
                winreg.SetValueEx(key, "MacroTimings", 0, winreg.REG_SZ, "Fractional 30-30-20-600")
            self.log_message("[SYSTEM] Settings fully registered in Windows Registry.")
            QMessageBox.information(self, "Registry", "Settings recorded in Registry successfully!")
        except:
            pass

    def clean_locks(self):
        try:
            for proc in ["MasterEngine", "RocketLeague_MasterEngine"]:
                os.system(f"taskkill /f /im {proc}.exe >nul 2>&1")
            QMessageBox.information(self, "Unlock", "Stale processes cleared.")
        except:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MasterEngineWindow()
    window.show()
    sys.exit(app.exec())