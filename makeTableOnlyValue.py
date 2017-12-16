import sys
import math
import string

#check the number of input arguments
if len(sys.argv) < 4:
    sys.exit('Usage of script with parameters: \n' +
             '  [1]: the file with the variation of coordinates \n' +
             '  [2]: the name of the property \n' +
             '  [3]: the mechanical value of material 1 \n' +
             '  [4]: the mechanical value of material 2 \n')

# Organization of arguments
# [1] the file with the variation of coordinates
# [2] the name of the property
# [3] the first value
# [4] the second value of the property

#########################################################

fileName = sys.argv[1]

spacingFile=open(fileName,'r')

firstLine = (spacingFile.readline()).split()
totalLines = string.atoi(firstLine[0])

numberOfLayers = (totalLines - 2) // 4

# load property name
propName = sys.argv[2]

# load values of the property
valueMat1 = sys.argv[3]
valueMat2 = sys.argv[4]

# load the deltas from the filename
deltas = fileName.replace('.geos', '').split('_')
deltaMat1 = deltas[1]
deltaMat2 = deltas[2]

# Values file

fileName = (str(propName) + '_' +
            str(deltaMat1) + '_' +
            str(deltaMat2) + '.geos')

valueFile = open(fileName,"w")

print('Writing file ' + fileName)

headerString = '{}'.format(totalLines) + ' 1 1\n'
valueFile.write(headerString)

# Iterating along the number of pairs of layers
for index in range(0, numberOfLayers):
    value = '{}'.format(valueMat1) + '\n'
    valueFile.write(value)
    valueFile.write(value)
    value = '{}'.format(valueMat2) + '\n'
    valueFile.write(value)
    valueFile.write(value)

# Adding the final 2 lines for the infinite material
value = '{}'.format(valueMat1) + '\n'
valueFile.write(value)
valueFile.write(value)

valueFile.close()
