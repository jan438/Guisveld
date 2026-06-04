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

festivalfont = "LiberationSerif"
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
    
def drawallroundRect(c, x, y, w, h, a, color):    
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
    
def drawrightroundRect(c, x, y, w, h, a, color):    
    c.setFillColor(HexColor(color))
    p = c.beginPath()
    p.moveTo(x + 0.5 * a, y)
    p.lineTo(x + 0.5 * a + w, y)
    p.arcTo(x + w, y, x + w + a, y + a, startAng = 270, extent = 90)
    p.lineTo(x + w + a, y + h)
    p.arcTo(x + w, y + h, x + w + a, y + h + a, startAng = 0, extent = 90)
    p.lineTo(x + 0.5 * a, y + h + a)
    p.lineTo(x + 0.5 * a, y + 0.5 * a)
    c.drawPath(p, stroke = 0, fill = 1)
    
def drawleftroundRect(c, x, y, w, h, a, color):    
    c.setFillColor(HexColor(color))
    p = c.beginPath()
    p.moveTo(x, y + 0.5 * a)
    p.arcTo(x, y, x + a, y + a, startAng = 180, extent = 90)
    p.lineTo(x + w + 0.5 * a, y)
    p.lineTo(x + w + 0.5 * a, y + h + a)
    p.lineTo(x + 0.5 * a, y + h + a)
    p.arcTo(x, y + h, x + a, y + h + a, startAng = 90, extent = 90)
    p.lineTo(x, y + 0.5 * a)
    c.drawPath(p, stroke = 0, fill = 1)
    
def drawtoproundRect(c, x, y, w, h, a, color):    
    c.setFillColor(HexColor(color))
    p = c.beginPath()
    p.moveTo(x, y + 0.5 * a)
    p.lineTo(x + w + a, y + 0.5 * a)
    p.lineTo(x + w + a, y + h)
    p.arcTo(x + w, y + h, x + w + a, y + h + a, startAng = 0, extent = 90)
    p.lineTo(x + 0.5 * a, y + h + a)
    p.arcTo(x, y + h, x + a, y + h + a, startAng = 90, extent = 90)
    p.lineTo(x, y + 0.5 * a)
    c.drawPath(p, stroke = 0, fill = 1)
    
def drawbottomroundRect(c, x, y, w, h, a, color):    
    c.setFillColor(HexColor(color))
    p = c.beginPath()
    p.moveTo(x, y + 0.5 * a)
    p.arcTo(x, y, x + a, y + a, startAng = 180, extent = 90)
    p.lineTo(x + w, y)
    p.arcTo(x + w, y, x + w + a, y + a, startAng = 270, extent = 90)
    p.lineTo(x + w + a, y + h + 0.5 * a)
    p.lineTo(x, y + h + 0.5 * a)
    p.lineTo(x, y + 0.5 * a)
    c.drawPath(p, stroke = 0, fill = 1)
    
def star(c, title, aka, xcenter, ycenter, nvertices):
    c.setFont(festivalfont, 10)
    radius=cm/3.0
    c.drawCentredString(xcenter, ycenter+1.3*radius, title)
    c.drawCentredString(xcenter, ycenter-1.4*radius, aka)
    p = c.beginPath()
    p.moveTo(xcenter,ycenter+radius)
    angle = (2*pi)*2/5.0
    startangle = pi/2.0
    for vertex in range(nvertices-1):
        nextangle = angle*(vertex+1)+startangle
        x = xcenter + radius*cos(nextangle)
        y = ycenter + radius*sin(nextangle)
        p.lineTo(x,y)
    if nvertices==5:
        p.close()
    c.drawPath(p)
    
def hexagon(c, x, y, s):
    c.setFont(festivalfont, 7)
    c.drawCentredString(x, y, "Hexagon")
    p = c.beginPath()
    angle = 60
    p.moveTo(x, y)
    dy1 = s * sin(radians(angle))
    dx1 = sqrt(s**2 - dy1**2)
    x = x + dx1
    y = y + dy1
    p.lineTo(x, y)
    x = x + s
    p.lineTo(x, y)
    x = x + dx1
    y = y - dy1
    p.lineTo(x, y)
    x = x - dx1
    y = y - dy1
    p.lineTo(x, y)
    x = x - s
    p.lineTo(x, y)
    p.close()
    c.drawPath(p)
    
def octagon1(c, x, y, s):
    c.setFont(festivalfont, 7)
    c.drawCentredString(x, y, "Octagon1")
    angle = 67.5
    p = c.beginPath()
    p.moveTo(x, y)
    dy1 = s * sin(radians(angle))
    dx1 = sqrt(s**2 - dy1**2)
    x = x + dx1
    y = y + dy1
    p.lineTo(x, y)
    angle = 22.5
    dy2 = s * sin(radians(angle))
    dx2 = sqrt(s**2 - dy2**2)
    x = x + dx2
    y = y + dy2
    p.lineTo(x, y)
    x = x + dx2
    y = y - dy2
    p.lineTo(x, y)
    x = x + dx1
    y = y - dy1
    p.lineTo(x, y)
    x = x - dx1
    y = y - dy1
    p.lineTo(x, y)
    x = x - dx2
    y = y - dy2
    p.lineTo(x, y)
    x = x - dx2
    y = y + dy2
    p.lineTo(x, y)
    x = x - dx1
    y = y + dy1
    p.lineTo(x, y)
    p.close()
    c.drawPath(p)
    
