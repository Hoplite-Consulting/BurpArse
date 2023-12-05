from xml.etree.ElementTree import Element
import fnmatch
from os.path import exists, splitext
from csv import DictWriter
from alive_progress import alive_it
import pkg_resources
import time
import base64

SORT_PATH = pkg_resources.resource_filename("burparse.config", "SORT.conf")

def readConfig(PATH: str) -> list:
    """_summary_

    Args:
        PATH (str): Path of Config File

    Returns:
        list: List of Config File Options
    """
    DEF_SORT = ["name", "host", "ip", "path", "location", "severity", "confidence", "issueBackground", "remediationBackground", "vulnerabilityClassification", "request", "response", "issueDetail"]

    try:
        VAR = []
        with open(PATH, "r") as f:
            lines = f.readlines()
        for l in lines:
            if l[0] == '#':
                continue
            elif l.strip() == '':
                continue
            else:
                VAR.append(l.strip())
    except:
        print(f"Failed to read config file {PATH}...")
        if "SORT" in PATH:
            print("Using Default List:", DEF_SORT)
            VAR = DEF_SORT
    
    return VAR

def getReportDict(issue: Element, arguments):

    # Excel is lame, dont mind the character limits............... SIGH
    # This method is almost ALWAYS going to throw one or more of these errors in verbose mode. This is expected and totally normal operation.

    reportDict = {}

    try:
        reportDict["name"] = issue.find('name').text[:30000]
    except Exception as e:
        if arguments.verbose:
            print(f"Error in processing 'name': {e}")

    try:
        host = issue.find('host')
        reportDict["ip"] = host.attrib["ip"]
    except Exception as e:
        if arguments.verbose:
            print(f"Error in processing 'host': {e}")

    try:
        reportDict["host"] = host.text[:30000]
    except Exception as e:
        if arguments.verbose:
            print(f"Error in processing 'host': {e}")

    try:
        reportDict["path"] = issue.find('path').text[:30000]
    except Exception as e:
        if arguments.verbose:
            print(f"Error in processing 'path': {e}")

    try:
        reportDict["location"] = issue.find('location').text[:30000]
    except Exception as e:
        if arguments.verbose:
            print(f"Error in processing 'location': {e}")

    try:
        reportDict["severity"] = issue.find('severity').text[:30000]
    except Exception as e:
        if arguments.verbose:
            print(f"Error in processing 'severity': {e}")

    try:
        reportDict["confidence"] = issue.find('confidence').text[:30000]
    except Exception as e:
        if arguments.verbose:
            print(f"Error in processing 'confidence': {e}")

    try:
        reportDict["issueBackground"] = issue.find('issueBackground').text.replace("<p>","").replace("</p>","")[:30000]
    except Exception as e:
        if arguments.verbose:
            print(f"Error in processing 'issueBackground': {e}")

    try:
        reportDict["remediationBackground"] = issue.find('remediationBackground').text.replace("<p>","").replace("</p>","")[:30000]
    except Exception as e:
        if arguments.verbose:
            print(f"Error in processing 'remediationBackground': {e}")

    try:
        reportDict["vulnerabilityClassification"] = issue.find('vulnerabilityClassification').text.replace("<ul>","").replace("</ul>","").replace("\n","")[:30000]
    except Exception as e:
        if arguments.verbose:
            print(f"Error in processing 'vulnerabilityClassification': {e}")

    try:
        reportDict["request"] = base64.b64decode(issue.find('requestresponse').find('request').text)[:30000]
    except Exception as e:
        if arguments.verbose:
            print(f"Error in processing 'request': {e}")

    try:
        reportDict["response"] = base64.b64decode(issue.find('requestresponse').find('response').text)[:30000]
    except Exception as e:
        if arguments.verbose:
            print(f"Error in processing 'response': {e}")

    try:
        reportDict["issueDetail"] = issue.find('issueDetail').text[:30000]
    except Exception as e:
        if arguments.verbose:
            print(f"Error in processing 'issueDetail': {e}")

    return reportDict
    
def saveCSVFile(reports: list, filePath: str, args) -> bool:

    # Initial Sort Config Reset for Each Report
    SORT_CONFIG = readConfig(SORT_PATH)
    
    # Check is OutFile Already Exists
    if not args.Force:
        try:
            if exists(f"{filePath}"):
                raise FileExistsError
        except FileExistsError as err:
            print(f"Output File Already Exists: {filePath}")
            if args.verbose:
                print(err)
            return False

    # Write to OutFile
    with open(f"{filePath}", "w") as outFile:
         writer = DictWriter(outFile, SORT_CONFIG)
         writer.writeheader()
         bar = alive_it(reports, title=f"Writing to file... {filePath}")
         for report in bar:
                                                # Use dictionary comprehension to filter unwanted fields
            sortedReport = {}                   # Initialize an empty dictionary to store filtered data
            for key, value in report.items():   # Iterate over key-value pairs in the original data
                if key in set(SORT_CONFIG):     # Check if the key is in the set of fields to include
                    sortedReport[key] = value   # Add filtered key value pair to the empty dictionary
            
            if args.Slow:
                time.sleep(.001)
            writer.writerow(sortedReport)

    return True

def getFileType(files: list, type: str, args) -> list:
    sortedFiles = []
    for file in files:
        fileType = splitext(file)[1]
        if fileType == type:
            sortedFiles.append(file)
        else:
            if args.verbose:
                print(f"'{file}' is not a valid filetype and will be skipped.")
    return sortedFiles