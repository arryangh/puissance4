from PIL import Image

img = Image.open("HandMadeImages/folder.png").convert("RGBA")
pixels = img.load()

width, height = img.size



for y in range(height):
    for x in range(width):
        r, g, b, a = pixels[x, y]
        if r >= 150 and g >= 150 and b >= 150:
            pixels[x, y] = (255, 255, 255, 0)  # transparent

img.save("HandMadeImages/folder2.png")