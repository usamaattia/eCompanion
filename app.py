
from hand_event import stringtoDate
import random
import json
import torch
from model import NeuralNet
from datetime import datetime
from nltk_utils import bag_of_words, tokenize
from flask import Flask, render_template, request, jsonify
from word import word
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import spacy

    


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)




FILE = "data.pth"
data = torch.load(FILE)
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()
bot_name = "eCompanion"


app = Flask(__name__)


app.secret_key = "caircocoders-ednalan"   
DB_HOST = "localhost"
DB_NAME = "postgres"
PORT = "5433"
DB_USER = "postgres"
DB_PASS = "password"       
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=PORT) 
 

 

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/calendar" ,methods=['GET','POST'])
def canlendar():

    my_input = request.form.get('plan')
    if my_input == None:
        my_input=''
    sentence = tokenize(my_input)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    out_put = ''
  

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM events ORDER BY id")
    calendar = cur.fetchall()

    conv = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    conv.execute("delete from convo where input_='' OR input_ IS NULL;")
    conv.execute("SELECT * FROM convo ORDER BY id DESC")
    
    conv = conv.fetchall()

    convv = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
   

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                if tag == "booking": # dealing with booking events
                    out = word().process_input(my_input=my_input) #working with spacy

                
                    if out == "all good":
                        date_value = stringtoDate().get_date(my_input)
                        print(date_value)
                        
                        global begin
                        begin = ''
                        global endd
                        endd = ''
                        if date_value != '':
                            for dic in date_value:
                                for val,cal in dic.items():
                                    if val == 'timex-value':
                                        date_in_day = cal
                                
                                    if val == 'value':
                                        if isinstance(cal, dict):
                                            for vall,call in cal.items():
                                                    if vall == 'begin':
                                                        begin = call
                                                    if vall == 'end':
                                                        endd = call
                        
                        
                        print(date_in_day)
                        print(begin)
                        print(endd)
                        nlp = spacy.load("en_core_web_sm")
                        doc = nlp(my_input)
                        for tok in doc:
                            print(tok, tok.pos_)
                        Noun_phrases = [chunk.text for chunk in doc.noun_chunks]
                        print(Noun_phrases)
                        date_start = date_in_day + begin
                        date_end = date_in_day + endd
                        convo =conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                        title = 'appointment'
                        start = date_start 
                        end =date_end
                        print(title)     
                        print(start)  
                        convo.execute("INSERT INTO events (title,start_event,end_event) VALUES (%s,%s,%s)",[title,start,end])
                        conn.commit()       
                        convo.close()
                        date_value = ''
                        
                    while out !=  "all good": # validating the input
                        convv.execute("INSERT INTO convo(input_,output_) VALUES (%s, %s);",[my_input, out])
                        conn.commit()       
                        convv.close()
                        return render_template('calendar.html',calendar=calendar, my_input=my_input, out_put=out, conv=conv)
                
                if tag == 'cancel':
                    try:
                        date_value = stringtoDate().get_date(my_input)
                        if date_value != '':
                                for dic in date_value:
                                    for val,cal in dic.items():
                                        if val == 'value':
                                            date_day = cal
                        print(date_day)
                        date_dayy = datetime.strptime(date_day,'%Y-%m-%dT%H:%M')
                        
                        curre = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                        curre.execute("DELETE FROM events WHERE start_event = %s;",[date_dayy])
                        conn.commit()       
                        curre.close()
                    except:
                        out_put = 'please specify what time it is.'
                        convv.execute("INSERT INTO convo(input_,output_) VALUES (%s, %s);",[my_input, out_put])
                        print('please specify what time it is.')
                        

                out_put= f"{bot_name}: {random.choice(intent['responses'])}"
                convv.execute("INSERT INTO convo(input_,output_) VALUES (%s, %s);",[my_input, out_put])
                conn.commit()       
                convv.close()
                
            if tag =="time":
                out_put=  "eCompanion" + datetime.now().strftime(" %d/%m/%Y %H:%M:%S")
                convv.execute("INSERT INTO convo(input_,output_) VALUES (%s, %s);",[my_input, out_put])
                conn.commit()       
                convv.close()
                return render_template('calendar.html',calendar=calendar, my_input=my_input, out_put=out_put, conv=conv)
                
    else:
        out_put=f"{bot_name}: I do not understand..."
        convv.execute("INSERT INTO convo(input_,output_) VALUES (%s, %s);",[my_input, out_put])
        conn.commit()       
        convv.close()
    return render_template('calendar.html',calendar=calendar, my_input=my_input , out_put=out_put, conv=conv)



@app.route("/insert",methods=["POST","GET"])
def insert():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        print(title)     
        print(start)  
        cur.execute("INSERT INTO events (title,start_event,end_event) VALUES (%s,%s,%s)",[title,start,end])
        conn.commit()       
        cur.close()
        msg = 'success' 
    return jsonify(msg)


@app.route("/update",methods=["POST","GET"])
def update():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        id = request.form['id']
        print(title)     
        print(start)  
        cur.execute("UPDATE events SET title = %s, start_event = %s, end_event = %s WHERE id = %s ", [title, start, end, id])
        conn.commit()       
        cur.close()
        msg = 'success' 
    return jsonify(msg) 

@app.route("/ajax_delete",methods=["POST","GET"])
def ajax_delete():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        getid = request.form['id']
        print(getid)
        cur.execute('DELETE FROM events WHERE id = {0}'.format(getid))
        conn.commit()       
        cur.close()
        msg = 'Record deleted successfully' 
    return jsonify(msg) 



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
