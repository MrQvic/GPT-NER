#!/usr/bin/perl
# Conversion tool from named entities annotations to smple xml

use strict;
use warnings;

@ARGV > 0 or die "Usage: namedent_annotations_to_simple_xml.pl <text_file(s)>\n"; 

foreach my $filename (@ARGV) {
    open I,"<$filename" or die "Can't open file $filename for reading\n";
    my @lines = grep { /\S/ and !/^#/ } <I>;
    print "<doc>\n";
    map { $_ =~ s/^\d+: //; } @lines;
    map { $_ =~ s/>/<\/ne>/g; } @lines;
    map { $_ =~ s/<([^ <\/]+)\s*/<ne type=\"$1\">/g; } @lines;
    map { print $_; } @lines;
    print "</doc>\n";
}


