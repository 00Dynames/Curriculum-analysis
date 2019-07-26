import nltk

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


# TODO: separate the parsing stuff
def syntax_chunk(tokenised):

    result = {}
    pattern = """
        V: {<VB>|<VDB>}
        P: 
          {<.*>+} 
          }<IN>+|<VBG>{
    """
    
    parser = nltk.RegexpParser(pattern)
    st = nltk.tag.stanford.StanfordPOSTagger('./stanford-postagger/models/english-bidirectional-distsim.tagger', './stanford-postagger/stanford-postagger.jar')
    
    result['tree'] = parser.parse(tokenised)

    result['phrases'] = []
    # check one level below root
    for tree in result['tree']:
        if type(tree) == nltk.tree.Tree:
            result['phrases'].append(" ".join([i[0] for i in tree.leaves()])) 

    return result
   
def basic_stats(lo):
    #
    return 1

# TODO: rename it away from syntax_analysis
def syntax_analysis(lo):
    # Call the natural language api
    client = language.LanguageServiceClient()
    document = types.Document(content=lo, type=enums.Document.Type.PLAIN_TEXT);
    s_result = client.analyze_syntax(document)
    e_result = client.analyze_entities(document)

    result = {}
    # TODO: map gcp pos enum to a standard
    result['pos'] = [(word.text.content, gcp_to_nltk_pos_tags[word.part_of_speech.tag]) for word in s_result.tokens]
    
    # TODO: make dependency tree
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
    return True if list(filter(lambda x: x['d_label'] == enums.DependencyEdge.Label.ROOT, d_tree))[0]['pos'] == enums.PartOfSpeech.Tag.VERB else False
