# e-Companion

BSc Computer Science final-year project, Queen Mary University of London (2022).
Supervisor: Dr Julian Hough.

e-Companion is a web-based personal assistant that holds a conversation and manages the user's calendar. You can ask it to book or cancel events in plain English ("book a meeting next Tuesday at 3"), and it turns the request into a real calendar entry, asking a follow-up question when the date or time is missing.

## How it works

```
user message ──► tokenise + stem (NLTK) ──► bag of words ──► intent classifier (PyTorch)
                                                                  │
                         confidence < 0.75 ──► "I do not understand..."
                                                                  │
                    booking / cancel ──► spaCy NER: is there a DATE and a TIME?
                                              │ no  ──► ask a follow-up question
                                              │ yes ──► SUTime ──► timestamps ──► PostgreSQL events table
                                                                  │
                    other intents ──► scripted response
```

- **Intent recognition.** A small feed-forward neural network (three linear layers with ReLU) built in PyTorch classifies each message into one of nearly sixty intents defined in `intents.json`, such as booking, cancelling, asking the time, greetings and small talk. Messages are tokenised and stemmed with NLTK and encoded as a bag of words.
- **Understanding dates and times.** For calendar requests, spaCy's named entity recognition checks whether the message contains a date and a time. If either is missing, the assistant asks for it. SUTime then converts expressions like "next Tuesday at 3" into exact timestamps.
- **Calendar and memory.** Events are stored in PostgreSQL and shown in a calendar view, where they can also be added, edited or deleted by hand. Every exchange is logged in a conversation table.
- **Web app.** Built with Flask, with HTML/CSS templates for the chat and calendar pages.

## Project structure

| File | Purpose |
|---|---|
| `app.py` | Flask app: chat handling, calendar routes, database access |
| `model.py` | PyTorch intent classifier |
| `train.py` | Trains the classifier from `intents.json` and saves `data.pth` |
| `nltk_utils.py` | Tokenising, stemming and bag-of-words encoding |
| `word.py` | spaCy checks for dates and times in a message |
| `hand_event.py` | SUTime date and time parsing |
| `intents.json` | Intents, example phrases and responses |
| `templates/`, `static/` | Web pages and styles |

## Setup

1. Create the database tables (for example in pgAdmin):

   ```sql
   CREATE TABLE convo (
       id SERIAL PRIMARY KEY,
       input_ VARCHAR(1000) NOT NULL,
       output_ VARCHAR(1000) NOT NULL,
       created_at TIMESTAMP DEFAULT timezone('utc'::TEXT, now())
   );

   CREATE TABLE events (
       id SERIAL PRIMARY KEY,
       title VARCHAR(255) NOT NULL,
       start_event TIMESTAMP NOT NULL,
       end_event TIMESTAMP NOT NULL
   );
   ```

2. Create a virtual environment and install the dependencies:

   ```
   pip3 install virtualenv
   virtualenv env
   source env/bin/activate
   pip3 install flask torch torchvision spacy nltk sutime dateparser psycopg2-binary
   python -m spacy download en_core_web_sm
   ```

3. SUTime needs its Java dependencies (requires Maven):

   ```
   mvn dependency:copy-dependencies -DoutputDirectory=./jars -f $(python3 -c 'import importlib; import pathlib; print(pathlib.Path(importlib.util.find_spec("sutime").origin).parent / "pom.xml")')
   ```

   Then update the SUTime jar path in `hand_event.py` to match your environment.

4. Update the database connection details in `app.py`, then train the model and start the app:

   ```
   python3 train.py
   python3 app.py
   ```
