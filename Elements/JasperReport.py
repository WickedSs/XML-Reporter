import os, sys, re
from Elements.Elements import TextField, StaticText, Rectangle



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
    
    def __init__(self, name, section, v_position):
        super().__init__()
        self.section = section
        self.section_name = name
        self.section_band = None
        self.section_band_attrib = None
        self.section_v_position = v_position

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

    def parse_paramater(self, url):
        desription_paramater = self.paramater.find(f"{url}parameterDescription")
        if desription_paramater != None:
            self.description = desription_paramater.text


class Field:
    def __init__(self, field):
        self.field = field
        self.name = field.get("name")
        self.type = field.get("class").split(".")[-1]

    def parse_field(self, url):
        pass


class JasperReport:
    def __init__(self, root):
        self.known_sections = [ "title", "pageHeader", "columnHeader", "groupheader", "detail", "groupfooter", "columnFooter",
            "pageFooter", "lastpagefooter", "summary", "nodata", "background" ]
        self.root = root
        self.jasperReport = root.attrib
        self.document_margin = [int(self.jasperReport.get(f"{side}Margin")) for side in ["top", "right", "bottom", "left"]]
        self.parameters = []
        self.fields = []
        self.sections = []
        self.URL = None
        self.get_url_suffix()

    def get_url_suffix(self):
        for attribute in self.jasperReport:
            if "schemaLocation" in attribute:
                self.URL = "{" + self.jasperReport.get(attribute).split(" ")[0] + "}"

    def process_sections(self):
        current_v_position = 0
        for child in self.root:
            section_name = re.sub(r'{.+}', '', str(child.tag)).rstrip().lstrip()
            match section_name:
                case "parameter":
                    _new_parameter = Paramater(child)
                    _new_parameter.parse_paramater(self.URL)
                    self.parameters.append(_new_parameter)
                case "field":
                    _new_field = Field(child)
                    self.fields.append(_new_field)
                case _:
                    _new_section = Section(section_name, child, current_v_position).parse_section(self.URL)
                    self.sections.append(_new_section)
                    _height = _new_section.section_band_attrib.get("height")
                    if _height != None:
                        current_v_position += int(_height)
        
    def run(self):
        self.process_sections()

