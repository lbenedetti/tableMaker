import sys
import math
import os

def makeTableFun(dirStr,propNames,propValues,domainCoord,deltaMat1,deltaMat2, singleOutDir):

    # Organization of arguments
    # [1]: dirStr - the direction, either x or y or z
    # [2]: propNames - the name of the properties to be used (list)
    # [3]: propValues - the values of the properties to be used (array)
    # [4]: the x, y, z coordinates (array with begin and end)
    # [5]: the spacing of material 1
    # [6]: the spacing of material 2

    #########################################################

    # check the direction of the variation
    if (dirStr!='x' and dirStr!='y' and dirStr!='z' ):
        sys.exit('Table Function: Direction not valid')

    # check if the names and the values have the correct size
    if(len(propNames)!=len(propValues)):
        sys.exit('Table Function: Properties and names mismatch')

    for idx, pairOfValues in enumerate(propValues):
        if(len(pairOfValues)!=2):
            sys.exit('Table Function: Property '+ str(idx) + ' has '
                     + str(len(pairOfValues)) + ' instead of 2.')

    # checking the dimensions of the model (begin and end in x, y, z)
    if (len(domainCoord)!=3):
        sys.exit('You need to provide 3D domain')

    for idx, pairOfValues in enumerate(domainCoord):
        if (len(pairOfValues) != 2):
            sys.exit('Table Function: Domain coordinates have mismatch dimensions at row ', idx)
        if (pairOfValues[0] > pairOfValues[1]):
            sys.exit('Table Function: End coordinate should be bigger than the begin one at row ', idx)

    #########################################################

    # Some checks
    if(dirStr == 'x'):
        dirStrNum = 0
    elif(dirStr == 'y'):
        dirStrNum = 1
    elif(dirStr == 'z'):
        dirStrNum = 2

    if(deltaMat1 > ( domainCoord[dirStrNum][1]-domainCoord[dirStrNum][0])):
        sys.exit('Table Function: material 1 is larger than the domain xStart-->xEnd')

    if(deltaMat2 > ( domainCoord[dirStrNum][1]-domainCoord[dirStrNum][0] )):
        sys.exit('Table Function: material 2 is larger than the domain xStart-->xEnd')

    #########################################################

    xStart = domainCoord[dirStrNum][0]
    xEnd = domainCoord[dirStrNum][1]

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

    os.makedirs(singleOutDir)

    #########################################################

    # SpacingFile

    # name of the file
    fileName = ( str(dirStr)  + '_' +
                 str(deltaMat1) + '_' +
                 str(deltaMat2) + '.geos' )

    spacingFile = open(os.path.join(singleOutDir,fileName),"w")

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
    otherFile1 = open(os.path.join(singleOutDir,fileName), "w")
    print('Writing file ' + fileName)
    otherFile1.write(str(xStart) + '\n')
    otherFile1.write(str(almostInfinite) + '\n')
    otherFile1.close()

    fileName = ( str(otherDir2) + '_homo.geos' )
    otherFile2 = open(os.path.join(singleOutDir,fileName), "w")
    print('Writing file ' + fileName)
    otherFile2.write(str(xStart) + '\n')
    otherFile2.write(str(almostInfinite) + '\n')
    otherFile2.close()

    #########################################################

    for idx,oneProp in enumerate(propNames):

        # Values file
        fileName = (str(oneProp) + '_' +
                    str(deltaMat1) + '_' +
                    str(deltaMat2) + '.geos')

        valueFile = open(os.path.join(singleOutDir,fileName),"w")

        print('Writing file ' + fileName)

        headerString = '{}'.format(totalLines) + ' 1 1\n'
        valueFile.write(headerString)

        valueMat1 = propValues[idx][0]
        valueMat2 = propValues[idx][1]

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


    #########################################################