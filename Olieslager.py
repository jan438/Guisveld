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

class Kamer:
    def __init__(self, nummer, pad, zijde, bewoner):
        self.nummer = nummer
        self.pad = pad
        self.zijde = zijde
        self.bewoner = bewoner

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
    d.add(Rect(7.5, 740, 190, 100, fillColor = colors.yellow))
    d.add(Rect(7.5, 635, 190, 100, fillColor = colors.yellow))
    d.add(Rect(7.5, 530, 190, 100, fillColor = colors.yellow))
    d.add(Rect(7.5, 425, 190, 100, fillColor = colors.yellow))
    d.add(Rect(7.5, 320, 190, 100, fillColor = colors.yellow))
    d.add(Rect(7.5, 215, 190, 100, fillColor = colors.yellow))
    d.add(Rect(7.5, 110, 190, 100, fillColor = colors.yellow))
    d.add(Rect(7.55, 5, 190, 100, fillColor = colors.yellow))
    d.add(String(10, 745, 'Hello World', fontSize = 18, fillColor = colors.red))
    d.add(String(10, 640, 'Hello World', fontSize = 18, fillColor = colors.red))
    d.add(String(10, 535, 'Hello World', fontSize = 18, fillColor = colors.red))
    d.add(String(10, 430, 'Hello World', fontSize = 18, fillColor = colors.red))
    d.add(String(10, 325, 'Hello World', fontSize = 18, fillColor = colors.red))
    d.add(String(10, 220, 'Hello World', fontSize = 18, fillColor = colors.red))
    
    d.add(Rect(397.5, 740, 190, 100, fillColor = colors.yellow))
    d.add(Rect(397.5, 635, 190, 100, fillColor = colors.yellow))
    d.add(Rect(397.5, 530, 190, 100, fillColor = colors.yellow))
    d.add(Rect(397.5, 425, 190, 100, fillColor = colors.yellow))
    d.add(Rect(397.5, 320, 190, 100, fillColor = colors.yellow))
    d.add(Rect(397.5, 215, 190, 100, fillColor = colors.yellow))
    d.add(Rect(397.5, 110, 190, 100, fillColor = colors.yellow))
    d.add(Rect(397.5, 5, 190, 100, fillColor = colors.yellow))
    
    for i in range(len(kamers)):
        print(kamers[i].bewoner)

    d.add(String(100, 155, '259', fontSize = 20, fillColor = colors.blue))
    d.add(String(100, 130, 'Dick', fontSize = 15, fillColor = colors.red))
    d.add(String(100, 115, 'Kingma', fontSize = 15, fillColor = colors.red))
    d.add(Image(path = "Foto/dick.png", width = 75, height = 95, x = 12, y = 112.5))

    d.add(String(100, 50, '265', fontSize = 20, fillColor = colors.blue))
    d.add(String(100, 25, 'Joop', fontSize = 15, fillColor = colors.red))
    d.add(String(100, 10, 'Mooijboer', fontSize = 15, fillColor = colors.red))
    d.add(Image(path = "Foto/joop.png", width = 75, height = 95, x = 12, y = 7.5))
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
    kamers.append(Kamer(nummer, pad, zijde, bewoner))

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
