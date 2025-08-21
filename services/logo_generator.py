from google import genai
from google.genai import types

import config

import typing
import os
from datetime import datetime

from PIL import Image as PIL_Image
from PIL import ImageOps as PIL_ImageOps

client = genai.Client(
    vertexai=True, project=config.PROJECT_ID, location=config.LOCATION
)


def display_image(
    image,
    max_width: int = 700,
    max_height: int = 400,
) -> None:
    pil_image = typing.cast(PIL_Image.Image, image._pil_image)
    if pil_image.mode != "RGB":
        # RGB is supported by all Jupyter environments (e.g. RGBA is not yet)
        pil_image = pil_image.convert("RGB")
    image_width, image_height = pil_image.size
    if max_width < image_width or max_height < image_height:
        # Resize to display a smaller notebook image
        pil_image = PIL_ImageOps.contain(pil_image, (max_width, max_height))

    # Use PIL's show() method for regular Python scripts instead of IPython.display
    pil_image.show()

    # Create images directory if it doesn't exist
    os.makedirs("images", exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_logo_{timestamp}.png"
    filepath = os.path.join("images", filename)

    # Save the image in the images folder
    pil_image.save(filepath)
    print(f"Image displayed and saved as '{filepath}'")

    # Also save a copy as 'generated_logo.png' in the root for backward compatibility
    pil_image.save("generated_logo.png")
    print("Also saved a copy as 'generated_logo.png' in the root directory")


prompt = """
A white wall with two Art Deco travel posters mounted. First poster has the text: "NEPTUNE", tagline: "The jewel of the solar system!' Second poster has the text: "JUPITER", tagline: "Travel with the giants!
"""

image = client.models.generate_images(
    model="imagen-4.0-ultra-generate-001",
    prompt=prompt,
    config=types.GenerateImagesConfig(
        aspect_ratio="16:9",
        number_of_images=1,
        image_size="2K",
        safety_filter_level="BLOCK_MEDIUM_AND_ABOVE",
        person_generation="ALLOW_ADULT",
    ),
)

display_image(image.generated_images[0].image)
