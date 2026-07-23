#-*- coding: utf-8 -*-

import sys
import fontforge

infile = sys.argv[1]
feafile = sys.argv[2]

hcr = fontforge.open(infile)

family = hcr.familyname[4:]

### drop native jamo lookups; our feature files replace them
for lookup in hcr.gsub_lookups:
    feats = hcr.getLookupInfo(lookup)[2]
    tags = set(f[0] for f in feats)
    scripts = set(s[0] for f in feats for s in f[1])
    if tags & {"ljmo","vjmo","tjmo"} or ("rlig" in tags and "hang" in scripts):
        hcr.removeLookup(lookup)

### remove buggy glyphs
hcr.removeGlyph(-1, "uni302F.vert")
hcr.removeGlyph(-1, "uni302E.vert")
hcr.removeGlyph(-1, "Oldhangul_1")
hcr.removeGlyph(-1, "Oldhangul_705Oldhangul_702")
hcr.removeGlyph(-1, "Oldhangul_3254")
hcr.removeGlyph(-1, "Oldhangul_3253")
hcr.removeGlyph(-1, "Oldhangul_705glyph702")

### also drop orphaned helper lookups: any substitution still pointing
### at a pre-rename or removed glyph name is dead and would only emit
### "unused glyph" warnings at generate time
def missing(name):
    try:
        hcr[name]
        return False
    except Exception:
        return True

deadsubs = set()
for gl in hcr.glyphs():
    for entry in gl.getPosSub("*"):
        if entry[1] in ("Substitution","AltSubs","MultSubs","Ligature") \
           and any(missing(t) for t in entry[2:]):
            deadsubs.add(entry[0])
for sub in deadsubs:
    lookup = hcr.getLookupOfSubtable(sub)
    if lookup in hcr.gsub_lookups:
        hcr.removeLookup(lookup)

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
for j in list(range(0x1100,0x115F))+list(range(0xA960,0xA97D)):
    jamo = "uni%04X" % j
    hcr[jamo].left_side_bearing = int(hcr[jamo].left_side_bearing + hcr[jamo].right_side_bearing) // 2
    hcr[jamo].width = 970

hcr["uni1160"].width = 970

for j in list(range(0x1161,0x1200))+list(range(0xD7B0,0xD7C7))+list(range(0xD7CB,0xD7FC)):
    jamo = "uni%04X" % j
    hcr[jamo].transform((1,0,0,1,970,0))
    hcr[jamo].left_side_bearing = int(hcr[jamo].left_side_bearing + hcr[jamo].right_side_bearing) // 2
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
    hcr[tm].left_side_bearing = int(250 - wd) // 2
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

