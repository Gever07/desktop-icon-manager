import os
import sys
import time
import threading
import subprocess
import ctypes
import customtkinter as ctk
from tkinter import messagebox

# Appearance settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def safe_beep(freq, duration):
    def run():
        try:
            import winsound
            winsound.Beep(freq, duration)
        except Exception:
            pass
    threading.Thread(target=run, daemon=True).start()

def play_save_sound():
    safe_beep(2000, 100)

def play_restore_sound():
    safe_beep(1200, 150)

class DesktopIconManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Desktop Icon Manager")
        self.geometry("450x380")
        self.resizable(False, False)
        
        # Physical REG file paths in the working directory (supports both .py and .exe)
        if getattr(sys, 'frozen', False):
            current_folder = os.path.dirname(sys.executable)
        else:
            current_folder = os.path.dirname(os.path.abspath(__file__))

        self.backup_path = os.path.join(current_folder, "MyLayout.reg")
        self.undo_path = os.path.join(current_folder, "UndoLayout.reg")
        self.redo_path = os.path.join(current_folder, "RedoLayout.reg")

        self.title_label = ctk.CTkLabel(
            self, text="Desktop Icon Manager", 
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color="#3a86ff"
        )
        self.title_label.pack(pady=15)

        self.save_btn = ctk.CTkButton(
            self, text="📸 Save Current Layout", font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            fg_color="#06d6a0", hover_color="#05b88a", height=45, command=self.save_layout
        )
        self.save_btn.pack(pady=8, fill="x", padx=40)

        self.restore_btn = ctk.CTkButton(
            self, text="⚡ Restore Saved Layout", font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            fg_color="#7209b7", hover_color="#560bad", height=45, command=self.restore_layout
        )
        self.restore_btn.pack(pady=8, fill="x", padx=40)

        # File-based Undo/Redo panel
        self.undo_redo_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.undo_redo_frame.pack(pady=10, fill="x", padx=40)

        self.undo_btn = ctk.CTkButton(
            self.undo_redo_frame, text="↩️ Undo", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color="#3a86ff", hover_color="#2a6fdb", height=35, command=self.undo_action
        )
        self.undo_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.redo_btn = ctk.CTkButton(
            self.undo_redo_frame, text="↪️ Redo", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color="#3a86ff", hover_color="#2a6fdb", height=35, command=self.redo_action
        )
        self.redo_btn.pack(side="right", expand=True, fill="x", padx=(5, 0))

        self.status_label = ctk.CTkLabel(self, text="Ready!", font=ctk.CTkFont(family="Segoe UI", size=12))
        self.status_label.pack(side="bottom", pady=10)

    def save_state(self, target_path):
        """Exports the current desktop icon positions to a physical registry file."""
        try:
            cmd = f'reg export "HKCU\\Software\\Microsoft\\Windows\\Shell\\Bags\\1\\Desktop" "{target_path}" /y'
            subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

    def apply_state_and_refresh(self, source_path):
        """Imports a registry file and refreshes the Windows desktop quickly."""
        try:
            cmd = f'reg import "{source_path}"'
            subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Internal Windows shell refresh notification
            ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
            
            # Restart explorer.exe to apply layout changes immediately
            subprocess.run("taskkill /f /im explorer.exe && start explorer.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            subprocess.run("start explorer.exe", shell=True)

    def save_layout(self):
        try:
            self.status_label.configure(text="Saving icon positions...", text_color="yellow")
            self.update()
            self.save_state(self.backup_path)
            play_save_sound()
            self.status_label.configure(text="Layout saved to REG!", text_color="#06d6a0")
            messagebox.showinfo("Success", "Current desktop layout saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def restore_layout(self):
        if not os.path.exists(self.backup_path): 
            messagebox.showwarning("Warning", "Backup file MyLayout.reg not found!")
            return
        try:
            self.status_label.configure(text="Restoring layout...", text_color="orange")
            self.update()
            self.save_state(self.undo_path)  # Save current state for Undo
            self.apply_state_and_refresh(self.backup_path)
            play_restore_sound()
            self.status_label.configure(text="Layout restored!", text_color="#06d6a0")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def undo_action(self):
        if not os.path.exists(self.undo_path):
            messagebox.showinfo("Undo", "No UndoLayout.reg file available in the directory!")
            return
        try:
            self.status_label.configure(text="Undoing last action...", text_color="yellow")
            self.update()
            
            # Save current state to Redo before reverting
            self.save_state(self.redo_path)
            
            # Apply the Undo state
            self.apply_state_and_refresh(self.undo_path)
            
            # Remove used Undo file to prevent duplicates
            try:
                os.remove(self.undo_path)
            except Exception:
                pass
            
            play_save_sound()
            self.status_label.configure(text="Undo completed successfully!", text_color="#3a86ff")
        except Exception as e:
            messagebox.showerror("Undo Error", str(e))

    def redo_action(self):
        if not os.path.exists(self.redo_path):
            messagebox.showinfo("Redo", "No RedoLayout.reg file available in the directory!")
            return
        try:
            self.status_label.configure(text="Redoing action...", text_color="yellow")
            self.update()
            
            # Save current state to Undo
            self.save_state(self.undo_path)
            
            # Apply the Redo state
            self.apply_state_and_refresh(self.redo_path)
            
            # Remove used Redo file
            try:
                os.remove(self.redo_path)
            except Exception:
                pass
            
            play_save_sound()
            self.status_label.configure(text="Redo completed successfully!", text_color="#3a86ff")
        except Exception as e:
            messagebox.showerror("Redo Error", str(e))

if __name__ == "__main__":
    app = DesktopIconManagerApp()
    app.mainloop()