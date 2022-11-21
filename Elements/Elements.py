from elements.Objects import *
from typing import Any, Union
from math import ceil
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

class StaticText(Util, ReportElement, TextElement, Text):
    
    def __init__(self, element):
        super().__init__()
        self.name = "StaticText"
        self.element = element
        self.subElements = []
        self.paragraph = None
        self.x, self.y = -10, -10

    def run(self, url):
        self.subElements.append(ReportElement().fetch(self.element, url))
        self.subElements.append(TextElement().fetch(self.element, url))
        self.subElements.append(Text().fetch(self.element, url))
        return self

    def prepare(self, canvas, section, jasperAttrib, jasperMargin, jasperParameters, current_v_position):
        size = [jasperAttrib.get("pageWidth"), jasperAttrib.get("pageHeight")]
        coords_element, text_element, text = self.subElements
        
        x = int(coords_element.coords.get("x"))
        y = int(coords_element.coords.get("y"))
        self.width = int(coords_element.coords.get("width"))
        self.height = int(coords_element.coords.get("height"))
        self.hAlignment = text_element.alignement.get("textAlignment")
        self.vAlignment = text_element.alignement.get("verticalAlignment") # always set to center
        self.text_value = text.text

        self.x, self.y = Util.coord(x, y, current_v_position + (self.height * 0.75), jasperMargin)
        # self.x, self.y = Util.new_page(self.x, self.y, jasperAttrib, jasperMargin, canvas)

        fontFamily = "Arial" if text_element.font.get("fontName") == None else text_element.font.get("fontName")
        fontSize = 11 if text_element.font.get("size") == None else int(text_element.font.get("size"))
        text_width = stringWidth(text.text, fontFamily, fontSize)
        self.indentation = Util.calculate_alignment(self.width, text_width, self.hAlignment)

        # print(f"{self.name} {x, y} {width, height} {indentation} {text.text} ")
        # print(f"{self.name} [{x, y}]")
        canvas.pdf_canvas.setFillColorRGB(0, 0, 0)
        canvas.pdf_canvas.setFont(fontFamily, fontSize)
        # canvas.pdf.circle(x, y, 5, 1, 0)
        # canvas.pdf_canvas.drawString(self.x + self.indentation, self.y, text.text, mode, charSpace, direction, wordSpace)


class TextField(Util, ReportElement, TextElement, textFieldExpression):
    
    def __init__(self, element):
        super().__init__()
        self.name = "TextField"
        self.element = element
        self.subElements = []
        self.x, self.y = -10, -10

    def run(self, url):
        self.subElements.append(ReportElement().fetch(self.element, url))
        self.subElements.append(TextElement().fetch(self.element, url))
        self.subElements.append(textFieldExpression().fetch(self.element, url))
        return self

    def prepare(self, canvas, section, jasperAttrib, jasperMargin, jasperParameters, current_v_position):
        size = [jasperAttrib.get("pageWidth"), jasperAttrib.get("pageHeight")]
        coords_element, text_element, text_expression = self.subElements
        
        self.text_value = ""
        if text_expression.expression_type == "parameter":
            parameter = jasperParameters.get(text_expression.expression)
            if parameter != None:
                self.text_value = parameter
        else:
            field = section.fields.get(text_expression.expression)
            # print(f"[{text_expression.expression_type}] {text_expression.expression} {field}")
            if field != None:
                self.text_value = field

        if text_expression.expression in ["price", "total", "FactureTVA", "FactureTotal"]:
            self.text_value = str(Util.format_currency(self.text_value))

        x = int(coords_element.coords.get("x"))
        y = int(coords_element.coords.get("y"))
        self.width = int(coords_element.coords.get("width"))
        self.height = int(coords_element.coords.get("height"))
        self.hAlignment = text_element.alignement.get("textAlignment")
        self.vAlignment = text_element.alignement.get("verticalAlignment") # always set
        
        self.x, self.y = Util.coord(x, y, current_v_position + (self.height * 0.75), jasperMargin)
        # self.x, self.y = Util.new_page(self.x, self.y, jasperAttrib, jasperMargin, canvas)

        fontFamily = "Arial" if text_element.font.get("fontName") == None else text_element.font.get("fontName")
        fontSize = 11 if text_element.font.get("size") == None else int(text_element.font.get("size"))
        text_width = stringWidth(self.text_value, fontFamily, fontSize)
        self.indentation = Util.calculate_alignment(self.width, text_width, self.hAlignment)
        
        if text_element.paragraph.get("leftIndent") != None:
            self.indentation += int(text_element.paragraph.get("leftIndent"))
        if text_element.paragraph.get("rightIndent") != None:
            self.indentation -= int(text_element.paragraph.get("rightIndent"))
        
        # print(f"{self.name} [{x, y}]")
        canvas.pdf_canvas.setFillColorRGB(0, 0, 0)
        canvas.pdf_canvas.setFont(fontFamily, fontSize)
        # canvas.pdf_canvas.drawString(self.x + self.indentation, self.y, self.text_value, mode, charSpace, direction, wordSpace)
        
class Rectangle(Util, ReportElement, GraphicElement):
    
    def __init__(self, element):
        super().__init__()
        self.name = "Rectangle"
        self.element = element
        self.element_attrib = self.element.attrib
        self.subElements = []
        self.x, self.y = -10, -10
    
    def run(self, url):
        self.subElements.append(ReportElement().fetch(self.element, url))
        self.subElements.append(GraphicElement().fetch(self.element, url))
        return self

    def prepare(self, canvas, section, jasperAttrib, jasperMargin, jasperParameters, current_v_position):
        size = [jasperAttrib.get("pageWidth"), jasperAttrib.get("pageHeight")]
        coords_element, graphic_element = self.subElements

        x = int(coords_element.coords.get("x"))
        y = int(coords_element.coords.get("y"))
        self.width = int(coords_element.coords.get("width"))
        self.height = int(coords_element.coords.get("height"))
        
        self.x, self.y = Util.coord(x, y, current_v_position, jasperMargin)
        # self.x, self.y = Util.new_page(self.x, self.y, jasperAttrib, jasperMargin, canvas)

        self.radius = self.element_attrib.get("radius")
        self.stroke = float(graphic_element.pen.get("lineWidth"))
        self.fill = 0
        backcolor = coords_element.coords.get("backcolor")

        if backcolor != None and backcolor != "#FFFFFF":
            r, g, b = Util.hex_to_RGB(backcolor.replace("#", ""))
            canvas.pdf_canvas.setFillColorRGB(r/255, g/255, b/255)
            self.fill = 1

        # print(f"{self.name} [{self.x, self.y}]")
        # print(f"{self.name} {x, y} {width, height} {backcolor} {float(radius) if radius else 0, stroke} {ceil(stroke)} {fill}")
        canvas.pdf_canvas.setStrokeColorRGB(0, 0, 0)
        # canvas.pdf_canvas.roundRect(self.x, self.y, self.width, self.height, float(self.radius) if self.radius else 0, ceil(self.stroke), self.fill)