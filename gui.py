import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os 
from threading import Thread
from processor import overlay_video

class ObjectLabelingTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Object Labeling Tool")

        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack()

        self.load_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack()
        self.save_button = tk.Button(root, text="Start", command=self.save_labels)
        self.save_button.pack()

        self.image = None
        self.image_path = ""
        self.objects = []

        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_rectangle)

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])

        if self.image_path:
            self.image = Image.open(self.image_path)
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.config(width=self.image.width, height=self.image.height)
            self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")


    def start_draw(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rectangle = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y, outline="red"
        )

    def draw_rectangle(self, event):
        self.canvas.coords(self.rectangle, self.start_x, self.start_y, event.x, event.y)
        x, y, x1, y1 = self.canvas.coords(self.rectangle)
        width = x1 - x
        height = y1 - y
        self.root.title(f"Object Labeling Tool - x: {x}, y: {y}, width: {width}, height: {height}")

    def save_labels(self):
        if self.image_path:
            x, y, x1, y1 = self.canvas.coords(self.rectangle)
            width = x1 - x
            height = y1 - y
            
            def _demo():
                file_name_without_extension = os.path.splitext(os.path.basename(self.image_path))[0]
                overlay_video(file_name_without_extension, x, y, width, height)

            Thread(target=_demo).start()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ObjectLabelingTool(root)
    app.run()

