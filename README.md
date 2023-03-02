# eCompanion
we need a database
to start create two sql tabels
the first one called events
run the following commands on pgAdmin or similar patform:
create table convo(
	id serial PRIMARY KEY,
	input_ varchar(1000) NOT NULL,
	output_ varchar(1000) NOT NULL,
	created_at TIMESTAMP DEFAULT timezone('utc' :: TEXT, now())
);
create table events(
    id serial PRIMARY KEY,
    title varchar(255) NOT NULL,
	start_event TIMESTAMP NOT NULL,
    end_event TIMESTAMP NOT NULL

);

then install the virulal venv and flask in the following comands:

pip3 install virtualenv

virtualenv env

source env/bin/activate

pip3 install flask

pip3 install torch torchvision

pip3 install spacy

python -m spacy download en_core_web_sm

pip install sutime

mvn dependency:copy-dependencies -DoutputDirectory=./jars -f $(python3 -c 'import importlib; import pathlib; print(pathlib.Path(importlib.util.find_spec("sutime").origin).parent / "pom.xml")')

pip install psycopg2-binary

_______________________________________
please make sure you have the nltk in python 





