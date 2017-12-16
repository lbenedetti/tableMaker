import sys
import os
import math


# The main script should be able of
# 1. taking the interval range of data,
#    and in particular the fact that we have
#       - unit cells 1 and 2
#       - mechanical parameters E, nu, K, Shmin, Shmax
#       - combination of the previous quantities
# 2. creating the directories that are required for the computation
# 3. create the files of the tables
# 4. create the files for the analyses (?)
# 5. launch the analysis


##################################################################
# consider that we have a list of thickness (and we do not care at
# the moment how they are generated). also we have a list of different
# values of toughness, elastic parameters and in-situ stress condition
# we want to create the python script that setups all the unitCell.xml
# files and setups the folders which we will allocate them and, finally,
# the files that will launch the slurm scripts

# to make directories
if not os.path.exists(directory):
    os.makedirs(directory)

# full fledge use of creation of directories and creation of files


import os

path = chap_name

if not os.path.exists(path):
    os.makedirs(path)

filename = img_alt + '.jpg'
with open(os.path.join(path, filename), 'wb') as temp_file:
    temp_file.write(buff)

