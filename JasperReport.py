import os, sys, re
from math import ceil
from elements.Elements import TextField, StaticText, Rectangle
from elements.Objects import Util
import xml.etree.ElementTree as ET
from PDF import PDF


BASE_DIR = os.path.dirname(__file__)


class Element:

    def __init__(self):
        self.band_elements = []

    def process_elements(self, url, band):
        for child in band:
            element_name = re.sub(r'{.+}', '', str(child.tag)).rstrip().lstrip()
            match element_name:
                case "staticText":
                    _new_element = StaticText(child).run(url)
                    self.band_elements.append(_new_element)
                case "textField":
                    _new_element = TextField(child).run(url)
                    self.band_elements.append(_new_element)
                case "rectangle":
                    _new_element = Rectangle(child).run(url)
                    self.band_elements.append(_new_element)


class Section(Element):
    
    def __init__(self, name, section, fields):
        super().__init__()
        self.section = section
        self.section_name = name
        self.section_band = None
        self.section_band_attrib = None
        self.fields = fields

    def parse_section(self, url):
        self.section_band = self.section.find(f"{url}band")
        self.section_band_attrib = self.section.find(f"{url}band").attrib
        self.process_elements(url, self.section_band)
        return self


class Paramater:
    
    def __init__(self, parameter):
        self.paramater = parameter
        self.name = parameter.get("name")
        self.type = parameter.get("class").split(".")[-1]
        self.description = None
        self.value = ""

    def parse_paramater(self, url):
        desription_paramater = self.paramater.find(f"{url}parameterDescription")
        if desription_paramater != None:
            self.description = desription_paramater.text


class Field:

    def __init__(self, field):
        self.field = field
        self.name = field.get("name")
        self.type = field.get("class").split(".")[-1]
        self.value = ""

    def parse_field(self, url):
        pass


class JasperReport:

    def __init__(self, parameters, fields):
        self.known_sections = [ "title", "pageHeader", "columnHeader", "groupheader", "detail", "groupfooter", "columnFooter",
            "pageFooter", "lastpagefooter", "summary", "nodata", "background" ]
        self.pdf = PDF()
        self.URL = None
        self.paramaters_values = parameters
        self.fields_values = fields
        self.report_parameters = []
        self.report_fields = []
        self.sections = []

    def open_file(self, filename: str):
        file_path = os.path.join(BASE_DIR, "reports", filename)
        return ET.parse(file_path).getroot()

    def get_url_suffix(self):
        for attribute in self.attrib:
            if "schemaLocation" in attribute:
                self.URL = "{" + self.attrib.get(attribute).split(" ")[0] + "}"

    def process_detail_band(self, name, child):
        row_count, curr_height = 0, 0
        for row in self.fields_values:
            new_section = Section(f"{name}_{row_count}", child, row).parse_section(self.URL)
            curr_height += int(new_section.section_band_attrib.get("height"))
            self.sections.append(new_section)
            row_count += 1

        return curr_height

    def parse_sections(self):
        for child in self.root:
            section_name = re.sub(r'{.+}', '', str(child.tag)).rstrip().lstrip()
            match section_name:
                case "parameter":
                    new_parameter = Paramater(child)
                    new_parameter.value = self.paramaters_values.get(new_parameter.name)
                    new_parameter.parse_paramater(self.URL)
                    self.report_parameters.append(new_parameter)
                case "field":
                    _new_field = Field(child)
                    self.report_fields.append(_new_field)
                case _:
                    if section_name == "detail":
                        self.process_detail_band(section_name, child)
                    else:
                        new_section = Section(section_name, child, {}).parse_section(self.URL)
                        self.sections.append(new_section)
                 
    def draw_sections(self):
        current_v_position = 0
        for section in self.sections:
            if current_v_position >= self.height - self.document_margin[2] * 6:
                self.pdf.new_page()
                current_v_position = 0

            # print(f"{section.section_name} {current_v_position}")
            for element in section.band_elements:
                element.prepare(canvas=self.pdf, section=section, jasperAttrib=self.attrib, jasperMargin=self.document_margin, jasperParameters=self.paramaters_values, current_v_position=current_v_position)
                if element.name in ["StaticText", "TextField"]:
                    self.pdf.pdf_canvas.drawString(element.x + element.indentation, element.y, element.text_value, None, 0, None, None)
                    print(f"{element.name, element.x, element.y, self.height - self.document_margin[0]} {element.text_value}")
                elif element.name in ["Rectangle"]:
                    self.pdf.pdf_canvas.roundRect(element.x, element.y, element.width, element.height, float(element.radius) if element.radius else 0, ceil(element.stroke), element.fill)
                
            current_v_position += int(section.section_band_attrib.get("height") or 0)
        # self.pdf.show_page()
        self.pdf.save_pdf()

    def run(self, filename):
        self.root = self.open_file(filename)
        self.attrib = self.root.attrib
        self.height = int(self.attrib.get("pageHeight"))
        self.document_margin = [int(self.attrib.get(f"{side}Margin")) for side in ["top", "right", "bottom", "left"]]
        self.pdf.create_pdf(filename.split(".")[0], self.document_margin)
        self.get_url_suffix()
        self.parse_sections()
        self.draw_sections()
        

