__author__ = 'Nitin'
from shayar.analyse.detectors.rhythm import get_stress_pattern
import builder
import jpype
from shayar.analyse.detectors.utils import set_up_globals
set_up_globals(ono=False)


class NP():
    def __init__(self, noun):
        self.noun = noun
        self.specifier = None
        self.num = 'sg'
        self.animation = 'n'
        self.gender = 'n'
        self.person = 'third'
        self.possessive = False
        self.pronominal = False
        self.modifiers = []
        self.complements = []
        self.stress_patterns = get_stress_pattern([noun])[0]

    def translate_to_nlg(self):
        phrase = builder.phraseFactory.createNounPhrase(self.noun)

        phrase.setSpecifier(self.specifier)
        phrase.setFeature(builder.feature.PRONOMINAL, jpype.JBoolean(self.pronominal))
        phrase.setFeature(builder.feature.POSSESSIVE, jpype.JBoolean(self.possessive))

        for modifier in self.modifiers:
            phrase.addModifier(modifier.adjective)
        for complement in self.complements:
            phrase.addComplement(complement.translate_to_nlg())

        if self.gender == 'n':
            phrase.setFeature(builder.lexical_feature.GENDER, builder.gender.NEUTER)
        elif self.gender == 'f':
            phrase.setFeature(builder.lexical_feature.GENDER, builder.gender.FEMININE)
        elif self.gender == 'm':
            phrase.setFeature(builder.lexical_feature.GENDER, builder.gender.MASCULINE)

        if self.gender == 'sg':
            phrase.setFeature(builder.feature.NUMBER, builder.number_agreement.SINGULAR)
        elif self.gender == 'pl':
            phrase.setFeature(builder.feature.NUMBER, builder.number_agreement.PLURAL)

        if self.gender == 'first':
            phrase.setFeature(builder.feature.PERSON, builder.person.FIRST)
        elif self.gender == 'second':
            phrase.setFeature(builder.feature.PERSON, builder.person.SECOND)
        elif self.gender == 'third':
            phrase.setFeature(builder.feature.PERSON, builder.person.THIRD)

        return phrase


class PP():
    def __init__(self, prep, np):
        self.prep = prep
        self.np = np
        self.modifiers = []
        self.complements = []
        self.stress_patterns = get_stress_pattern([prep])[0]

    def translate_to_nlg(self):
        phrase = builder.phraseFactory.createPrepositionPhrase(self.prep)
        for modifier in self.modifiers:
            self.np.modifiers.append(ADJ(modifier.adjective))
        for complement in self.complements:
            self.np.complements.append(complement)

        phrase.addComplement(self.np.translate_to_nlg())
        return phrase


class VP():
    def __init__(self, verb):
        self.verb = verb
        self.negated = False
        self.tense = ''
        self.aspect = ''
        self.modifiers = []
        self.complements = []
        self.stress_patterns = get_stress_pattern([verb])[0]

    def translate_to_nlg(self):
        phrase = builder.phraseFactory.createVerbPhrase(self.verb)

        phrase.setFeature(builder.feature.NEGATED, jpype.JBoolean(self.negated))

        for modifier in self.modifiers:
            phrase.addModifier(modifier.adverb)
        for complement in self.complements:
            phrase.addComplement(complement.translate_to_nlg())

        if self.tense == 'past':
            phrase.setFeature(builder.feature.TENSE, builder.tense.PAST)
        elif self.tense == 'present':
            phrase.setFeature(builder.feature.TENSE, builder.tense.PRESENT)
        elif self.tense == 'future':
            phrase.setFeature(builder.feature.TENSE, builder.tense.FUTURE)

        if self.aspect == 'perfect':
            phrase.setFeature(builder.feature.PERFECT, True)
            phrase.setFeature(builder.feature.PASSIVE, False)
            phrase.setFeature(builder.feature.PROGRESSIVE, False)
        elif self.aspect == 'passive':
            phrase.setFeature(builder.feature.PASSIVE, True)
            phrase.setFeature(builder.feature.PERFECT, False)
            phrase.setFeature(builder.feature.PROGRESSIVE, False)
        elif self.aspect == 'progressive':
            phrase.setFeature(builder.feature.PROGRESSIVE, True)
            phrase.setFeature(builder.feature.PERFECT, False)
            phrase.setFeature(builder.feature.PASSIVE, False)

        return phrase


class ADJ():
    def __init__(self, adjective):
        self.adjective = adjective
        self.stress_patterns = get_stress_pattern([adjective])[0]


class ADV():
    def __init__(self, adverb):
        self.adverb = adverb
        self.stress_patterns = get_stress_pattern([adverb])[0]