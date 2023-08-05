

import os
import csv
import json

class Choice1:

    def __init__(self) -> None:
        super().__init__()
    
    def convertToJson(self,filepath):
        # json array convert from python dictionary place holder
        jsonArray = []
        # open csv file as csvfile and convert it into a python dictory list object
        with open(filepath, encoding='utf-8') as csvfile:
            csvReader = csv.DictReader(csvfile)
            # getting the name of the file
            filename = os.path.basename(filepath).split('.')[0]
            # creates a file under the current directory with the name of the file
            jsonfile =  open("./"+filename+".json", 'w+', encoding='utf-8')
            for row in csvReader:
                jsonArray.append(row)
            jsonfile.write(json.dumps(jsonArray,indent=4))
            jsonfile.close()