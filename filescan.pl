my $file = "$ARGV[0]";
open (FILE, $file);
my @flist = <FILE>;
print "Search for: ";
my $search = <STDIN>;
chomp $search;
@lines = grep /$search/, @flist;
print @lines;
