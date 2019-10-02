import components
import sqlite3

#select learning outcomes from assessments
conn = sqlite3.connect('./data/database.sqlite')
cursor = conn.cursor()

cursor.execute("select l.description from acad_objects as a, learning_outcomes as l where a.type='course' and a.id=l.acad_object")

# TODO: parse learning outcomes 
for outcome in cursor.fetchmany(10):
    print(outcome[0])
    result = components.syntax_analysis(outcome[0])
    print(result)
    print(components.syntax_chunk(result['pos']))
    print(components.is_root_verb(result['d_tree']))
