import tkinter as tk
from PIL import Image, ImageDraw

"""
bleu utilisé dans le jeu
body_color="#FFF4CC", border_color="#D4B24C"
"""



def generate_cell_images(body_color="#FFF4CC", border_color="#D4B24C", size=1500, border_width=30):
    """
    Génère les deux images de cellules en haute qualité
    """

    # Marge pour le cercle
    circle_margin = int(size * 0.12)
    half_border = border_width * 2

    # ========== NORMAL CELL ==========
    img_normal = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw_normal = ImageDraw.Draw(img_normal)

    # Fond
    draw_normal.rectangle([0, 0, size, size], fill=body_color)

    # Bordures
    draw_normal.rectangle([0, 0, border_width, size], fill=border_color)
    draw_normal.rectangle([size - border_width, 0, size, size], fill=border_color)

    # Cercle (contour)
    draw_normal.ellipse(
        [circle_margin, circle_margin, size - circle_margin, size - circle_margin],
        outline=border_color,
        width=int(border_width * 1.5)
    )

    # Trou transparent
    hole_margin = circle_margin + int(border_width * 0.75)
    draw_normal.ellipse(
        [hole_margin, hole_margin, size - hole_margin, size - hole_margin],
        fill=(0, 0, 0, 0)
    )

    img_normal.save("normalCELL.png", "PNG")
    print("✅ normalCELL.png généré (1500x1500)")

    # ========== BOTTOM CELL ==========
    img_bottom = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw_bottom = ImageDraw.Draw(img_bottom)

    # Fond
    draw_bottom.rectangle([0, 0, size, size], fill=body_color)

    # Bordures
    draw_bottom.rectangle([0, 0, border_width, size], fill=border_color)
    draw_bottom.rectangle([size - border_width, 0, size, size], fill=border_color)
    draw_bottom.rectangle(
        [-half_border, size - border_width, size + half_border, size],
        fill=border_color
    )

    # Cercle (contour)
    draw_bottom.ellipse(
        [circle_margin, circle_margin, size - circle_margin, size - circle_margin],
        outline=border_color,
        width=int(border_width * 1.5)
    )

    # Trou transparent
    hole_margin = circle_margin + int(border_width * 0.75)
    draw_bottom.ellipse(
        [hole_margin, hole_margin, size - hole_margin, size - hole_margin],
        fill=(0, 0, 0, 0)
    )

    img_bottom.save("bottomCELL.png", "PNG")
    print("✅ bottomCELL.png généré (1500x1500)")


# Génération
generate_cell_images(body_color="#1B62F1", border_color="#143B6C")
# generate_cell_images(body_color="#FF62C2", border_color="#E12E8B")