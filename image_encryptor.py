import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

# --- Image Encryption / Decryption Functions ---
def encrypt_image(img, key):
    img_array = np.array(img, dtype=np.uint16)  # allow temporary >255
    encrypted_array = (img_array + key) % 256
    return Image.fromarray(encrypted_array.astype(np.uint8))

def decrypt_image(img, key):
    img_array = np.array(img, dtype=np.uint16)
    decrypted_array = (img_array - key) % 256
    return Image.fromarray(decrypted_array.astype(np.uint8))

# --- GUI Functions ---
def browse_image():
    global original_image
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        original_image = Image.open(file_path).convert("RGB")
        show_image(original_image, original_panel)

def show_image(img, panel):
    img_resized = img.resize((300, 300))
    tk_img = ImageTk.PhotoImage(img_resized)
    panel.config(image=tk_img)
    panel.image = tk_img

def process_image(mode):
    global processed_image
    if original_image is None:
        messagebox.showerror("Error", "Please select an image first!")
        return
    try:
        key = int(key_entry.get())
        if not (1 <= key <= 255):
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Key must be an integer between 1 and 255.")
        return
    
    if mode == "encrypt":
        processed_image = encrypt_image(original_image, key)
    else:
        processed_image = decrypt_image(original_image, key)

    show_image(processed_image, processed_panel)

def save_processed_image():
    if processed_image is None:
        messagebox.showerror("Error", "No processed image to save!")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".png", 
                                             filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])
    if file_path:
        processed_image.save(file_path)
        messagebox.showinfo("Success", "Image saved successfully!")

# --- Main Window ---
root = tk.Tk()
root.title("Simple Image Encryption Tool")
root.geometry("800x600")
root.configure(bg="#d4e6f1")

original_image = None
processed_image = None

# Title
title_label = tk.Label(root, text="🔒 Simple Image Encryption Tool", font=("Helvetica", 20, "bold"), bg="#d4e6f1", fg="#1f618d")
title_label.pack(pady=10)

# Browse Button
browse_btn = tk.Button(root, text="Browse Image", command=browse_image, bg="#5dade2", fg="white", font=("Arial", 12), width=20)
browse_btn.pack(pady=10)

# Key Entry
key_label = tk.Label(root, text="Enter Key (1-255):", font=("Arial", 12), bg="#d4e6f1")
key_label.pack()
key_entry = tk.Entry(root, font=("Arial", 12), justify="center")
key_entry.pack(pady=5)

# Encrypt / Decrypt / Save Buttons (Always Visible Here)
frame_buttons = tk.Frame(root, bg="#d4e6f1")
frame_buttons.pack(pady=10)
btn_encrypt = tk.Button(frame_buttons, text="Encrypt", command=lambda: process_image("encrypt"), bg="#58d68d", width=15, height=2)
btn_encrypt.pack(side=tk.LEFT, padx=10)
btn_decrypt = tk.Button(frame_buttons, text="Decrypt", command=lambda: process_image("decrypt"), bg="#f5b041", width=15, height=2)
btn_decrypt.pack(side=tk.LEFT, padx=10)
btn_save = tk.Button(frame_buttons, text="Save Processed Image", command=save_processed_image, bg="#85c1e9", width=20, height=2)
btn_save.pack(side=tk.LEFT, padx=10)

# Panels for Original & Processed Images
frame_images = tk.Frame(root, bg="#d4e6f1")
frame_images.pack(pady=10)
original_panel = tk.Label(frame_images, bg="#d4e6f1")
original_panel.pack(side=tk.LEFT, padx=20)
processed_panel = tk.Label(frame_images, bg="#d4e6f1")
processed_panel.pack(side=tk.LEFT, padx=20)

root.mainloop()
