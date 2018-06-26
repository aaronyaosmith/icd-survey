import os, random, re
from django.contrib.staticfiles.templatetags.staticfiles import static
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
    estimator_bonus = c(5) # received if estimate within 10 of answer
    advisor_bonus = c(5) # received if estimate > answer
    advisor_big_bonus = c(10) # received if estimate >= answer + 100
    appeal_reward = c(5) # given to estimator on appeal win
    appeal_reward_split = appeal_reward / 2 # given to both estimator and advisor if appeal lost or no appeal
    appeal_cost = c(1) # cost of appeal to estimator

class Subsession(BaseSubsession):
    def creating_session(self):
        # randomize players in groups, then assign disclosure/non-disclosure randomly to groups
        self.group_randomly()
        for group in self.get_groups():
            group.disclosure = random.choice([True, False])
            group.choose_grid()

class Group(BaseGroup):

    def shuffle_choices(choices):
        random.shuffle(choices)
        return choices

    disclosure = models.BooleanField()
    appealed = models.BooleanField(
        label="Would you like to send the case to the judge?",
        choices=shuffle_choices([
            [True, "Yes"],
            [False, "No"]
        ]),
        widget=widgets.RadioSelect
    ) # did estimator appeal?
    appeal_granted = models.BooleanField(
        label="As judge, I determine that the "+str(Constants.appeal_reward)+" bonus shall be awarded as follows:", 
        choices=shuffle_choices([
            [False, "The estimator and advisor shall both receive "+str(Constants.appeal_reward_split)+"."],
            [True, "The estimator shall receive "+str(Constants.appeal_reward)+
                " and the advisor shall receive nothing."],
        ]), 
        widget=widgets.RadioSelect
    )
    recommendation = models.IntegerField(
        min=0,
        max=900,
    )
    estimate = models.IntegerField(
        min=0,
        max=900,
    )

    grid_number = models.IntegerField()
    correct_answer = models.IntegerField()
    grid_path = models.StringField()
    small_grid_path = models.StringField()
    
    example_grid_number = models.IntegerField()
    example_grid_path = models.StringField()
    example_small_grid_path = models.StringField()


    # Likert scale questions
    e1 = make_Likert_agreement("I blame myself for my guess.")
    e2 = make_Likert_agreement("I blame my advisor for my guess.")
    e3 = make_Likert_agreement("I have a legitimate grievance against my advisor.")
    e4 = make_Likert_agreement("I have a strong case if I chose to pursue an appeal.")
    e5 = make_Likert_agreement("I believe that others would rule in my favor on an appeal.")
    e6 = make_Likert_agreement("My advisor treated me fairly.")
    e7 = make_Likert_agreement("I was mistreated by my advisor.")
    e8 = make_Likert_agreement("I deserve to receive the full bonus of "+str(Constants.appeal_reward)+".")
    e9 = make_Likert_agreement("My advisor does not deserve to receive "+str(Constants.appeal_reward_split)+
            " of the bonus.")
    j1 = make_Likert_agreement("I blame the estimator for his/her estimate.")
    j2 = make_Likert_agreement("I blame the advisor for the estimator's estimate.")
    j3 = make_Likert_agreement("The estimator has a legitimate grievance against the advisor.")
    j4 = make_Likert_agreement("The estimator has a strong case if he/she chooses to pursue an appeal.")
    j5 = make_Likert_agreement("I believe that others would rule in the estimator's favor on an appeal.")
    j6 = make_Likert_agreement("The advisor treated the estimator fairly.")
    j7 = make_Likert_agreement("The estimator was mistreated by the advisor.")
    j8 = make_Likert_agreement("The estimator deserves to receive the full bonus of "+str(Constants.appeal_reward)+".")
    j9 = make_Likert_agreement("The advisor does not deserve to receive "+str(Constants.appeal_reward_split)+
            " of the bonus.")
    a1 = make_Likert_agreement("I blame the estimator for his/her estimate.")
    a2 = make_Likert_agreement("I blame myself, the advisor, for the estimator's estimate.")
    a3 = make_Likert_agreement("The estimator has a legitimate grievance against me, the advisor.")
    a4 = make_Likert_agreement("The estimator has a strong case if he/she chooses to pursue an appeal.")
    a5 = make_Likert_agreement("I believe that others would rule in the estimator's favor on an appeal.")
    a6 = make_Likert_agreement("I, the advisor treated the estimator fairly.")
    a7 = make_Likert_agreement("The estimator was mistreated by me, the advisor.")
    a8 = make_Likert_agreement("The estimator deserves to receive the full bonus of "+str(Constants.appeal_reward)+".")
    a9 = make_Likert_agreement("I, the advisor, do not deserve to receive "+str(Constants.appeal_reward_split)+
            "of the bonus.")

    # Calculates rewards based on the advisor's recommendation and estimator's estimate, then stores them per player
    # in grid_reward.
    def calculate_grid_rewards(self):
        advisor = self.get_player_by_role('advisor')
        estimator = self.get_player_by_role('estimator')

        # advisor reward
        if self.estimate >= (self.correct_answer + 100):
            advisor.grid_reward = Constants.advisor_big_bonus
        elif self.estimate > self.correct_answer:
            advisor.grid_reward = Constants.advisor_bonus
        else:
            advisor.grid_reward = c(0)

        # estimator reward
        if self.estimate >= (self.correct_answer - 10) and self.estimate <= (self.correct_answer + 10):
            estimator.grid_reward = Constants.estimator_bonus
        else:
            estimator.grid_reward = c(0)


    # Chooses a grid. Will choose a random grid-3x3_grid pair based on what is in the directory. Files must be named
    # in this format: gridX_N.svg and small_gridX.svg, where X is a unique number per grid-3x3_grid pair, and N is 
    # the number of filled in dots in the entire grid.
    # Will assign values to group variables: grid_number, correct_answer, grid_path, small_grid_path.
    def choose_grid(self):
        static_dir = './study/static/study'
        static_files = os.listdir(static_dir)
        grid_choices = list(filter(lambda x: re.match("grid[0-9]*_[0-9]*\.svg", x), static_files))

        random.shuffle(grid_choices)

        self.grid_path = 'study/' + grid_choices.pop()
        self.grid_number = int(re.search("grid([0-9]*)_[0-9]*\.svg", self.grid_path).group(1))
        self.correct_answer = int(re.search("grid[0-9]*_([0-9]*)\.svg", self.grid_path).group(1))
        self.small_grid_path = 'study/small_grid' + str(self.grid_number) + '.svg'

        self.example_grid_path = 'study/' + grid_choices.pop()
        self.example_grid_number = int(re.search("grid([0-9]*)_[0-9]*\.svg", self.grid_path).group(1))
        self.example_small_grid_path = 'study/small_grid' + str(self.example_grid_number) + '.svg'



