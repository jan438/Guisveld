from reportlab.lib.pagesizes import A3, A4
from reportlab.pdfgen import canvas
import os
import csv
import sys
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from svglib.svglib import svg2rlg, load_svg_file, SvgRenderer
from reportlab.graphics import renderPDF
from reportlab.lib.colors import yellow, green, red, black, HexColor
from reportlab.lib.colors import tan, black, green
from reportlab.lib.units import inch, cm, mm
from math import pi, cos, sin, radians, sqrt

cheatsheetfont = "LiberationSerif"
templatedata = []

def scaleSVG(svgfile, scaling_factor):
    svg_root = load_svg_file(svgfile)
    svgRenderer = SvgRenderer(svgfile)
    drawing = svgRenderer.render(svg_root)
    scaling_x = scaling_factor
    scaling_y = scaling_factor
    drawing.width = drawing.minWidth() * scaling_x
    drawing.height = drawing.height * scaling_y
    drawing.scale(scaling_x, scaling_y)
    return drawing
    
def cadre(c, pagesize):
    width = pagesize[0]
    height = pagesize[1]
    dx = width / 10
    for i in range(11):
        c.line(i * dx, 0, i * dx, height)
    for i in range(15):
        c.line(0, i * dx, width, i * dx)
        
def albireo(c, x, y):
    c.setFillColor(HexColor('#c7c7c7'))
    c.rect(150, 250, x + 40, y + 40, stroke=0, fill=1)
    renderPDF.draw(scaleSVG("SVG/arc_330_30deg.svg", 0.5), c, x + 20, y + 20)
    renderPDF.draw(scaleSVG("SVG/arc_60_120deg.svg", 0.5), c, x + 20, y + 20)
    renderPDF.draw(scaleSVG("SVG/arc_150_210deg.svg", 0.5), c, x + 20, y + 20)
    renderPDF.draw(scaleSVG("SVG/arc_240_300deg.svg", 0.5), c, x + 20, y + 20)
    c.setFillColor(HexColor('#ff0000'))
    c.circle(x + 95, y + 95, 25, stroke=0, fill=1)
    c.setFillColor(HexColor('#ffffff'))
    c.circle(x + 43, y + 95, 5, stroke=0, fill=1)
    c.setFillColor(HexColor('#ffffff'))
    c.rect(x + 100, y + 90, 10, 10, stroke=0, fill=1)
    p = c.beginPath()
    xcenter = x + 80
    radius = 10
    p.moveTo(xcenter-radius, y+20)
    p.lineTo(xcenter+radius, y+20)
    p.lineTo(xcenter, y + 10)
    c.setFillColor(HexColor('#ffffff'))
    c.setFillColor(HexColor('#ff00ff'))
    c.drawPath(p, stroke=0, fill=1)
    
def create_CheatSheetAlbireo(filename, ps, pagesize, title="Cheat Sheet Albireo"):
    try:
        c = canvas.Canvas(filename, pagesize=pagesize)
        c.setTitle(title)
        width, height = pagesize
        c.setFillColor(HexColor('#FFFFFF'))
        c.rect(0, 0, width, height, fill=1)
        c.setFillColor(HexColor('#000000'))
        cadre(c, pagesize)
        titlefontsize_value = variable_dict["titlefontsize" + ps]
        titley_value = variable_dict["titley" + ps]
        namewidth = pdfmetrics.stringWidth(title, cheatsheetfont, titlefontsize_value)
        c.setFont(cheatsheetfont, titlefontsize_value)
        c.drawCentredString(width / 2, height - titley_value, title)
        c.setLineWidth(1)
        albireo(c, 200, 200)
        renderPDF.draw(scaleSVG("SVG/mizar.svg", 0.5), c, 350, 300)
        c.showPage()
        c.save()
        print(f"✅ PDF CheatSheetAlbireo '{filename}' created successfully.")
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")

if sys.platform[0] == 'l':
    path = '/home/jan/git/Guisveld'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/Guisveld"
os.chdir(path)

pdfmetrics.registerFont(TTFont('LiberationSerif', 'LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBold', 'LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifItalic', 'LiberationSerif-Italic.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBoldItalic', 'LiberationSerif-BoldItalic.ttf'))

file_to_open = "Data/template.csv"
with open(file_to_open, 'r') as file:
    csvreader = csv.reader(file, delimiter = ';')
    count = 0
    for row in csvreader:
        templatedata.append(row)
        count += 1
print(count)

variable_dict = {}

for i in range(len(templatedata)):
    variable_dict[templatedata[i][0]] = float(templatedata[i][1])

create_CheatSheetAlbireo("PDF/CheatSheetAlbireoPython_A4.pdf", "A4", A4, title="A4 Cheat Sheet Albireo")
create_CheatSheetAlbireo("PDF/CheatSheetAlbireoPython_A3.pdf", "A3", A3, title="A3 Cheat Sheet Albireo")

key = input("Wait")
