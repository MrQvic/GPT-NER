#!/usr/bin/perl

use strict;
use warnings;

@ARGV == 1 or die "Usage: namedent_annotations_to_html.pl text_file\n";

our $html_template = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>
       Czech Named Entity Corpus 2.0
    </title>
    <style type="text/css"><!--
      span { color: #000; font-family: sans-serif; font-weight: bold; }

      span.namedent_A { color: #600; border-bottom: 1px solid #600; }
      span.namedent_C { color: #f50; border-bottom: 1px solid #f50; }
      span.namedent_T { color: #939; border-bottom: 1px solid #939; }
      span.namedent_P { color: #090; border-bottom: 1px solid #090; }

      span.namedent_ah, span.namedent_at, span.namedent_az
        { color:#00f; }

      span.namedent_g_, span.namedent_gc, span.namedent_gh, span.namedent_gl,
      span.namedent_gq, span.namedent_gr, span.namedent_gs, span.namedent_gt,
      span.namedent_gu
        { color:#600; }

      span.namedent_i_, span.namedent_ia, span.namedent_ic, span.namedent_if,
      span.namedent_io
        { color:#399; }

      span.namedent_me, span.namedent_mi, span.namedent_mn, span.namedent_ms
        { color:#f08; }

      span.namedent_n_, span.namedent_na, span.namedent_nb, span.namedent_nc,
      span.namedent_ni, span.namedent_no, span.namedent_ns
        { color:#933; }

      span.namedent_o_, span.namedent_oa, span.namedent_oe, span.namedent_om,
      span.namedent_op, span.namedent_or
        { color:#c90; }

      span.namedent_p_, span.namedent_pc, span.namedent_pd, span.namedent_pf,
      span.namedent_pm, span.namedent_pp, span.namedent_ps
        { color:#090; }

      span.namedent_td, span.namedent_tf, span.namedent_th, span.namedent_tm,
      span.namedent_ty
        { color:#939; }
    --></style>
  </head>
<body>

<!-- Legenda -->
<h2>Legend</h2>
<ul>
    <li><span class="namedent_az">a - Numbers in addresses</span>
      <ul><li><span class="namedent_A">A - Group of named entities forming an address</span></li></ul></li>
    <li><span class="namedent_gc">g - Geographical names</span></li>
    <li><span class="namedent_ia">i - Institutions</span></li>
    <li><span class="namedent_mn">m - Media names</span></li>
    <li><span class="namedent_na">n - Number expressions</span>
      <ul><li><span class="namedent_C">C - Group of named entities forming a bibliographic item</span></li></ul></li>
    <li><span class="namedent_oa">o - Artifact names</span></li>
    <li><span class="namedent_ps">p - Personal names</span>
        <ul><li><span class="namedent_P">P - Group of named entities forming a name</span></li></ul></li>
    <li><span class="namedent_tc">t - Time expressions</span>
        <ul><li><span class="namedent_T">T - Group of named entities forming a date or time</span></li></ul></li>
</ul>

<hr />

<p>
#output#
</p>
</body>
</html>
';

open I,"<$ARGV[0]" or die "Can't open file $ARGV[0] for reading\n";
my @lines = grep { /\S/ and !/^#/ } <I>;
map { chomp($_); } @lines;
map { $_ =~ s/>/<\/span>/g; } @lines;
map { $_ =~ s/<([^ <\/]+)\s*/<span class=\"namedent_$1\">/g; } @lines;
my $output = join "<br />\n", @lines;
$html_template =~ s/#output#/$output/;
print $html_template;
