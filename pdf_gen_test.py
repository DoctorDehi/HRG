from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


coords = {
    "exterierove_vady": (49, 380),
    "exterierove_prednosti": (49, 331),
    "cil_slechteni": (49, 276),
    "povahove_vlastnosti": (),
    "holub": (335, 280, 360, 280),
    "holubice": (365, 280, 400, 280),
    "cislo_krouzku": (455, 284),
    "plemeno": (380, 258),
    "barva": (380, 240),
    "kresba": (380, 220),
    "chovatel": (375, 190),
    "bydliste": (375, 166),
    "matka_cislo_krouzku": (393, 111),
    "matka_chovatel": (378, 95),
    "matka_bydliste": (340, 74),
    "otec_cislo_krouzku": (511, 111),
    "otec_chovatel": (496, 95),
    "otec_bydliste": (459, 74),

    "pm2_1_cislo_krouzku": (),
    "pm2_2_cislo_krouzku": (),
    "pm3_1_cislo_krouzku": (),
    "pm3_2_cislo_krouzku": (),
    "pm3_3_cislo_krouzku": (),
    "pm3_4_cislo_krouzku": (),
    "pm4_1_cislo_krouzku": (),
    "pm4_2_cislo_krouzku": (),
    "pm4_3_cislo_krouzku": (),
    "pm4_4_cislo_krouzku": (),
    "pm4_5_cislo_krouzku": (),
    "pm4_6_cislo_krouzku": (),
    "pm4_7_cislo_krouzku": (),
    "pm4_8_cislo_krouzku": (),
    "pm2_1_chovatel": (),
    "pm2_2_chovatel": (),
    # vertical
    "pm3_1_chovatel": (),
    "pm3_2_chovatel": (),
    "pm3_3_chovatel": (),
    "pm3_4_chovatel": (),
    "pm4_1_chovatel": (),
    "pm4_2_chovatel": (),
    "pm4_3_chovatel": (),
    "pm4_4_chovatel": (),
    "pm4_5_chovatel": (),
    "pm4_6_chovatel": (),
    "pm4_7_chovatel": (),
    "pm4_8_chovatel": (),
    "pm2_1_bydliste": (),
    "pm2_2_bydliste": (),
    "pm3_1_bydliste": (),
    "pm3_2_bydliste": (),
    "pm3_3_bydliste": (),
    "pm3_4_bydliste": (),

    "po2_1_cislo_krouzku": (),
    "po2_2_cislo_krouzku": (),
    "po3_1_cislo_krouzku": (),
    "po3_2_cislo_krouzku": (),
    "po3_3_cislo_krouzku": (),
    "po3_4_cislo_krouzku": (),
    "po4_1_cislo_krouzku": (90, -57),
    "po4_2_cislo_krouzku": (90, -87),
    "po4_3_cislo_krouzku": (90, -117),
    "po4_4_cislo_krouzku": (90, -147),
    "po4_5_cislo_krouzku": (),
    "po4_6_cislo_krouzku": (),
    "po4_7_cislo_krouzku": (),
    "po4_8_cislo_krouzku": (),
    "po2_1_chovatel": (),
    "po2_2_chovatel": (),
    # vertical
    "po3_1_chovatel": (),
    "po3_2_chovatel": (),
    "po3_3_chovatel": (),
    "po3_4_chovatel": (),
    "po4_1_chovatel": (105, -71),
    "po4_2_chovatel": (105, -101),
    "po4_3_chovatel": (105, -131),
    "po4_4_chovatel": (105, -161),
    "po4_5_chovatel": (),
    "po4_6_chovatel": (),
    "po4_7_chovatel": (),
    "po4_8_chovatel": (),
    "po2_1_bydliste": (),
    "po2_2_bydliste": (),
    "po3_1_bydliste": (),
    "po3_2_bydliste": (),
    "po3_3_bydliste": (),
    "po3_4_bydliste": (),

}
pdfmetrics.registerFont(TTFont('Calibri', './Carlito-Regular.ttf'))

