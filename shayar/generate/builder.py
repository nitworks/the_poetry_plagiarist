__author__ = 'Nitin'
from framenet_reader import lu_from_frames, valence_pattern_from_id, lu_from_word, lu_from_id, get_random_word
import random
import phrase_spec
from rephrase import fit_rhythm_pattern, fit_rhyme, get_synset
from pattern.text.en import wordnet, VERB
import logging
import creation
from shayar.knowledge.retrieval import collocations
from character_creation import create_new_character
from urllib2 import urlopen, URLError
from json import loads as json_load

knowledge = collocations()
pattern = ''
rhyme_token = ''
characters = []
character_i = None
used_relations = []
subj_pronominal = False
obj_pronominal = False


def build_hasproperty_phrase():
    pass


def build_takes_action_phrase(action):
    logging.info('Building action phrase: ' + str(action))
    tried_alternatives = set()
    alternatives = get_synonyms(action, pos=VERB)

    valence_pattern = []
    lu = None
    logging.info('Getting lu and valence pattern')
    while not valence_pattern:
        lu = None
        while lu is None:
            try:
                lu = lu_from_word(action, 'v')
            except IndexError:
                logging.info("I don't know how to use this word, looking for alternatives: " + action)
                tried_alternatives.add(action)
                remaining_alternatives = [word for word in alternatives if word not in tried_alternatives]
                if remaining_alternatives:
                    action = random.choice(remaining_alternatives)
                else:
                    action = get_random_word('V')

        valence_pattern = valence_pattern_from_id(lu.get('ID'))
        if not valence_pattern:
            tried_alternatives.add(action)
            remaining_alternatives = [word for word in alternatives if word not in tried_alternatives]
            if remaining_alternatives:
                action = random.choice(remaining_alternatives)
            else:
                action = get_random_word('V')

    #Get an isa that has not already been chosen
    subj = get_is_a()

    #Get an object that generally receives this action
    obj = ''
    if valence_pattern[1]:
        obj = get_receives_action(action)

    #Get an object that is usually involved in this action
    dep = ''
    if valence_pattern[2]:
        dep = get_action_theme(valence_pattern, action, obj)

    phrases = fit_rhyme(fit_rhythm_pattern(create_phrases(valence_pattern, lu, subj=subj), pattern), rhyme_token,
                        pattern)

    return phrases


def build_name_phrase(name):
    frames = ['Referring_by_name']
    lu = random.choice([lu_from_frames(frames), lu_from_id('5544')])
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    #Get an isa that has not already been chosen
    subj = get_is_a()

    logging.info('Creating phrases')
    phrases = []
    starters_done = False
    for group in valence_pattern:
        phrase = None
        for valence_unit in group:

            pos = valence_unit.get('PT')
            if pos.startswith('N'):
                if subj:
                    new_elem = phrase_spec.NP(subj)
                    if subj_pronominal:
                        new_elem.pronominal = True
                    new_elem.animation = characters[character_i].object_state
                    new_elem.num = characters[character_i].num
                    new_elem.gender = characters[character_i].gender
                    subj = ''
                else:
                    new_elem = phrase_spec.NP(get_random_word(pos))

                if phrase:
                    phrase.complements.append(new_elem)
                else:
                    phrase = new_elem

            elif pos.startswith('V'):
                new_elem = phrase_spec.VP(get_random_word(pos))
                if phrase:
                    phrase.complements.append(new_elem)
                else:
                    phrase = new_elem

            elif pos.startswith('P'):
                n = phrase_spec.NP(get_random_word('N'))

                new_elem = phrase_spec.PP(pos.partition('[')[-1].rpartition(']')[0], n)
                if phrase:
                    phrase.complements.append(new_elem)
                else:
                    phrase = new_elem

        if not starters_done:
            phrases.append(phrase)
            phrase = None
            word = lu.get('name').rpartition('.')[0]
            pos = lu.get('name').partition('.')[-1].upper()
            if pos.startswith('N'):
                new_elem = phrase_spec.NP(word)
                if phrase:
                    phrase.complements.append(new_elem)
                else:
                    phrase = new_elem

            elif pos.startswith('V') or pos.startswith('A'):
                new_elem = phrase_spec.VP(word)
                new_elem.tense = 'past'
                if phrase:
                    phrase.complements.append(new_elem)
                else:
                    phrase = new_elem

            elif pos.startswith('P'):
                n = phrase_spec.NP(word)
                new_elem = phrase_spec.PP(pos.partition('[')[-1].rpartition(']')[0], n)
                if phrase:
                    phrase.complements.append(new_elem)
                else:
                    phrase = new_elem

            starters_done = True

        phrases.append(phrase)

    phrases = [phrase for phrase in phrases if phrase is not None]

    phrases = phrases[:2] + [phrase_spec.NP(name)] + phrases[2:]
    if 'specifier' in phrases[0].__dict__:
        phrases[0].specifier = 'a'

    phrases = fit_rhyme(fit_rhythm_pattern(phrases, pattern), rhyme_token, pattern)

    return phrases


