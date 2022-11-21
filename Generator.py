# import xml.etree.ElementTree as ET
# from Elements.Elements import *
# from reportlab.lib.units import inch, cm, px, mm
# from PDF import PDF
# from Elements import JasperReport
# import os, sys, re



# class Generator:
#     def __init__(self, paramaters, fields):
#         self.pdf = PDF()
#         self.jasperReport = None
#         self.parameters = paramaters
#         self.fields = fields

#     def open_file(self, filename: str):
#         file_path = os.path.join(BASE_DIR, "reports", filename)
#         self.pdf.create_pdf(filename.split(".")[0])
#         return ET.parse(file_path)

#     def process_file(self, tree: ET):
#         root = tree.getroot()
#         self.jasperReport = JasperReport(root, len(self.fields))
#         self.jasperReport.run()

#     def process_paramaters(self):
#         for jparamater in self.jasperReport.parameters:
#             jparamater.value = self.parameters.get(jparamater.name)

#     def process_detail_band(self, section):
#         return

#     def generate_pdf(self):
#         for section in self.jasperReport.sections:
#             for element in section.band_elements:
#                 element.draw(canvas=self.pdf, section_height=section.section_v_position, jasperReport=self.jasperReport)


#         # self.pdf.show_page()
#         self.pdf.save_pdf()


#     def run(self, filename: str):
#         tree = self.open_file(filename)
#         self.process_file(tree)
#         self.process_paramaters()
#         self.generate_pdf()
        
    