def octagon2(c, x, y, s):
    c.setFont(festivalfont, 7)
    c.drawCentredString(x, y, "Octagon2")
    angle = 45
    p = c.beginPath()
    p.moveTo(x, y)
    y = y + s
    p.lineTo(x, y)
    dy1 = s * sin(radians(angle))
    dx1 = sqrt(s**2 - dy1**2)
    x = x + dx1
    y = y + dy1
    p.lineTo(x, y)
    x = x + s
    p.lineTo(x, y)
    x = x + dx1
    y = y - dy1
    p.lineTo(x, y)
    y = y - s
    p.lineTo(x, y)
    x = x - dx1
    y = y - dy1
    p.lineTo(x, y)
    x = x - s
    p.lineTo(x, y)
    x = x - dx1
    y = y + dy1
    p.lineTo(x, y)
    p.close()
    c.drawPath(p)
    
def bezier2(c, x, y):
    xd,yd = 5.5*cm/2, 3*cm/2
    xc,yc = xd,yd
    dxdy = [(0,0.33), (0.33,0.33), (0.75,1), (0.875,0.875),(0.875,0.875), (1,0.75), (0.33,0.33), (0.33,0)]
    pointlist = []
    for xoffset in (1,-1):
        yoffset = xoffset
        for (dx,dy) in dxdy:
            px = xc + xd*xoffset*dx
            py = yc + yd*yoffset*dy
            pointlist.append((px,py))
        yoffset = -xoffset
        for (dy,dx) in dxdy:
            px = xc + xd*xoffset*dx
            py = yc + yd*yoffset*dy
            pointlist.append((px,py))
    c.setLineWidth(cm*0.1)
    while pointlist:
        [(x1,y1),(x2,y2),(x3,y3),(x4,y4)] = pointlist[:4]
        del pointlist[:4]
        c.setLineWidth(cm*0.1)
        c.setStrokeColor(black)
        c.bezier(x+x1,y+y1, x+x2,y+y2, x+x3,y+y3, x+x4,y+y4)

def cadre(c, pagesize):
    width = pagesize[0]
    height = pagesize[1]
    dx = width / 10
    for i in range(11):
        c.line(i * dx, 0, i * dx, height)
    for i in range(15):
        c.line(0, i * dx, width, i * dx)

def penciltip(c, x, y, debug=1):
    u = cm/10.0
    c.setLineWidth(4)
    if debug:
        c.scale(2.8,2.8) # make it big
        c.setLineWidth(1) # small lines
    c.setStrokeColor(black)
    c.setFillColor(tan)
    p = c.beginPath()
    p.moveTo(x+10*u,y)
    p.lineTo(x,y+5*u)
    p.lineTo(x+10*u,y+10*u)
    p.curveTo(x+11.5*u,y+10*u, x+11.5*u,y+7.5*u, x+10*u,y+7.5*u)
    p.curveTo(x+12*u,y+7.5*u, x+11*u,y+2.5*u, x+9.7*u,y+2.5*u)
    p.curveTo(x+10.5*u,y+2.5*u, x+11*u,y, x+10*u,y)
    c.drawPath(p, stroke=1, fill=1)
    c.setFillColor(black)
    p = c.beginPath()
    p.moveTo(x,y+5*u)
    p.lineTo(x+4*u,y+3*u)
    p.lineTo(x+5*u,y+4.5*u)
    p.lineTo(x+3*u,y+6.5*u)
    c.drawPath(p, stroke=1, fill=1)
    if debug:
        c.setStrokeColor(green) # put in a frame of reference
        c.grid([x,x+5*u,x+10*u,x+15*u], [y,y+5*u,y+10*u])
        
def hand(c, x, y):
    (startx, starty) = (x,y)
    curves = [
( 0, 2), ( 0, 4), ( 0, 8), # back of hand
( 5, 8), ( 7,10), ( 7,14),
(10,14), (10,13), ( 7.5, 8), # thumb
(13, 8), (14, 8), (17, 8),
(19, 8), (19, 6), (17, 6),
(15, 6), (13, 6), (11, 6), # index, pointing
(12, 6), (13, 6), (14, 6),
(16, 6), (16, 4), (14, 4),
(13, 4), (12, 4), (11, 4), # middle
(11.5, 4), (12, 4), (13, 4),
(15, 4), (15, 2), (13, 2),
(12.5, 2), (11.5, 2), (11, 2), # ring
(11.5, 2), (12, 2), (12.5, 2),
(14, 2), (14, 0), (12.5, 0),
(10, 0), (8, 0), (6, 0), # pinky, then close
]
    u = cm*0.2
    p = c.beginPath()
    p.moveTo(startx, starty)
    ccopy = list(curves)
    while ccopy:
        [(x1,y1), (x2,y2), (x3,y3)] = ccopy[:3]
        del ccopy[:3]
        p.curveTo(x+x1*u,y+y1*u,x+x2*u,y+y2*u,x+x3*u,y+y3*u)
    p.close()
    c.drawPath(p, fill=0)
    
