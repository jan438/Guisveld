import os
import sys
import csv
import math
import unicodedata
from pathlib import Path
from datetime import datetime, date, timedelta
from ics import Calendar, Event
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import LETTER, A4, landscape, portrait
from reportlab.lib.units import inch
from reportlab.lib.colors import blue, green, black, red, pink, gray, brown, purple, orange, yellow, white, lightgrey
from reportlab.pdfbase import pdfmetrics  
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.graphics.shapes import *
from reportlab.graphics import renderPDF

kamerdata = []
kamers = []
d = Drawing(595, 842)

rectwidth = 190
rectheight = 100
leftmargin =  15
middlehormargin = 15
bottommargin = 5

class Kamer:
    def __init__(self, nummer, pad, zijde, bewoner, initialen):
        self.nummer = nummer
        self.pad = pad
        self.zijde = zijde
        self.bewoner = bewoner
        self.initialen = initialen

def processcsv(csvfile):
    with open(file_to_open, 'r') as file:
        csvreader = csv.reader(file, delimiter = ';')
        count = 0
        for row in csvreader:
            if count > 0:
                kamerdata.append(row)
            count += 1
            
def processreport():
    renderPDF.drawToFile(d, 'PDF/olieslager.pdf') 
            
def fillKamerReport(count):
    print("fillKamerReport", count)
    for i in range(8):
        d.add(Rect(leftmargin, bottommargin + (i * rectheight), rectwidth, rectheight, fillColor = colors.yellow))
    
    for i in range(8):
        d.add(Rect(leftmargin + rectwidth + middlehormargin, bottommargin + (i * rectheight), rectwidth, rectheight, fillColor = colors.yellow))
   
    for i in range(len(kamers)):
        print(kamers[i].bewoner, kamers[i].initialen)

    d.add(String(100, 155, '259', fontSize = 20, fillColor = colors.blue))
    d.add(String(100, 130, 'Dick', fontSize = 15, fillColor = colors.red))
    d.add(String(100, 115, 'Kingma', fontSize = 15, fillColor = colors.red))
    d.add(Image(path = "Foto/dick.png", width = 75, height = 95, x = leftmargin + 5, y = 7.5 + rectheight))

    d.add(String(100, 50, '265', fontSize = 20, fillColor = colors.blue))
    d.add(String(100, 25, 'Joop', fontSize = 15, fillColor = colors.red))
    d.add(String(100, 10, 'Mooijboer', fontSize = 15, fillColor = colors.red))
    d.add(Image(path = "Foto/joop.png", width = 75, height = 95, x = leftmargin + 5, y = 7.5))
    return

if sys.platform[0] == 'l':
    path = '/home/jan/git/Guisveld'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/Guisveld"
os.chdir(path)

file_to_open = "Data/Kamers.csv"
processcsv(file_to_open)
print(len(kamerdata))
for i in range(len(kamerdata)):
    nummer = kamerdata[i][0]
    pad = kamerdata[i][1]
    zijde = kamerdata[i][2]
    bewoner = kamerdata[i][3]
    initialen = kamerdata[i][4]
    kamers.append(Kamer(nummer, pad, zijde, bewoner, initialen))

pdfmetrics.registerFont(TTFont('Ubuntu', 'Ubuntu-Regular.ttf'))
pdfmetrics.registerFont(TTFont('UbuntuBold', 'Ubuntu-Bold.ttf'))
pdfmetrics.registerFont(TTFont('UbuntuItalic', 'Ubuntu-Italic.ttf'))
pdfmetrics.registerFont(TTFont('UbuntuBoldItalic', 'Ubuntu-BoldItalic.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerif', 'LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBold', 'LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifItalic', 'LiberationSerif-Italic.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBoldItalic', 'LiberationSerif-BoldItalic.ttf'))
fillKamerReport(len(kamers))
processreport()
key = input("Wait")
