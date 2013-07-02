# CS121 A'11 
# HW6
# Working with Crime and 311 call center data
#
# Arin Schwartz


from pylab import *
import plot_map

filenames = ["data/311_Service_Requests_-_Graffiti_Removal__2011_.csv",
             "data/311_Service_Requests_-_Pot_Holes_Reported__2011_.csv",
             "data/311_Service_Requests_-_Rodent_Baiting__2011_.csv",
             "data/311_Service_Requests_-_Sanitation_Code_Complaints__2011_.csv",
             "data/311_Service_Requests_-_Street_Lights_-_All_Out__2011_.csv",
             "data/311_Service_Requests_-_Tree_Debris__2011_.csv",
             "data/311_Service_Requests_-_Vacant_and_Abandoned_Buildings_Reported.csv",
             "data/crime-ASSAULT.csv",
             "data/crime-BATTERY.csv",
             "data/crime-BURGLARY.csv",
             "data/crime-CRIMINAL DAMAGE.csv",
             "data/crime-CRIMINAL TRESPASS.csv",
             "data/crime-DECEPTIVE PRACTICE.csv",
             "data/crime-MOTOR VEHICLE THEFT.csv",
             "data/crime-NARCOTICS.csv",
             "data/crime-OTHER.csv",
             "data/crime-ROBBERY.csv",
             "data/crime-THEFT.csv"
             ]


# map file names to labels for use in plots
filenamesToLabels = {
    "data/311_Service_Requests_-_Graffiti_Removal__2011_.csv" : "Graffiti",
    "data/311_Service_Requests_-_Pot_Holes_Reported__2011_.csv" : "Pot_Holes",
    "data/311_Service_Requests_-_Rodent_Baiting__2011_.csv" : "Rodents",
    "data/311_Service_Requests_-_Sanitation_Code_Complaints__2011_.csv" : "Garbage",
    "data/311_Service_Requests_-_Street_Lights_-_All_Out__2011_.csv" : "Street_lights",
    "data/311_Service_Requests_-_Tree_Debris__2011_.csv" : "Tree debris",
    "data/311_Service_Requests_-_Vacant_and_Abandoned_Buildings_Reported.csv" : "Abandoned_buildings",
    "data/crime-ASSAULT.csv" : "ASSAULT",
    "data/crime-BATTERY.csv" : "BATTERY",
    "data/crime-BURGLARY.csv": "BURGLARY",
    "data/crime-CRIMINAL DAMAGE.csv" : "CRIMINAL_DAMAGE",
    "data/crime-CRIMINAL TRESPASS.csv" : "CRIMINAL_TRESSPASS",
    "data/crime-DECEPTIVE PRACTICE.csv" : "DECEPTIVE_PRACTICE",
    "data/crime-MOTOR VEHICLE THEFT.csv" : "MOTOR_VEHICLE_THEFT",
    "data/crime-NARCOTICS.csv" : "NARCOTICS",
    "data/crime-OTHER.csv" : "OTHER",
    "data/crime-ROBBERY.csv" : "ROBBERY",
    "data/crime-THEFT.csv" : "THEFT"
    }


# bounding box for the City of Chicago
# ((lower left), (upper right))
chicagoBoundingBox = ((-87.946432568413186, 41.625680270515986),
                      (-87.504436649263894, 42.041562932637788))


# bounding box for Hyde Park
hydeParkBoundingBox = ((-87.61, 41.7852), (-87.5825, 41.8054))


# plot data on top of a map of Hyde Park
#   data: list of lists of strings
#   title: string
#   outputFilename: string
#
# save the figure in the specified file name, if
# outputFilename is non-empty
def plotOnHydePark(data, title, outputFilename):
    f = figure()
    # the following statement draws the map of Hyde Park
    plot_map.plot_google_static_map(41.7961,-87.5965)

# createInitBuckets:
# N: integer
# returns an NxN list of lists with entries that have been
# initialized to zero.
def createInitBuckets(N):
    return [[0]* (N) for i in range(0, (N))]

#Task 1: Read the Data

def readFile(filename):
    r = open(filename, 'r')
    r = r.readlines()
    r = [x.strip().split(",") for x in r]
    return r

#Task 2: Find the index of a field

def findIndexOfField(rows, fieldName):
    if fieldName in rows[0]:
        return rows[0].index(fieldName)
    else:
        return -1

