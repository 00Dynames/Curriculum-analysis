import nltk
from nltk.corpus import wordnet
from textstat.textstat import textstatistics, easy_word_set, legacy_round
import six
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

gcp_to_nltk_pos_tags = {
    enums.PartOfSpeech.Tag.ADJ: 'JJ',
    enums.PartOfSpeech.Tag.ADP: 'IN',
    enums.PartOfSpeech.Tag.ADV: 'RB',
    enums.PartOfSpeech.Tag.CONJ: 'CC',
    enums.PartOfSpeech.Tag.DET: 'DT',
    enums.PartOfSpeech.Tag.NOUN: 'NN',
    enums.PartOfSpeech.Tag.NUM: 'CD',
    enums.PartOfSpeech.Tag.PRON: 'PRP',
    enums.PartOfSpeech.Tag.PRT: 'RP',
    enums.PartOfSpeech.Tag.PUNCT: '.',
    enums.PartOfSpeech.Tag.VERB: 'VB',
    enums.PartOfSpeech.Tag.X: '.',
    enums.PartOfSpeech.Tag.AFFIX: '.'
}

# TODO: return a score
def syntax_chunk(tokenised): 

    result = {}
    pattern = """
        V: {<VB>|<VDB>}
        P: 
          {<.*>+} 
          }<IN>+|<VBG>{
    """
    
    parser = nltk.RegexpParser(pattern)
    
    result['tree'] = parser.parse(tokenised)

    result['phrases'] = []
    # check one level below root
    for tree in result['tree']:
        if type(tree) == nltk.tree.Tree:
            result['phrases'].append(" ".join([i[0] for i in tree.leaves()])) 

    return result
  

    result = space.load('en')(text)
    return result.sents

def pre_processing(lo):
    # Call the natural language api
    client = language.LanguageServiceClient()
    document = types.Document(content=lo, type=enums.Document.Type.PLAIN_TEXT);
    s_result = client.analyze_syntax(document)
    e_result = client.analyze_entities(document)

    result = {}
    result['text'] = lo
    result['pos'] = [(word.text.content, gcp_to_nltk_pos_tags[word.part_of_speech.tag]) for word in s_result.tokens]
    
    result['d_tree'] = [{'text': word.text.content, 'd_label': word.dependency_edge.label, 'pos': word.part_of_speech.tag} for word in s_result.tokens]

    result['sentences'] = {
        'count': len(s_result.sentences),
        'sentences': [s.text.content for s in s_result.sentences]
    }

    result['entities'] = {}
    for item in e_result.entities:
        result['entities'][item.name] = {
            'type': item.type,
            'salience': item.salience, 
        }   

    return result 

def is_root_verb(d_tree):
    verb = list(filter(lambda  x: x['d_label'] == enums.DependencyEdge.Label.ROOT, d_tree))[0]
    return (1, verb['text']) if verb['pos'] == enums.PartOfSpeech.Tag.VERB else (0, "")

def avg_sentence_length(text):
    sentences = nltk.sent_tokenize(text)
    words = nltk.tokenize.word_tokenize(text)

    return float(len(words)/len(sentences))

def avg_syllables_per_word(text):
    syllable_count = textstatistics().syllable_count(text) 
    word_count = len(nltk.tokenize.word_tokenize(text))
    return legacy_round(float(syllable_count/word_count), 1)

# metrics + algorithms of how you got them
# what are the statistical properties of it/them
# how to go about validating them
# measure consistency => properly identify 
# boruta algorithm -> ???
# tenfold validation

# text => string 
def flesch_reading_ease(text):
    FRE = 206.835 - float(1.015 * avg_sentence_length(text)) -\
          float(84.6 * avg_syllables_per_word(text)) 
    return legacy_round(FRE, 2)

def salience_avg(lo):
    # TODO: take the mean of the entity saliences and return that as a score
    result = 0
    for e in lo['entites'].keys():
       result =+ lo['entities'][e]['salience']

    result = float(result / len(lo['entities']))

    return result

def verb_category(verb):
    bt_categories = {
        'KNOWLEDGE': wordnet.synset('know.v.11'),
        'COMPREHENSION': wordnet.synset('understand.v.01'),
        'APPLICATION': wordnet.synset('apply.v.02'),
        'ANALYSIS': wordnet.synset('analyze.v.01'),
        'SYNTHESIS': wordnet.synset('synthesize.v.01'),
        'EVALUATION': wordnet.synset('evaluate.v.02')       
    }
    
    # TODO: improve the filtering, actually validate(?) that we're using the right synset here
    syn_verb = wordnet.synsets(verb)[0]

    similarities = []
    for category in bt_categories.keys():
        similarities.append((category, wordnet.path_similarity(bt_categories[category], syn_verb)))
  
    return max(similarities, key = lambda x: x[1])

def aggregate(inputs):
    # root verb
    # TODO: syntax chunk
    # sentence count
    # TODO: syntactic complexity

    COMPONENT_COUNT = 3

    result = (inputs['salience_avg'] + inputs['reading_ease'] + inputs['verb_category']) / COMPONENT_COUNT

    return result
