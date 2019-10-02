import sqlite3
import sys
import json

conn = sqlite3.connect('../data/database.sqlite')
cursor = conn.cursor()
cursor.execute("select l.description from acad_objects as a, learning_outcomes as l where a.type='course' and a.id=l.acad_object order by random()")

def make_sample(size):
    results = []

    for outcome in cursor.fetchmany(size):
        print(outcome[0]);
        label = input()
        results.append((outcome[0], label))

    with open('sample.json', 'w') as fp:
        json.dump(results, fp)    

    return results

# TODO: load sample
def load_sample(sample):
    result = []
    with open(sample, 'r') as fp:
        result = json.loads(fp.read())

    return result
