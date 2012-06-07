#!/usr/bin/env perl
use strict;
use warnings;
use Modern::Perl;

my $password;
my @wordlist;
my $number;

@wordlist = qw[parallax
focus
macro
ambient
view
aperture
bulb
shutter
stock
angle
color
density
depth
flash
diffuse
filter
finder
focal
frame
ortho
print
film
zoom
lens];

my $word_count = @wordlist;
my $word = $wordlist[int(rand($word_count))];
$number = int(rand(999));
$password = $word.$number;

say "Password is: $password";



