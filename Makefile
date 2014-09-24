
NAME = ${HCRTTF}
SUFF = LVT
FEA = $(NAME).fea
FONT = $(NAME)-$(SUFF)
VHEA = $(FONT)-vhea
VMTX = $(FONT)-vmtx
DATE = $(shell date "+%Y%m%d%H%M")

all: sfd glyphs ttf ttx

sfd:
	fontforge -script 00savesfd.pe $(NAME).ttf
	perl 01jamoglyphnames.pl $(NAME).sfd > $(FONT).sfd

glyphs:
	fontforge -script 03tweakglyphs.py  $(FONT).sfd $(FEA)

ttf:
	fontforge -script 04mergefeature.py $(FONT).sfd $(FEA)

ttx:
	ttx -o $(VMTX).ttx -t vmtx $(FONT).ttf
	perl fix-vmtx.pl $(VMTX).ttx > $(VMTX)-fix.ttx 
	ttx -o $(FONT)-tmp.ttf -m $(FONT).ttf $(VMTX)-fix.ttx
	mv -f $(FONT)-tmp.ttf $(FONT).ttf
	ttx -o $(VHEA).ttx -t vhea $(FONT).ttf
	perl fix-vhea.pl $(VHEA).ttx > $(VHEA)-fix.ttx 
	ttx -o $(FONT)-tmp.ttf -m $(FONT).ttf $(VHEA)-fix.ttx
	mv -f $(FONT)-tmp.ttf $(FONT).ttf

test:
	xetex '\def\testfontname{$(FONT)}\input oldhangulcomposed-test.tex'
	xetex '\def\testfontname{$(FONT)}\input newhangultest.tex'

clean:
	rm -f $(NAME).sfd *.log *.pdf *.ttx 

clean-all:
	rm -f *.sfd *.log *.pdf *.ttx

dist-source:
	cd .. && tar -czf make-hcr-gsub_$(DATE).tar.gz \
		hcr-lvt/*.pl hcr-lvt/*.py hcr-lvt/*.pe hcr-lvt/*.fea \
		hcr-lvt/*.tex hcr-lvt/Makefile* hcr-lvt/README 

dist-font:
	cd .. && zip Hamchorom-LVT.zip hcr-lvt/HAN*-LVT.ttf

