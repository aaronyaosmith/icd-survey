from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

# These pages roughly follow the page divisions as specified in the Qualtrics survey.

class Consent(Page):

    form_model = 'player'
    form_fields = ['consent18', 'consentRead', 'consentWant']

    def error_message(self, values):
        print('values is', values)
        if values["consent18"] != True or values["consentRead"] != True or values["consentWant"] != True:
            return 'Sorry, but you are not eligible for this study.'

# "You will play the role of %role%."
class Intro1(Page):
    pass

class Intro2(Page):
    pass

page_sequence = [
    Consent,
    Intro1,
    Intro2,
]
