import sys
import math

#check the number of input arguments
if len(sys.argv) < 7:
    sys.exit('Usage of script with parameters: \n'
             '  [1]: the direction, either x or y or z \n'
             '  [2]: the name of the property to be used \n'
             '  [3]: the starting coordinate \n'
             '  [4]: the finishing coordinate \n'
             '  [5]: the spacing of material 1 \n'
             '  [6]: the mechanical value of material 1 \n'
             '  [7]: the spacing of material 2 \n'
             '  [8]: the mechanical value of material 2 \n')

# Organization of arguments
# [1]: the direction, either x or y or z
# [2]: the name of the property to be used
# [3]: the starting coordinate
# [4]: the finishing coordinate
# [5]: the spacing of material 1
# [6]: the mechanical value of material 1
# [7]: the spacing of material 2
# [8]: the mechanical value of material 2

#########################################################

# saving the direction of the variation
if (sys.argv[1]!='x' and sys.argv[1]!='y' and sys.argv[1]!='z' ):
    sys.exit('Usage not valid')
else:
    dirStr=sys.argv[1]

# saving the name of the property
propName = sys.argv[2]

# saving the start and the end of the coordinate
xStart = float(sys.argv[3])
xEnd = float(sys.argv[4])

# saving the spacing of material 1
deltaMat1 = float(sys.argv[5])
# and the value of the mechanical property of material 1
valueMat1 = float(sys.argv[6])

# saving the spacing of material 2
deltaMat2 = float(sys.argv[7])
# and the value of the mechanical property of material 1
valueMat2 = float(sys.argv[8])

#########################################################

# Some checks
if(xEnd<=xStart):
    sys.exit('xEnd must be larger than xStart')

if(deltaMat1 > ( xEnd - xStart )):
    sys.exit('material 1 is larger than the domain xStart-->xEnd')

if(deltaMat2 > ( xEnd - xStart )):
    sys.exit('material 2 is larger than the domain xStart-->xEnd')

#########################################################

# the number of values that will be printed in the files
numOfPairOfLayers = int(math.floor((xEnd - xStart + deltaMat1 + deltaMat2)
                                   / ( deltaMat1 + deltaMat2 )))

totalLines = numOfPairOfLayers * 4 + 2

#########################################################

print('The total number of lines will be '
      + str(totalLines)
      + ' whereas the number of pair of layers will be '
      + str(numOfPairOfLayers))

# the perturbation is required to define the intervals
perturbation = 1.0e-6 * (xEnd-xStart)/5
# after the alternance of mat1 and mat2, we will have mat1 forever
almostInfinite = 1.0e4 * xEnd

#########################################################

# SpacingFile

# name of the file
fileName = ( str(dirStr)  + '_' +
             str(deltaMat1) + '_' +
             str(deltaMat2) + '.geos' )

spacingFile = open(fileName,"w")

print('Writing file ' + fileName)

location = xStart

while (location < xEnd):
    # coordinates work
    # begin of material 1
    value = '{}'.format(location + perturbation) + '\n'
    spacingFile.write(value)

    location = location + deltaMat1

    value = '{}'.format(location - perturbation) + '\n'
    spacingFile.write(value)

    # begin of material 2
    value = '{}'.format(location + perturbation) + '\n'
    spacingFile.write(value)

    location = location + deltaMat2

    value = '{}'.format(location - perturbation) + '\n'
    spacingFile.write(value)
    # end of loop

# here add the last two lines
value = '{}'.format(location + perturbation) + '\n'
spacingFile.write(value)

value = '{}'.format(almostInfinite) + '\n'
spacingFile.write(value)

#########################################################

# Remaining files in the other two directions which are constant

if(dirStr == 'x'):
    otherDir1 = 'y'
    otherDir2 = 'z'
elif(dirStr == 'y'):
    otherDir1 = 'x'
    otherDir2 = 'z'
elif(dirStr == 'z'):
    otherDir1 = 'x'
    otherDir2 = 'y'

fileName = ( str(otherDir1) + '_homo.geos' )
otherFile1 = open(fileName, "w")
print('Writing file ' + fileName)
otherFile1.write(str(xStart) + '\n')
otherFile1.write(str(almostInfinite) + '\n')
otherFile1.close()

fileName = ( str(otherDir2) + '_homo.geos' )
otherFile2 = open(fileName, "w")
print('Writing file ' + fileName)
otherFile2.write(str(xStart) + '\n')
otherFile2.write(str(almostInfinite) + '\n')
otherFile2.close()

#########################################################

# Values file

fileName = (str(propName) + '_' +
            str(deltaMat1) + '_' +
            str(deltaMat2) + '.geos')

valueFile = open(fileName,"w")

print('Writing file ' + fileName)

headerString = '{}'.format(totalLines) + ' 1 1\n'
valueFile.write(headerString)

# Iterating along the number of pairs of layers
for index in range(0, numOfPairOfLayers):
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


