from reportlab.pdfgen import canvas
import xml.etree.ElementTree as ET
from reportlab.lib.units import inch, cm, px, mm
from reportlab.lib.pagesizes import letter
from typing import Any, Union
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont

import os, sys

BASE_DIR = os.path.dirname(__file__)

class PDF:
    def __init__(self):
        self.width, self.height = letter
        self.mmConv = 0.2645833333
        registerFont(TTFont("Arial", os.path.join(BASE_DIR, "fonts", f"Arial.ttf")))

    def create_pdf(self, filename: str):
        self.path = os.path.join(BASE_DIR, "pdfs", f"test01.pdf")
        self.pdf = canvas.Canvas(self.path, pagesize=letter)
        # self.pdf.translate(0, self.height)

    def draw_string(self, coords, font, text, direction: Any = None, charSpace: str = 0, mode: Any = None, wordSpace: str = None):
        x, y = self.coord(int(coords.get("x")) * self.mmConv, int(coords.get("y")) * self.mmConv, mm)
        fontFamily = "Arial" if font.get("fontName") == None else font.get("fontName")
        fontSize = 11 if font.get("size") == None else int(font.get("size"))
        self.pdf.setFont(fontFamily, fontSize)
        print(x, y, text)
        self.pdf.drawString(x, y, text, mode, charSpace, direction, wordSpace)

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, line_width: float = .3):
        self.pdf.setLineWidth(line_width)
        self.pdf.line(x1, y1, x2, y2)

    def draw_circle(self, x, y, radius, color: tuple, stroke: int = 1, fill: int = 0):
        self.pdf.setStrokeColorRGB(color)
        self.pdf.circle(x, y, radius, stroke, fill)

    def draw_rectange(self):
        self.pdf

    def draw_image(self, x, y, imagePath):
        self.pdf.drawImage(imagePath, x, y, 
            width=None, height=None, mask=None, preserveAspectRatio=False, 
            anchor='c', anchorAtXY=False, showBoundary=False
        )

    def set_font(self, fontname: str = "Arial", size: int = 11):
        self.pdf.setFont(fontname, size)

    
    def coord(self, x, y, unit=1):
        x, y = x * unit, (y + (self.height - y)) * unit
        return x, y

    def save_pdf(self):
        self.pdf.save()
