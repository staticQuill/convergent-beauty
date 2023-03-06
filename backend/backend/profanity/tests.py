from django.test import TestCase
from .extras import ProfanityFilter

pf = ProfanityFilter()

class TestUnspaced(TestCase):
    def test_hidden_profanity(self):
        bad_word = "fillerfuckdickfiller"
        self.assertTrue(pf.is_profane_nospace(bad_word))

    def test_false_positive(self):
        good_word = "basement"
        self.assertFalse(pf.is_profane_nospace(good_word))

    def test_half_false_positive(self):
        bad_word = "nosemenhere"
        self.assertTrue(pf.is_profane_nospace(bad_word))
