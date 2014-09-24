my @NEWJAMO = (
    0x1100..0x1112,
    0x1161..0x1175,
    0x11a8..0x11c2
);

my @NEWSET = qw/
33 33 46 46 46 46 38 38 38 38 38 38 38 38 38 33
46 46 38  6 12  6 12 60 60 60 60 40 40 45 40 50
30 20 25 20 30 22 18  6 13 13 13 13 13 13 13 13
13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13
13 13 13
/;

my @OLDJAMO = (
    0x115f, 0x1160,
    0x1100..0x115e,
    0xa960..0xa97c,
    0x1161..0x11a7,
    0xd7b0..0xd7c6,
    0x11a8..0x11ff,
    0xd7cb..0xd7fb
);

my @OLDSET = qw/
1   2
17 17 20 20 15 20 15 15 15 15 15 15 15 15 15 17
20 20 16 15 15 15 15 15 15 15 15 15 15 15 15 15
15 15 15 15 15 15 15 15 15 15 15 15 15 15 15 15
15 15 15 15 15 15 15 15 15 15 15 15 15 15 15 15
15 15 15 15 15 15 15 15 15 15 15 15 15 15 15 15
15 15 15 15 15 15 15 15 15 15 15 15 15 15 15 15
15 15 15 15 15 15 15 15 15 15 15 15 15 15 15 15
15 15 15 15 15 15 15 15 15 15 15 15
 8  8  8  8 16 16 16 16  8 12 12 12  8  3  4  4
 4  3  3  4  8  4  4  4  4  4  4  4  4  4 12 12
12  8  8 12 12 12  8 12  4  4  4  4  2  4  4  4
 4  4  2  4  2  2  4  8  8  4  4  4  8  3 16  8
 8  2  4  4 20 12 12 12  8 12 12 12  4  4  4  2
 4  4  4  2  4  8  8  8  4  4  4  8  8 16
 5  5  5  6  5  5  5  5  5  5  5  5  5  5  5  5
 5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5
 5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5
 5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5
 5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5
 5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5
 5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5
 5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5
 5  5  5  5  5  5  5  5  5
/;

my @BOLDSET = qw/
1   2
17 17 20 20 15 20 15 15 15 15 15 15 15 15 15 17
20 20 16 15 15 15 15 15 15 15 15 15 15 15 15 15
15 15 15 15 15 15 15 15 15 15 15 15 15 15 15 15
15 15 15 15 15 15 15 15 15 15 15 15 15 15 15 15
15 15 15 15 15 15 15 15 15 15 15 15 15 15 15 15
15 15 15 15 15 15 15 15 15 15 15 15 15 15 15 15
15 15 15 15 15 15 15 15 15 15 15 15 15 15 15 15
15 15 15 15 15 15 15 15 15 15 15 15
 8  8  8  8 16 20 16 20  8 12 12 12  8  3  4  4
 4  3  3  4  8  4  4  4  4  4  4  4  4  4 12 12
12  8  8 12 12 12  8 12  4  4  4  4  2  4  4  4
 4  4  2  4  2  2  4  8  8  4  4  4  8  3 16  8
 8  2  4  4 20 12 12 12  8 12 12 12  4  4  4  2
 4  4  4  2  4  8  8  8  4  4  4  8  8 20
 5  5  5  6  5  5  5  5  5  5  5  5  5  5  5  5
 5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5
 5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5
 5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5
 5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5
 5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5
 5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5
 5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5
 5  5  5  5  5  5  5  5  5
/;

#$ARGV[0] eq 'HANBatang.sfd' or @OLDSET = @BOLDSET;
@OLDSET = @BOLDSET;


my ($olddoit,$newdoit,$i,$j,$name) = (0,0,0,0,'');

while(<>) {
    if (/^Lookup.*kern/) {
	s/\)/'hang' <'KOR ' 'dflt' > \)/;
    }
###    if (/StartChar\:\s+hangul\.000\s*$/) {
    if (/StartChar\:\s+Oldhangul_2\s*$/) {
	$olddoit = 1;
	$newdoit = 0;
	$i = 0;
	$j = 0;
    }
    if (/StartChar\:\s+glyph97\s*$/) {
#       	$newdoit = 1;
       	$newdoit = 0;
	$olddoit = 0;
	$i = 0;
	$j = 0;
    }
    if ($newdoit and $NEWJAMO[$i] and /StartChar\:/) {
	$name = sprintf ("uni%04X.n%d",$NEWJAMO[$i],$j);
	$_ = "StartChar: $name\n";
	$j++;
	if($j >= $NEWSET[$i]) {
	    $i++;
	    $j = 0;
	}
    }
    if ($olddoit and $OLDJAMO[$i] and /StartChar\:/) {
	$name = sprintf ("uni%04X.y%d",$OLDJAMO[$i],$j);
	$_ = "StartChar: $name\n";
	$j++;
	if($j >= $OLDSET[$i]) {
	    $i++;
	    $j = 0;
	}
    }
    print;
}


