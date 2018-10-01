import pandas as pd
import collections
import numpy as np
import re
import uuid

from spellsource.context import Context
from spellsource.behaviour import *
from spellsource.utils import simulate

class ArenaCardPicker(object):
    """Arena Card Picker class generates independent card
    choices for each class"""

    def __init__(self, arena_card_list='cards.csv'):
        self.arena_cards = pd.read_csv(arena_card_list)
        self.draft_classes = set(self.arena_cards['Draft Class'])
    
    def GetCardChoice(self, draft_class: str):
        assert draft_class in self.draft_classes
        return list(self.GetAllCards(draft_class).sample(n=3))

    def GetAllCards(self, draft_class):
        return self.arena_cards[self.arena_cards['Draft Class'] == draft_class]['Card Name']

ArenaSelection = collections.namedtuple('ArenaSelection', 'choices, selected')

class Draft(object):
    """Represents card draft process in arena."""

    def __init__(self, draft_class: str, selections: List[ArenaSelection], name=None):
        self.draft_class = draft_class
        self.selections = selections
        self.name = name

    def Iter(self):
        """
        Replay the card selection process.
        Returns: an iterator that yield (Deck, ArenaSelection) tuple.
        """
        cards = []
        for selection in self.selections:
            yield Deck(self.draft_class, tuple(cards), self.name), selection
            cards.append(selection.selected)

    def GetDeck(self):
        return Deck(
                self.draft_class,
                [s.selected for s in self.selections],
                self.name)
    
    def Shuffle(self):
        """Returns a random shuffle of card selection process, used to generate
        training data."""
        new_selections = selections.deepcopy()
        np.random.shuffle(new_selections)
        return ArenaCardPickReplay(self.draft_class, new_selections, self.name)

class Deck(collections.namedtuple('Deck', 'draft_class, cards, name')):
    """Represents a arena deck."""
    def __new__(cls, draft_class: str, cards: List[str], name: str=None):
        if not name:
            name = uuid.uuid1()
        return super(Deck, cls).__new__(cls, draft_class, cards, name)
    
    def ToHSString(self):
        result = """### {}
# Class: {}
# Format: Standard
# Year of the Raven
#
""".format(self.name, self.draft_class)
        for card in self.cards:
            result += "# 1x (2) {}\n".format(card)
        return result
