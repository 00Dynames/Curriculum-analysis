import components
import sqlite3

#select learning outcomes from assessments
conn = sqlite3.connect('./data/database.sqlite')
cursor = conn.cursor()

cursor.execute("select l.description from acad_objects as a, learning_outcomes as l where a.type='course' and a.id=l.acad_object")

# TODO: parse learning outcomes 
for outcome in cursor.fetchone():
    print(outcome)
    result = components.syntax_analysis(outcome)
    print(result)
    lo_object = components.syntax_chunk(result['pos'])
    print(lo_object)

    break

#average lo lenght
#find an example look for similar in the dataset
#decision trees
#give scores based on frequency of occurence
#look at sentiment analysis as example
#strucyural fitness
#run through the process
#have an architecture of what you want to achieve
#entites salience to measure lo specificity
#concrete ify the parts of each section wrt the pos
