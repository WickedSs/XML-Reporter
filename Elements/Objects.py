import re



class Util:
    def coord(x, y, width, height, current_height, margin, size):
        position_x = ((margin[2] * 2) + x)
        position_y = (size[1] - 50 - (margin[2] * 2) - y) - current_height
        # print(x, y, position_x, position_y, current_height)
        return position_x, position_y



class ReportElement(object):
    coords = None

    def fetch(self, element, url):
        report_element = element.find(f"{url}reportElement")
        if report_element != None:
            self.coords = report_element.attrib

        return self


class TextElement(object):
    alignement = None
    font = None
    paragraph = None

    def fetch(self, element, url):
        text_element = element.find(f"{url}textElement")
        if text_element != None:
            self.alignement = text_element.attrib
            self.font = text_element.find(f"{url}font").attrib if text_element.find(f"{url}font") != None else {}
            self.paragraph = text_element.find(f"{url}paragraph").attrib if text_element.find(f"{url}paragraph") != None else {}

        return self


class GraphicElement(object):
    pen = { "lineWidth" : 0 }

    def fetch(self, element, url):
        graphic_element = element.find(f"{url}graphicElement")
        if graphic_element != None:
            self.pen = graphic_element.find(f"{url}pen").attrib if graphic_element.find(f"{url}pen") != None else { "lineWidth" : 0 }

        return self


class Text(object):
    text = None

    def fetch(self, element, url):
        text_element = element.find(f"{url}text")
        if text_element != None:
            self.text = text_element.text

        return self


class textFieldExpression(object):
    expression = None
    def fetch(self, element, url):
        text_Field_Expression = element.find(f"{url}textFieldExpression")
        if text_Field_Expression != None:
            self.expression = re.findall(r'{(.+?)}', str(text_Field_Expression.text))

        return self
