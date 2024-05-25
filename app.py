import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import random

root = tk.Tk()
root.title("Yüz Filtre ve Çil Ekleme Uygulaması")
image = None
photo_label = tk.Label(root)
photo_label.pack()
btn_add_freckles = None
btn_add_hat_mustache = None

def select_image():
    # Kullanıcıya dosya seçme iletişim kutusunu göster
    # Seçilen resmi işle ve görüntüle
    global image, photo_label, btn_add_freckles, btn_add_hat_mustache
    file_path = filedialog.askopenfilename()
    if file_path:
        image = cv2.imread(file_path)
        display_image(image)
        # Çil Ekle ve Şapka-Bıyık Ekle butonlarını görünür yap
        if not btn_add_freckles:
            btn_add_freckles = tk.Button(root, text="Çil Ekle", command=add_freckles)
            btn_add_freckles.pack()
        if not btn_add_hat_mustache:
            btn_add_hat_mustache = tk.Button(root, text="Şapka ve Bıyık Ekle", command=add_hat_mustache)
            btn_add_hat_mustache.pack()

def display_image(image):
    # Resmi Tkinter arayüzünde göstermek için yeniden boyutlandır ve güncelle
    global photo_label
    height, width, _ = image.shape
    max_height = 600
    max_width = 800
    if height > max_height or width > max_width:
        if height > width:
            ratio = max_height / height
        else:
            ratio = max_width / width
        image = cv2.resize(image, (int(width * ratio), int(height * ratio)))
    photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
    photo_label.configure(image=photo)
    photo_label.image = photo

def detect_faces(image):
    # Verilen resimde yüzleri tespit et
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    return faces

def add_freckles():
    # Yüzlerin üzerine çil ekle
    global image
    if image is None:
        return
    faces = detect_faces(image)
    for (x, y, w, h) in faces:
        x = x + int(w * 0.1)
        y = y + int(h * 0.1)
        w = int(w * 0.6)
        h = int(h * 0.6)
        num_freckles = random.randint(10, 20)
        for _ in range(num_freckles):
            fx = random.randint(x, x+w-1)
            fy = random.randint(y, y+h-1)
            radius = random.randint(1, 3)
            cv2.circle(image, (fx, fy), radius, (0, 0, 0), -1)
    display_image(image)

def add_hat_mustache():
    # Yüzlerin üzerine şapka ve bıyık ekle
    global image
    if image is None:
        return
    faces = detect_faces(image)
    for (x, y, w, h) in faces:
        hat = cv2.imread('hat.png', cv2.IMREAD_UNCHANGED)
        mustache = cv2.imread('mustache.png', cv2.IMREAD_UNCHANGED)
        hat_width = int(w * 1.2)
        hat_height = int(h * 0.6)
        hat = cv2.resize(hat, (hat_width, hat_height))
        x_offset_hat = x - int((hat_width - w) / 2)
        y_offset_hat = y - int(hat_height * 0.95)
        mustache_width = int(w * 0.8)
        mustache_height = int(h * 0.2)
        mustache = cv2.resize(mustache, (mustache_width, mustache_height))
        x_offset_mustache = x + int((w - mustache_width) / 2)
        y_offset_mustache = y + int(h * 0.6)

        hat_alpha = hat[:, :, 3] / 255.0
        mustache_alpha = mustache[:, :, 3] / 255.0

        # Şapka ekle
        if y_offset_hat >= 0 and x_offset_hat >= 0:
            for c in range(0, 3):
                image[y_offset_hat:y_offset_hat+hat.shape[0], x_offset_hat:x_offset_hat+hat.shape[1], c] = \
                    (1.0 - hat_alpha) * image[y_offset_hat:y_offset_hat+hat.shape[0], x_offset_hat:x_offset_hat+hat.shape[1], c] + \
                    hat_alpha * hat[:, :, c]

        # Bıyık ekle
        if y_offset_mustache >= 0 and x_offset_mustache >= 0:
            for c in range(0, 3):
                image[y_offset_mustache:y_offset_mustache+mustache.shape[0], x_offset_mustache:x_offset_mustache+mustache.shape[1], c] = \
                    (1.0 - mustache_alpha) * image[y_offset_mustache:y_offset_mustache+mustache.shape[0], x_offset_mustache:x_offset_mustache+mustache.shape[1], c] + \
                    mustache_alpha * mustache[:, :, c]

    display_image(image)

btn_select = tk.Button(root, text="Fotoğraf Seç", command=select_image)
btn_select.pack()  # İstenilen boyutu belirtmek için bu satırı kullanabilirsiniz

root.mainloop()
