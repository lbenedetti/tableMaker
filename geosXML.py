import os
import os.path
import sys
import math



from elementtree.ElementTree import parse, Element, SubElement, ElementTree

# Function to modify the base file into the derived files

# First check the files available in the "tables" folder
tableFolder = "../tables/"
# save the list of files in the
filesInTables = os.listdir(tableFolder)

print(filesInTables)

for name in filesInTables:
    print(name)

sys.exit(0)

# for every file called "E_*", "nu_*", "KIC_*" and "Shmin_*"
# we consider a different combination of thegit 



# open the BASE file
filename = 'unitCell_test.xml'

# load the XML tree and create
tree = parse(filename)
elemTable = tree.getroot()
# subelem = elem.getroot()

print('Loaded GEOS XML file')
print('It contains '+str(len(elemTable))+' objects. \n')


# array of items to be changed

# in element Tables,
# with subelement Table3D
# with name="ETable", "nuTable", "Shmin", "KICTable"
# but also for the properties of Sv and Shmax if required
# change x_file, y_file, z_file, voxel_file
# (this last one with the values of the mechanical properies)
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



