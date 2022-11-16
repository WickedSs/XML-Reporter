from Elements.Objects import *
from typing import Any, Union
from math import ceil


class StaticText(Util, ReportElement, TextElement, Text):
    
    def __init__(self, element):
        super().__init__()
        self.name = "StaticText"
        self.element = element
        self.subElements = []

    
    def run(self, url):
        self.subElements.append(ReportElement().fetch(self.element, url))
        self.subElements.append(TextElement().fetch(self.element, url))
        self.subElements.append(Text().fetch(self.element, url))
        return self

    def draw(self, canvas, section_height, margin, size, direction: Any = None, charSpace: str = 0, mode: Any = None, wordSpace: str = None):
        coords_element, font_element, text_element = self.subElements
        x = int(coords_element.coords.get("x"))
        y = int(coords_element.coords.get("y"))
        width = int(coords_element.coords.get("width"))
        height = int(coords_element.coords.get("height"))
        x, y = Util.coord(x, y, width, height, section_height, margin, size)
        fontFamily = "Arial" if font_element.font.get("fontName") == None else font_element.font.get("fontName")
        fontSize = 11 if font_element.font.get("size") == None else int(font_element.font.get("size")) + 4
        print("fontsize:", fontSize)
        canvas.pdf.setFont(fontFamily, fontSize)
        canvas.pdf.circle(x, y, 5, 1, 0)
        canvas.pdf.drawString(x, y, text_element.text, mode, charSpace, direction, wordSpace)



class TextField(Util, ReportElement, TextElement, textFieldExpression):
    
    def __init__(self, element):
        super().__init__()
        self.name = "TextField"
        self.element = element
        self.subElements = []
    
    def run(self, url):
        self.subElements.append(ReportElement().fetch(self.element, url))
        self.subElements.append(TextElement().fetch(self.element, url))
        self.subElements.append(textFieldExpression().fetch(self.element, url))
        return self

    def draw(self, canvas, section_height, margin, size, direction: Any = None, charSpace: str = 0, mode: Any = None, wordSpace: str = None):
        coords_element, font_element, text_expression = self.subElements
        # print(vars(coords_element), vars(font_element), vars(text_expression))
        x = int(coords_element.coords.get("x"))
        y = int(coords_element.coords.get("y"))
        width = int(coords_element.coords.get("width"))
        height = int(coords_element.coords.get("height"))
        x, y = Util.coord(x, y, width, height, section_height, margin, size)
        fontFamily = "Arial" if font_element.font.get("fontName") == None else font_element.font.get("fontName")
        fontSize = 11 if font_element.font.get("size") == None else int(font_element.font.get("size")) + 4
        print("fontsize:", fontSize)
        canvas.pdf.setFont(fontFamily, fontSize)
        canvas.pdf.circle(x, y, 5, 1, 0)
        canvas.pdf.drawString(x, y, "", mode, charSpace, direction, wordSpace)
        


class Rectangle(Util, ReportElement, GraphicElement):
    
    def __init__(self, element):
        super().__init__()
        self.name = "Rectangle"
        self.element = element
        self.element_attrib = self.element.attrib
        self.subElements = []
    
    def run(self, url):
        self.subElements.append(ReportElement().fetch(self.element, url))
        self.subElements.append(GraphicElement().fetch(self.element, url))
        return self

    def draw(self, canvas, section_height, margin, size, stroke: int = 0, fill: int = 0):
        coords_element, graphic_element = self.subElements
        x = int(coords_element.coords.get("x"))
        y = int(coords_element.coords.get("y"))
        width = int(coords_element.coords.get("width"))
        height = int(coords_element.coords.get("height"))
        x, y = Util.coord(x, y, width, height, section_height + ( height - (margin[0] / 2) ), margin, size)
        canvas.pdf.setStrokeColorRGB(0, 0, 0)
        if self.element_attrib.get("radius") != None:
            radius = ceil(float(self.element_attrib.get("radius")))
            stroke = 1 if float(graphic_element.pen.get("lineWidth")) == 0.0 and radius > 0 else ceil(float(graphic_element.pen.get("lineWidth")))
            canvas.pdf.roundRect(x, y, width, height, radius, stroke, fill)
        else:
            stroke = 1 if float(graphic_element.pen.get("lineWidth")) == 0.0 else ceil(float(graphic_element.pen.get("lineWidth")))
            canvas.pdf.rect(x, y, width, height, stroke, fill)
        
        canvas.pdf.circle(x, y, 5, 1, 0)
