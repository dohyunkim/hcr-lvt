
$found = 0;

while(<>) {
#  if (/name="uni(....)".+tsb="([\-\d]+)"/) {
#    my ($uni,$tsb) = ($1,$2);
#    my $c = hex $uni;
#    if (($c >= 0x1161 and $c <= 0x11ff) or ($c >= 0xd7b0 and $c <= 0xd7fb)) {
#      $tsb = $tsb - 1050 ; # 1050 is total height
#      s/tsb="[\-\d]+"/tsb="$tsb"/;
#      # s/height="\d+"/height="0"/; ## delete me
#    }
#  }
#  elsif (/name="glyph\d+"\s+height="0"\s+tsb="([\-\d]+)"/) {
  if (/name="glyph\d+"\s+height="0"\s+tsb="([\-\d]+)"/) {
    my $tsb = $1;
    if ($tsb and $tsb != 830 and $found >= 0) {
      $found = 1;
      $tsb = $tsb - 1050 ; # 1050 is total height
      s/tsb="[\-\d]+"/tsb="$tsb"/;
    }
  }
  else {
    $found and $found = -1;
  }
  print;
}

