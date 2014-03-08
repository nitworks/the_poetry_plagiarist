__author__ = 'Nitin'
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter


# Has all the options for producing poems, as well as plot functions for viewing the options
class Template:
    def __init__(self, collection):
        self.collection = collection        # The collection of poems that this template applies to

        self.stanzas = []                   # Number of stanzas
        self.num_lines = []                 # List of numbers indicating lines per stanza
        self.repeated_lines_locations = []  # List of tuples of lines that are the same
        self.num_repeated_lines = []
        self.num_distinct_sentences = []
        self.line_tenses = []
        self.overall_tense = []

        self.assonance = {}
        self.consonance = {}
        self.alliteration = {}

        self.rhyme_schemes = []
        self.syllable_patterns = []
        self.stress_patterns = []

        self.similes = []

        self.character_count = []
        self.character_genders = []
        self.character_nums = []
        self.character_animations = []
        self.character_personifications = []

    def plot(self, attribute):
        if not attribute:
            pass
        elif attribute == 'all':
            for func in attribute_plot_map.values():
                func(self)
        else:
            attribute_plot_map[attribute](self)

    def plot_stanzas(self):
        counts = Counter(self.stanzas).most_common()
        x = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Number of stanzas', 'Number of occurrences', x, 'Range of number of stanzas')

    def plot_num_lines(self):
        counts = Counter(self.num_lines).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Number of lines for all stanza amounts', 'Number of occurrences', x_ticks,
                        'Range of number of lines per stanza')

    def plot_repeated_lines(self):
        counts = Counter(self.repeated_lines_locations).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Positions of repeated lines', 'Number of occurrences', x_ticks,
                        'Range of positions of repeated lines')

    def plot_num_repeated_lines(self):
        counts = Counter(self.num_repeated_lines).most_common()
        x = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Number of repeated lines', 'Number of occurrences', x,
                        'Range of number of repeated lines')

    def plot_num_distinct_sentences(self):
        counts = Counter(self.num_distinct_sentences).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Number of distinct sentences', 'Number of occurrences', x_ticks,
                        'Range of number of distinct sentences')

    def plot_line_tenses(self):
        counts = Counter(self.line_tenses).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Permutations of line tenses', 'Number of occurrences', x_ticks,
                        'Range of permutations of tenses for each line')

    def plot_overall_tense(self):
        counts = Counter(self.overall_tense).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Overall tense', 'Number of occurrences', x_ticks, 'Range of overall poem tense')

    def plot_assonance(self):
        x = tuple(np.arange(len(self.assonance.keys())))
        x_ticks = tuple(self.assonance.keys())
        ys = self.assonance.values()

        for y in ys:
            if len(y) < len(x):
                y.extend([0] * (len(x) - len(y)))

        zipped_ys = zip(*ys)
        plot_bar_stacked(x, zipped_ys, 'Vowel Phonemes', 'Number of occurrences stacked by poem', x_ticks, 'Assonance')

    def plot_consonance(self):
        x = tuple(np.arange(len(self.consonance.keys())))
        x_ticks = tuple(self.consonance.keys())
        ys = self.consonance.values()

        for y in ys:
            if len(y) < len(x):
                y.extend([0] * (len(x) - len(y)))

        zipped_ys = zip(*ys)
        plot_bar_stacked(x, zipped_ys, 'Consonant Phonemes', 'Number of occurrences stacked by poem', x_ticks,
                         'Consonance')

    def plot_alliteration(self):
        x = tuple(np.arange(len(self.alliteration.keys())))
        x_ticks = tuple(self.alliteration.keys())
        ys = self.alliteration.values()

        for y in ys:
            if len(y) < len(x):
                y.extend([0] * (len(x) - len(y)))

        zipped_ys = zip(*ys)
        plot_bar_stacked(x, zipped_ys, 'Consonant Phonemes', 'Number of occurrences stacked by poem', x_ticks,
                         'Alliteration')

    def plot_rhyme(self):
        counts = Counter(self.rhyme_schemes).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Rhyme Scheme', 'Number of occurrences', x_ticks, 'Range of Possible Rhyme Schemes')

    def plot_syllable_patterns(self):
        counts = Counter(self.syllable_patterns).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Syllable Patterns', 'Number of occurrences', x_ticks, 'Possible Syllabic Rhythm')

    def plot_stress_patterns(self):
        for line in self.stress_patterns:
            counts = Counter(line).most_common()
            x = tuple(np.arange(len(counts)))
            x_ticks = tuple([num for num, count in counts])
            y = tuple([count for num, count in counts])
            plot_bar_simple(x, y, 'Stress Pattern', 'Number of occurrences', x_ticks,
                            'Range of Possible Stress Patterns for Line ' + str(self.stress_patterns.index(line) + 1))

    def plot_similes(self):
        counts = Counter(self.similes).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Existence', 'Number of occurrences', x_ticks, 'Exsistence of Simile')

    def plot_character_count(self):
        counts = Counter(self.character_count).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Number of characters', 'Number of occurrences', x_ticks, 'Range of number of characters')

    def plot_character_genders(self):
        counts = Counter(self.character_genders).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Gender', 'Number of occurrences', x_ticks, 'Range of character genders')

    def plot_character_nums(self):
        counts = Counter(self.character_nums).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Num', 'Number of occurrences', x_ticks, 'Range of character nums')

    def plot_character_animations(self):
        counts = Counter(self.character_animations).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Object State', 'Number of occurrences', x_ticks, 'Range of character animation')

    def plot_character_personifications(self):
        counts = Counter(self.character_personifications).most_common()
        x = tuple(np.arange(len(counts)))
        x_ticks = tuple([num for num, count in counts])
        y = tuple([count for num, count in counts])
        plot_bar_simple(x, y, 'Existence', 'Number of occurrences', x_ticks, 'Existence of character personification')



attribute_plot_map = {
    'stanzas': Template.plot_stanzas,
    'num_lines': Template.plot_num_lines,
    'repeated_lines': Template.plot_repeated_lines,
    'num_repeated_lines': Template.plot_num_repeated_lines,
    'num_distinct_sentences': Template.plot_num_distinct_sentences,
    'line_tenses': Template.plot_line_tenses,
    'overall_tense': Template.plot_overall_tense,
    'assonance': Template.plot_assonance,
    'consonance': Template.plot_consonance,
    'alliteration': Template.plot_alliteration,
    'rhyme': Template.plot_rhyme,
    'syllable_patterns': Template.plot_syllable_patterns,
    'stress_patterns': Template.plot_stress_patterns,
    'similes': Template.plot_similes,
    'character_count': Template.plot_character_count,
    'character_genders': Template.plot_character_genders,
    'character_nums': Template.plot_character_nums,
    'character_animations': Template.plot_character_animations,
    'character_personifications': Template.plot_character_personifications,
}


def plot_bar_simple(x, y, x_axis, y_axis, x_ticks, title):
    width = 0.5

    fig, ax = plt.subplots()
    ax.bar(x, y, width=width, align='center')

    ax.set_xticklabels(x_ticks)
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(title)
    plt.xticks(x, ha='center')

    plt.show()


def plot_bar_stacked(x, ys, x_axis, y_axis, x_ticks, title):
    width = 0.5

    fig, ax = plt.subplots()
    prev = 0
    colour = 'b'
    for y in ys:
        ax.bar(x, y, bottom=prev, width=width, color=colour, align='center')
        prev = y
        if colour == 'b':
            colour = 'r'
        else:
            colour = 'b'

    ax.set_xticklabels(x_ticks)
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(title)
    plt.xticks(x, ha='center')

    plt.show()







