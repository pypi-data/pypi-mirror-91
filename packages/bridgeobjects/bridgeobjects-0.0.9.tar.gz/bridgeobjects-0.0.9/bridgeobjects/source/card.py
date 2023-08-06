"""The Card class for the bridgeobjects package."""


from .constants import SUIT_NAMES, RANKS, SUITS

__all__ = ['Card']


class Card(object):
    """
    A card object for the bridgeobjects module.

    Parameters
    ----------
    name: (str) card's name (or rand if a two part parameter)

    Example
    -------
        card = Card("TS")

    suit_name: (str) (optional) card's suit name

    Example
    -------
        card = Card("T", "S")

    A card is defined by a two (or three in the case of '10') character string:
        the first character defines the rank (e.g. A, K, ... T, 9, ...);\n
        the second, the suit name (C, D, H, S).

    Cards can be compared based on their rank, provided they
    are in the same suit:

    Example
    -------
        assert Card('AS') > Card('TS')

    A card's value is based on A=13, K=12, etc.
"""

    def __init__(self, name, suit_name=None):
        """Create the card class."""
        if suit_name:
            name = ''.join([name, suit_name])
        if name[:2] == '10':
            name = f'T{name[2]}'
        if len(name) != 2:
            raise ValueError(f'Card name must contain precisely 2 characters: "{name}"')
        elif name[0] not in RANKS:
            raise ValueError(f'Invalid rank in card: "{name}"')
        elif name[1] not in SUIT_NAMES:
            raise ValueError(f'Invalid suit in card: "{name}"')

        self._name = name
        self._rank = name[0]
        self._suit_name = name[1]

        self.image = None
        self.bitmap = None
        self._suit = SUITS[self._suit_name]
        self._value = RANKS.index(self._rank)
        self._is_honour = self._value >= 10
        self._high_card_points = max(0, self._value-9)
        self.play_note_index = None

    def __eq__(self, other):
        if self._name == other.name:
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if self._suit == other.suit:
            if self._value > other.value:
                return True
        else:
            return False

    def __ge__(self, other):
        if self._suit == other.suit:
            if self._value >= other.value:
                return True
        else:
            return False

    def __lt__(self, other):
        if self._suit == other.suit:
            if self._value < other.value:
                return True
        else:
            return False

    def __le__(self, other):
        if self._suit == other.suit:
            if self._value <= other.value:
                return True
        else:
            return False

    def __repr__(self):
        return f'Card("{self._name}")'

    def __str__(self):
        return f'Card("{self._name}")'

    @property
    def name(self):
        """
        The card's name.
        Returns the card's name (e.g. "TS") as a string.
        """
        return self._name

    @property
    def rank(self):
        """
        The card's rank.
        Returns the card's rank (e.g. "A" or "T") as a string.
        """
        return self._rank

    @property
    def is_honour(self):
        """
        Return True if the card is A, K, Q or J.
        """
        return self._is_honour

    @property
    def suit_name(self):
        """
            The card's suit name.

            Returns the card's suit name (e.g. "S" or "D") as a string.
        """
        return self._suit_name

    @property
    def suit(self):
        """
        The card's suit.
        Returns the card's suit (e.g. the object Spades() for spades as a Suit instance.
        """
        return self._suit

    @property
    def value(self):
        """
        The card's value.
        Returns the card's value:
        e.g. 2 for 2, 3 for 3, 11 for J, 14 for A etc..
        """
        return self._value

    @property
    def high_card_points(self):
        """
        Return the high card points for the hand.
        e.g. A=4, K=3, Q=2, J=1, else zero
        """
        return self._high_card_points
