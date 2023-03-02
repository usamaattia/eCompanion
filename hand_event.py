from turtle import forward
from sutime import SUTime
import os, re
import json
from dateparser.search import search_dates
#import datefinder




class stringtoDate(): 
    def get_date_Value(self,my_input):
        jar_files = os.path.join(os.path.dirname('/Users/usamaal-attia/Desktop/eCompanion2/venv/lib/python3.8/site-packages/sutime/'), 'jars')
        #sutime = SUTime(mark_time_ranges=True, include_range=True)
        sutime = SUTime(jars=jar_files, mark_time_ranges=True)

        #print(json.dumps(sutime.parse(my_input), sort_keys=True, indent=4))
        evDate=search_dates(my_input)
        #matches = datefinder.find_dates(my_input)
        #for match in matches:
        #    print(type(match))
        date_value = json.dumps(sutime.parse(my_input), sort_keys=True, indent=4)
        
        return date_value
    
    def get_date(self,text):
        jar_files = os.path.join(os.path.dirname('/Users/usamaal-attia/Desktop/eCompanion2/venv/lib/python3.8/site-packages/sutime/'), 'jars')
        #sutime = SUTime(mark_time_ranges=True, include_range=True)
        sutime = SUTime(jars=jar_files, mark_time_ranges=True)
        text = re.sub(r'[,-.;@#?!&$]+\ *', ' ', text)
        result = sutime.parse(text)
        return result
                
