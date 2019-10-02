from tests import sample
import components
import sys

def accuracy(s):
    sample_set = sample.load_sample(s)
    count = 0
    
    for outcome, label in sample_set:
        p_outcome = components.pre_processing(outcome)
        result = components.is_root_verb(p_outcome['d_tree'])
            
        print("%s | %s | %s" % (outcome, result, label))

        if result and label == 'y':
            count += 1

    return (count, len(sample_set))

if __name__ == '__main__':
    print(accuracy(sys.argv[1]))
