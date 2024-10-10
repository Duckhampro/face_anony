import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

class FaceAnonymizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Face Anonymizer')
        self.root.geometry('900x700')
        self.root.configure(bg='#1E90FF')  # Dark background for modern look

        # Custom ttk style
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12), background='#9370DB', foreground='white', padding=10)
        style.configure('TLabel', font=('Arial', 14), background='#9370DB', foreground='white')
        style.configure('TScale', background='#A52A2A')

        # Title
        self.title_label = ttk.Label(root, text="Face Anonymizer App", font=('Arial', 20, 'bold'))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Video Display
        self.video_label = tk.Label(root, bg='#000')
        self.video_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Blur Level Slider
        self.blur_slider = tk.Scale(root, from_=1, to_=100, orient="horizontal", label="Blur Level",
                                    bg="#1E90FF", fg="white", highlightbackground="#FF8C00",command=self.update_blur, resolution=2, font=('Arial', 12))
        self.blur_slider.grid(row=2, column=0, padx=20, pady=10)

        # Pixelize Level Slider
        self.pixel_slider = tk.Scale(root, from_=2, to_=100, orient="horizontal", label="Pixelize Level",
                                     bg="#1E90FF", fg="white", highlightbackground="#FF8C00", command=self.update_pixelize, resolution=2, font=('Arial', 12))
        self.pixel_slider.grid(row=2, column=1, padx=20, pady=10)

        self.anonymize_icon = tk.Button(root, text="Icon",font= ("Arial", 12, "bold"), bg="#FF5722", fg="white",
                                         command=self.apply_icon)
        self.anonymize_icon.grid(row=3, column=2, padx=20, pady=10)
        # Blur Button
        self.blur_button = tk.Button(root, text="Blur",font= ("Arial", 12, "bold"), bg="#FF5722", fg="white",
                                      command=self.apply_blur)
        self.blur_button.grid(row=3, column=0, padx=20, pady=10)

        # Pixelize Button
        self.pixelize_button = tk.Button(root, text="Pixelize", font= ("Arial", 12, "bold"), bg="#FF5722", fg="white",
                                          command=self.apply_pixelization)
        self.pixelize_button.grid(row=3, column=1, padx=20, pady=10)

        # Variables
        self.blur_value = 15
        self.pixelize_value = 10
        self.mode = "blur"

        # Video capture
        self.cap = cv2.VideoCapture(0)
        self.root.after(0, self.update_frame)

    def update_blur(self, value):
        self.blur_value = int(value)

    def update_pixelize(self, value):
        self.pixelize_value = int(value)

    def apply_blur(self):
        self.mode = "blur"
        print("Mode changed to blur")

    def apply_pixelization(self):
        self.mode = "pixelize"
        print("Mode changed to pixelize")

    def apply_icon(self):
        self.mode = "icon"
        print("Mode changed to icon")

    def update_frame(self):
        _, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if self.mode == "blur":
            print("Applying blur...")
            frame = blur_faces(frame, faces, self.blur_value)
        elif self.mode == "pixelize":
            print("Applying Pixelize")
            frame = pixelate_faces(frame, faces, self.pixelize_value)
        elif self.mode == "icon":
            print("Applying Icon")
            frame = icon_faces(frame, faces, icon_path)

        # Display video
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        photo = ImageTk.PhotoImage(image=image)
        self.video_label.config(image=photo)
        self.video_label.image = photo

        self.root.after(10, self.update_frame)

# Blur and Pixelization functions
def blur_faces(frame, faces, blur_value):
    for (x, y, w, h) in faces:
        face_region = frame[y:y+h, x:x+w]
        blurred_face = cv2.GaussianBlur(face_region, (blur_value, blur_value), 30)
        frame[y:y+h, x:x+w] = blurred_face
    return frame

def pixelate_faces(frame, faces, pixel_size):
    for (x, y, w, h) in faces:
        face_region = frame[y:y+h, x:x+w]
        small = cv2.resize(face_region, (pixel_size, pixel_size), interpolation=cv2.INTER_LINEAR)
        pixelate_face = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
        frame[y:y+h, x:x+w] = pixelate_face
    return frame

icon_path = 'icon.png'
def icon_faces(frame, faces, icon_path):
    icon = cv2.imread(icon_path, cv2.IMREAD_UNCHANGED)
    for (x, y, w, h) in faces:
        icon_resized = cv2.resize(icon, (w, h))
        if icon_resized.shape[2] == 4:
            alpha_s = icon_resized[:, :, 3] / 255.0
            alpha_l = 1.0 - alpha_s
            for c in range(0, 3):
                frame[y: y+h, x: x+w, c] = (alpha_s * icon_resized[:, :, c] +
                                           alpha_l * frame[y: y+h, x: x+w, c])
        else:
            frame[y: y+h, x: x+w] = icon_resized
    return frame

# Run the app
root = tk.Tk()
app = FaceAnonymizerApp(root)
root.mainloop()