def spiral(c, x, y):
    p = c.beginPath()
    p.moveTo(x, y)
    for angle in range(0, 1800, 5):
        radius=angle/20
        dx=radius*cos(radians(angle))
        dy=radius*sin(radians(angle))
        p.lineTo(x + dx, y + dy)
    c.drawPath(p)
    p.close()
    
def heart(c, x, y, width, height):
    p = c.beginPath()
    pX = width/2.0
    pY = (height/100.0)*33.33
    
    x1 = (width/100.0)*50.0
    y1 = (height/100.0)*5.0
    x2 = (width/100.0)*90.0
    y2 = (height/100.0)*10.0
    x3 = (width/100.0)*90.0
    y3 = (height/100.0)*33.33
    p.moveTo(x + pX, y + pY)
    p.curveTo(x + x1, y + y1, x + x2, y + y2, x + x3, y + y3)
    p.moveTo(x + x3,y + pY)
    x1 = (width/100.0)*90.0
    y1 = (height/100.0)*55.0
    x2 = (width/100.0)*65.0
    y2 = (height/100.0)*60.0
    x3 = (width/100.0)*50.0
    y3 = (height/100.0)*90.0
    p.curveTo(x + x1, y + y1, x + x2, y + y2, x + x3, y + y3)
    x1 = (width/100.0)*50.0
    y1 = (height/100.0)*5.0
    x2 = (width/100.0)*10.0
    y2 = (height/100.0)*10.0
    x3 = (width/100.0)*10.0
    y3 = (height/100.0)*33.33
    p.moveTo(x + pX,y + pY)
    p.curveTo(x + x1, y + y1, x + x2, y + y2, x + x3, y + y3)
    p.moveTo(x + x3,y + pY)
    x1 = (width/100.0)*10.0
    y1 = (height/100.0)*55.0
    x2 = (width/100.0)*35.0
    y2 = (height/100.0)*60.0
    x3 = (width/100.0)*50.0
    y3 = (height/100.0)*90.0
    p.curveTo(x + x1, y + y1, x + x2, y + y2, x + x3, y + y3)
    p.moveTo(x + x3,y + y3)
    c.drawPath(p)
    p.close()
    
def create_CheatSheetAlbireo(filename, ps, pagesize, title="CheatSheetAlbireo"):
    try:
        c = canvas.Canvas(filename, pagesize=pagesize)
        c.setTitle(title)
        width, height = pagesize
        c.setFillColor(HexColor('#FECDE5'))
        c.rect(0, 0, width, height, fill=1)
        c.setFillColor(HexColor('#000000'))
        cadre(c, pagesize)
        titlefontsize_value = variable_dict["titlefontsize" + ps]
        titley_value = variable_dict["titley" + ps]
        namewidth = pdfmetrics.stringWidth(title, festivalfont, titlefontsize_value)
        c.setFont(festivalfont, titlefontsize_value)
        c.drawCentredString(width / 2, height - titley_value, title)
        c.setLineWidth(1)
        c.rect(325, 444, 40, 40)
        scale_value = variable_dict["scaleinfobox" + ps]
        drawing = scaleSVG('SVG/infobox.svg', float(scale_value))
        renderPDF.draw(drawing, c, 150, 475)
        dy = width / 10
        drawallroundRect(c,  30,  dy, 1, 1, 50, "#80ff84")
        drawrightroundRect(c,  230,  dy, 1, 40, 50, "#80ff84")
        drawleftroundRect(c,  430,  dy, 1, 40, 50, "#80ff84")
        drawtoproundRect(c,  230,  3 * dy, 40, 1, 50, "#80ff84")
        drawbottomroundRect(c,  430,  3 * dy, 40, 1, 50, "#80ff84")
        penciltip(c, 10, 50, True)
        star(c, title="Title", aka="Comment", xcenter=50, ycenter=130, nvertices=5)
        hexagon(c, x=100, y=130, s=20)
        octagon1(c, x=150, y=130, s=20)
        octagon2(c, x=140, y=170, s=20)
        bezier2(c, 100, 200)
        hand(c, 10, 200)
        spiral(c, 100, 350)
        heart(c, 200, 350, 50, 50)
        c.showPage()
        c.save()
        print(f"✅ PDF Festivals '{filename}' created successfully.")
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

create_CheatSheetAlbireo("PDF/CheatSheetAlbireo_A4.pdf", "A4", A4, title="A4 CheatSheetAlbireo")
create_CheatSheetAlbireo("PDF/CheatSheetAlbireo_A3.pdf", "A3", A3, title="A3 CheatSheetAlbireo")

key = input("Wait")
