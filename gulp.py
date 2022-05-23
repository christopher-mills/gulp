#!/usr/bin/python
import argparse, csv, sys

arguments = argparse.ArgumentParser()
arguments.add_argument('filename', metavar='FILE', type=str,help='Specify a file name')
arguments.add_argument('--fields',type=str,help='List the fields in output order')
arguments.add_argument('-d','--delimiter',type=str,help='Specify a delimiter for the output (default is comma)')
arguments.add_argument('-q','--qualifier',type=str,help='Specify a text qualifier to surround the fields (default is double quotes)')
arguments.add_argument('--outfile',type=str,help='Specify an output file, otherwise defaults to STDOUT')
args = arguments.parse_args()

lastKey = None

sourceFile = open(args.filename, 'r')
outputFields = args.fields.split(',')

# Default delimeter is a comma. It's overridden if specified on the commandline.
delimiter = ','
if args.delimiter:
    delimiter = args.delimiter

# Default text qualifier is double quotes. It's overridden if specified on the commandline.
qualifier = '"'
if args.qualifier:
    qualifier = args.qualifier

if args.outfile:
	outfile = open(args.outfile,'w')

# Configure the output
if args.outfile:
    print("Writing output to",args.outfile)
    write_output = csv.writer(outfile,delimiter=delimiter,quotechar=qualifier,quoting=csv.QUOTE_MINIMAL)
else:
    write_output = csv.writer(sys.stdout,delimiter=delimiter,quotechar=qualifier,quoting=csv.QUOTE_MINIMAL)

# Print column headers
# The headers are specified from the commandline, and not the dataset.
write_output.writerow(outputFields)

#Print data
def print_log(fieldDict):
    output_data = []
    for outputField in outputFields:
        if outputField in fieldDict:
            output_data.append(fieldDict[outputField].strip('"'))
        else:
            # Account for missing fields in the data and substitute a dash for the value.
            output_data.append('-')
    write_output.writerow(output_data)

# Parse data
for line in sourceFile:
    # For now, this only works with input files with a key=value format. Here, we split those apart into a List structure.
    fields = line.split('=')
    fieldNumber = 0
    
    # The python Dictionary structure seemed to make the most sense here for referencing fields by name for printing. Initializing it here.
    fieldDict = {}

    # Iterate through the list of fields, stopping before the final element because it has just the value, and not a key.
    while fieldNumber < len(fields):
        # Taking the list that was split by the equals sign, and further separating it by spaces.
        # The last element separated by a space is actually the "key" for the value in the next row.
        value = fields[fieldNumber].split(' ')
        # The first and last list items will only have one element when split by a space.
        # The first list item will be the first key.
        # The last list item will be the value for the final key.
        # The rows contain a key, and the value that matches up with the previous row's key.
        # This is messy, but we are here because some vendors thought it would be a good idea to write logs this way.
        if len(value) == 1:
            if lastKey:    
                fieldDict[lastKey]=' '.join(value).strip()
                lastKey = None
            else:
                lastKey = value[-1]
            fieldNumber += 1
        else:
            fieldDict[lastKey]=' '.join(value[0:-1]).strip()
            lastKey = value[-1]
            fieldNumber += 1
    print_log(fieldDict)