#FIXME: Guarantee a location for the object
def build_location_phrase(location):
    frames = ['Being_located']
    lu = random.choice([lu_from_frames(frames), lu_from_id('10640')])
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    phrases = fit_rhyme(fit_rhythm_pattern(create_phrases(valence_pattern, lu, obj=location), pattern), rhyme_token,
                        pattern)

    return phrases


#FIXME: Make sure that you check the pos of the 'has' word - sometimes noun, sometimes verb
def build_has_phrase(possession):
    # Need to use possessive pronouns as well
    frames = ['Possession']
    lu = lu_from_frames(frames)
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    phrases = fit_rhyme(fit_rhythm_pattern(create_phrases(valence_pattern, lu, subj=possession), pattern), rhyme_token,
                        pattern)

    return phrases


def build_desire_phrase(desire):
    frames = ['Desiring']
    lu = lu_from_frames(frames)
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    subj = get_is_a()

    phrases = fit_rhyme(fit_rhythm_pattern(create_phrases(valence_pattern, lu, subj=subj, obj=desire), pattern),
                        rhyme_token, pattern)

    return phrases


#FIXME: This is pretty bad
def build_capable_phrase():
    frames = ['Capability']
    lu = lu_from_frames(frames)
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    print_nlg_statement(valence_pattern, lu)


#FIXME: This is pretty bad too
def build_partof_phrase():
    frames = ['Part_inner_outer', 'Part_ordered_segments', 'Part_piece', 'Part_whole', 'Inclusion']
    lu = lu_from_frames(frames)
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    print_nlg_statement(valence_pattern, lu)


#FIXME: This isn't great either
def build_send_message_phrase(message):
    frames = ['Communication', 'Telling', 'Statement', 'Chatting']
    lu = lu_from_frames(frames)
    valence_pattern = valence_pattern_from_id(lu.get('ID'))
    #Get an isa that has not already been chosen
    subj = get_is_a()
    phrases = fit_rhyme(fit_rhythm_pattern(create_phrases(valence_pattern, lu, subj=subj, obj=message), pattern),
                        rhyme_token, pattern)

    return phrases


def create_phrases(valence_pattern, lu, subj='', obj='', dep=''):
    logging.info('Creating phrases')
    phrases = []
    starters_done = len(valence_pattern[0]) == 0
    objects_done = len(valence_pattern[1]) == 0
    for group in valence_pattern:
        phrase = None
        for valence_unit in group:

            pos = valence_unit.get('PT')
            if pos.startswith('N'):
                if subj:
                    new_elem = phrase_spec.NP(subj)
                    if subj_pronominal:
                        new_elem.pronominal = True
                    new_elem.animation = characters[character_i].object_state
                    new_elem.num = characters[character_i].num
                    new_elem.gender = characters[character_i].gender
                    subj = ''
                elif starters_done and not objects_done and obj:
                    new_elem = phrase_spec.NP(obj)
                    if obj_pronominal:
                        new_elem.pronominal = True
                    obj = ''
                else:
                    new_elem = phrase_spec.NP(get_random_word(pos))

                if phrase:
                    phrase.complements.append(new_elem)
                else:
                    phrase = new_elem

            elif pos.startswith('V'):
                new_elem = phrase_spec.VP(get_random_word(pos))
                new_elem.tense = 'past'
                if phrase:
                    phrase.complements.append(new_elem)
                else:
                    phrase = new_elem

            elif pos.startswith('P'):
                if subj:
                    n = phrase_spec.NP(subj)
                    if subj_pronominal:
                        n.pronominal = True
                    n.animation = characters[character_i].object_state
                    n.num = characters[character_i].num
                    n.gender = characters[character_i].gender
                    subj = ''
                elif starters_done and obj:
                    n = phrase_spec.NP(obj)
                    if obj_pronominal:
                        n.pronominal = True
                    obj = ''
                else:
                    n = phrase_spec.NP(get_random_word(pos))

                new_elem = phrase_spec.PP(pos.partition('[')[-1].rpartition(']')[0], n)
                if phrase:
                    phrase.complements.append(new_elem)
                else:
                    phrase = new_elem

        if not starters_done:
            phrases.append(phrase)
            phrase = None
            word = lu.get('name').rpartition('.')[0]
            pos = lu.get('name').partition('.')[-1].upper()
            if pos.startswith('N'):
                new_elem = phrase_spec.NP(word)
                if phrase:
                    phrase.complements.append(new_elem)
                else:
                    phrase = new_elem

            elif pos.startswith('V') or pos.startswith('A'):
                new_elem = phrase_spec.VP(word)
                new_elem.tense = 'past'
                if phrase:
                    phrase.complements.append(new_elem)
                else:
                    phrase = new_elem

            elif pos.startswith('P'):
                n = phrase_spec.NP(word)
                new_elem = phrase_spec.PP(pos.partition('[')[-1].rpartition(']')[0], n)
                if phrase:
                    phrase.complements.append(new_elem)
                else:
                    phrase = new_elem

            starters_done = True
        elif not objects_done:
            objects_done = True

        phrases.append(phrase)

    return [phrase for phrase in phrases if phrase is not None]


