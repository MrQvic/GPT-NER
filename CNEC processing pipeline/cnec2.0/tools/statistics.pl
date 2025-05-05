#!/usr/bin/perl

use strict;
use warnings;

@ARGV > 0 or die "Usage: statistics.pl <plain_text_file(s)>\n";

our %classes;

foreach my $filename (@ARGV) {
    open I, "<$filename" or die "Can't open $filename for reading\n";
    while (<I>) {
        while ( m/<([^ <\/]+)\s*/g ) {
            $classes{$1}++;
        }
    }
}

my $sum = 0;
foreach my $c (keys %classes) {
    $sum += $classes{$c};
}

foreach my $c (sort keys %classes) {
    printf "%s %d %.2f%%\n",$c,$classes{$c},$classes{$c}*100/$sum;
}
