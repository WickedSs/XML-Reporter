from reportlab.pdfgen import canvas
import xml.etree.ElementTree as ET
from reportlab.lib.units import inch, cm, px, mm
from reportlab.lib.pagesizes import letter, A4, A0_Pixel
from typing import Any, Union
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont

import os, sys

BASE_DIR = os.path.dirname(__file__)

class PDF:
    def __init__(self, current_height: int = 0):
        self.dimensions = A4
        self.register_fonts()
        self.current_height = current_height

    def set_height(self, value):
        self.current_height += value

    def register_fonts(self):
        registerFont(TTFont("Arial", os.path.join(BASE_DIR, "fonts", f"Arial.ttf")))
        registerFont(TTFont("Bahnschrift", os.path.join(BASE_DIR, "fonts", f"Bahnschrift.ttf")))

    def create_pdf(self, filename: str):
        self.path = os.path.join(BASE_DIR, "pdfs", f"test01.pdf")
        self.pdf = canvas.Canvas(self.path, pagesize=letter, bottomup=1, )

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, line_width: float = .3):
        self.pdf.setLineWidth(line_width)
        self.pdf.setStrokeColorRGB(255, 0, 0)
        self.pdf.line(x1, y1, x2, y2)

    def draw_circle(self, x, y, radius, color: tuple, stroke: int = 1, fill: int = 0):
        self.pdf.setStrokeColorRGB(color[0], color[1], color[2])
        self.pdf.circle(x, y, radius, stroke, fill)

    def draw_image(self, x, y, imagePath):
        self.pdf.drawImage(imagePath, x, y, 
            width=None, height=None, mask=None, preserveAspectRatio=False, 
            anchor='c', anchorAtXY=False, showBoundary=False
        )

    def set_font(self, fontname: str = "Arial", size: int = 11):
        self.pdf.setFont(fontname, size)

    
    def coord(self, x, y, width, height, unit=1.33):
        x, y = x * unit, (y + height + self.current_height) * unit
        return x, y

    def new_page(self):
        self.pdf.showPage()

    def save_pdf(self):
        self.pdf.save()