packet0 = io.BytesIO()
packet1 = io.BytesIO()

can = canvas.Canvas(packet1, pagesize=letter)
can.setFont("Calibri", 10)
can.rotate(90)
can.drawString(90, -57, "U5831/13")
can.drawString(105, -71, "Denisa Krebsová")
can.drawString(90, -87, "U5432/13")
can.drawString(105, -101, "Denisa Krebsová")
can.drawString(90, -117, "U5433/13")
can.drawString(105, -131, "Denisa Krebsová")
can.drawString(90, -147, "U5434/13")
can.drawString(105, -161, "Denisa Krebsová")
can.drawString(90, -176, "U5435/13")
can.drawString(105, -191, "Denisa Krebsová")
can.drawString(90, -206, "U543/13")
can.drawString(105, -221, "Denisa Krebsová")
can.drawString(90, -236, "U543/13")
can.drawString(105, -251, "Denisa Krebsová")
can.drawString(90, -266, "U543/13")
can.drawString(105, -281, "Denisa Krebsová")

can.drawString(90, -346, "U543/13")
can.drawString(105, -360, "Denisa Krebsová")
can.drawString(90, -376, "U543/13")
can.drawString(105, -390, "Denisa Krebsová")
can.drawString(90, -406, "U543/13")
can.drawString(105, -420, "Denisa Krebsová")
can.drawString(90, -435, "U543/13")
can.drawString(105, -450, "Denisa Krebsová")
can.drawString(90, -465, "U543/13")
can.drawString(105, -480, "Denisa Krebsová")
can.drawString(90, -495, "U543/13")
can.drawString(105, -510, "Denisa Krebsová")
can.drawString(90, -525, "U543/13")
can.drawString(105, -540, "Denisa Krebsová")
can.drawString(90, -555, "U543/13")
can.drawString(105, -570, "Denisa Krebsová")
can.save()

can = canvas.Canvas(packet0, pagesize=letter)

can.setFont("Calibri", 12)
can.line(365, 280, 400, 280)
can.drawString(455, 284, "AT520/20")
can.drawString(380, 258, "Český stavák")
can.drawString(380, 240, "modrý")
can.drawString(380, 220, "sedlatý")

can.drawString(375, 190, "Denisa Krebsová")
can.drawString(375, 166, "Libochovany 45, 41103 Litoměřice")

can.drawString(49, 380, "nějaká vada") # w / 1.42, (645-h) / 1.42
can.drawString(49, 331, "nějaká přednost")
can.drawString(49, 276, "nějaký cíl")
can.drawString(49, 228, "nějaká vlastnost")

can.setFont("Calibri", 10)
can.drawString(393, 111, "B9187/17")
can.drawString(511, 111, "N982/19")
can.setFont("Calibri", 7)
can.drawString(378, 95, "Stanislav Brückner")
can.drawString(496, 95, "Denisa Krebsová")
can.drawString(340, 74, "Blíževedly 89, 42442 Česká Lípa")
can.drawString(459, 74, "Libochovany 45, 41103 Litoměřice")


can.save()

#move to the beginning of the StringIO buffer
packet0.seek(0)
packet1.seek(0)

# create a new PDF with Reportlab
new_pdf0 = PdfFileReader(packet0)
new_pdf1 = PdfFileReader(packet1)
# read your existing PDF
existing_pdf = PdfFileReader(open("static/Rodokmen_holuba1.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page0 = existing_pdf.getPage(0)
page1 = existing_pdf.getPage(1)
page0.mergePage(new_pdf0.getPage(0))
page1.mergePage(new_pdf1.getPage(0))
output.addPage(page0)
output.addPage(page1)
# finally, write "output" to a real file
outputStream = open("destination.pdf", "wb")
output.write(outputStream)
outputStream.close()
