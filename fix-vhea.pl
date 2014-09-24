my $myvalue = $ARGV[0] =~ /win/ ? 800 : 1000;

my $mintsb = 0;

if ($myvalue == 1000) { # not windows
  my $vmtx = $ARGV[0];
  $vmtx =~ s/vhea/vmtx-fix/;

  open $fh, $vmtx or die;
  while (<$fh>) {
    if(/tsb="([\-\d]+)"/) {
      $mintsb = $1 < $mintsb ? $1 : $mintsb;
    }
  }
  close $fh;
}

while(<>) {
  if (/ascent value="[\-\d]+"/) {
    if ($myvalue == 800) {
      s/value="[\-\d]+"/value="800"/; # windows
    }
    else {
      s/value="[\-\d]+"/value="1000"/;
    }
  }
  elsif (/descent value="[\-\d]+"/) {
    if ($myvalue == 800) {
      s/value="[\-\d]+"/value="800"/; # windows
    }
    else {
      s/value="[\-\d]+"/value="600"/;
    }
  }
  elsif (/minTopSideBearing value="[\-\d]+"/) {
    if ($myvalue == 1000) { # not windows
      s/value="[\-\d]+"/value="$mintsb"/;
    }
  }
  print;
}

