# gulp
General Utility Log Parser - Make oddball log formats ingestible.

I am a new coder, so there's lot of comments in the script so I don't get lost.

23 MAY 2022 - Currently supports input files of key=value format.

To use: ./gulp.py <input file name> --fields=your,fields,here
    This will read the specified input data file, look for the fields you specify with --fields, and then output as a CSV.

Example:
    Input file named "sample.txt" contains: sport=12345 sip=192.168.1.1 dport=31337 dip=172.22.99.88 timestamp="2022-01-01 22:01:01" deviceid=12345

    Command line: ./gulp.py sample.txt --fields=sip,sport,dip,dport,deviceid,timestamp

    Output:
        sip,sport,dip,dport,deviceid,timestamp
        192.168.1.1,12345,172.22.99.88,31337,12345,2022-01-01 22:01:01