#-*- coding: utf-8 -*-

import sys
import fontforge

infile = sys.argv[1]
feafile = sys.argv[2]

hcr = fontforge.open(infile)

family = hcr.familyname[4:]

### turn on vertical metrics
hcr.hasvmetrics = 1

for gl in hcr.glyphs():
    if gl.unicode >= 0:
        gl.glyphname = fontforge.nameFromUnicode(gl.unicode)
        gl.vwidth = 1050
    else:
        if feafile.find("win") > 0:
            gl.vwidth = 1050
        elif gl.width > 0:
            gl.vwidth = 1050
        else:
            gl.vwidth = 0

hcr["space"].vwidth = 525

### make jungseong/jongseong full-width
for j in range(0x1100,0x115F)+range(0xA960,0xA97D):
    jamo = "uni%04X" % j
    hcr[jamo].left_side_bearing = (hcr[jamo].left_side_bearing + hcr[jamo].right_side_bearing) /2
    hcr[jamo].width = 970

hcr["uni1160"].width = 970

for j in range(0x1161,0x1200)+range(0xD7B0,0xD7C7)+range(0xD7CB,0xD7FC):
    jamo = "uni%04X" % j
    if family == "Dotum":
        if j == 0x117D: # hcr dotum uni117D bug
            hcr.selection.select(jamo+".y0")
            hcr.copy()
            hcr.selection.select(jamo)
            hcr.paste()
        elif j == 0xD7B0: # hcr dotum uniD7B0 bug.
            hcr.selection.select(jamo+".y6")
            hcr.copy()
            hcr.selection.select(jamo)
            hcr.paste()
    hcr[jamo].transform((1,0,0,1,970,0))
    hcr[jamo].left_side_bearing = (hcr[jamo].left_side_bearing + hcr[jamo].right_side_bearing) /2
    hcr[jamo].width = 970


if feafile.find("win") < 0 and feafile.find("mac") < 0: # no windows, no mac
    for tm in ["uni302E", "uni302F"]:
        newchrname = tm+".other"
        hcr.createChar(-1, newchrname)
        hcr.selection.select(tm)
        hcr.copy()
        hcr.selection.select(newchrname)
        hcr.paste()
        hcr[newchrname].width = 0
        hcr[newchrname].vwidth = 0
    for tm in ["uni302E", "uni302F"]:
        newchrname = tm+".othervert"
        hcr.createChar(-1, newchrname)
        hcr.selection.select(tm)
        hcr.copy()
        hcr.selection.select(newchrname)
        hcr.paste()
        hcr[newchrname].transform((1,0,0,1,970,0))
        hcr[newchrname].width = 970
        hcr[newchrname].vwidth = 0

### hA hAn
"""
if feafile.find("win") < 0 and feafile.find("mac") < 0: # no windows, no mac
    hcr.createChar( -1, "uni1112119E")
    hcr["uni1112119E"].addReference("uniF537")
    hcr["uni1112119E"].width = 970
    hcr["uni1112119E"].vwidth = 1050
    hcr.createChar( -1, "uni1112119E11AB")
    hcr["uni1112119E11AB"].addReference("uniF53A")
    hcr["uni1112119E11AB"].width = 970
    hcr["uni1112119E11AB"].vwidth = 1050
if feafile.find("win") < 0 and feafile.find("mac") < 0: # no windows, no mac
    hcr.createChar( -1, "space.hwid")
    hcr["space.hwid"].width = 485
    hcr["space.hwid"].vwidth = 525
"""

### tone marks
### positive width of Tone Marks
for tm in ["uni302E", "uni302F"]:
    wd = -hcr[tm].left_side_bearing - hcr[tm].right_side_bearing
    hcr[tm].left_side_bearing = (250 - wd) / 2
    hcr[tm].width = 250
    newchrname = tm+".vert"
    hcr.createChar(-1, newchrname)
    hcr.selection.select(tm)
    hcr.copy()
    hcr.selection.select(newchrname)
    hcr.paste()
    hcr[newchrname].transform((1,0,0,1,-250,0))
    hcr[newchrname].vwidth = 0
    if feafile.find("win") > 0:
        hcr[newchrname].width = 0
    else:
        hcr[newchrname].width = 970

#if feafile.find("win") > 0 or feafile.find("mac") > 0: # windows, mac
#    hcr.createChar( -1, "space.hwid")
#    hcr["space.hwid"].width = 485
#    hcr["space.hwid"].vwidth = 525

### vertical parentheses
for opening in [0xFE17,0xFE35,0xFE37,0xFE39,0xFE3B,0xFE3D,0xFE3F,0xFE41,0xFE43,0xFE47]:
    closing = opening + 1
    op = "uni%04X" % opening
    cl = "uni%04X" % closing
    clbb = hcr[cl].boundingBox()
    opbb = hcr[op].boundingBox()
    delta = hcr.ascent - clbb[3]
    delta = delta - hcr.descent - opbb[1] ### - 50
    hcr[op].transform((1,0,0,1,0,delta))
    hcr[op].vwidth = 1050

### horizontal halfwidth glyphs
hcr["uniFF61"].transform((1,0,0,1,0,-160))
hcr["uniFF61"].vwidth = 1050
hcr["uniFF65"].transform((1,0,0,1,0,-70))
hcr["uniFF65"].vwidth = 1050
if family == 'Dotum':
    hcr["uniFF64"].transform((1,0,0,1,0,-160))
    hcr["uniFF64"].vwidth = 1050

### horizontal fullwidth glyphs
for period in ["uniFF0C","uniFF0E"]:
    d = 110 - hcr[period].left_side_bearing
    hcr[period].transform((1,0,0,1,d,0))
    hcr[period].width = 970

for opening in ["uniFF08","uniFF1C","uniFF3B","uniFF5B","uniFF5F","uniFF40"]:
    d = hcr[opening].right_side_bearing - 54
    hcr[opening].transform((1,0,0,1,d,0))
    hcr[opening].width = 970

for closing in ["uniFF09","uniFF1E","uniFF3D","uniFF5D","uniFF60","uniFF07"]:
    d = 54 - hcr[closing].left_side_bearing
    hcr[closing].transform((1,0,0,1,d,0))
    hcr[closing].width = 970

hcr.save(infile)

