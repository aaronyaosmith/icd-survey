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

# show EXAMPLE image based on role
class Intro2(Page):
    pass

# SorComm: Communication pages for the advisor
class SorComm1(Page):
    def is_displayed(self):
        return self.player.isAdvisor()

class SorComm2(Page):
    def is_displayed(self):
        return self.player.isAdvisor()

class SorComm3(Page):
    def is_displayed(self):
        return self.player.isAdvisor()

class SorComm4(Page):
    def is_displayed(self):
        return self.player.isAdvisor()

class SorComm5(Page):
    def is_displayed(self):
        return self.player.isAdvisor()
    
class SorComm6(Page):
    def is_displayed(self):
        return self.player.isAdvisor()

class SorComm7(Page):
    form_model = 'group'
    form_fields = ['recommendation']

    def is_displayed(self):
        return self.player.isAdvisor()



page_sequence = [
    Consent,
    Intro1,
    Intro2,
    SorComm1,
    SorComm2,
    SorComm3,
    SorComm4,
    SorComm5,
    SorComm6,
    SorComm7,
]
