import threading
import traceback
import tkinter as tk
from tkinter import messagebox

# Try to import the keyboard module for a global hotkey.
# If it's unavailable or fails to initialize (requires elevated privileges on some setups),
# we'll still provide a local GUI button to capture.
try:
    import keyboard
    _KEYBOARD_AVAILABLE = True
except Exception:
    _KEYBOARD_AVAILABLE = False

import capture

DEFAULT_HOTKEY = "ctrl+shift+s"


def _safe_call(func, *a, **kw):
    try:
        return func(*a, **kw)
    except Exception:
        traceback.print_exc()


class CaptureGUI:
    def __init__(self, root):
        self.root = root
        root.title("pkr.ai — Capture")
        root.geometry("380x150")
        root.resizable(False, False)

        frm = tk.Frame(root, padx=12, pady=12)
        frm.pack(fill=tk.BOTH, expand=True)

        tk.Label(frm, text="Capture (one-click or global hotkey)", font=(None, 11, "bold")).pack(anchor=tk.W)

        btn = tk.Button(frm, text="Capture Now", width=14, command=self.on_capture_click)
        btn.pack(pady=(10, 6))

        hk_row = tk.Frame(frm)
        hk_row.pack(fill=tk.X)
        tk.Label(hk_row, text="Global hotkey:", width=12).pack(side=tk.LEFT)
        self.hotkey_var = tk.StringVar(value=DEFAULT_HOTKEY)
        self.hotkey_entry = tk.Entry(hk_row, textvariable=self.hotkey_var, width=18)
        self.hotkey_entry.pack(side=tk.LEFT)

        bind_btn = tk.Button(hk_row, text="Bind", command=self.bind_hotkey)
        bind_btn.pack(side=tk.LEFT, padx=(8, 0))

        self.status = tk.Label(frm, text=self._status_text(), anchor=tk.W, fg="#666")
        self.status.pack(fill=tk.X, pady=(10, 0))

        # If keyboard module is available, auto-bind default hotkey.
        self._registered = False
        if _KEYBOARD_AVAILABLE:
            self.bind_hotkey()
        else:
            self.status.config(text=self._status_text())

        # Ensure we unbind keyboard hooks on close
        root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _status_text(self):
        if _KEYBOARD_AVAILABLE:
            return f"Global hotkey available. Default: {DEFAULT_HOTKEY} — press to capture (or use button)."
        else:
            return "Global hotkey unavailable. Using local button only. (Install 'keyboard' package and run as admin for global hotkey)"

    def on_capture_click(self):
        threading.Thread(target=_safe_call, args=(self._capture_and_notify,)).start()

    def _capture_and_notify(self):
        filename = capture.take_screenshot()
        # update label in main thread
        self.root.after(0, lambda: self.status.config(text=f"Saved: {filename}"))

    def bind_hotkey(self):
        if not _KEYBOARD_AVAILABLE:
            messagebox.showwarning("Hotkey unavailable", "The 'keyboard' module is not available. Install it with `pip install keyboard` and run as admin to enable global hotkeys.")
            return

        hk = self.hotkey_var.get().strip()
        if not hk:
            messagebox.showerror("Invalid hotkey", "Please enter a valid hotkey string (e.g. ctrl+shift+s).")
            return

        try:
            # Unregister previous if any
            if self._registered:
                keyboard.unhook_all_hotkeys()
                self._registered = False

            keyboard.add_hotkey(hk, lambda: threading.Thread(target=_safe_call, args=(self._capture_and_notify,)).start())
            self._registered = True
            self.status.config(text=f"Bound global hotkey: {hk}. Press it to capture.")
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Bind failed", f"Failed to bind hotkey '{hk}': {e}\n\nNote: on Windows this may require running the program as Administrator.")

    def on_close(self):
        if _KEYBOARD_AVAILABLE and self._registered:
            try:
                keyboard.unhook_all_hotkeys()
            except Exception:
                pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = CaptureGUI(root)
    root.mainloop()
