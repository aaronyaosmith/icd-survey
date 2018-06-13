import random
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Aaron Yao-Smith'

doc = """
Incentive Compatible Disclosure Study
"""

def make_Likert_agreement(label):
    return models.IntegerField(
        choices=[
            [7, "Strongly agree"],
            [6, "Agree"],
            [5, "Somewhat agree"],
            [4, "Neither agree nor disagree"],
            [3, "Somewhat disagree"],
            [2, "Disagree"],
            [1, "Strongly disagree"]
        ],
        label=label,
        widget=widgets.RadioSelect
    )

class Constants(BaseConstants):
    name_in_url = 'study'
    players_per_group = 3
    num_rounds = 1
    base_reward = c(5) # base reward for completing the survey
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
    appealed = models.BooleanField(
        label="Would you like to send the case to the judge?",
        widget=widgets.RadioSelect
    ) # did advisee appeal?
    appeal_granted = models.BooleanField(
        label="As judge, I determine that the "+str(Constants.appeal_reward)+" bonus shall be awarded as follows:", 
        choices=[
            [False, "The advisee and advisor shall both receive "+str(Constants.appeal_reward_split)+"."],
            [True, "The advisee shall receive "+str(Constants.appeal_reward)+
                " and the advisor shall receive nothing."],
        ], 
        widget=widgets.RadioSelect
    )
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

    # Likert scale questions
    a1 = make_Likert_agreement("I blame myself for my guess.")
    a2 = make_Likert_agreement("I blame my advisor for my guess.")
    a3 = make_Likert_agreement("I have a legitimate grievance against my advisor.")
    a4 = make_Likert_agreement("I have a strong case if I chose to pursue an appeal.")
    a5 = make_Likert_agreement("I believe that others would rule in my favor on an appeal.")
    a6 = make_Likert_agreement("My advisor treated me fairly.")
    a7 = make_Likert_agreement("I was mistreated by my advisor.")
    a8 = make_Likert_agreement("I deserve to receive the full bonus of "+str(Constants.appeal_reward)+".")
    a9 = make_Likert_agreement("My advisor does not deserve to receive "+str(Constants.appeal_reward_split)+
            " of the bonus.")
    e1 = make_Likert_agreement("I blame the advisee for her estimate.")
    e2 = make_Likert_agreement("I blame the advisor for the advisee's estimate.")
    e3 = make_Likert_agreement("The advisee has a legitimate grievance against the advisor.")
    e4 = make_Likert_agreement("The advisee has a strong case if she chooses to pursue an appeal.")
    e5 = make_Likert_agreement("I believe that others would rule in the advisee's favor on an appeal.")
    e6 = make_Likert_agreement("The advisor treated the advisee fairly.")
    e7 = make_Likert_agreement("The advisee was mistreated by the advisor.")
    e8 = make_Likert_agreement("The advisee deserves to receive the full bonus of "+str(Constants.appeal_reward)+".")
    e9 = make_Likert_agreement("The advisor does not deserve to receive "+str(Constants.appeal_reward_split)+
            " of the bonus.")
   
    # Manipulation checks
    m1 = models.BooleanField(
        label="I make more money if the advisee overestimates the correct number of dots.",
        widget=widgets.RadioSelect
    )
    m2 = models.BooleanField(
        label="The advisee is informed that I make more money if he or she overestimates the true number of "+
           "solid dots.",
        widget=widgets.RadioSelect
    )

       
                       
        

class Player(BasePlayer):
    grid_reward = models.CurrencyField(initial=c(0))
    email = models.StringField(
        label="Please provide your email address. We will send your payment as an Amazon.com gift card to this "+
            "email address within five business days."
    )

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

    # Demographic questions
    d1 = models.IntegerField(
        label="What is your gender?",
        choices=[
            [1, 'Male'],
            [2, 'Female']
        ],
        widget=widgets.RadioSelect,
        blank=True
    )
    d2 = models.IntegerField(
        label="How old are you, in years?",
        min=18,
        max=130,
        blank=True
    )
    d3 = models.IntegerField(
        label="What is your race?",
        choices=[
            [1, 'White'],
            [2, 'Black, African-American'],
            [3, 'American Indian or Alaska Native'],
            [4, 'Asian or Asian-American'],
            [5, 'Pacific Islander'],
            [6, 'Some other race']
        ],
        widget=widgets.RadioSelect,
        blank=True
    )
    d4 = models.IntegerField(
        label="Please indicate the highest level of education completed.",
        choices=[
            [1, 'Grammar school'],
            [2, 'High school or equivalent'],
            [3, 'Vocational/technical school (2 year)'],
            [4, 'Some college'],
            [5, 'College graduate (4 year)'],
            [6, 'Master\'s degree (MS, etc.)'],
            [7, 'Doctoral degree (PhD, etc.)'],
            [8, 'Professional degree (MD, JD, etc.)'],
            [9, 'Other']
        ],
        widget=widgets.RadioSelect,
        blank=True
    )
    d5 = models.IntegerField(
        label="Please indicate your current household income in U.S. dollars",
        choices=[
            [1, 'Under $10,000'],
            [2, '$10,000 - $19,999'],
            [3, '$20,000 - $29,999'],
            [4, '$30,000 - $39,999'],
            [5, '$40,000 - $49,999'],
            [6, '$50,000 - $74,999'],
            [7, '$75,000 - $99,999'],
            [8, '$100,000 - $150,000'],
            [9, 'Over $150,000']
        ],
        widget=widgets.RadioSelect,
        blank=True
    )
    
    comment = models.LongStringField(label="Do you have any comments for the researchers? (Optional)", blank=True)


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

    # Calculates rewards based on the advisor's recommendation and advisee's estimate, then stores them per player
    # in grid_reward.
    def calculate_grid_rewards(self):
        if self.is_advisor(): 
            if self.group.estimate >= (self.group.correct_answer + 100):
                self.grid_reward = Constants.advisor_big_bonus
            elif self.group.estimate > self.group.correct_answer:
                self.grid_reward = Constants.advisor_bonus
            else:
                self.grid_reward = c(0)

        elif self.is_advisee():
            if (
                    self.group.estimate >= (self.group.correct_answer - 10) 
                    and self.group.estimate <= (self.group.correct_answer + 10)
            ):
                self.grid_reward = Constants.advisee_bonus
            else:
                self.grid_reward = c(0)

    # Assigns rewards to players based on initially calculated grid estimation rewards and appeal results.
    def assign_rewards(self):
        self.payoff = Constants.base_reward + self.grid_reward
        
        if self.is_advisor():
            if not (self.group.appealed and self.group.appeal_granted):
                self.payoff += Constants.appeal_reward_split

        if self.is_advisee():
            if self.group.appealed:
                self.payoff -= Constants.appeal_cost

            if self.group.appealed and self.group.appeal_granted:
                self.payoff += Constants.appeal_reward
            else:
                self.payoff += Constants.appeal_reward_split
     
