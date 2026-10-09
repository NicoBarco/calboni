from PIL import Image

image = Image.open("calboni.png").convert("RGBA")

image.save(
    "calboni.ico",
    format="ICO",
    sizes=[(16, 16), (32, 32), (48, 48),
           (64, 64), (128, 128), (256, 256)]
)