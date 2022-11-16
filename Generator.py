import xml.etree.ElementTree as ET
from Elements.Elements import *
from reportlab.lib.units import inch, cm, px, mm
from PDF import PDF
from Elements import JasperReport
import os, sys, re

BASE_DIR = os.path.dirname(__file__)


class Generator:
    def __init__(self):
        self.pdf = PDF()
        self.jasperReport = None

    def open_file(self, filename: str):
        file_path = os.path.join(BASE_DIR, "reports", filename)
        self.pdf.create_pdf(filename.split(".")[0])
        return ET.parse(file_path)

    def process_file(self, tree: ET):
        root = tree.getroot()
        self.jasperReport = JasperReport(root)
        self.jasperReport.run()

    def process_detail_band(self, section):
        return

    def generate_pdf(self):
        for section in self.jasperReport.sections:
            if section.section_name in ["title", "pageHeader", "columnHeader", "detail"]:
                for element in section.band_elements:
                    element.draw(canvas=self.pdf, section_height=section.section_v_position, margin=self.jasperReport.document_margin, size=self.pdf.dimensions)

            print(section.section_name, section.section_v_position)
            x, y = Util.coord(0, section.section_v_position, 0, 0, section.section_v_position, [0, 0, 0, 0], self.pdf.dimensions)
            self.pdf.draw_line(0, y, self.pdf.dimensions[0]+50, y, 1)
        # self.pdf.show_page()
        self.pdf.save_pdf()


    def run(self, filename: str):
        tree = self.open_file(filename)
        self.process_file(tree)
        self.generate_pdf()
        
    

reporter = Generator()
reporter.run("NoName-M01.jrxml")