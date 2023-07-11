# import tkinter as tk
# from tkinter import filedialog
#
# from PIL import Image, ImageDraw, ImageFont
#
# root = tk.Tk() # initialize GUI (create the window)
# root.withdraw() # closes the window created from root = tk.Tk()
#
# filename = filedialog.askopenfilename(initialdir='images', title='Select an Image:') # retrieves the filename from the user
# ## print(filename) ### check to see if the filedialog window pops up then comment out
#
# def add_watermark(image, watermark_text): # create function to add watermark to image, so it requires an image argument & a text argument to display on the image
#     # CREATES THE IMAGE OBJECT
#     opened_image = Image.open(image) # create an image object
#
#     # GET THE IMAGE SIZE (HEIGHT AND WIDTH)
#     image_width, image_height = opened_image.size # opened_image.size gives the dimensions of the image, and we are assigning the dimensions to the
#                                                   # image_width and image_height variables to we can reference them later
#     # DRAW ON THE IMAGE
#     draw = ImageDraw.Draw(opened_image) # create an ImageDraw object by passing the opened image to the ImageDraw.Draw() function
#                                         # ImageDraw.Draw() provides a convenient way to draw shapes and text on images
#     # SPECIFY A FONT SIZE
#     font_size = int(image_width/8)  # aspect ratio goes inside the () the more text you want, the larger you need to set the denominator and vice versa
#
#     # FOR WINDOWS, CHANGE FONT TYPE TO "arial" not "Arial"
#     font = ImageFont.truetype('arial.ttf', font_size) # designate font for the watermark, lowercase acceptable for windows OS
#
#     # COORDINATES FOR WHERE WE WANT TO PLACE THE IMAGE TEXT
#     x, y = int(image_width/2), int(image_height/2) # this will place the watermark text at the center of the image
#
#     # ADD THE WATERMARK
#     draw.text((x,y), watermark_text, font=font, fill="#FFF", stroke_width=5, stroke_fill="#222", anchor='ms') # argument requires tuple of x, y coordinates,
#                                                                                                               # the watermark text, the font, fill color,
#                                                                                                 # stroke width and stroke fill (outline and outline fill for text)
#                                                                                                               # and anchor='ms' will center the text on the image
#     # SHOW THE NEW IMAGE
#     opened_image.show()
#
# add_watermark(filename, "Hook 'Em Horns")

# ABOVE IS THE SIMPLER VERSION

# # Import necessary libraries

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk


def apply_watermark(image_path, watermark_text):
    # Open the image using Pillow
    image = Image.open(image_path)

    # Create a transparent overlay image
    overlay = Image.new(mode="RGBA", size=image.size, color=(0, 0, 0, 0)) # Image.new() method creates a new image with a specified size and color ex: Image.new(Mode, Size, Color)
#                                                           # RGBA - red, green, blue, alpha channels, first 3 values set the color, fourth value sets the opacity
#                                                           # RGB - red, green, blue, 3 values instead of 4 for the color tuple.

    # Specify the font, size, and color for the watermark text
    font = ImageFont.truetype("arial.ttf", 40) # specified font to verdana.ttf and size to 40
    text_color = (255, 255, 255, 128) # color is white, the 128 value indicates the transparency/opacity (0 means completely transparent)

    # Calculate the position to center the watermark text
    text_width, text_height = font.getsize(watermark_text)
    x = (image.width - text_width) // 2
    y = (image.height - text_height) // 2

    # Draw the watermark text onto the overlay image
    draw = ImageDraw.Draw(overlay)
    draw.text((x, y), watermark_text, font=font, fill=text_color)

    # Apply the overlay image as a watermark to the original image
    rgba_image = image.convert('RGBA')  # convert the image to RGBA, no need to convert the overlay image to RGBA bc it was already created as a RGBA image
    watermarked_image = Image.alpha_composite(rgba_image, overlay) # alpha_composite(image1, image2) method takes two images as parameters and merges them
#                                                                    # images must both be RGBA, hence, the A standing for alpha as in alpha composite

    # Save the watermarked image
    watermarked_image.save("watermarked_image.png") # save the image and specify the name, PNG files support transparent backgrounds so they're preferred
#                                                     # this will save the photo in the project file with the main.py file, not the file you selected the photo from

def open_file():
    # Ask the user to select an image file
    file_types = [("Image files", "*.jpg;*.png")]
    file_path = filedialog.askopenfilename(filetypes=file_types) # filedialog opens the files window
#                                                                                     # askopenfile() returns the full path to the selected file as a string
#                                                                                     # filetypes=[('any name you want to display', 'extension of file type')]
#                                                                                     # filetypes parameter ^^
    if file_path: # if the file path exists (if the selected photo exists)
        # Display the selected image in the GUI

        # Open the image using Pillow
        image = Image.open(file_path)

        # Resize the image to fit the label, otherwise the image may not appear because it does not fit the label
        image = image.resize((300, 300))

        # Convert the image to PhotoImage
        photo = ImageTk.PhotoImage(image) # the ImageTk.PhotoImage() method converts the image to a 'PhotoImage' that tkinter can handle

        # Update the image in the label
        image_preview.config(image=photo) # the .config() method is used to update the image in the 'image_preview' with the newly created 'PhotoImage'
        image_preview.image = photo # the 'image_preview.image' attribute is assigned the 'photo' object to be displayed in the GUI

        # Enable the watermark button
        watermark_button.config(state=tk.NORMAL) # state parameter allows you to enable or disable user interaction, normal is default state (enabled)
        watermark_text_entry.config(state=tk.NORMAL) # enabled the watermark button and watermark text entry
        watermark_text_entry.delete(0, tk.END) # clears the watermark text entry from 0 index to the END i.e. (0, tk.END)
        watermark_text_entry.focus() # .focus() method sets the focus to the text entry widget after the button is clicked

        # Store the selected file path into a variable so the watermarking function can reference it
        global selected_image_path # global makes the variable accessible to the whole program not just the function it is inside of
        selected_image_path = file_path


def watermark_image():
    # Get the entered watermark text
    watermark_text = watermark_text_entry.get()

    if watermark_text: # if there was an entry in the text entry box
        # Apply the watermark to the selected image
        apply_watermark(selected_image_path, watermark_text)

        # Show a success message
        tk.messagebox.showinfo(title="Success", message="Watermark applied successfully!")


# Create the main application window
window = tk.Tk()
window.title("Watermarking App")

# Create a label for the image preview
image_preview = tk.Label(master=window)
image_preview.pack(padx=10, pady=10)

# Create a button to open the image file
open_button = tk.Button(master=window, text="Open Image", command=open_file)
open_button.pack(pady=5)

# Create an entry for the watermark text
watermark_text_entry = tk.Entry(window, state=tk.DISABLED) # the watermark text entry is disabled until the watermark button is clicked, the button is enabled
watermark_text_entry.pack(pady=5)

# Create a button to apply the watermark
watermark_button = tk.Button(window, text="Apply Watermark", state=tk.DISABLED, command=watermark_image) # the button to apply the watermark is disabled until
                                                                                                         # a watermark is created
watermark_button.pack(pady=5)

# Start the Tkinter event loop
window.mainloop()
