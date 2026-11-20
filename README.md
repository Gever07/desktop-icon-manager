# 🖥️ Desktop Icon Manager (`desktop-icon-manager`)

A sleek, dark-mode Windows utility built with Python and `customtkinter` that allows you to back up, restore, undo, and redo your Windows desktop icon positions with a single click.

---

## ✨ Features

* **📸 Save Current Layout:** Exports your exact Windows desktop icon arrangement (`HKCU\Software\Microsoft\Windows\Shell\Bags\1\Desktop`) into a local `MyLayout.reg` backup file.
* **⚡ Restore Saved Layout:** Re-imports your saved layout and refreshes `explorer.exe` to snap all icons back to their saved positions.
* **↩️ Undo / ↪️ Redo System:** Automatically creates state snapshots (`UndoLayout.reg` and `RedoLayout.reg`) so you can safely revert or reapply layout changes.
* **🎨 Modern Dark GUI:** Built with `customtkinter` with audio feedback cues for save and restore actions.

---

## 🛠️ Requirements & Installation

* **OS:** Windows 10 / Windows 11
* **Python:** Python 3.7+

### Install Dependencies


pip install customtkinter
🚀 Usage
Run the application:

Bash
python desktop_icon_manager.py
Click Save Current Layout to create your baseline MyLayout.reg backup in the application folder.

Whenever your icons get scrambled (e.g., after resolution changes or desktop shows), click Restore Saved Layout.

Use Undo and Redo to step back and forth between recent layout states.

Note: When restoring a layout, the app briefly restarts explorer.exe to apply the Windows Registry changes immediately.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
