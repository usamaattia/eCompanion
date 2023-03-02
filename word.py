
import spacy
from hand_event import stringtoDate
import json
class word():

    def process_input(self,my_input):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(my_input)
        print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
        print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
        label_list = []
        for entity in doc.ents:
            print(entity.text, entity.label_)
            label_list.append(entity.label_)
        
        

        
        val = [0,0]
        for list in label_list:
            if list == "DATE":
                val[0]=1
            
            if list == "TIME":
                val[1]=1
        date=stringtoDate().get_date_Value(my_input)
        with open('data.json', 'w') as f:
            json.dump(date, f)

        
        if val[0]==0:
            return "which day is it? please write the full date and specify the day of the week."
        if val[1]==0:
            return "What Time is it? please write the full date"
        return "all good"