from PyPDF2 import PdfFileReader, PdfFileWriter
from pathlib import *
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import io

test_folder = Path.cwd() / "Vendor Files"
output_folder = Path.home() / "Z:" / "Assembly and Production" / "Assembly" / "Vendor File PDFs"


def main():
    iter_file()



def edit_page():
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    #fill in with white
    can.setFillColor(colors.white)
    can.rect(615, 55, 147, 11, stroke=0, fill=1)
    can.rect(25, 30, 120, 34, stroke=0, fill=1)

    #draw left side
    can.setStrokeColorRGB(0.75, 0.75, 0.75)
    can.setLineWidth(0.4)
    can.line(23.5, 42, 145.5, 42)
    can.setFillColor(colors.black)
    can.setFont("Helvetica", 3.5)
    can.drawString(38, 60, "THE INFORMATION CONTAINED IN THIS DRAWING IS")
    can.drawString(38, 56, "THE SOLE PROPERTY OF ALLSALT MARITIME CORP.")
    can.drawString(38, 52, "ANY REPORDUCTION IN PART OR AS A WHOLE")
    can.drawString(38, 48, "WITHOUT THE WRITTEN PERMISSION OF")
    can.drawString(38, 44, "ALLSALT MARITIME CORP. IS PROHIBITED")
    can.drawString(42, 36, "THREADS, UNLESS OTHERWISE SPECIFIED:")
    can.drawString(42, 32, "INTERNAL: CLASS 2B || EXTERNAL: CLASS 2A")
    
    #draw right side
    can.setFont("Helvetica-Bold", 10)
    can.drawString(620, 57, "ALLSALT MARITIME CORP.")
    can.save()
    return packet

def iter_page(file):
    file_path = str(test_folder) + '\\' + file
    existing_pdf = PdfFileReader(open(file_path, "rb"))
    num_pages = existing_pdf.getNumPages()
    output = PdfFileWriter()
    for i in range(num_pages):
        packet = edit_page()
        #move to the beginning of the StringIO buffer
        packet.seek(0)
        # create a new PDF with Reportlab
        new_pdf = PdfFileReader(packet)
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(i)
        page.mergePage(new_pdf.getPage(0))
        #output = PdfFileWriter()
        output.addPage(page)
        # finally, write "output" to a real file
        output_pdf = str(output_folder) + '\\' + file
        output_stream = open(output_pdf, "ab")
        output.write(output_stream)
    output_stream.close()


def iter_file():
    for file in test_folder.iterdir():
        s = re.search(r"(13\d{4} [R|X]-\d{2}\.pdf$)", str(file), re.IGNORECASE)
        if s:
            #print(s.group(1))
            iter_page(s.group(1))

if __name__ == "__main__":
    main()

