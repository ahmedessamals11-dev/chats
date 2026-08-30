import tkinter as tk
from PIL import Image
import mss
import pytesseract

_selected_region = None  # (left, top, width, height)


def select_region(root):
    """
    Dim the screen and let the user drag a rectangle over the chat window.
    Returns (left, top, width, height) in screen coordinates, or None.
    """
    global _selected_region
    _selected_region = None

    overlay = tk.Toplevel(root)
    overlay.attributes("-fullscreen", True)
    overlay.attributes("-alpha", 0.3)
    overlay.configure(bg="black")
    overlay.attributes("-topmost", True)
    overlay.title("Drag to select the chat area, then release")

    canvas = tk.Canvas(overlay, cursor="cross", bg="grey11", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    start = {}
    rect_id = {"id": None}

    def on_press(event):
        start["x"], start["y"] = event.x, event.y
        rect_id["id"] = canvas.create_rectangle(
            event.x, event.y, event.x, event.y, outline="#ff5555", width=2
        )

    def on_drag(event):
        if rect_id["id"] is not None:
            canvas.coords(rect_id["id"], start["x"], start["y"], event.x, event.y)

    def on_release(event):
        global _selected_region
        x0, y0 = start.get("x", event.x), start.get("y", event.y)
        x1, y1 = event.x, event.y
        left, top = min(x0, x1), min(y0, y1)
        width, height = abs(x1 - x0), abs(y1 - y0)
        _selected_region = (left, top, width, height)
        overlay.destroy()

    def on_escape(_event):
        overlay.destroy()

    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)
    overlay.bind("<Escape>", on_escape)

    overlay.wait_window()
    return _selected_region


def capture_region(region):
    """region: (left, top, width, height). Returns a PIL Image of that screen area."""
    left, top, width, height = region
    if width <= 0 or height <= 0:
        raise ValueError("Invalid capture region. Please re-select the chat area.")
    with mss.mss() as sct:
        monitor = {"left": left, "top": top, "width": width, "height": height}
        shot = sct.grab(monitor)
        img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
    return img


def extract_text(img: Image.Image) -> str:
    """Run OCR on the captured image and return the extracted text."""
    return pytesseract.image_to_string(img)
