import threading
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk

from screen_capture import select_region, capture_region, extract_text
from ai_client import generate_response


class AgentAssistApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Service Copilot")
        self.root.geometry("1200x740")
        self.region = None
        self.last_image = None

        self._build_layout()

    # ---------- UI ----------
    def _build_layout(self):
        toolbar = ttk.Frame(self.root, padding=8)
        toolbar.pack(side="top", fill="x")

        ttk.Button(
            toolbar, text="1. Select Chat Area", command=self.on_select_region
        ).pack(side="left", padx=4)
        ttk.Button(
            toolbar,
            text="2. Capture && Suggest Reply",
            command=self.on_capture_and_generate,
        ).pack(side="left", padx=4)

        ttk.Label(toolbar, text="Extra note for AI (optional):").pack(
            side="left", padx=(20, 4)
        )
        self.tone_entry = ttk.Entry(toolbar, width=40)
        self.tone_entry.pack(side="left")

        main = ttk.Frame(self.root)
        main.pack(fill="both", expand=True, padx=8, pady=8)

        # Left: captured chat view
        left = ttk.LabelFrame(main, text="Chat Screen (captured)")
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        self.preview_label = ttk.Label(
            left,
            text="No region selected yet.\nClick 'Select Chat Area' and drag over your chat window.",
            anchor="center",
            justify="center",
        )
        self.preview_label.pack(fill="both", expand=True, padx=8, pady=8)

        ttk.Label(left, text="Extracted chat text (you can edit before generating):").pack(
            anchor="w", padx=8
        )
        self.transcript_box = tk.Text(left, height=10, wrap="word")
        self.transcript_box.pack(fill="both", expand=False, padx=8, pady=(0, 8))

        # Right: AI suggested response
        right = ttk.LabelFrame(main, text="AI Suggested Response")
        right.pack(side="right", fill="both")
        right.configure(width=380)
        right.pack_propagate(False)

        self.response_box = tk.Text(right, wrap="word", font=("Segoe UI", 11))
        self.response_box.pack(fill="both", expand=True, padx=8, pady=8)

        btn_row = ttk.Frame(right)
        btn_row.pack(fill="x", padx=8, pady=(0, 8))
        ttk.Button(btn_row, text="Copy to Clipboard", command=self.on_copy).pack(
            side="left"
        )
        ttk.Button(
            btn_row, text="Regenerate", command=self.on_capture_and_generate
        ).pack(side="left", padx=6)

        self.status = ttk.Label(self.root, text="Ready.", anchor="w", padding=4)
        self.status.pack(side="bottom", fill="x")

    # ---------- Actions ----------
    def on_select_region(self):
        self.status.config(text="Drag a rectangle over the chat window...")
        self.root.update()
        region = select_region(self.root)
        if region and region[2] > 5 and region[3] > 5:
            self.region = region
            self.status.config(text=f"Region selected: {region}")
        else:
            self.status.config(text="No valid region selected.")

    def on_capture_and_generate(self):
        if not self.region:
            messagebox.showwarning(
                "No region selected", "Select the chat area on your screen first."
            )
            return
        self.status.config(text="Capturing screen...")
        self.root.update()
        threading.Thread(target=self._capture_and_generate_worker, daemon=True).start()

    def _capture_and_generate_worker(self):
        try:
            img = capture_region(self.region)
            self.last_image = img
            self._update_preview(img)

            self.status_safe("Reading chat text (OCR)...")
            text = extract_text(img)
            self._set_text(self.transcript_box, text)

            self.status_safe("Asking AI for a suggested reply...")
            tone_note = self.tone_entry.get()
            reply = generate_response(text, tone_note)
            self._set_text(self.response_box, reply)

            self.status_safe("Done.")
        except Exception as e:
            self.status_safe(f"Error: {e}")
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))

    # ---------- Thread-safe UI helpers ----------
    def status_safe(self, msg):
        self.root.after(0, lambda: self.status.config(text=msg))

    def _set_text(self, widget, text):
        def _do():
            widget.delete("1.0", "end")
            widget.insert("1.0", text)

        self.root.after(0, _do)

    def _update_preview(self, img):
        def _do():
            display_img = img.copy()
            display_img.thumbnail((560, 360))
            tk_img = ImageTk.PhotoImage(display_img)
            self.preview_label.configure(image=tk_img, text="")
            self.preview_label.image = tk_img  # keep a reference

        self.root.after(0, _do)

    def on_copy(self):
        text = self.response_box.get("1.0", "end").strip()
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status.config(text="Response copied to clipboard.")


def main():
    root = tk.Tk()
    AgentAssistApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
