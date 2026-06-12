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
        
def drawroundRect(c, x, y, w, h, a, color):    
    c.setFillColor(HexColor(color))
    p = c.beginPath()
    p.moveTo(x, y + 0.5 * a)
    p.arcTo(x, y, x + a, y + a, startAng = 180, extent = 90)
    p.lineTo(x + w, y)
    p.arcTo(x + w, y, x + w + a, y + a, startAng = 270, extent = 90)
    p.lineTo(x + w + a, y + h)
    p.arcTo(x + w, y + h, x + w + a, y + h + a, startAng = 0, extent = 90)
    p.lineTo(x + 0.5 * a, y + h + a)
    p.arcTo(x, y + h, x + a, y + h + a, startAng = 90, extent = 90)
    p.lineTo(x, y + 0.5 * a)
    c.drawPath(p, stroke = 0, fill = 1)
      
def albireo(c, x, y):
    alarmbutton_y = y + 160
    alarmbutton_r = 35
    resetbutton_y = y + 70
    resetbutton_r = 10
    triggerbutton_y = y + 70
    updownbutton_x = x + 60
    updownbutton_y = y + 70
    albireo_width = 330
    albireo_angle = albireo_width / 10
    middle_x = x + (albireo_width + albireo_angle) / 2
    beziers_width = 300
    beziers_x = middle_x - 0.5 * beziers_width
    middle_beziers_y = y + 15
    drawroundRect(c, x, y, albireo_width, 600, albireo_angle, "#EEEFEA")   
    #c.rect(x, y, albireo_width, 600, stroke=0, fill=1)
    renderPDF.draw(scaleSVG("SVG/arc_330_30degouter.svg", 1.0), c, beziers_x, middle_beziers_y)
    renderPDF.draw(scaleSVG("SVG/arc_330_30deg.svg", 1.0), c, beziers_x, middle_beziers_y)
    renderPDF.draw(scaleSVG("SVG/arc_60_120degouter.svg", 1.0), c,beziers_x, middle_beziers_y)
    renderPDF.draw(scaleSVG("SVG/arc_60_120deg.svg", 1.0), c, beziers_x, middle_beziers_y)
    renderPDF.draw(scaleSVG("SVG/arc_150_210degouter.svg", 1.0), c, beziers_x, middle_beziers_y)
    renderPDF.draw(scaleSVG("SVG/arc_150_210deg.svg", 1.0), c, beziers_x, middle_beziers_y)
    renderPDF.draw(scaleSVG("SVG/arc_240_300degouter.svg", 1.0), c, beziers_x, middle_beziers_y)
    renderPDF.draw(scaleSVG("SVG/arc_240_300deg.svg", 1.0), c, beziers_x, middle_beziers_y)
    c.setFillColor(HexColor('#ff0000'))
    c.circle(middle_x, alarmbutton_y, alarmbutton_r, stroke=0, fill=1)
    c.setFillColor(HexColor('#ffffff'))
    c.circle(middle_x-30, y + resetbutton_y, resetbutton_r, stroke=0, fill=1)
    c.setFillColor(HexColor('#ffffff'))
    c.rect(middle_x+30, y + triggerbutton_y, 10, 10, stroke=0, fill=1)
    p = c.beginPath()
    radius = 10
    p.moveTo(middle_x-radius, y+43)
    p.lineTo(middle_x+radius, y+43)
    p.lineTo(middle_x, y + 33)
    c.setFillColor(HexColor('#ffffff'))
    c.drawPath(p, stroke=0, fill=1)
    p = c.beginPath()
    radius = 10
    p.moveTo(middle_x-radius, y+updownbutton_y+43)
    p.lineTo(middle_x+radius, y+updownbutton_y+43)
    p.lineTo(middle_x, y+updownbutton_y+53)
    c.setFillColor(HexColor('#ffffff'))
    c.drawPath(p, stroke=0, fill=1)
    
def create_CheatSheetAlbireo(filename, ps, pagesize, title="Cheat Sheet Albireo"):
    try:
        c = canvas.Canvas(filename, pagesize=pagesize)
        c.setTitle(title)
        width, height = pagesize
        c.setFillColor(HexColor('#afafaf'))
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
        renderPDF.draw(scaleSVG("SVG/mizar.svg", 0.5), c, 450, 400)
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
