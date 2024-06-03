from alive_progress import alive_it
import xml.etree.ElementTree as ET
import pyfiglet
import argparse
from .utils import saveCSVFile, getFileType, getReportDict
import time

def parseFile(filePath: str, arguments) -> list:

	# Empty Reports List
	reports = []

	# Try to Parse XML Element Tree
	try:
		rawParse = ET.parse(filePath)
	except Exception as err:
		print(f"Failed to Parse XML File: {filePath}")
		if arguments.verbose:
			print(err)
		return False
	
	# Process Report Data from Nessus File
	bar = alive_it(rawParse.getroot().findall('issue'), title=f"Reading Report... {filePath}")
	for report in bar:
		if arguments.Slow:
			time.sleep(.01)
		reports.append(getReportDict(report, arguments))	
	return reports

def main(xmlFiles, args):

	reportsList = []

	for xmlFile in xmlFiles:
		try:
			nessusReport = parseFile(xmlFile, args)

			# Multi File Output
			if args.out == None:
				path = xmlFile + ".csv"
				saveCSVFile(nessusReport, path, args)

			# Single File Output
			if args.out != None:
				for i in nessusReport:
						reportsList.append(i)

		except Exception as err:
			print(f"Unable to Parse File: {xmlFile}")
			if args.verbose:
				print(err)
	
	if args.out != None:
		saveCSVFile(reportsList, args.out, args)
		pass

def setup():

	__version__ = "0.1.2"
	NAME = "BurpArse"
	DESC = """
	BurpArse is a BurpSuite .xml parser.

	It can be used in two different ways.
	It can create multiple CSV output files for every .xml file input, or it can create one CSV output file from all the .xml files.

	This is specified through the '-o/--out' flag.
	Without using this flag every .xml file will have an output of the same name and location as the original with .csv appended to the end.
	With this flag all the .xml files will be combined into one CSV output at your desired name and location.
	"""
	TITLE = pyfiglet.figlet_format(NAME, font="stop") + f"\n{NAME}\n{__version__}\n{DESC}"

	PARSER = argparse.ArgumentParser(description=f"{TITLE}", formatter_class=argparse.RawTextHelpFormatter)

	PARSER.add_argument('xmlFiles', type=str, nargs='+', help='.xml file/files or directory')
	PARSER.add_argument('-o', '--out', type=str, help='single output file location')
	PARSER.add_argument('-v', '--verbose', action='store_true', help='verbose error messaging')
	PARSER.add_argument('-F', '--Force', action='store_true', help='force file write')
	PARSER.add_argument('-S', '--Slow', action='store_true', help=argparse.SUPPRESS) # Runs the program slowly so you can watch the flashy loading bar.

	parsedArguments = PARSER.parse_args()

	# Make sure there are only .xml files being parsed.
	xmlFiles = getFileType(parsedArguments.xmlFiles, ".xml", parsedArguments)

	# Parse the files.
	main(xmlFiles, parsedArguments)

if __name__ == "__main__":
	setup()
