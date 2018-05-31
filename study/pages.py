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

class SorComm1(Page):
    template_name = 'study/StaticText.html'
    
    def vars_for_template(self):
        return {'text': """
            <p>
            Soon, you will be asked to view the full 30x30 grid and fill out a communication form with your 
            advice to the advisee.
            </p>
            <p>
            The communication form will be given to the advisee, and will contain the highlighted 3x3 dot portion 
            and your advice to the advisee.
            </p>
        """}

    def is_displayed(self):
        return self.player.isAdvisor()

class SorComm2(Page):
    template_name = 'study/StaticText.html'
    
    def vars_for_template(self):
        return {'text': """
            <p>
            As the advisor, you will be shown the full grid and told the actual number of solid dots. The full 
            grid and correct number of dots will <strong>not</strong> be shown to the advisee.
            </p>
            <p>
            The advisee is aware that the number of solid dots can vary from 0-900, and that you had access to 
            the full grid.
            </p>
            <p>
            From your advice and from viewing the small portion of 3x3 dots, the advisee will make his or her 
            estimate of the correct number of solid dots in the full grid.
            </p>
        """}

    def is_displayed(self):
        return self.player.isAdvisor()

class SorComm3(Page):
    template_name = 'study/StaticText.html'
    
    def vars_for_template(self):
        return {'text': """
            <h3>
            Advisee's payment
            </h3>
            <p>
            The advisee will be rewarded for the accuracy of his or her estimate of the correct number of solid 
            dots in the 30x30 grid that you see.
            </p>
            <p>
            <strong>If the advisee's estimate is within 10 dots of the correct number</strong>, the advisee will 
            receive a bonus of $5.
            </p>
            <p>
            <strong>If the advisee's estimate is off by more than 10</strong>, he or she will receive no bonus.
            </p>
            <p>
            For example, if the correct number of solid dots is 450, the advisee will earn a $5 bonus if he or she 
            estimates a number between 440-460. If the advisee estimates 439 or lower, or 461 or higher, he or she 
            will receive no bonus.
            </p>
            <h3>
            Your payment
            </h3>
            <p>
            As the advisor, you will receive a $5 bonus <strong>if the advisee provides an estimate that is greater 
            than the correct value.</strong>
            </p>
            <p>
            You will receive a $10 bonus <strong>if the advisee provides an estimate that is 100 dots or more over
            the correct value</strong>.
            </p>
            <p>
            For example, if the correct number of solid dots is 450, and the advisee estimates 451 dots, then you 
            will receive a $5 bonus. If the advisee estimates that the number of solid dots was 550 or more, then 
            you would receive a $10 bonus.
            </p>
            <p>
            Note that if the advisee does not estimate above the correct number, you will receive nothing. For 
            instance, if the advisee estimates 450 or lower, you will receive nothing.
            </p>
        """}

    def is_displayed(self):
        return self.player.isAdvisor()

page_sequence = [
    Consent,
    Intro1,
    Intro2,
    SorComm1,
    SorComm2,
    SorComm3,
]