class Player(BasePlayer):
    grid_reward = models.CurrencyField(initial=c(0))
    entered_email = models.BooleanField()
    email = models.StringField(
        label="Please provide your email address. We will send your payment as an Amazon.com gift card to this "+
            "email address within five business days.",
        blank=True,
        initial=""
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
        label="What is your age?",
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
  
    # Manipulation checks
    m1 = models.BooleanField(
        label="In the dots-estimation task, the advisor would get a bonus if the estimator overestimated the true number of "
            + "solid dots.",
        widget=widgets.RadioSelect
    )
    m2 = models.BooleanField(
        label="In the dots-estimation task, the estimator would get a bonus if they were within 10 dots of the true number of " 
            + "solid dots.",
        widget=widgets.RadioSelect
    )
    m3 = models.BooleanField(
        label="In the dots-estimation task, the estimator was informed that the advisor would make more money if the estimator overestimated "
            + "the true number of solid dots.",
        widget=widgets.RadioSelect
    )
   
    comment = models.LongStringField(label="Do you have any comments for the researchers? (Optional)", blank=True)


    # define group IDs such that the "advisor" role corresponds to ID==1, "estimator" to ID==2, "judge/judge"
    # to ID==3. Use player.role() to retrieve this role.
    def role(self):
        if self.id_in_group == 1:
            return 'advisor'
        elif self.id_in_group == 2:
            return 'estimator'
        elif self.id_in_group == 3:
            return 'judge'

    def is_advisor(self):
        return self.id_in_group == 1
    def is_estimator(self):
        return self.id_in_group == 2
    def is_judge(self):
        return self.id_in_group == 3

    # Assigns rewards to players based on initially calculated grid estimation rewards and appeal results.
    def assign_rewards(self):
        self.payoff = Constants.base_reward + self.grid_reward
        
        if self.is_advisor():
            if not (self.group.appealed and self.group.appeal_granted):
                self.payoff += Constants.appeal_reward_split

        if self.is_estimator():
            if self.group.appealed:
                self.payoff -= Constants.appeal_cost

            if self.group.appealed and self.group.appeal_granted:
                self.payoff += Constants.appeal_reward
            else:
                self.payoff += Constants.appeal_reward_split
     
