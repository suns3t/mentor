from django import forms
from mentor.questionaire.models import Questionaire
from datetime import date 
from captcha.fields import CaptchaField

class QuestionaireForm(forms.ModelForm):

    STUDENT = 'ST'
    MENTOR = 'MT'
    IDENTITY_CHOICES = (
        (STUDENT, 'Student'),
        (MENTOR, 'Mentor'),
    )

    UNST_CHOICES = (
        ('FRINQ','FRINQ (Freshman Inquiry)'),
        ('SINQ','SINQ (Sophomore Inquiry)')
    )

    COURSE_TYPE_CHOICES = (
        ('HB','Hybrid'),
        ('OL','Online'),
        ('IP','In-person')
    )
    
    WHEN_CHOICES = (
        ('Few days', 'In the past few days'),
        ('Last week', 'In the last week'),
        ('Last two weeks', 'In the last two weeks'),
        ('Last month', 'In the last month'),
        ('Over a month', 'Over a month ago'),
        ('Dont know', "Don't know/Other")
    )
    name = forms.CharField(label='Name',error_messages={'required':'Please enter your name'})
    student_ID = forms.DecimalField(label='Student ID# (optional)')
    student_name = forms.CharField(label='Name of student',
        error_messages={'required':'Please enter student name'})
    mentor_name = forms.CharField(label='Name of mentor',
        error_messages={'required':'Please enter mentor name'})
    
    UNST_course = forms.ChoiceField(
        choices=UNST_CHOICES,
        label='What University Studies course are you enrolled in?')

    type_of_course = forms.ChoiceField(
        choices=COURSE_TYPE_CHOICES,
        label='Is your UNST course in-person or online or hybrid?')

    identity = forms.ChoiceField(
        choices=IDENTITY_CHOICES,
        label='Are you a student or a mentor?')
    
    primary_concern = forms.CharField(
        widget=forms.widgets.Textarea,
        label='What are your primary concerns?',)
    
    step_taken = forms.CharField(
        widget=forms.widgets.Textarea,
        label="Please share the steps you've taken to address these concerns (if any)",
        required=False,
    )

    when_take_step = forms.ChoiceField(
        choices=WHEN_CHOICES,
        label='When did you take these steps?'
    )
    
    support_from_MAPS = forms.CharField(
        widget=forms.widgets.Textarea,
        label="What kind of support did you receive from MAPS before?",
        required=False,
    )
    follow_up_email = forms.EmailField(
        widget=forms.widgets.EmailInput,
        label='Email',
        required=False)
    follow_up_phone = forms.CharField(
        error_messages={'required':'Please insert an appropriate phone number'},
        label='Phone call',
        required=False)
    follow_up_appointment = forms.DateField(
        label='Face-to-face meeting in',
        required=False)

    captcha = CaptchaField(label='Verify Code', required=True)
    
    def save(self, user, *args, **kwargs):
        """
        Overide the save method to input username automatically from
        CAS authentication information
        """

        self.instance.user = user
        post = super(QuestionaireForm, self).save(*args, **kwargs)
        post.sendNotification() 

    def clean_follow_up_appointment(self):
        #cleaned_data = super(QuestionaireForm, self).clean_follow_up_appointment()

        appointment = self.cleaned_data.get("follow_up_appointment")
        
        if appointment:
            if appointment < date.today():
                raise forms.ValidationError('Appointment date should be in the future')

        return appointment

    def clean(self):
        cleaned_data = super(QuestionaireForm, self).clean()

        # Make sure that user enters at least one method of follow-up
        email = cleaned_data.get("follow_up_email")
        phone = cleaned_data.get("follow_up_phone")
        appointment = cleaned_data.get("follow_up_appointment")

        # import pdb; pdb.set_trace();
        if not email and not appointment and not phone :
            raise forms.ValidationError('Fill at least one method to follow-up you')

        return cleaned_data
    class Meta:
        model = Questionaire 
        fields = (
            'student_name',
            'mentor_name',
            'identity',
            'primary_concern',
            'step_taken',
            'support_from_MAPS',
            'follow_up_email',
            'follow_up_phone',
            'follow_up_appointment',
        )

class DownloadResponseForm(forms.Form):

    start_date = forms.DateField(
        label="Start Date: ",
        required=True,
        )

    end_date = forms.DateField(
        label="End Date: ",
        required=True,
        )

    def clean(self):
        cleaned_data = super(DownloadResponseForm, self).clean()

        try:
            start_date = cleaned_data['start_date']
            end_date = cleaned_data['end_date']
        except KeyError:
            raise forms.ValidationError("Fill in the required dates.")
        

        if end_date < start_date:
            raise forms.ValidationError("End Date can't smaller then Start Date.")

        return cleaned_data