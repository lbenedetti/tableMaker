##### IMPORTS #####
import os
import os.path
import sys

import math
import shutil
import itertools


from elementtree.ElementTree import parse, Element, SubElement, ElementTree
from makeTablesFun import makeTableFun

def does_file_exist_in_dir(path):
    return any(os.path.isfile(os.path.join(path, i)) for i in os.listdir(path))

def main():
    ###### TO BE CHANGED WITH SYS ARG IN #####
    outputDir = 'outputDirectory'
    tablesDir = 'tables'
    initialFile = 'unitCell_init.xml'

    ##########################################

    # Start of script
    print('Script to build GEOS files with heterogeneos properties')

    PREFIX = os.path.realpath(os.getcwd())
    outputDir = os.path.join(PREFIX, outputDir)

    if((not os.path.exists(outputDir)) and (not os.path.isdir(outputDir))):
        print('Making directory ' + outputDir)
        os.makedirs(outputDir)
    elif((os.path.exists(outputDir)) and (not os.path.isdir(outputDir))):
        print('Output path is not a valid directory.')
        sys.exit(1)
    # else the path exists and it is a directory

    print( 'Working directory: ' + outputDir)

    tablesDir = os.path.join(outputDir, tablesDir)
    if((not os.path.exists(tablesDir)) and (not os.path.isdir(tablesDir))):
        print('Making directory ' + tablesDir)
        os.makedirs(tablesDir)
    elif((os.path.exists(tablesDir)) and (not os.path.isdir(tablesDir))):
        print('Tables path is not a valid directory.')
        sys.exit(1)
    # else the path exists and it is a directory

    # Now take the inital GEOS file and copy it to the outputDir
    if(not os.path.isfile(os.path.join(outputDir,initialFile))):
        shutil.copy2(initialFile, outputDir)
        print('Copied file ' + initialFile
              + ' to folder ' + outputDir)
    # else the file is already in the output  directory

    # Let's open the file and parse it:
    initialFile = os.path.join(outputDir,initialFile)
    tree = parse(initialFile)
    elemTable = tree.getroot()
    print('Loaded XML file')
    print('It contains '+str(len(elemTable))+' objects. \n')


    ######################################################################
    #
    # Take min and max of the three dimensions (in meters)
    Xmin = -5.0
    Xmax =  5.0
    Ymin =  0.0
    Ymax = 20.0
    Zmin =  0.0
    Zmax =  1.0

    # Take the direction of the fracture opening
    dirLayering = 'y'

    # Take the min and max size of the two layers (in meters)
    minLayer1 = 0.01
    maxLayer1 = 1.0

    minLayer2 = 0.01
    maxLayer2 = 1.0

    # Take the min number of elements per layer
    minElemPerLayer = 10

    # Take the values of "E_*", "nu_*", "KIC_*" and "Shmin_*"
    # tagsToChange = ['KICTable','ETable', 'nuTable', 'ShTable', 'SHTable','SvTable']
    # print(tagsToChange)
    tagsToChange = ['ETable', 'nuTable', 'Shmin']


    layerThick = [  # mostly the thickness of the layers
        0.5,  # mudstone layer
        0.02,  # beef layer
        #0.1,  # ash layer
        #0.02  # beef layer
    ]
    numLayers = len(layerThick)

    mechProp = [ # set of mechanical properties
        [  [30e9], [0.1,0.25], [3e6,1e6] ], # [ [ E1 ] , [ nu1 ], [ SH1] ]
        [  [10e9,20e9], [0.1] , [3e6]  ]  # [ [ E2 ], [ nu2 ], [ SH2  ] ]
    ]

    numProps = len(tagsToChange)

    # here check dimensions of the various matrices
    if(len(mechProp) != numLayers):
        sys.exit('Number of mechanical properties is different '
                 'from the number of layers')
    for idx, propSet in enumerate(mechProp):
        if (len(propSet) != numProps):
            sys.exit('Mechanical properties does not match at line ', idx)

    # first permutation (properties of 1 layer)
    perm1 = [] #[None] * (numLayers-1)
    for i in range(0,numLayers):
        temp = [list(a) for a in itertools.product(*mechProp[i])]
        perm1.append(temp)

    print('\n perm1 ')
    print(perm1)
    print('\n\n\n')

    # second permutation (a layer with another)
    perm2 = [list(a) for a in itertools.product(*perm1)]

    print('\n perm2 ')
    print(perm2)

    print('===== Analyses to be run =====')
    print('{:1.4f}'.format(perm2[0][0][0]))


    sys.exit(0)

    # print(tagsToChange1)
    # print(tagsToChange1[2])
    # print(tagsToChange1[3][1])
    # print(len(tagsToChange1[0]))
    # print(len(tagsToChange1[2]))
    # print(len(tagsToChange1))
    # print(sum(len(x) for x in tagsToChange1))

    # Build the range of thicknesses for both layer 1 and 2
    # thickness1 = [ 0.25, 0.5, 0.75, 1.0 ]
    thickness1 = [0.5, 1.0]

    # thickness2 = [ 0.01, 0.02, 0.05,
    #                0.1,  0.2,  0.5,
    #                1.0]
    thickness2 = [0.05, 0.1, 0.2, 0.5]

    domainCoord = [[Xmin, Xmax],
                   [Ymin, Ymax],
                   [Zmin, Zmax]]

    KIC1 = [2.5e6, 2.0e6]
    KIC2 = [1.5e6, 1.0e6, 0.5e6]

    E1 = [30e9]
    E2 = [30e9, 25e9, 20e9, 15e9]

    nu1 = [0.25]
    nu2 = [0.1]

    valuesToChange = [[ [E1, E2], [nu1, nu2] ],
                      [ [KIC1, KIC2]],
                      # [ [KIC1, KIC2], [E1, E2], [nu1, nu2] ]
                     ]

    # print(valuesToChange)
    ######################################################################

    # number of elements in tagsToChange = (sum(len(x) for x in tagsToChange))

    # Total number of analyses:
    # totalNumAnalyses = len(tagsToChange) * len(thickness1) * len(thickness2)
    # print('Total number of analyses: ', totalNumAnalyses)

    # for idx, groupTag in enumerate(tagsToChange):

    for idx,aSet in enumerate(valuesToChange):
        print('Considering the set of analyses for ' + str(tagsToChange[idx]))

        numOfParamtersToChange = len(tagsToChange[idx])

        finalPerms=[]

        for x in range(numOfParamtersToChange):
            # print(valuesToChange[idx][x])
            # print('Layer 1: ' + str(valuesToChange[idx][x][0]))
            # print('Layer 2: ' + str(valuesToChange[idx][x][1]))

            vecValuesLayer1 = valuesToChange[idx][x][0]
            vecValuesLayer2 = valuesToChange[idx][x][1]

            permutationsOfValues = [list(a) for a in itertools.product(valuesToChange[idx][x][0], valuesToChange[idx][x][1])]

            # print('The permutations in the two layers for the values of '+tagsToChange[idx][x]+ ' are:')
            # print(permutationsOfValues)

            finalPerms.append(permutationsOfValues)

        print('The final permutation matrix is:')
        print(finalPerms)
        print('\n\n------------------------------------------------')

        # n = numOfParametersToChange
        # print('n='+str(len(finalPerms)))
        # print(numOfParamtersToChange)

        # print('n1='+ str(len(permutationsOfValues)))
        print('\n\t\t Analyses to be done: ')

        for jdx,property in enumerate(finalPerms):
            # print('Property '+str(tagsToChange[idx][jdx]))
            # print(property)
            #
            # print('\n \n Layer 1 E -- Layer 2 E')

            for x1,lines in enumerate(property):
                for x2,columns in enumerate(lines):
                    sys.stdout.write(str(property[x1][x2]))
                    sys.stdout.write('\t')
                sys.stdout.write('\n')

        numOfPermTables = len(finalPerms)
        numOfPermPerVal = []
        for property in finalPerms:
            numOfPermPerVal.append(len(property))
            print(len(property))
            # then, next level is the value of the properties at the layer 1 and the layer 2

        dataForAnalysis = [list(a) for a in itertools.product(finalPerms,repeat=numOfPermTables)]

        print(dataForAnalysis)

        print('\n\n------------------------------------------------')

        # for t1 in thickness1:
        #     for t2 in thickness2:
        #         print('t1=' + str(t1) + ' t2=' + str(t2))
        #         for x in range(len(finalPerms[0])):
        #             print('finalPerm['+str(x)+']=' + str(finalPerms[0][x]))




                # for x in range(len(finalPerms)):
                #     for y in range(len(finalPerms[x])):
                #         for z in range(len(finalPerms[x][y])):
                #             print('A='+str(finalPerms[x][y][z])+' t1='+str(t1)+' '+'t2='+str(t2))


                #### HERE, PICK ONE OR PICK OTHER

                # print(groupTag)
                # print(idx)
                # print(tagsToChange[idx])
                # print(len(groupTag))
                #
                # for jdx in range(len(groupTag)):
                #     print(valuesToChange[0][jdx])
                #
                #
                # for jdx, aProperty in enumerate(valuesToChange[idx]):
                #     print(aProperty)

                # singleOutDir = (('_'.join(groupTag)).replace('Table', '')) \
                #                + str(idx) + '_' + str(t1) + '_' + str(t2)
                #
                # singleOutDir = os.path.join(outputDir,singleOutDir)
                #
                # print('Here we change t1=' + str(t1) + ' t2=' + str(t2) + ' with values ' + str(groupTag))
                #
                # print(valuesToChange[idx])
                #
                # for jdx,aProperty in enumerate(valuesToChange[idx]):
                #     print(aProperty)
                #     # print(enumerate(valuesToChange[idx]))
                #
                #     # for val1 in aProperty[jdx][]
                #     #     for val2 in [1]:
                #     #         print(str(val1)+'_'+str(val2))
                #
                # # creating the file with the thickness variation and properties variation
                # # in the required direction
                # # --- makeTableFun(dirLayering, groupTag, valuesToChange[idx], domainCoord, t1, t2, singleOutDir)

    sys.exit(0)

