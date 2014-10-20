
my $batang = $ARGV[0] =~ /Batang/ ? 1 : 0;

my ($start,$stop,$tmvstart, $tmvstop) = (62864,64219,64791,64794);
if ($batang) {
  $start = 62420;
  $stop = 63775;
  $tmvstart = 64347;
  $tmvstop = 64350;
}

while(<>) {
  if (/name="glyph(\d+)"\s+height="0"\s+tsb="([\-\d]+)"/) {
    my ($glyph,$tsb) = ($1,$2);
    if ( ($glyph >= $start and $glyph <= $stop)
        or ($glyph >= $tmvstart and $glyph <= $tmvstop) ) {
      $tsb = $tsb - 1050 ; # 1050 is total height
      s/tsb="[\-\d]+"/tsb="$tsb"/;
    }
  }
  print;
}

