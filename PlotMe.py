import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os


class MyError(Exception):
    pass


def selectData():
    """ Clear the Command Prompt Window
    """
    os.system('cls')

    """ Input the .CSV filename for plotting.
    """
    while True:
        try:
            fname = input("\nEnter .CSV filename for analysis: ")
            """ Filename change to all CAPS makes it easier to
                error-check.
            """
            if (fname.upper().endswith(".CSV") == False):
                raise MyError("")
            df = pd.read_csv(fname)
            break
        except OSError:
            print("\n*** Filename '%s' does not exist! ***" % fname)
        except pd.parser.CParserError:
            print("\n*** Incompatible file type: Select valid .CSV file! ***")
        except UnicodeDecodeError:
            print("\n*** Incompatible file type: Select valid .CSV file! ***")
        except MyError:
            print("\n*** Incompatible file type: Select valid .CSV file! ***")
    return df, fname


def displayParams(parameterList, fname):
    """ Create a dictionary with the keys being a range of numbers from
        1 to the max number of parameters, and the values are the
        individual parameter names.  Display the keys and values
        (shortened header names).
    """
    print()
    print("File: ", fname)
    print()
    print("AVAILABLE PARAMETERS FOR PLOTTING:")
    dataDict = {}
    count = 1
    for item in parameterList:
        dataDict[count] = item
        print(str(count) + " - " + item)
        count += 1
    # print(list(dataDict.items()))
    return count, dataDict


def selectParams(plotsCount, plotsDict):
    while True:
        try:
            selNumberList = []
            selParameterList = []
            print("\nSelect up to 8 parameters to plot...\n",
                  "   [Enter 0 to PLOT selections]\n")
            for num in range(0, 8):
                entry = int(input("Plot #%d" % (num + 1) +
                                  " [Enter 1 - %d]" % (plotsCount - 1) + ": "))
                """ User must enter at least one parameter to in order
                    to proceed to plotting.  Raise an error if a '0' is
                    entered on the very first input.
                """
                if num == 0:
                    if entry == 0:
                        raise MyError("")
                if entry == 0:
                    break
                else:
                    selNumberList.append(entry)
                    selParameterList.append(plotsDict[int(selNumberList[num])])
            return selParameterList
            break
        except MyError:
            print("\n*** Select at least one parameter to plot! ***")
        except:
            print("\n*** Entry is invalid! ***\n")


def plotParams(dataFrame, paramList):
    matplotlib.style.use('ggplot')
    """ Set up the x-axis in order to plot against time in 12.5ms
        increments where df.index is essentially the list of table entry
        numbers, starting with 0 to the last record in the table.
    """
    xAxis = dataFrame.index * 0.0125
    paramListLen = len(paramList)

    """ Determine the number of rows and columns in figure, based on the
        length of the parameter list.  Position the subplots such that
        they are ordered from top to bottom, starting with the first
        column and continuing top to bottom in the second column.
    """
    plotDict = {1: (111,), 2: (211, 212), 3: (311, 312, 313),
                4: (411, 412, 413, 414), 5: (321, 323, 325, 322, 324),
                6: (321, 323, 325, 322, 324, 326),
                7: (421, 423, 425, 427, 422, 424, 426),
                8: (421, 423, 425, 427, 422, 424, 426, 428)}
    subplotPos = plotDict[paramListLen]
    count = 0
    for param in paramList:
        if (count == 0):
            ax1 = plt.subplot(subplotPos[count])
        else:
            plt.subplot(subplotPos[count], sharex=ax1)
        plt.title(param, fontsize=10, color="blue")
        plt.xlabel("Seconds")
        plt.plot(xAxis, dataFrame[param])
        count += 1
    plt.subplots_adjust(top=0.95, bottom=0.06, left=0.04, right=0.98,
                        hspace=0.62, wspace=0.25)
    # plt.savefig("myfigure.png")
    plt.show()


""" Function call to 'selectData' to select .CSV file and returns entire
    data frame and the selected file name.
"""
dframe, selFilename = selectData()

""" Convert the Data Frame Columns object to a list and assign to
    headerList.
"""
headerList = list(dframe.columns)

""" Create a temporary list to store short parameter names.
"""
shortHeaderList = []

""" Find the first backslash in each header, and store the
    shortened parameter name (removing "ASCB D\", and stripping any
    spaces.)
"""
for header in headerList:
    backslashPos = header.find("\\")
    shortHeader = header[backslashPos + 1:]
    """ Remove spaces within the string using this trick...
        Split the header into parts separated by a space, then
        join the parts together, placing an empty space ("") between
        them, essentially removing spaces altogether
    """
    shortHeader = "".join(shortHeader.split())
    shortHeaderList.append(shortHeader)

""" Rename the column in Data Frame with the shortened header names
"""
dframe.columns = shortHeaderList

while True:
    """ Function call to 'displayParams' to display the available
        parameters for plotting. This function returns the number of
        parameters selected for plotting (stored in plotCount variable)
        and their header titles (stored in plotDict variable).
    """
    plotCount, plotDict = displayParams(shortHeaderList, selFilename)

    """ Function call to 'selectParams' and populate myNumberList and
        myParameterList variables to be used for plotting later.
    """
    myParameterList = selectParams(plotCount, plotDict)

    """ Function call to 'plotParams'
    """
    plotParams(dframe, myParameterList)
    os.system('cls')
