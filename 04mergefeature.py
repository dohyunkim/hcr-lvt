#-*- coding: utf-8 -*-

import sys
import time
import fontforge

infile = sys.argv[1]
feafile = sys.argv[2]
outfile = infile.replace('.sfd','.ttf')

hcr = fontforge.open(infile)

family = hcr.familyname[4:]

hcr.mergeFeature(feafile)
# disable aalt as we have 16bit limit
# hcr.buildOrReplaceAALTFeatures()


today = time.strftime('%Y%m%d',time.localtime(time.time()))
hcr.version = 'Version 1.959; KTS Build '+today
hcr.sfntRevision = None

hcr.familyname = hcr.familyname.replace(family,family+' LVT')
hcr.fullname   = hcr.fullname.replace(family,family+' LVT')
hcr.fontname   = hcr.fontname.replace(family,family+'LVT')

hcr.appendSFNTName(0x409,3,'YoonDesign: '+hcr.fullname+': KTS '+today)
hcr.appendSFNTName(0x409,5, hcr.version)
hcr.appendSFNTName(0x409,8,'YoonDesign; The Korean TeX Society')
hcr.appendSFNTName(0x409,10,'The Korean TeX Society has added GSUB/GPOS/vhea/vmtx tables chiefly for old hangul rendering. Please contact http://www.ktug.org for these issues.')
hcr.appendSFNTName(0x409,18, hcr.fullname)

if family == 'Batang':
    hangulfamily = '함초롬바탕 LVT'
else:
    hangulfamily = '함초롬돋움 LVT'
if hcr.os2_weight == 400:
    hangulfull = hangulfamily
else:
    hangulfull = hangulfamily+' Bold'

hcr.appendSFNTName('Korean',1,hangulfamily)
hcr.appendSFNTName('Korean',3,'YoonDesign: '+hcr.fullname+': KTS '+today)
hcr.appendSFNTName('Korean',4,hangulfull)

# 'post' format is now 3.0 (no postscript glyph names)
# because dvipdfmx gives warning with format 2.0
# NO! this brings up tounicode issue!
hcr.generate(outfile,flags=('short-post','opentype'))
#hcr.generate(outfile)

