import random
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Aaron Yao-Smith'

doc = """
Incentive Compatible Disclosure Study
"""


class Constants(BaseConstants):
    name_in_url = 'study'
    players_per_group = 3
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        # randomize players in groups, then assign disclosure/non-disclosure randomly to groups
        self.group_randomly()
        for group in self.get_groups():
            group.disclosure = random.choice([True, False])

class Group(BaseGroup):
    disclosure = models.BooleanField()
    recommendation = models.IntegerField(
        min=0,
        max=900,
        widget=widgets.Slider(attrs={'step': '1'})
    )

class Player(BasePlayer):
    # define group IDs such that the "advisor" role corresponds to ID==1, "advisee" to ID==2, "judge/evaluator" to ID==3. Use player.role() to retrieve this role.
    def role(self):
        if self.id_in_group == 1:
            return 'advisor'
        elif self.id_in_group == 2:
            return 'advisee'
        elif self.id_in_group == 3:
            return 'evaluator'

    def isAdvisor(self):
        return self.id_in_group == 1
    def isAdvisee(self):
        return self.id_in_group == 2
    def isEvaluator(self):
        return self.id_in_group == 3

    consent18 = models.BooleanField(
        label="I am age 18 or older",
        widget=widgets.RadioSelect
        )
    consentRead = models.BooleanField(
        label="I have read and understand the above information",
        widget=widgets.RadioSelect
        )
    consentWant = models.BooleanField(
        label="I want to participate in this research and continue with this study",
        widget=widgets.RadioSelect
        )
 
