import nltk

import six
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# TODO: separate the parsing stuff
def parse_lo(lo):

    result = {}
    tokenised = nltk.word_tokenize(lo)
    pattern = """
        V: {<VB>|<VDB>}
        P: 
          {<.*>+} 
          }<IN>+|<VBG>{
    """
    
    parser = nltk.RegexpParser(pattern)
    st = nltk.tag.stanford.StanfordPOSTagger('./stanford-postagger/models/english-bidirectional-distsim.tagger', './stanford-postagger/stanford-postagger.jar')
    
    result['tree'] = parser.parse(st.tag(tokenised))

    result['phrases'] = []
    # check one level below root
    for tree in result['tree']:
        if type(tree) == nltk.tree.Tree:
            result['phrases'].append(" ".join([i[0] for i in tree.leaves()])) 
    
    result['verb'] = []
    for item in result['tree'][0]:
        if type(item) == nltk.tree.Tree and item.label() == "V":
            result['verb'].append(item)

    return result

 # TODO: score verbs on where they land in a dependency parse tree. they should be the root
  
def basic_stats(lo):
    #
    return 1

def syntax_analysis(lo):
    # Call the natural language api
    client = language.LanguageServiceClient()
    document = types.Document(content=lo, type=enums.Document.Type.PLAIN_TEXT);
    raw_result = client.analyzeSyntax(document)

    result = {}
    # TODO: map gcp pos enum to a standard
    result['pos'] = [(word.text.content, word.part_of_speech.tag) for word in raw_result.tokens]
    # TODO: make dependency tree
    result['d_tree'] = ''
    result['sentences'] = {
        'count': len(raw_result.sentences),
        'sentences': [s.text.content for s in raw_result.sentences]
    }


def is_verb_root(d_tree):
    # TODO: Check if the verb is close to the root of the dependency tree

    return True

def get_bt_category(verb):
    # TODO: fetch bt category by checking sysnonyms of the verb
    # get synset for verb based of lesk in context with the whole lo
    # for each category, path_similarity the verb to the category
    # return match with the highest score


