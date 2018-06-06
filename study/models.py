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
    base_reward = c(10) # base reward for completing the survey
    advisee_bonus = c(5) # received if estimate within 10 of answer
    advisor_bonus = c(5) # received if estimate > answer
    advisor_big_bonus = c(10) # received if estimate >= answer + 100
    appeal_reward = c(5) # given to advisee on appeal win
    appeal_reward_split = appeal_reward / 2 # given to both advisee and advisor if appeal lost or no appeal
    appeal_cost = c(1) # cost of appeal to advisee

class Subsession(BaseSubsession):
    def creating_session(self):
        # randomize players in groups, then assign disclosure/non-disclosure randomly to groups
        self.group_randomly()
        for group in self.get_groups():
            group.disclosure = random.choice([True, False])

class Group(BaseGroup):
    disclosure = models.BooleanField()
    appealed =  models.BooleanField(
        label="Would you like to send the case to the judge?",
        widget=widgets.RadioSelect
        ) # did advisee appeal?
    correct_answer = models.IntegerField(initial=409)
    recommendation = models.IntegerField(
        min=0,
        max=900,
        initial=0,
        widget=widgets.Slider(attrs={'step': '1'})
    )
    estimate = models.IntegerField(
        min=0,
        max=900,
    )

    # Calculates rewards based on the advisor's recommendation and advisee's estimate, then stores them per player
    # in grid_reward.
    def calculate_grid_rewards(self):
        advisor = self.get_player_by_role('advisor')
        advisee = self.get_player_by_role('advisee')

        # advisor reward
        if self.estimate >= (self.correct_answer + 100):
            advisor.grid_reward = c(10)
        elif self.estimate > self.correct_answer:
            advisor.grid_reward = c(5)
        else:
            advisor.grid_reward = c(0)

        # advisee reward
        if self.estimate >= (self.correct_answer - 10) and self.estimate <= (self.correct_answer + 10):
            advisee.grid_reward = c(5)
        else:
            advisee.grid_reward = c(0)
        

class Player(BasePlayer):
    grid_reward = models.CurrencyField()

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

    # define group IDs such that the "advisor" role corresponds to ID==1, "advisee" to ID==2, "judge/evaluator"
    # to ID==3. Use player.role() to retrieve this role.
    def role(self):
        if self.id_in_group == 1:
            return 'advisor'
        elif self.id_in_group == 2:
            return 'advisee'
        elif self.id_in_group == 3:
            return 'evaluator'

    def is_advisor(self):
        return self.id_in_group == 1
    def is_advisee(self):
        return self.id_in_group == 2
    def is_evaluator(self):
        return self.id_in_group == 3

