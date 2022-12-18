import json

from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class PedigreePDFGenerator:
    def __init__(self):
        self.template_filename = "pdf_gen/Rodokmen_holuba1.pdf"
        self._load_template()
        pdfmetrics.registerFont(TTFont('Carlito', 'pdf_gen/Carlito-Regular.ttf'))
        with open("pdf_gen/pdf_coords.json", mode="r") as f:
            self.coords = json.loads(f.read())
        self.generated_page0 = io.BytesIO()
        self.generated_page1 = io.BytesIO()
        self.output = PdfFileWriter()

    def _load_template(self):
        self.template = PdfFileReader(open(self.template_filename, mode="rb"))

    def _generate_packets_from_paths(self, paths):
        self._write_pigeon_data(paths[0]["path"][0])
        self._write_ancestors_data(paths)

        self.generated_page0.seek(0)
        self.generated_page1.seek(0)

    def _wpd_write_string_bbk(self, can, data, key):
        c = self.coords["data"]
        can.drawString(c[key][0], c[key][1], data[key])

    def _write_pigeon_data(self, data: dict):
        c = self.coords["data"]
        can = canvas.Canvas(self.generated_page0, pagesize=letter)
        can.setFont("Carlito", 10)
        if data.get("pohlavi"):
            p_coords = c[data["pohlavi"]]
            can.line(p_coords[0], p_coords[1], p_coords[2], p_coords[3])
        ckf = f"{data.get('cislo_krouzku')}/{data.get('rocnik')}"
        can.drawString(c["cislo_krouzku"][0], c["cislo_krouzku"][1], ckf)

        self._wpd_write_string_bbk(can, data, key="plemeno")
        self._wpd_write_string_bbk(can, data, key="barva")
        self._wpd_write_string_bbk(can, data, key="kresba")
        self._wpd_write_string_bbk(can, data, key="chovatel")
        self._wpd_write_string_bbk(can, data, key="bydliste")

        self._wpd_write_string_bbk(can, data, key="exterierove_vady")
        self._wpd_write_string_bbk(can, data, key="exterierove_prednosti")
        self._wpd_write_string_bbk(can, data, key="cil_slechteni")
        self._wpd_write_string_bbk(can, data, key="povahove_vlastnosti")
        can.save()


    def _write_ancestors_data(self, data):
        can = canvas.Canvas(self.generated_page1, pagesize=letter)
        can.setFont("Carlito", 10)

        can.drawString(68, 358, "RS453/19")
        can.save()

    def _generate_output(self):
        page0 = self.template.getPage(0)
        page1 = self.template.getPage(1)
        generated_pdf_page0 = PdfFileReader(self.generated_page0)
        generated_pdf_page1 = PdfFileReader(self.generated_page1)
        page0.mergePage(generated_pdf_page0.getPage(0))
        page1.mergePage(generated_pdf_page1.getPage(0))
        self.output.addPage(page0)
        self.output.addPage(page1)

    def _write_output_to_file(self, file):
        self.output.write_stream(file)
        file.seek(0)
        return file

    def generate_pedigree_from_paths(self, paths, file):
        self._load_template()
        self._generate_packets_from_paths(paths)
        self._generate_output()
        return self._write_output_to_file(file)
