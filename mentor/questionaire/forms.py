from django import forms
from mentor.questionaire.models import Questionaire
from datetime import date 

class USPhoneNumberMultiWidget(forms.MultiWidget):
    """
    A Widget that splits US Phone number input into three  boxes.
    """
    def __init__(self,attrs=None):
        widgets = (
            forms.TextInput(attrs={'size':'3','maxlength':'3', 'class':'phone form-control-noblock input-sm'}),
            forms.TextInput(attrs={'size':'3','maxlength':'3', 'class':'phone form-control-noblock input-sm'}),
            forms.TextInput(attrs={'size':'4','maxlength':'4', 'class':'phone form-control-noblock input-sm'}),
        )
        super(USPhoneNumberMultiWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value[0:3],value[3:6],value[6:10]]
        return [None,None,None]

    def value_from_datadict(self, data, files, name):
        values = super(USPhoneNumberMultiWidget, self).value_from_datadict(data, files, name)
        return u'%s%s%s' % tuple(values)

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

    YN_CHOICES = (
        ('Y','Yes'),
        ('N','No')
    )
    name = forms.CharField(label='Name',error_messages={'required':'Please enter your name'})

    student_ID = forms.DecimalField(label='Student ID# (optional)', required=False, max_digits=9, decimal_places=0)

    student_name = forms.CharField(label='Name of student',required=False)
    mentor_name = forms.CharField(label='Name of mentor',required=False)
    
    UNST_course = forms.ChoiceField(
        choices=UNST_CHOICES,
        label='What University Studies course are you enrolled in?')

    type_of_course = forms.ChoiceField(
        choices=COURSE_TYPE_CHOICES,
        label='Is your UNST course in-person or online or hybrid?')

    identity = forms.ChoiceField(
        choices=IDENTITY_CHOICES,
        label='Are you a student or a mentor?',
        widget=forms.RadioSelect())
    
    on_behalf_of_student = forms.ChoiceField(
        choices=YN_CHOICES,
        label='Are you filling out this form on behalf of student?',
        widget=forms.RadioSelect(),
        required=False)
    primary_concern = forms.CharField(
        widget=forms.widgets.Textarea(attrs={'rows':'3'}),
        label='What are your primary concerns?',)
    
    step_taken = forms.CharField(
        widget=forms.widgets.Textarea(attrs={'rows':'3'}),
        label="Please share the steps you've taken to address these concerns (if any)",
        required=False,
    )

    when_take_step = forms.ChoiceField(
        choices=WHEN_CHOICES,
        label='When did you take these steps?'
    )
    
    support_from_MAPS = forms.CharField(
        widget=forms.widgets.Textarea(attrs={'rows':'3'}),
        label="What kind of support did you receive from MAPS before?",
        required=False,
    )
    follow_up_email = forms.EmailField(
        widget=forms.widgets.EmailInput,
        label='Email',
        required=False)

    follow_up_phone = forms.DecimalField(
        widget = USPhoneNumberMultiWidget,
        error_messages={'required':'Please insert an appropriate phone number'},
        label='Phone number',
        required=False)

    follow_up_appointment = forms.DateField(
        label='Face-to-face meeting in',
        required=False)
    
    def __init__(self, *args, **kwargs):
        super(QuestionaireForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control input-sm'  
        self.fields['student_ID'].widget.attrs['class'] = 'form-control input-sm'
        self.fields['student_name'].widget.attrs['class'] = 'form-control input-sm'

        self.fields['mentor_name'].widget.attrs['class'] = 'form-control input-sm'

        self.fields['when_take_step'].widget.attrs['class'] = 'form-control input-sm'
        self.fields['UNST_course'].widget.attrs['class'] = 'form-control input-sm'
        self.fields['type_of_course'].widget.attrs['class'] = 'form-control input-sm'

        self.fields['primary_concern'].widget.attrs['class'] ='form-control input-sm'
        self.fields['step_taken'].widget.attrs['class'] ='form-control input-sm'
        self.fields['when_take_step'].widget.attrs['class'] ='form-control input-sm'
        self.fields['support_from_MAPS'].widget.attrs['class'] ='form-control input-sm'

        self.fields['follow_up_email'].widget.attrs['class'] ='form-control input-sm'
        self.fields['follow_up_appointment'].widget.attrs['class'] ='form-control input-sm'

    def save(self, user, *args, **kwargs):
        """
        Overide the save method to input username automatically from
        CAS authentication information
        """

        self.instance.user = user
        post = super(QuestionaireForm, self).save(*args, **kwargs)
        post.sendNotification() 

    def clean_on_behalf_of_student(self):
        on_behalf_of_student = self.cleaned_data.get("on_behalf_of_student")
        identity = self.cleaned_data.get("identity")

        if (identity == 'MT') and (not on_behalf_of_student):
            raise form.ValidationError('Please answer this question')

        if (identity == 'ST'):
            on_behalf_of_student = ''

        return on_behalf_of_student

    def clean_follow_up_appointment(self):
        #cleaned_data = super(QuestionaireForm, self).clean_follow_up_appointment()

        appointment = self.cleaned_data.get("follow_up_appointment")
        
        if appointment:
            if appointment < date.today():
                raise forms.ValidationError('Appointment date should be in the future')

        return appointment

    def clean_mentor_name(self):
        mentor_name = self.cleaned_data.get("mentor_name")
        identity = self.cleaned_data.get("identity")

        # Mentor name is required when student fill out the form.
        if (identity == 'ST') and (mentor_name == ''):
            raise forms.ValidationError('Please enter mentor name')

        return mentor_name

    def clean_student_name(self):
        student_name = self.cleaned_data.get("student_name")
        on_behalf_of_student = self.cleaned_data.get("on_behalf_of_student")
        identity = self.cleaned_data.get("identity")

        # Student name is required when mentor fills out the form on behalf of student.
        if (identity == 'MT') and (on_behalf_of_student == 'Y') and (student_name == ''):
            raise forms.ValidationError('Please enter student name')

        return student_name


    def clean(self):
        cleaned_data = super(QuestionaireForm, self).clean()

        name = cleaned_data.get("name")
        student_name = cleaned_data.get("student_name")
        mentor_name = cleaned_data.get("mentor_name")
        on_behalf_of_student = cleaned_data.get("on_behalf_of_student")
        identity = cleaned_data.get("identity")

        if identity == 'ST':
            # Student is filling out the form, pop out name and assign that value to student_name
            cleaned_data.pop("name", None)
            cleaned_data["student_name"] = name
        
        elif identity == 'MT':
            # Mentor is filling out the form, pop out name and assign that value to mentor_name
            cleaned_data.pop("name", None)
            cleaned_data["mentor_name"] = name

        # Make sure that user enters at least one method of follow-up
        email = cleaned_data.get("follow_up_email")
        phone = cleaned_data.get("follow_up_phone")
        appointment = cleaned_data.get("follow_up_appointment")

        if not email and not appointment and not phone :
            raise forms.ValidationError('Fill at least one method to follow-up you')


        return cleaned_data
    class Meta:
        model = Questionaire 
        fields = (
            'identity',
            'on_behalf_of_student',
            'student_name',
            'student_ID',
            'mentor_name',
            'UNST_course',
            'type_of_course',
            'primary_concern',
            'step_taken',
            'when_take_step',
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
