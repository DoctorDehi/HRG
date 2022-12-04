from docx import Document
from docx.shared import Inches

from docxtpl import DocxTemplate

doc = DocxTemplate("Rodokmen_holuba.docx")
context = { 'company_name' : "World company" }
doc.render(context)
doc.save("generated_doc.docx")