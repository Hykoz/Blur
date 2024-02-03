import cv2
from tkinter import Tk, Canvas, Button, filedialog
from PIL import Image, ImageTk

class FaceBlurApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Face Blur App")

        self.canvas = Canvas(master)
        self.canvas.pack(fill="both", expand=True)

        self.load_button = Button(master, text="Ouvrir une image", command=self.load_image)
        self.load_button.pack()

        self.select_button = Button(master, text="Sélectionner les visages", command=self.select_faces)
        self.select_button.pack()

        self.confirm_button = Button(master, text="Confirmer la sélection", command=self.confirm_selection, state="disabled")
        self.confirm_button.pack()

        self.blur_button = Button(master, text="Flouter les visages", command=self.blur_faces, state="disabled")
        self.blur_button.pack()

        self.save_button = Button(master, text="Enregistrer", command=self.save_image, state="disabled")
        self.save_button.pack()

        self.image_path = None
        self.image = None
        self.cv_image = None
        self.face_rectangles = []

        self.selected_faces = []

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.image_path = file_path
            self.image = Image.open(file_path)
            self.cv_image = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)
            self.display_image()

    def display_image(self):
        if self.image:
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.config(width=self.tk_image.width(), height=self.tk_image.height())
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

    def select_faces(self):
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.select_button.config(state="disabled")
        self.confirm_button.config(state="normal")

    def on_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="blue", width=2)

    def on_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, cur_x, cur_y)

    def on_release(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)
        self.face_rectangles.append((min(self.start_x, end_x), min(self.start_y, end_y), max(self.start_x, end_x), max(self.start_y, end_y)))
        self.start_x, self.start_y = None, None
        self.confirm_button.config(state="normal")

    def confirm_selection(self):
        self.canvas.delete("all")
        self.display_image()

        for rect in self.face_rectangles:
            self.canvas.create_rectangle(rect, outline="green", width=2)

        self.selected_faces = self.face_rectangles.copy()
        self.face_rectangles = []
        self.confirm_button.config(state="disabled")
        self.select_button.config(state="normal")
        self.blur_button.config(state="normal")

    def blur_faces(self):
        if self.cv_image is not None:
            for rect in self.selected_faces:
                x1, y1, x2, y2 = rect
                face = self.cv_image[int(y1):int(y2), int(x1):int(x2)]
                blurred_face = cv2.GaussianBlur(face, (99, 99), 30)
                self.cv_image[int(y1):int(y2), int(x1):int(x2)] = blurred_face

            # Convertir l'image OpenCV en format PhotoImage sans changement de couleur
            image_pil = Image.fromarray(self.cv_image)
            self.tk_image = ImageTk.PhotoImage(image_pil)

            self.canvas.config(width=self.tk_image.width(), height=self.tk_image.height())
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

            self.save_button.config(state="normal")

    def save_image(self):
        if self.cv_image is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                cv2.imwrite(save_path, cv2.cvtColor(self.cv_image, cv2.COLOR_RGB2BGR))

if __name__ == "__main__":
    root = Tk()
    app = FaceBlurApp(root)
    root.mainloop()
