import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.configure(bg="black")

gif_path = "C:/Users/Venom/Documents/studywork/gifpy/gif.gif"

label = tk.Label(root, bg="black", bd=0, highlightthickness=0)
label.pack(fill="both", expand=True)

pil_frames = []
img = Image.open(gif_path)

try:
    while True:
        pil_frames.append(img.copy().convert("RGBA"))
        img.seek(len(pil_frames))
except EOFError:
    pass

scale = 1.0
frames = []
frame_index = 0
resize_job = None
frame_cache = {}

def build_frames(target_scale):
    global frames
    rounded = round(target_scale * 10) / 10  # round to 1 decimal
    if rounded in frame_cache:
        frames = frame_cache[rounded]
        return
    built = []
    for frame in pil_frames:
        w, h = frame.size
        resized = frame.resize((int(w * rounded), int(h * rounded)), Image.LANCZOS)
        built.append(ImageTk.PhotoImage(resized))
    frame_cache[rounded] = built
    frames = built

build_frames(scale)

def animate():
    global frame_index
    if frames:
        label.config(image=frames[frame_index])
        frame_index = (frame_index + 1) % len(frames)
    root.after(40, animate)

animate()

def start_move(event):
    root.x = event.x
    root.y = event.y

def do_move(event):
    x = event.x_root - root.x
    y = event.y_root - root.y
    root.geometry(f"+{x}+{y}")

label.bind("<Button-1>", start_move)
label.bind("<B1-Motion>", do_move)

def apply_resize():
    global frame_index
    build_frames(scale)
    frame_index = 0
    w = frames[0].width()
    h = frames[0].height()
    root.geometry(f"{w}x{h}")

def resize(event):
    global scale, resize_job
    if event.delta > 0:
        scale += 0.1
    else:
        scale -= 0.1
    scale = max(0.2, min(scale, 3.0))

    if resize_job:
        root.after_cancel(resize_job)
    resize_job = root.after(150, apply_resize)  # wait 150ms after last scroll tick

root.bind("<MouseWheel>", resize)

w, h = frames[0].width(), frames[0].height()
x = (root.winfo_screenwidth() // 2) - (w // 2)
y = (root.winfo_screenheight() // 2) - (h // 2)
root.geometry(f"{w}x{h}+{x}+{y}")

root.mainloop()