from PIL import Image, ImageOps
import os
# Open the image
image = Image.open(os.path.expanduser('~\\PycharmProjects\\Sniff0_Scripts\\multimedia\\images\\dot_white.jpg'))

# Convert to negative
downsampled_image = image.resize((1280, 800))

# Save the negative image
downsampled_image.save(os.path.expanduser('~\\PycharmProjects\\Sniff0_Scripts\\multimedia\\images\\dot_white_proj.jpg'))

# Show the image (optional)
downsampled_image.show()
