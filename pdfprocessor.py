# -*- coding: utf-8 -*-
"""
Created on Thu May 10 09:53:13 2018
This script removes Header and Footer from PDF File
@author: NIRAV
"""

from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import sys
import logging


class PdfProcessor:
    """Base class for Pdf Processing"""
    header_pos_x = 0
    header_pos_y = 0

    def __init__(self, h_pos_x, h_pos_y):
        self.header_pos_x = h_pos_x
        self.header_pos_y = h_pos_y

    def processpdf(self, inputpdfname, outputfilename):
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFillColorRGB(1, 1, 1)
        can.rect(0, self.header_pos_x, 1000, 24, 0, fill=1)
        can.rect(0, self.header_pos_y, 1000, 20, 0, fill=1)
        can.save()
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        try:
            existing_pdf = PdfFileReader(open(inputpdfname, "rb"))
        except Exception as e2:
            print(e2)
            logging.error(e2)
            sys.exit()
        total_pages = existing_pdf.numPages
        output = PdfFileWriter()
        i = 0
        while i < total_pages:
            page = existing_pdf.getPage(i)
            page.mergePage(new_pdf.getPage(0))
            output.addPage(page)
            i += 1

        outputting = open(outputfilename, "wb")
        output.write(outputting)
        outputting.close()
        existing_pdf.stream.close()
        print("Process Complete")


if __name__ == '__main__':
    logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s : %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    try:
        sourcepdf_file = sys.argv[1]
        outputpdfname = sys.argv[2]
        verticalpos = int(input("Enter Position from Bottom for Footer\t"))
        horizontalpos = int(input("Enter Position from Bottom for Header\t"))

        obj1 = PdfProcessor(horizontalpos, verticalpos)
        obj1.processpdf(sourcepdf_file, outputpdfname)
    except IndexError as e1:
        print('Pls provide input and output pdf file with path')
        logging.error(e1)