########################################################################################################################

    #
    # for idx, groupTag in enumerate(tagsToChange):
    #     print(idx,groupTag)

# also, create the homogeneous files
        #
        #
        # for nameTag in groupTag
        # print(names)




    # namesOfDir = {{x[i].replace('Table','') for i in x} for x in tagsToChange1}
    # print(namesOfDir)



    # Number of analysis per


    # for every file called "E_*", "nu_*", "KIC_*" and "Shmin_*"
    # we consider a different combination of thegit

    # array of items to be changed



    # in element Tables,
    # with subelement Table3D
    # with name="ETable", "nuTable", "Shmin", "KICTable"
    # but also for the properties of Sv and Shmax if required
    # change x_file, y_file, z_file, voxel_file
    # (this last one with the values of the mechanical properties)
    #

    # One property goes hetereogeneous by just changing the property
    # table like E_homo.geos with x_homo.geos to E_hete.geos and x_spacing



    # To decide is how many intervals we want to study

    counter = 0
    for subelem in elemTable:
        # print(subelem.tag)
        # print(str(subelem.tag)=='InitialConditions')
        if (str(subelem.tag) == 'Tables'):
            print('Tables found at position ' + str(counter))
            break
        counter = counter + 1

    tablesLoc = elemTable[counter]
    print(tablesLoc.tag)



    # look for ETable

    for subsubelem in tablesLoc:
        if(subsubelem.attrib['name']=='ETable'):
            print(subsubelem.tag)
            print(subsubelem.attrib['name'])
            # subsubelem.attrib['name'].write('yoooooo')
            # attrToChange=SubElement(subsubelem,'name')
            # ElementTree(attrToChange).write()
            print(subsubelem.get('name'))

            # this sets the values on the tree
            # (that has been previously loaded in memory)
            # but it does not change the value in the file
            subsubelem.set('name', 'yoooooooo')
            # to write the value in the file, you have to
            # basically rewrite all the file from the tree
            # and giving the same filename as the input file
            # you would technically overwrite


    # Attributes to be changed as required
    # files have a PREFIX = "../table/"
    #
    # name="nuTable"
    # voxel_file="../tables/nu_het.geos"
    # x_file="../tables/x_spacing1.geos"
    # y_file="../tables/y.geos"
    # z_file="../tables/z.geos"
    #


    # to write the value in the file, you have to
    # basically rewrite all the file from the tree
    # and giving the same filename as the input file
    # you would technically overwrite

    tree.write(filename)


    #
    # print(tablesLoc[0].tag)
    # print(tablesLoc[1].tag)


    # counter = 0
    # for subelem in elemTable:
    #     # print(subelem.tag)
    #     # print(str(subelem.tag)=='InitialConditions')
    #     if (str(subelem.tag) == 'Tables'):
    #         print('initial condition found at position ' + str(counter))
    #     counter = counter + 1


    # theElementToChange = elemTable[counter]
    #
    #
    # subelem = list(elemTable)
    # for subelem in elemTable:
    #     print(subelem.tag)
    #
    # print(elemTable[:1])
    # print(elemTable[-1:])
    #
    # start = elemTable[:1]
    # end = elemTable[-1:]
    #
    # print(start[0].tag)
    # print(end[0].tag)
    #
    # someTags = elemTable[:4]
    #
    # print(someTags[0].tag)
    # print(someTags[3].tag)
    #
    # subsubelem = list(elemTable[3])
    # print(subsubelem[0].tag)
    # print(subsubelem[0].attrib)


if __name__ == "__main__":
    main()
