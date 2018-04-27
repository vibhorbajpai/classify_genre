from settings import *
from json_to_csv import *
import pandas as pd
import os
from fnmatch import fnmatch

#The outputfile should not have any extension like mp3 or wav
def extract_lowleveldata(inputfile, outputfile, profile=False):
    profilepath = ""
    if profile:
        if (os.path.exists(os.path.join(LOW_LEVEL_EXTRACTOR_BASE_PATH, 'profile'))):
            profilepath = os.path.join(LOW_LEVEL_EXTRACTOR_BASE_PATH, 'profile')
        else:
            print("There is no profile found. Continuing without it.")

    low_level_extractor = os.path.join(LOW_LEVEL_EXTRACTOR_BASE_PATH, LOW_LEVEL_EXTRACTOR_NAME)
    command = low_level_extractor+' %s %s %s' %(inputfile, outputfile, profilepath)
    print(command)
    os.system(command)

def extract_highleveldata(inputfile, outputfile, profile=False):
    profilepath = ""
    if profile:
        if (os.path.exists(os.path.join(HIGH_LEVEL_EXTRACTOR_BASE_PATH, 'profile'))):
            profilepath = os.path.join(HIGH_LEVEL_EXTRACTOR_BASE_PATH, 'profile')
        else:
            print("There is no profile found. Continuing without it.")

    high_level_extractor = os.path.join(HIGH_LEVEL_EXTRACTOR_BASE_PATH, HIGH_LEVEL_EXTRACTOR_NAME)
    command = high_level_extractor+' %s %s %s' %(inputfile, outputfile, profilepath)
    print(command)
    os.system(command)

def extract_data(dataset_list):
    for dataset in dataset_list:
        datasetpath = os.path.join(DATASET_BASE_PATH, dataset)
        class_list = list()
        for root, dirs, files in os.walk(datasetpath):
            classname = root.split(os.path.sep)[-1]
            class_list.append(classname)
            for f in files:
                outputfilename = f
                if(f.endswith('.mp3')):
                    outputfilename = outputfilename.replace('.mp3', '')
                elif(f.endswith('wav')):
                    outputfilename = outputfilename.replace('.wav', '')
                if not os.path.exists(os.path.join(LOW_LEVEL_DATA_BASE_PATH, dataset, classname)):
                    os.makedirs(os.path.join(LOW_LEVEL_DATA_BASE_PATH, dataset, classname))
                extract_lowleveldata(os.path.join(datasetpath, classname, f),
                                     os.path.join(LOW_LEVEL_DATA_BASE_PATH, dataset, classname, outputfilename))

        for root, dirs, files in os.walk(os.path.join(LOW_LEVEL_DATA_BASE_PATH, dataset)):
            classname = root.split(os.path.sep)[-1]
            for f in files:
                if not os.path.exists(os.path.join(HIGH_LEVEL_DATA_BASE_PATH, dataset, classname)):
                    os.makedirs(os.path.join(HIGH_LEVEL_DATA_BASE_PATH, dataset, classname))
                extract_highleveldata(os.path.join(LOW_LEVEL_DATA_BASE_PATH, dataset, classname, f),
                                      os.path.join(HIGH_LEVEL_DATA_BASE_PATH, dataset, classname, f))

def convert_to_csv(inputpath, outputpath):
    masterfields = set()
    for root, dirs, files in os.walk(inputpath):
        classname = root.split(os.path.sep)[-1]
        for f in files:
            if '.sig' not in f and 'DS_Store' not in f and '&' not in f:
                if not os.path.exists(os.path.join(outputpath, classname)):
                    os.makedirs(outputpath)
                inputfile = os.path.join(root, f)
                outputfile = os.path.join(outputpath, f, '.csv')
                convert_all(inputfile, outputfile)
                df = pd.read_csv(outputfile)
                header_list = list(df)
                for h in header_list:
                    masterfields.add(h)
    return masterfields

def extract_csv(dataset_list):
    for dataset in dataset_list:
        if not os.path.exists(os.path.join(CSV_BASE_PATH, dataset)):
            os.makedirs(os.path.join(CSV_BASE_PATH, dataset))
        masterfields = convert_to_csv(os.path.join(LOW_LEVEL_DATA_BASE_PATH, dataset), os.path.join(CSV_BASE_PATH, dataset))
        print(len(masterfields))
