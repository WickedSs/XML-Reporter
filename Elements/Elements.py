import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import inspect, sys


URL = "{http://jasperreports.sourceforge.net/jasperreports}"


class Base:
    def __init__(self):
        self.coords = None
        self.alignement = None
        self.font = None
        self.paragraph = None
        self.lineStyle = None
        self.text = None
        self.base_classes = [object, Base, TextField, Rectangle]


    def reportElement(self):
        report_element = self.element.find(f"{URL}reportElement")
        if report_element != None:
            self.coords = report_element.attrib


    def textElement(self):
        text_element = self.element.find(f"{URL}textElement")
        if text_element != None:
            self.alignement = text_element.attrib
            self.font = text_element.find(f"{URL}font").attrib if text_element.find(f"{URL}font") != None else None
            self.paragraph = text_element.find(f"{URL}paragraph").attrib if text_element.find(f"{URL}paragraph") != None else None

    def graphicElement(self):
        graphic_element = self.element.find(f"{URL}graphicElement")
        if graphic_element != None:
            self.lineStyle = graphic_element.find(f"{URL}pen").attrib if graphic_element.find(f"{URL}pen") != None else None

    def textValue(self):
        text_element = self.element.find(f"{URL}text")
        if text_element != None:
            self.text = text_element.text

    def parse(self):
        self.reportElement()
        self.textElement()
        self.graphicElement()
        self.textValue()
        return self


class StaticText(Base):
    def __init__(self, element: Element):
        self.element = element
        self.name = "StaticText"
        super().__init__()

    def draw(self):
        return


class TextField(Base):
    def __init__(self, element: Element):
        self.element = element
        self.name = "TextField"
        super().__init__()

    def draw(self):
        return
        

class Rectangle(Base):
    def __init__(self, element: Element):
        self.element = element
        self.name = "Rectangle"
        super().__init__()

    def draw(self):
        return