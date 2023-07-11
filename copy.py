import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk

# Create this function last
def apply_watermark(image_path, watermark_text):
    image = Image.open(image_path)

    overlay = Image.new(mode="RGBA", size=image.size, color=(0, 0, 0, 0))
    rgba_image = image.convert(mode="RGBA") # convert the image to be in the same mode as the overlay so that they are compatible to make a composite

    font = ImageFont.truetype("arial.ttf", 40)
    text_color = (255, 255, 255, 128)

    text_width, text_height = font.getsize(watermark_text)
    x = (image.width - text_width) // 2
    y = (image.height - text_height) // 2

    draw = ImageDraw.Draw(overlay) # draw on the overlay and then you will slay that layer onto the image layer
    draw.text(text=watermark_text, font=font, fill=text_color, xy=(x,y))

    watermarked_image = Image.alpha_composite(rgba_image, overlay)
    watermarked_image.save('watermarked_image.png')

# Create this function second to get the image_path for the apply_watermark function
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

    if file_path:
        image = Image.open(file_path) # Pillow opens the photo file and assigns it to a variable "image"
        image = image.resize((300, 300)) # Here we resize the image by calling the resize function and passing in the desired dimensions to the image
        photo = ImageTk.PhotoImage(image) # Here the ImageTk.PhotoImage() method converts the image to a 'PhotoImage' that tkinter can handle, we assign the new img to a var named photo

        image_preview.config(image=photo) # Here we are updating the image_preview component in the GUI with the new image via the .config() method
        image_preview.image = photo # Then the 'image_preview.image' attribute is assigned the 'photo' object to be displayed in the GUI

        watermark_button.config(state=tk.NORMAL)
        watermark_text_entry.config(state=tk.NORMAL)
        watermark_text_entry.delete(0, tk.END)
        watermark_text_entry.focus()

        global selected_image_path
        selected_image_path = file_path

# Create this function third to get the watermark_text for the apply_watermark function
def get_watermark():
    watermark_text = watermark_text_entry.get()

    if watermark_text:
        apply_watermark(selected_image_path, watermark_text)

        tk.messagebox.showinfo(title="Success", message="Watermark successfully applied!")

# Set up the GUI first then build the functions after
window = tk.Tk()
window.title("Watermarking App")

image_preview = tk.Label(master=window)
image_preview.pack(pady=10, padx=10)

open_button = tk.Button(master=window, text="Open Image", command=open_file)
open_button.pack(pady=5)

watermark_text_entry = tk.Entry(master=window, state=tk.DISABLED)
watermark_text_entry.pack(pady=5)

watermark_button = tk.Button(master=window, text="Apply Watermark", state=tk.DISABLED, command=get_watermark)
watermark_button.pack(pady=5)

window.mainloop()