def make_clause(spec_phrases):
    phrases = []

    for spec_phrase in spec_phrases:
        phrases.append(spec_phrase.translate_to_nlg())

    if len(phrases) > 2:
        line = creation.phraseFactory.createClause(phrases[0], phrases[1], phrases[2])
        for phrase in phrases[3:]:
            line.addComplement(phrase)
    elif len(phrases) > 1:
        line = creation.phraseFactory.createClause(phrases[0], phrases[1])
    else:
        line = phrases[0]

    return line


def get_synonyms(word, pos=None):
    synonyms = []

    if pos is not None:
        synset = wordnet.synsets(word, pos=pos)
    else:
        synset = wordnet.synsets(word)

    if synset:
        synonyms.extend(synset[0].synonyms)
        synonyms.extend([str(holonym).partition("'")[-1].rpartition("'")[0] for holonym in synset[0].holonyms()])
        synonyms.extend([str(hypernym).partition("'")[-1].rpartition("'")[0] for hypernym in synset[0].hypernyms()])

    return synonyms


def get_is_a(character_index=character_i):
    #Get an isa that has not already been chosen
    char = characters[character_index]
    isas = char.type_to_list['IsA']
    filtered_isas = [isa for isa in isas if tuple([characters[character_index], 'IsA', isa]) not in used_relations]
    if filtered_isas:
        isa = random.choice(filtered_isas)
        used_relations.append(tuple([characters[character_index], 'IsA', isa]))
    else:
        #If all chosen then use pronominal or typeof (introduce anaphora)
        #TODO: Introduce typeof or synonym
        global subj_pronominal
        subj_pronominal = True
        isa = random.choice(isas)

    return isa


def get_receives_action(action):
    #Look through the other characters, finding a receives action for the given verb
    for character in characters:
        if action in character.type_to_list['ReceivesAction']:
            return get_is_a(character_index=characters.index(character))

    #Otherwise, add a new character that *would* receive such an action
    candidates = []
    for similarity_score in [x / 20.0 for x in reversed(range(0, 21, 1))]:
        candidates = [head for head, tail, relation in knowledge if relation == 'ReceivesAction' and
                      wordnet.similarity(get_synset(tail), get_synset(action)) > similarity_score]
        if candidates:
            break

    noun = random.choice(candidates)
    new_character = create_new_character(noun, len(characters))
    new_character.add_relation('ReceivesAction', action)

    return noun


def get_action_theme(valence_pattern, action, obj):
    prep = ''
    for group in valence_pattern:
        for valence_unit in group:
            pos = valence_unit.get('PT')
            if pos.startswith('P'):
                prep = pos.partition('[')[-1].rpartition(']')[0]

    #Make an API request to Google autocomplete (firefox gives fewer answers than chrome, but we only need one now)
    url = "http://suggestqueries.google.com/complete/search?client=firefox&q="
    request_url = url + ' '.join([action, obj, prep])
    try:
        socket = urlopen(request_url)
        json = json_load(socket.read())
        socket.close()
    except URLError:
        raise Exception("You are not connected to the Internet!")

    dep = json[1][1].replace(json[0], '')
    return dep




