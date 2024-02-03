import os
import argparse
import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter


class ImageBlurringApp:
    def __init__(self, master, image_path):
        self.master = master
        self.master.title("Image Blurring Tool")

        self.image_path = image_path
        self.image = cv2.imread(self.image_path)
        self.temp_image = self.image.copy()
        self.ROIs = []

        # UI Elements
        self.canvas = tk.Canvas(self.master)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.blur_button = tk.Button(self.master, text="Blur Selection", command=self.blur_selection)
        self.blur_button.pack(pady=5)

        self.save_button = tk.Button(self.master, text="Save Blurred Image", command=self.save_blurred_image)
        self.save_button.pack(pady=5)

        self.display_image()

        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

    def display_image(self):
        image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        self.photo = ImageTk.PhotoImage(image_pil)
        self.canvas.config(width=image_pil.width, height=image_pil.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def blur_selection(self):
        if self.ROIs:
            self.image = self.blur_boxes(self.image, self.ROIs)
            self.display_image()

    def blur_boxes(self, image, boxes):
        for box in boxes:
            x, y, w, h = [int(d) for d in box]
            sub = image[y:y+h, x:x+w]
            blur = cv2.GaussianBlur(sub, (23, 23), 30)
            image[y:y+h, x:x+w] = blur
        return image

    def save_blurred_image(self):
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if output_path:
            cv2.imwrite(output_path, self.image)

    def on_mouse_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

    def on_mouse_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.ROIs.append([self.start_x, self.start_y, cur_x, cur_y])
        self.display_image()

    def on_mouse_release(self, event):
        self.start_x = None
        self.start_y = None


def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Prompt user to select an image file
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])

    if image_path:
        app = ImageBlurringApp(root, image_path)
        root.mainloop()


if __name__ == "__main__":
    main()
