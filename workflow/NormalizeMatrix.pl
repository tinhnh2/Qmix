#!/usr/bin/perl -w
#use Getopt::Long;  # to parse command line parameters
use Getopt::Std;  # to parse command line parameters
use strict;
use warnings;
use feature qw/switch/; 
my $MINVALUE = 0.0000000001;
sub usage()
{
  print STDERR << "EOF";

usage: perl $0 -i input
EOF

  exit;
}

my %options=();
my $opt_string = 'i:h';
getopts("$opt_string",\%options) or usage();

if (!keys %options) { usage(); };
usage() if $options{h};

my $origFile = $options{i};


#my $usage = "Usage: perl NormalizeMatrix.pl paml_file\n";
#my $origFile = shift or die($usage);
my $outputFile = "$origFile".".normalized";

open ( my $inFile, '<', $origFile )		   or die "Cannot open the input file: $origFile: $!";
open ( my $outFile, '>', $outputFile )		   or die "Cannot open the output file: $outputFile: $!";

my @R;
my @Q;
my @pi;
my @temp;
my $line;

# Read paml file into matrix "R" and vector "pi" 
for (my $i=0; $i<20; $i++) {
	for (my $j=0; $j<20; $j++) {
		$R[$i][$j] = 0.0;
	}
}
$R[0][0] = 0;
for (my $i=1; $i<20; $i++){
		$line = <$inFile>;
		my @values = split(' ',$line);
		for (my $j=0; $j<$i; $j++){
			$R[$i][$j]=$values[$j];
		}
}
#$line = <$inFile>;
$line = <$inFile>;
my @values = split(' ',$line);
for(my $j=0; $j<20; $j++) {
	$pi[$j] = $values[$j];
}
for (my $i=0; $i<20; $i++) {
	for (my $j=0; $j<20; $j++) {
		if( $j > $i){
			$R[$i][$j] = $R[$j][$i];
		}
	}
}
for (my $i=0; $i<20; $i++) {
	for (my $j=0; $j<20; $j++) {
		$Q[$i][$j] = $pi[$j]*$R[$i][$j];
	}
}

my $temp=0;
for(my $x=0;$x<20;$x++) {
	$temp = 0;
	for(my $y=0;$y<20;$y++) {
		if($x!=$y) {
			$temp += $Q[$x][$y];
		}
	}
	$Q[$x][$x] = -$temp;
}
my $miu=0;
for(my $x=0;$x<20;$x++) {
	$miu = $miu - $pi[$x]*$Q[$x][$x];
}
#
print "MIU: $miu\n";

for(my $x=0;$x<20;$x++) {
	for(my $y=0;$y<20;$y++) {
		if($y<$x) {
			$R[$x][$y]=$R[$x][$y]/$miu;
		}
	}
}

for (my $i=0; $i<20; $i++) {
	for (my $j=0; $j<20; $j++) {
		if ($i > $j) {
			printf $outFile "\%.6f ",$R[$i][$j];
		}
	}
	if ($i > 0) {
		print $outFile "\n";
	}
}

#print $outFile "\n";

for (my $j=0; $j<20; $j++) {
	printf $outFile "\%.6f ",$pi[$j];

}

close ($outFile);
close ($inFile);
