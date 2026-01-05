from PIL import Image

img = Image.open("HandMadeImages/bottomCELL.png").convert("RGBA")
pixels = img.load()

width, height = img.size

for y in range(height):
    for x in range(width):
        r, g, b, a = pixels[x, y]
        if r == 255 and g == 255 and b == 255:
            pixels[x, y] = (255, 255, 255, 0)  # transparent

img.save("bottomCELL2.png")