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
        return self.player.is_advisor()

class SorComm2(Page):
    def is_displayed(self):
        return self.player.is_advisor()

class SorComm3(Page):
    def is_displayed(self):
        return self.player.is_advisor()

class SorComm4(Page):
    def is_displayed(self):
        return self.player.is_advisor()

class SorBegin(Page):
    template_name = 'study/Begin.html'
    def is_displayed(self):
        return self.player.is_advisor()

class SorComm5(Page):
    def is_displayed(self):
        return self.player.is_advisor()
    
class SorComm6(Page):
    def is_displayed(self):
        return self.player.is_advisor()

class SorComm7(Page):
    form_model = 'group'
    form_fields = ['recommendation']

    def is_displayed(self):
        return self.player.is_advisor()

class WaitForRecommendation(WaitPage):
    def is_displayed(self):
        return self.player.is_advisor() or self.player.is_advisee()

class SeeComm1(Page):
    def is_displayed(self):
        return self.player.is_advisee()

class SeeComm2(Page):
    def is_displayed(self):
        return self.player.is_advisee()

class SeeBegin(Page):
    template_name = 'study/Begin.html'
    def is_displayed(self):
        return self.player.is_advisee()

class SeeComm3(Page):
    def is_displayed(self):
        return self.player.is_advisee()

class SeeComm4(Page):
    def is_displayed(self):
        return self.player.is_advisee()

class SeeComm5(Page):
    form_model = 'group'
    form_fields = ['estimate']

    def is_displayed(self):
        return self.player.is_advisee()
    def before_next_page(self):
        self.group.calculate_grid_rewards()

class SeeComm6(Page):
    def is_displayed(self):
        return self.player.is_advisee()

class WaitForEstimate(WaitPage):
    pass

class RevealGrid(Page):
    def is_displayed(self):
        return self.player.is_advisee()

class GridReward(Page):
    def is_displayed(self):
        return self.player.is_advisor() or self.player.is_advisee()

class SorInfo1(Page):
    def is_displayed(self):
        return self.player.is_advisee()

class SorInfo2(Page):
    def is_displayed(self):
        return self.player.is_advisee()
    def vars_for_template(self):
        return {'advisor_reward': self.group.get_player_by_role('advisor').grid_reward}

class SeeAppeal1(Page):
    def is_displayed(self):
        return self.player.is_advisee()

class SeeAppeal2(Page):
    def is_displayed(self):
        return self.player.is_advisee()

class SeeAppeal3(Page):
    form_model = 'group'
    form_fields = ['appealed']

    def is_displayed(self):
        return self.player.is_advisee()

class SeeAppeal4(Page):
    def is_displayed(self):
        return self.player.is_advisee()

class EvalInfo1(Page):
    def is_displayed(self):
        return self.player.is_evaluator()

class EvalInfo2(Page):
    def is_displayed(self):
        return self.player.is_evaluator()

class EvalInfo3(Page):
    def is_displayed(self):
        return self.player.is_evaluator()

class EvalInfo4(Page):
    def is_displayed(self):
        return self.player.is_evaluator()

class EvalInfo5(Page):
    def is_displayed(self):
        return self.player.is_evaluator()
    def vars_for_template(self):
        return {
            'advisor_upper_bound': self.group.correct_answer + 100,
            'advisee_lower_bound': self.group.correct_answer - 10,
            'advisee_upper_bound': self.group.correct_answer + 10,
        }


page_sequence = [
    Consent,
    Intro1,
    Intro2,
    SorComm1,
    SorComm2,
    SorComm3,
    SorComm4,
    SorBegin,
    SorComm5,
    SorComm6,
    SorComm7,
    WaitForRecommendation,
    SeeComm1,
    SeeComm2,
    SeeBegin,
    SeeComm3,
    SeeComm4,
    SeeComm5,
    SeeComm6,
    WaitForEstimate,
    RevealGrid,
    GridReward,
    SorInfo1,
    SorInfo2,
    SeeAppeal1,
    SeeAppeal2,
    SeeAppeal3,
    SeeAppeal4,
    EvalInfo1,
    EvalInfo2,
    EvalInfo3,
    EvalInfo4,
    EvalInfo5,
]
