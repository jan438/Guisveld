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
from reportlab.graphics import shapes
from reportlab.graphics import widgetbase
from reportlab.graphics.widgetbase import Widget
from reportlab.graphics.widgets import signsandsymbols
from reportlab.graphics.widgets.signsandsymbols import _Symbol
from reportlab.graphics.charts.textlabels import Label

kamerdata = []
kamers = []
d = Drawing(595, 842)

rectwidth = 145
rectheight = 100
leftmargin =  2.5
middlehormargin = 2.5
bottommargin = 5
middlehorseparator = 5
topmargin = 8 + (8 * rectheight)
roompos = [0, 0]
nummeroffset = [85, 50]
initialenoffset = [80, 35]
naamoffset = [80, 25]
   
class MyArrow(_Symbol):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = 100
        self.fillColor = colors.red

    def draw(self):
        g = shapes.Group()
        arrow = shapes.Polygon(points = [
        226.1, 714.0,
        211.2, 728.9,
        214.5, 733.0,
        207.2, 734.2,
        200.0, 736.1, # arrow point
        201.9, 728.9,
        203.8, 721.6,
        207.2, 724.9,
        222.1, 710.0 
        ],
               fillColor = self.fillColor,
               strokeColor = None,
               strokeWidth=0)
        g.add(arrow)
        lab = Label()
        lab.setOrigin(190,740)
        lab.boxAnchor = 'ne'
        lab.angle = 45
        lab.dx = 3
        lab.dy = 10
        lab.boxStrokeColor = colors.black
        lab.setText("N")
        g.add(lab)
        return g
        
class Kamer:
    def __init__(self, nummer, pad, zijde, bewoner, initialen, naam, foto):
        self.nummer = nummer
        self.pad = pad
        self.zijde = zijde
        self.bewoner = bewoner
        self.initialen = initialen
        self.naam = naam
        self.foto = foto
        
def lookuproomposition(number):
    roomposition = [[] for _ in range(300)]
    # Hazenpad
    roomposition[244] = [155, 608]
    roomposition[245] = [155, 508]
    roomposition[246] = [155, 408]
    roomposition[247] = [155, 308]
    roomposition[248] = [155, 208]
    roomposition[249] = [155, 108]
    roomposition[250] = [155, 8]
    roomposition[251] = [7.5, 8]
    roomposition[252] = [7.5, 108]
    roomposition[253] = [7.5, 208]
    roomposition[254] = [7.5, 308]
    roomposition[255] = [7.5, 408]
    roomposition[256] = [7.5, 508]
    roomposition[257] = [7.5, 608]
    roomposition[258] = [7.5, 708]
    # Middelpunt
    roomposition[259] = [305, 708]
    # Boerenpad
    roomposition[260] = [450, 708]
    roomposition[261] = [450, 608]
    roomposition[262] = [450, 508]
    roomposition[263] = [450, 408]
    roomposition[264] = [450, 308]
    roomposition[265] = [450, 208]
    roomposition[266] = [450, 108]
    roomposition[267] = [450, 8]
    roomposition[268] = [305, 8]
    roomposition[269] = [305, 108]
    roomposition[270] = [305, 208]
    roomposition[271] = [305, 308]
    roomposition[272] = [305, 408]
    roomposition[273] = [305, 508]
    roomposition[274] = [305, 608]
    return roomposition[int(number)]

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
        d.add(Rect(leftmargin, bottommargin + (i * rectheight), rectwidth, rectheight, fillColor = "#DAEEC9"))
    for i in range(7):
        d.add(Rect(leftmargin + rectwidth + middlehormargin, bottommargin + (i * rectheight), rectwidth, rectheight, fillColor = "#DAEEC9"))
    for i in range(7):
        d.add(Rect(leftmargin+2*rectwidth + middlehormargin + middlehorseparator, bottommargin + (i * rectheight), rectwidth, rectheight, fillColor = "#aaffff"))
    d.add(Rect(leftmargin + 2*rectwidth + middlehormargin + middlehorseparator, bottommargin + (7 * rectheight), rectwidth, rectheight, fillColor = "#FEDDB9"))
    a = MyArrow()
    d.add(a)
    for i in range(8):
        d.add(Rect(leftmargin + 2*rectwidth + middlehormargin + middlehorseparator + rectwidth + middlehormargin, bottommargin + (i * rectheight), rectwidth, rectheight, fillColor = "#aaffff"))
    for i in range(len(kamers)):
        print(kamers[i].bewoner, kamers[i].initialen, kamers[i].naam, kamers[i].foto)
    d.add(String(leftmargin, bottommargin + topmargin, "Wegzijde", fontSize = 20, fillColor = colors.purple))
    d.add(String(leftmargin + middlehormargin + 1.75*rectwidth, bottommargin + topmargin, "Tuinzijde", fontSize = 20, fillColor = colors.purple))
    d.add(String(leftmargin + 2*rectwidth + 2*middlehormargin + middlehorseparator + 1.45*rectwidth, bottommargin + topmargin, "Wegzijde", fontSize = 20, fillColor = colors.purple))
    d.add(String(leftmargin + 2.5 + middlehormargin + 0.8*rectwidth, bottommargin + topmargin, "Hazenpad", fontSize = 25, fillColor = colors.blue))
    d.add(String(leftmargin + 2.45*rectwidth + 2*middlehormargin + middlehorseparator, bottommargin + topmargin, "Boerenpad", fontSize = 25, fillColor = colors.blue))
    d.add(String(leftmargin + rectwidth + 4*middlehormargin + middlehorseparator, bottommargin + topmargin - 50, "Middelpunt", fontSize = 25, fillColor = colors.blue))
    for i in range(len(kamers)):
        roompos = lookuproomposition(kamers[i].nummer)
        d.add(String(roompos[0] + nummeroffset[0], roompos[1] + nummeroffset[1], kamers[i].nummer, fontSize = 20, fillColor = colors.blue))
        d.add(String(roompos[0] + initialenoffset[0], roompos[1] + initialenoffset[1], kamers[i].initialen, fontSize = 10, fillColor = colors.red))
        d.add(String(roompos[0] + naamoffset[0], roompos[1] + naamoffset[1], kamers[i].naam, fontSize = 10, fillColor = colors.red))
        d.add(Image(path = "Foto/" + kamers[i].foto, width = 71.25, height = 95, x = roompos[0], y = roompos[1]))
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
    naam = kamerdata[i][5]
    foto = kamerdata[i][6]
    kamers.append(Kamer(nummer, pad, zijde, bewoner, initialen, naam, foto))

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
