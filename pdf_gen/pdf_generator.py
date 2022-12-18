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
        self.fontname = 'Carlito'
        pdfmetrics.registerFont(TTFont(self.fontname, 'pdf_gen/Carlito-Regular.ttf'))
        with open("pdf_gen/pdf_coords.json", mode="r") as f:
            self.coords = json.loads(f.read())
        self.generated_page0 = io.BytesIO()
        self.generated_page1 = io.BytesIO()
        self.can_page0 = canvas.Canvas(self.generated_page0, pagesize=letter)
        self.can_page1 = canvas.Canvas(self.generated_page1, pagesize=letter)
        self.last_can_page1_rotation = 0
        self.output = PdfFileWriter()


    def _load_template(self):
        self.template = PdfFileReader(open(self.template_filename, mode="rb"))


    def _generate_packets_from_paths(self, paths):
        self._write_pigeon_data(paths[0]["path"][0])
        self._write_ancestors_data(paths)

        self.can_page0.save()
        self.can_page1.save()
        self.generated_page0.seek(0)
        self.generated_page1.seek(0)


    def _get_ckf(self, pigeon):
        return f"{pigeon.get('cislo_krouzku')}/{pigeon.get('rocnik')}"


    def _write_pigeon_data(self, pigeon: dict):
        c = self.coords["data"]
        can = self.can_page0
        can.setFont(self.fontname, 10)
        if pigeon.get("pohlavi"):
            p_coords = c[pigeon["pohlavi"]]
            can.line(p_coords[0], p_coords[1], p_coords[2], p_coords[3])
        can.drawString(c["cislo_krouzku"][0], c["cislo_krouzku"][1], self._get_ckf(pigeon))

        self._wpd_write_string_bbk(can, pigeon, key="plemeno")
        self._wpd_write_string_bbk(can, pigeon, key="barva")
        self._wpd_write_string_bbk(can, pigeon, key="kresba")
        self._wpd_write_string_bbk(can, pigeon, key="chovatel")
        self._wpd_write_string_bbk(can, pigeon, key="bydliste")

        self._wpd_write_string_bbk(can, pigeon, key="exterierove_vady")
        self._wpd_write_string_bbk(can, pigeon, key="exterierove_prednosti")
        self._wpd_write_string_bbk(can, pigeon, key="cil_slechteni")
        self._wpd_write_string_bbk(can, pigeon, key="povahove_vlastnosti")


    def _wpd_write_string_bbk(self, can, pigeon, key):
        c = self.coords["data"]
        can.drawString(c[key][0], c[key][1], pigeon[key])


    def _write_ancestors_data(self, paths):
        # HOTFIX proti padani v pripade prazdne strany
        self.can_page1.line(0, 0, 0, 0)
        for i in paths:
            path = i["path"]
            if len(path) > 3:
                self._write_ancestor_data(path)

            elif len(path) == 3:
                # matka či otec
                parent =  path[-1]
                relationship = path[1]
                self._write_parent_data(relationship, pigoen=parent)


    def _write_ancestor_data(self, path):
        ancestor = path[-1]
        c = self._get_ancestor_coords(path)
        can = self.can_page1
        rotation = c["cislo_krouzku"][3]
        if rotation != self.last_can_page1_rotation:
            can.rotate(-self.last_can_page1_rotation)
            can.rotate(rotation)
            self.last_can_page1_rotation = rotation
        can.setFont(self.fontname, 10)
        can.drawString(c["cislo_krouzku"][0], c["cislo_krouzku"][1], self._get_ckf(ancestor))
        can.setFont(self.fontname, 8)
        can.drawString(c["chovatel"][0], c["chovatel"][1], ancestor.get("chovatel", ""))
        if c.get("bydliste"):
            can.drawString(c["bydliste"][0], c["bydliste"][1], ancestor.get("bydliste", ""))


    def _get_ancestor_coords(self, path):
        node = self.coords
        for rel_i in range(1, len(path), 2):
            relationship = path[rel_i]
            node = node[relationship]
        return node


    def _write_parent_data(self, relationship, pigoen):
        c = self.coords[relationship]
        can = self.can_page0
        can.setFont(self.fontname, 10)
        can.drawString(c["cislo_krouzku"][0], c["cislo_krouzku"][1], self._get_ckf(pigoen))
        can.setFont(self.fontname, 7)
        can.drawString(c["chovatel"][0], c["chovatel"][1], pigoen.get("chovatel"))
        can.drawString(c["bydliste"][0], c["bydliste"][1], pigoen.get("bydliste"))


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
