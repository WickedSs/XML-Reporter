import xml.etree.ElementTree as ET
from Elements.Elements import *
from reportlab.lib.units import inch, cm, px, mm
from PDF import PDF
import os, sys, re

BASE_DIR = os.path.dirname(__file__)

class Generator:
    def __init__(self):
        self.known_sections = [
            "title", "pageHeader", "columnHeader", "groupheader", "detail", "groupfooter", "columnFooter",
            "pageFooter", "lastpagefooter", "summary", "nodata", "background"
        ]
        self.sections = {}
        self.parameters = []
        self.fields = []
        self.xmlns = ""
        self.pdf = PDF()

    def set_paramaters(self, parameters_values):
        for parameter in self.parameters:
            return

    def parse_file(self, filename: str):
        file_path = os.path.join(BASE_DIR, "reports", filename)
        self.pdf.create_pdf(filename.split(".")[0])
        return ET.parse(file_path)

    def extract_tags(self, tree: ET):
        root = tree.getroot()
        for child in root:
            tag = re.sub(r'{.+}', '', str(child.tag)).rstrip().lstrip()
            match tag:
                case "parameter":
                    self.parameters.append(child)
                case "field":
                    self.fields.append(child)
                case _:
                    if tag in self.known_sections:
                        self.sections[tag] = {}
                        self.sections[tag]["element"] = child
                        self.sections[tag]["bands"] = []

    def process_section(self):
        for section in self.sections:
            element = self.sections.get(section).get("element");
            if "detail" in section:
                self.process_detail_band(element)
            else:
                self.process_default_band(section, element)

    def process_default_band(self, section, element):
        band = element.find("{http://jasperreports.sourceforge.net/jasperreports}band")
        for element in band:
            element_name = re.sub(r'{.+}', '', str(element.tag)).rstrip().lstrip()
            match element_name:
                case "staticText":
                    _new_element = StaticText(element).parse()
                    # print(f"[StaticText] {_new_element.coords} {_new_element.text}")
                    self.sections.get(section).get("bands").append(_new_element)
                case "textField":
                    _new_element = TextField(element).parse()
                    # print(f"[TextField] {_new_element.coords}")
                    self.sections.get(section).get("bands").append(_new_element)
                case "rectangle":
                    _new_element = Rectangle(element).parse()
                    # print(f"[Rectangle] {_new_element.coords}")
                    self.sections.get(section).get("bands").append(_new_element)


    def process_detail_band(self, section):
        return

    def generate_pdf(self):
        for element in self.sections:
            bands = self.sections.get(element).get("bands")
            for band in bands:
                match band.name:
                    case "StaticText":
                        self.pdf.draw_string(band.coords, band.font, band.text)
                        break
                    case _:
                        pass

        self.pdf.save_pdf()


    def run(self, filename: str):
        tree = self.parse_file(filename)
        self.extract_tags(tree)
        self.process_section()
        self.generate_pdf()
        
    

reporter = Generator()
reporter.run("Asma01.jrxml")