#Task 3: Extract a column of floats

def extractFloatField(rows, fieldName):
    i = findIndexOfField(rows, fieldName)
    floatList = []
    floatList.append(rows[0][i])
    [floatList.append(float(x[i])) for x in rows[1:]]
    return floatList
    

#Task 4: Extract rows from within a region
def extractRowsWithinBoundingBox(rows, boundingBox):
    boundedList = []
    lon = findIndexOfField(rows, 'LONGITUDE')
    lat = findIndexOfField(rows, 'LATITUDE')
    boundedList.append(rows[0])
    for x in rows[1:]:
        if float(x[lon]) > boundingBox[0][0] and float(x[lon]) < boundingBox[1][0]:
            if float(x[lat]) > boundingBox[0][1] and float(x[lat]) < boundingBox[1][1]:
                boundedList.append(x)
    return boundedList

#Task 5: Create a location scatter plot
def plotLonLat(rows):
    lon = extractFloatField(rows, 'LONGITUDE')
    lat = extractFloatField(rows, 'LATITUDE')
    matplotlib.pyplot.scatter(lon[1:], lat[1:])
    
#Putting it all together
def mkChicagoPlot(rows, title, outputFilename):
    boundedList = extractRowsWithinBoundingBox(rows, chicagoBoundingBox)
    plotLonLat(boundedList)
    matplotlib.pyplot.savefig(outputFilename)
    
def mkHydeParkPlot(rows, title, outputFilename):
    plotOnHydePark(rows, 'Hyde Park', 'Hyde Park Plot')
    boundedList = extractRowsWithinBoundingBox(rows, hydeParkBoundingBox)
    plotLonLat(boundedList)
    matplotlib.pyplot.savefig(outputFilename)


#Task 6: Draw grid lines
def drawGridLines(boundingBox, N):
    lon = boundingBox[1][0] - boundingBox[0][0]
    increment = lon/N
    x = arange(boundingBox[0][0], boundingBox[1][0], increment)
    lat = boundingBox[1][1] - boundingBox[0][1]
    incrementTwo = lat/N
    y = arange(boundingBox[0][1], boundingBox[1][1], incrementTwo)
    matplotlib.pyplot.vlines(x, boundingBox[0][1], boundingBox[1][1], color ='k', linestyles = 'dashed')
    matplotlib.pyplot.hlines(y, boundingBox[0][0], boundingBox[1][0], color = 'k', linestyles = 'dashed')


#Intermediary functions for grid cell conversion
def gridLocX(L, boundingBox, N):
    q = boundingBox[1][0] - boundingBox[0][0]
    increment = q/N
    gridLoc = (L-boundingBox[0][0])/increment
    gridLoc = int(gridLoc)
    return gridLoc
    
def gridLocY(L, boundingBox, N):
    r = boundingBox[1][1] - boundingBox[0][1]
    incrementTwo = r/N
    gridLoc = (L-boundingBox[0][1])/incrementTwo
    gridLoc = int(gridLoc)
    return gridLoc

#Task 7: Calculate Summary Buckets
def calculateRegionBuckets(rows, boundingBox, N):
    buckets = createInitBuckets(N)
    lon = findIndexOfField(rows, 'LONGITUDE')
    lat = findIndexOfField(rows, 'LATITUDE')
    
    for x in rows[1:]:
        buckets[gridLocX(float(x[lon]), boundingBox, N)][gridLocY(float(x[lat]), boundingBox, N)] += 1
    
    return buckets
    
    
    
#Task 8: Plotting summary buckets
def plotBucketsVsBuckets(buckets0, buckets1):
    i = []
    for x in buckets0:
        i.extend(x)
    j = []
    for y in buckets1:
        j.extend(y)
    matplotlib.pyplot.scatter(i, j)
    
    

#Putting it all together
def plotCrimeVsComplaint(crimeRows, complaintRows, N, x_label, y_label, title, outputFilename):
    s = readFile(crimeRows)
    t = readFile(complaintRows)
    x = calculateRegionBuckets(s, chicagoBoundingBox, N)
    y = calculateRegionBuckets(t, chicagoBoundingBox, N)
    
    plotBucketsVsBuckets(x, y)
    
    matplotlib.pyplot.xlabel = x_label
    matplotlib.pyplot.ylabel = y_label
    matplotlib.pyplot.title = title
    matplotlib.pyplot.savefig(outputFilename)




