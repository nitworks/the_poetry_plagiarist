__author__ = 'Nitin'

from nltk.sem.drt import *
from nltk.parse import load_parser
from utils import get_tokenized_words
from nltk.featstruct import FeatStructParser
from nltk.grammar import FeatStructNonterminal
from shayar.drt import grammar_dir
from pattern.text.en import parsetree
from shayar.character import Character
from nltk.corpus import verbnet
from shayar.analyse import timex

characters = []
negative_adverbs = set(['not', 'seldom', 'hardly', 'barely', 'scarcely', 'rarely'])


def build_story(poem):
    lines = ""
    for line in poem:
        lines += line.lower() + " "

    parse_sentences = parsetree(lines, tags=True, chunks=True, relations=True, lemmata=True, tagset=True)

    for sentence in parse_sentences:
        analyse_sentence(sentence.words)


def analyse_sentence(sentence):
    is_a_relations = find_is_a_relations(sentence)
    for relation in is_a_relations:
        print relation

    at_location_relations = find_at_location_relations(sentence)
    for relation in at_location_relations:
        print relation


# Return a 2D array, one with the subject and one with the object
#def find_capable_of_relations(sentence):


def find_is_a_relations(sentence):
    #Assume this is an IsA and not a NotIsA
    positive = True

    #Get the list of words that are like 'is'
    is_a_verbs = set(verbnet.lemmas(verbnet.classids('be')[0]))
    #Find all the verbs
    verbs = set([word for word in sentence if word.type.startswith('V')])

    for verb in verbs:
        #Check if there is a verb like 'is'
        if verb.lemma in is_a_verbs:
            n = 1
            #Check that it is followed by a determiner, possibly after a number of adverbs
            while sentence[sentence.index(verb) + n].type.startswith('R'):
                n += 1
            if sentence[sentence.index(verb) + n].type.startswith('D'):
                #We have an IsA for sure, now split the sentence
                before_is = sentence[:sentence.index(verb)]
                after_dt = sentence[sentence.index(verb) + n + 1:]
                adverbs = set([word for word in sentence if word not in before_is and word not in after_dt])
                if sentence[sentence.index(verb) + n] == 'no' or sentence[sentence.index(verb) + n] == 'neither':
                    positive = not positive

                if len(adverbs & negative_adverbs) % 2 == 1:
                    positive = not positive

                return positive, before_is, after_dt

    return ()

#def find_has_a_relations(sentence):


#def determine_if_has_a_is_part_of_relation(hasA_relations):


def find_at_location_relations(sentence):
    #Assume this is an AtLocation not NotAtLocation
    positive = True

    single_at_location_preps = set(['abaft', 'aboard', 'about', 'above', 'across', 'after', 'against', 'along', 'alongside',
                             'amid', 'amidst', 'among', 'amongst', 'anenst', 'around', 'aside', 'astride', 'at',
                             'athwart', 'atop', 'before', 'behind', 'below', 'beneath', 'beside', 'besides', 'between',
                             'betwixt', 'by', 'down', 'forenenst', 'in', 'inside', 'into', 'mid', 'midst', 'near',
                             'next', 'nigh', 'on', 'onto', 'opposite', 'outside', 'over', 'round', 'through', 'thru',
                             'to', 'toward', 'towards', 'under', 'underneath', 'up', 'upon', 'with', 'within',
                             'behither', 'betwixen', 'betwixt', 'biforn', 'ere', 'fornent', 'gainst', "'gainst", 'neath',
                             "'neath", 'overthwart', 'twixt', "'twixt"])

    double_at_location_preps = set(['ahead of', 'back to', 'close to', 'in to', 'inside of', 'left of', 'near to',
                                    'next to', 'on to', 'outside of', 'right of'])

    triple_at_location_preps = set(['in front of', 'on top of'])

    single_not_at_location_preps = set(['beyond', 'from', 'off', 'out', 'past', 'via', 'ayond', 'ayont', 'froward',
                                        'frowards', 'fromward', 'outwith'])

    double_not_at_location_preps = set(['far from', 'out from', 'out of', 'away from'])

    unparsed = ''
    for word in sentence:
        unparsed += ' ' + word.string
    unparsed = unparsed.lstrip().split(' ')

    prep = ''

    for triple_prep in triple_at_location_preps:
        if triple_prep in unparsed:
            prep = triple_prep
            break

    if not prep:
        for double_prep in double_at_location_preps:
            if double_prep in unparsed:
                prep = double_prep
                break

    if not prep:
        for double_not_prep in double_not_at_location_preps:
            if double_not_prep in unparsed:
                prep = double_not_prep
                positive = False
                break

    if not prep:
        for single_prep in single_at_location_preps:
            if single_prep in unparsed:
                prep = single_prep
                break

    if not prep:
        for single_not_prep in single_not_at_location_preps:
            if single_not_prep in unparsed:
                prep = single_not_prep
                positive = False
                break

    if not prep:
        return ()

    print prep.split(' ')
    prep_first_word_index = unparsed.index(prep.split(' ')[0])
    prep_last_word_index = prep_first_word_index + prep.count(' ')

    n = 1
    #Check that the next noun is not a time
    while not sentence[prep_last_word_index + n].type.startswith('N'):
        n += 1
    if not timex.tag(sentence[prep_last_word_index + n].string):
        m = 1
        while not sentence[prep_first_word_index - m].type.startswith('N'):
            m += 1

        before_prep = sentence[:prep_first_word_index]
        after_prep = sentence[prep_last_word_index+1:]
        adverbs = set([word for word in sentence if word not in before_prep and word not in after_prep])
        if len(adverbs & negative_adverbs) % 2 == 1:
            positive = not positive
        #The object that can be found, the preposition, the location (need to take into account len(prep)
        return positive, sentence[prep_first_word_index - m], prep, \
               sentence[prep_last_word_index:prep_last_word_index + n + 1]

    return ()

#def find_receives_action_relations(sentence):



#def find_used_for_relations(sentence):



#def find_created_by_relations(sentence):



#def find_desires_relations(sentence):



#def find_has_property_relations(sentence):



#def resolve_characters():


"""
def build_drs(poem):
    #parser = load_parser('file:' + grammar_dir.replace('\\', '/'), trace=0, fstruct_parser=FeatStructParser(fdict_class=FeatStructNonterminal, logic_parser=DrtParser()))
    parser = load_parser('file:' + grammar_dir.replace('\\', '/'), trace=0, logic_parser=DrtParser())

    lines = ""
    for line in poem:
        lines += line + " "

    parse_sentences = parsetree(lines, tags=True, chunks=True, relations=True, lammata=True, tagset=True)

    accepted_types = ['JJ', 'JJR', 'JJS', 'MD', 'NN', 'NNP', 'NNPS', 'NNS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP','VBZ'   ]

    for sentence in parse_sentences:
        words = []
        for word in sentence.words:
            if word.type in accepted_types:
                words.extend(word)
        if not sentence.subjects:
            line = ""
            for word in words:
                line += word.string
            reparse_line = parsetree(lines, tags=True, chunks=True, relations=True, lammata=True, tagset=True)[0]
            words = []
            for reparse_word in reparse_line:
                words.extend(reparse_word)


    parse_sentences = parsetree(new_lines, tags=True, chunks=True, relations=True, lammata=True, tagset=True)


    #trees = parser.nbest_parse(line)
    trees = parser.nbest_parse('the bartender said the neutron'.split())
    if not trees: print 'no way to parse this!'
    for tree in trees:
        print(tree.node['SEM'].simplify())
"""