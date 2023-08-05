#####################################################################
#Programm author: Carmelo Sammarco
#####################################################################

#<tool4nc - tool for manipulate the netcdf files.>
#Copyright (C) <2018>  <Carmelo Sammarco>

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
#########################################################################

#Import modules

import pandas as pd
import xarray as xr
import os
import csv342 as csv 
from shapely.geometry import Point, mapping
from fiona import collection
import cdo
import sys


#definition functions

def nctocsv(filein,out):
    ''' This fuction convert a netCDF file to a csv file. It will generate
        two csv files called file.csv and file_NANcleaned.csv respectively.
        The file_cleaned.csv is cleaned by all the NAN values and it is
        considered the final output file of this fuction.

        -USE:

        nctocsv("file_input", "path_output_folder")
        '''
    ds = xr.open_dataset(filein, decode_times=False)
    df = ds.to_dataframe()
    df.to_csv(out + "/" + filein + ".csv")
    data = pd.read_csv(out + "/" + filein + ".csv")
    data.dropna().to_csv(out + "/" + filein + "_NANcleaned.csv", index = False)
    
#############################################################################


def nctoshape(filein,out,variable):
    ''' This fuction convert a netCDF file into a shape file(Point features). Firsly It will generate
        two csv files called file.csv and file_cleaned.csv respectively. After that
        the file_cleaned.csv ( purified by all the NAN values) is used to extract
        the corresponding shapefile rappresenting a variable's values which is the
        third argument of this fuction.

        -USE:

        nctoshape("file_input", "path_output_folder", "variable")
        '''
    ds = xr.open_dataset(filein, decode_times=False)
    df = ds.to_dataframe()
    df.to_csv(out + "/" + filein + ".csv")
    data = pd.read_csv(out + "/" + filein + ".csv")
    data.dropna().to_csv(out + "/" + filein + "_Cleaned" + ".csv", index = False)

    filecsv = open(out + "/" + filein + "_Cleaned" + ".csv")
    listed=[]
    line = filecsv.readline()
    for u in line.split(','):
        listed.append(u)
    
    if 'lat' in listed:
        schema = { 'geometry': 'Point', 'properties': { variable : 'float' } }
        with collection(out +"/" + filein + ".shp", "w", "ESRI Shapefile", schema) as output:
            with open(out + "/" + filein + "_Cleaned" + ".csv", 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    point = Point(float(row['lon']), float(row['lat']))
                    output.write({
                          'properties': {
                              variable: row[ variable ]
                          },
                          'geometry': mapping(point)
                    })
                
    elif 'Lat' in listed:
        schema = { 'geometry': 'Point', 'properties': { variable : 'float' } }
        with collection(out +"/" + filein + ".shp", "w", "ESRI Shapefile", schema) as output:
            with open(out + "/" + filein + "_Cleaned" + ".csv", 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    point = Point(float(row['Lon']), float(row['Lat']))
                    output.write({
                          'properties': {
                              variable: row[ variable ]
                          },
                          'geometry': mapping(point)
                    })
                
    elif 'Latitude' in listed:
        schema = { 'geometry': 'Point', 'properties': { variable : 'float' } }
        with collection(out +"/" + filein + ".shp", "w", "ESRI Shapefile", schema) as output:
            with open(out + "/" + filein + "_Cleaned" + ".csv", 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    point = Point(float(row['Longitude']), float(row['Latitude']))
                    output.write({
                        'properties': {
                            variable : row[ variable ]
                        },
                        'geometry': mapping(point)
                    })
                
    elif 'latitude' in listed:
        schema = { 'geometry': 'Point', 'properties': { variable : 'float' } }
        with collection(out +"/" + filein + ".shp", "w", "ESRI Shapefile", schema) as output:
            with open(out + "/" + filein + "_Cleaned" + ".csv", 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    point = Point(float(row['longitude']), float(row['latitude']))
                    output.write({
                        'properties': {
                            variable : row[ variable ]
                        },
                        'geometry': mapping(point)
                    })
                
    else:
        print("Need to be added a new text format. Please contact Carmelo!")
    

#######################################################################################

def nctogdr(filein,out):
    ''' This fuction convert a netCDF file to a GRD file. 

        -USE:

        nctogdr("file_input", "path_output_folder")
    '''
    command = "cdo  -f grb copy  " + filein  + "   " + out + "/" + filein + ".grb"
    print(command)
    os.system(command)

########################################################################################


def concatnc(folderimput):
    ''' This fuction is able to concatenate segments of data coming from the same dataset 
        but at different time steps. It will generate a file called "concatenated.nc" as 
        final result. The only atgument needed is the folder where the files are located.

        -USE:

        concatenate("path_folder_input")
    '''
    command = "cdo mergetime  " + folderimput +"/*.nc  " +  folderimput + "/Concatenated.nc"
    print(command)
    os.system(command)

###########################################################################################

def splitnc(filein,out,types,suffix):
    '''This fuction is able to split the data by type: DAY(DD), MONTH(YYYYMM) and YEAR(YYYY). It 
       gives the option to add a suffix to the so generated data.

       -USE

        splitnc("file_input", "path_output_folder", "Types"[DAY,MONTH or YEAR], Suffix")
    '''

    if types == "DAY":
        command = "cdo splitday" +"  " + filein + "  " + out +"/"+ suffix
        print(command)
        os.system(command)

    elif types == "MONTH":
        command = "cdo splityearmon" +"  " + filein + "  " + out +"/"+ suffix
        print(command)
        os.system(command)

    elif types == "YEAR":
        command = "cdo splityear" +"  " + filein + "  " + out +"/"+ suffix
        print(command)
        os.system(command)
    
    else:
        print("Please to insert DAY, MONTH or YEAR option")

###########################################################################################
