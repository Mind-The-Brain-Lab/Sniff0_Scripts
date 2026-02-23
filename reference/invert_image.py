from PIL import Image, ImageOps
import os
# Open the image
image = Image.open(os.path.expanduser('~\\PycharmProjects\\Sniff0_Scripts\\multimedia\\images\\fixation_black.jpg'))  # Replace with your image file

# Convert to negative
negative_image = ImageOps.invert(image.convert("RGB"))

# Save the negative image
negative_image.save(os.path.expanduser('~\\PycharmProjects\\Sniff0_Scripts\\multimedia\\images\\fixation_negative.jpg'))

# Show the image (optional)
negative_image.show()
