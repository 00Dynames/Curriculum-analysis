from src import components
from tests import sample
import sys, os, json

# read sample name from argv[1]

if os.path.isfile("./%s.json"%(sys.argv[1])):
    s = sample.load_sample(sys.argv[1])
else:
    s = sample.make_sample(50, sys.argv[1])

result = []
for lo in s:
    print(lo)
    lo_processed = components.pre_processing(lo)

    lo_result = {}
    lo_result['text'] = lo
    lo_result['flesch_reading_ease'] = components.flesch_reading_ease(lo_processed['text'])
    lo_result['verb_root'], lo_result['verb'] = components.is_root_verb(lo_processed['d_tree'])
    lo_result['salience_average'] = components.salience_avg(lo_processed)

    if lo_result['verb'] != "":
        lo_result['verb_category'] = components.verb_category(lo_result['verb'])
    else: 
        lo_result['verb_category'] = ("", 0)

    lo_result['sentence_count'] = lo_processed['sentences']['count']
   
    ag = components.aggregate(lo_result)
    lo_result['aggregate'] = ag

    result.append(lo_result)

with open("%s_result.json"%(sys.argv[1]), 'w') as fp:
    json.dump(result, fp)
