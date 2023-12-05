# BurpArse

BurpSuite XML parser written in Python with config files for easy setup and usage.

Written by [Oliver Scotten](https://www.github.com/oliv10).

### Requirements
- Python 3.10.4 or greater

### Configuration
- SORT.conf - This is both the order and which items are shown in the CSV output.

### Usage
- Install requirements
```
pip3 install .
```

Run the command ```burparse``` anywhere!

```
usage: burparse [-h] [-o OUT] [-v] [-F] xmlFiles [xmlFiles ...]

 ______                                           
(____  \                     /\                   
 ____)  )_   _  ____ ____   /  \   ____ ___  ____ 
|  __  (| | | |/ ___)  _ \ / /\ \ / ___)___)/ _  )
| |__)  ) |_| | |   | | | | |__| | |  |___ ( (/ / 
|______/ \____|_|   | ||_/|______|_|  (___/ \____)
                    |_|                           

BurpArse
0.1.1

        BurpArse is a BurpSuite .xml parser.

        It can be used in two different ways.
     It can create multiple CSV output files for every .xml file input, or it can create one CSV output file from all the .xml files.

     This is specified through the '-o/--out' flag.
     Without using this flag every .xml file will have an output of the same name and location as the original with .csv appended to the end.
     With this flag all the .xml files will be combined into one CSV output at your desired name and location.


positional arguments:
  xmlFiles           .xml file/files or directory

options:
  -h, --help         show this help message and exit
  -o OUT, --out OUT  single output file location
  -v, --verbose      verbose error messaging
  -F, --Force        force file write
```