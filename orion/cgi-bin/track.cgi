#!/usr/bin/perl -w
# Modules included by "use"
use strict;
use CGI qw(:standard);
# use CGI qw(:standard Vars);
use Fcntl qw(:flock :seek);
# use Socket;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
# end of Modules included by "use"

#-----------------------------------
# Tracking script
# Version	1.3.1
#-----------------------------------

# configugation start
my $debug = 0;					# 1 means "debug mode"

# configure IPs
my $MY_LOCAL_IP_ADDR = "127.0.0.1";		# this is me
my $MY_REMOTE_IP_ADDR = "84.238.140.75";	# this is me

# configure "var" directory depending on server
my $host = $ENV{SERVER_NAME} ? $ENV{SERVER_NAME} : "";
my $script_filename = $ENV{SCRIPT_FILENAME} ? $ENV{SCRIPT_FILENAME} : "$0";
my $my_dir = $script_filename;
$my_dir =~ s#(.*)/.*$#$1#;			# script directory
chdir ($my_dir);				# ensure the current directory

my $var_dir = ".";
$var_dir = "$ENV{DOCUMENT_ROOT}/var"	if $host =~ /.*netfirms\.com.*/;
$var_dir = "../var"			if $host =~ /.*prohosting\.com.*/;
$var_dir = "../private/var"		if $host =~ /.*stonestreem.com.*/;
$var_dir = "../test"			if $host =~ /.*localhost.*/;

# configure track & log files
my $track_file = "$var_dir/track.csv";		# .csv format
my $log_file = "$var_dir/log.csv";		# .csv format
# configuration end

#-----------------------------------

# begin here
# IP address
my $remote_addr = $ENV{REMOTE_ADDR} ? $ENV{REMOTE_ADDR} : "IP is not set";
# page - http://page?page_referer
my $query_string = $ENV{QUERY_STRING} ? $ENV{QUERY_STRING} : "direct referer";
# page referer
my $referer = $ENV{HTTP_REFERER} ? $ENV{HTTP_REFERER} : "unknown page";
# browser
my $user_agent = $ENV{HTTP_USER_AGENT} ? $ENV{HTTP_USER_AGENT} : "unknown browser";


my ($key, $val);
my %tracks = ();
my $page_visits = join (',', $referer, "");	# separator is ',' (http://page,)


if ($debug == 1)
{
	print header;
	print start_html("OK");
}
else
{
	print header;
#	print "// comment output";
}
&handle_IP ();				# IP handler


# open for read/write or create file
open (FH, "+<$track_file") or open (FH, ">$track_file") or die "Can't open file: $!";
flock (FH, LOCK_EX);			# set an exclusive lock 
seek (FH, 0, SEEK_SET);			# then seek the beginning of file

while (my $rec = <FH>)			# read hash from file
{
	($key, $val) = ($rec =~ m'(.*\D)(\d+)$');	# non digits, digits
	$tracks{$key} = $val;
}
if (!exists $tracks{$page_visits})	# if page entry not exist - create in hash
{
	$tracks{$page_visits} = 0;
}
$tracks{$page_visits}++;		# increment count visits for this page

seek (FH, 0, SEEK_SET);			# then seek the beginning of file
foreach my $key (keys(%tracks))		# write hash to file
{
	print FH $key, $tracks{$key}, "\n";
}

close (FH);				# close file


# write to lof file
&log_this (" $remote_addr ", ",\"$referer\"", ",\"$query_string\"", ",\"$user_agent\"");


print end_html	if ($debug == 1);

#-----------------------------------





# subroutines begin here

sub handle_IP
{
	#	$ENV{REMOTE_ADDR} - IP address
	
	if ($remote_addr eq "$MY_REMOTE_IP_ADDR")
	{
		if ($debug == 1)
		{
			print "<h1>", "Remote IP &nbsp;&nbsp;", $remote_addr, "</h1>";
			print end_html;
		}
		exit;
	}
	if ($remote_addr eq "$MY_LOCAL_IP_ADDR")
	{
		if ($debug == 1)
		{
			print "<h1>", "Local IP &nbsp;&nbsp;", $remote_addr, "</h1>";
			print end_html;
		}
		exit;
	}
}


sub log_this
{
	my @log_data = @_;
	
	open (FH, ">>$log_file") or die "Can't create file: $!";
	flock (FH, LOCK_EX);		# set an exclusive lock 
	seek (FH, 0, SEEK_END);		# then seek the end of file

	print FH "[", my $now_GMT = gmtime, " GMT], ", "$0,", @log_data, "\n";

	close (FH);
}