paramaters = {
    "Buyer" : "Souleymane Guerida",
    "OperationDate" : "10-12-2022",
    "BC" : "12",
    "DateBC" : "10-12-2022",
    "BL" : "15",
    "DateBL" : "15-12-2022",
    "FactureNumber" : "10/2022",
    "FactureTotal" : "12000",
    "PriceInWords" : "Twelve hundereds Dinars",
    "Address" : "Rue Kaddour Ben Litim N 34",
    "TVA" : "19",
    "FactureTVA" : "1200",
    "ValidationDate" : "25-12-2022",
    "ClientTelephone" : "0664436207",
    "sellingType" : "U",
    "clientRC" : "1543513541351",
    "clientCA" : "5465453135",
    "clientMF" : "54185431",
    "clientNIS" : "56454351",
    "clientAI" : "541854351",
    "NoNamePayable" : "Paid",
    "CompteBNA" : "54385435184385435 54",
    "Language" : "Arabic",
}
fields = [
    { "product_name" : "First Product", "quantity" : "10", "price": "1200.5", "total" : str(1200 * 10), "reference" : ""},
    { "product_name" : "Second Product", "quantity" : "12", "price": "900.59", "total" : str(1200 * 10), "reference" : ""},
    { "product_name" : "Third Product", "quantity" : "5", "price": "1560.45", "total" : str(1200 * 10), "reference" : ""},
    { "product_name" : "Fourth Product", "quantity" : "6", "price": "100", "total" : str(1200 * 10), "reference" : ""},
    { "product_name" : "Fourth Product", "quantity" : "6", "price": "100", "total" : str(1200 * 10), "reference" : ""},
    { "product_name" : "Fourth Product", "quantity" : "6", "price": "100", "total" : str(1200 * 10), "reference" : ""},
    { "product_name" : "Fourth Product", "quantity" : "6", "price": "100", "total" : str(1200 * 10), "reference" : ""},
    { "product_name" : "Fourth Product", "quantity" : "6", "price": "100", "total" : str(1200 * 10), "reference" : ""},
    { "product_name" : "Fourth Product", "quantity" : "6", "price": "100", "total" : str(1200 * 10), "reference" : ""},
    { "product_name" : "Fourth Product", "quantity" : "6", "price": "100", "total" : str(1200 * 10), "reference" : ""},
    { "product_name" : "Fourth Product", "quantity" : "6", "price": "100", "total" : str(1200 * 10), "reference" : ""},
    { "product_name" : "Fourth Product", "quantity" : "6", "price": "100", "total" : str(1200 * 10), "reference" : ""},
    { "product_name" : "Fourth Product", "quantity" : "6", "price": "100", "total" : str(1200 * 10), "reference" : ""},
]
reporter = JasperReport(parameters=paramaters, fields=fields)
reporter.run("NoName-M02.jrxml")