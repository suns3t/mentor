from django.db import models
from django import forms
from mentor.users.models import User
from django.conf import settings as SETTINGS

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class PrimaryConcernChoice(models.Model):
    """
    A choice table for primary concerns
    """
    choice_id = models.AutoField(primary_key=True)
    created_on = models.DateTimeField(auto_now_add=True)
    value = models.CharField(max_length=256, blank=False)

    def __unicode__(self):
        return self.value

class Questionaire(models.Model):
    questionaire_id = models.AutoField(primary_key=True)
    created_on = models.DateTimeField(auto_now_add=True)

    # User submited this form
    user = models.ForeignKey(User)

    # Questions
    student_name = models.CharField(max_length=30, blank=True)     # Student name
    student_ID = models.DecimalField(null=True,max_digits=9,decimal_places=0, blank=True)       # Student ID
    mentor_name = models.CharField(max_length=30, blank=True)      # Mentor name
    
    identity = models.CharField(max_length=2,blank=True)           # Are you mentor or student? 
    on_behalf_of_student = models.CharField(max_length=2, blank=True)     # Are you filling out this form on behalf of student?

    UNST_course = models.CharField(max_length=20, blank=True)       # What University Studies course are you enrolled in?
    type_of_course = models.CharField(max_length=20, blank=True)    # Is your UNST course in-person or online?
    
    primary_concern = models.ManyToManyField(PrimaryConcernChoice)  # What are your primary concerns?
    primary_concern_other = models.TextField(blank=True)            # Other concerns?
    step_taken = models.TextField(blank=True)                       # Please share the steps you've taken to address these concerns (if any)
    when_take_step = models.CharField(max_length=20,blank=True)                   # When did you take these steps? (Dropdown menu)
    support_from_MAPS = models.TextField(blank=True)                # What kind of support would be helpful from the MAPS team?
    
    contact_who = models.CharField(max_length=2, blank=True)        # Do you want us to contact student directly?
    follow_up_email = models.EmailField(null=True,blank=True)
    follow_up_phone = models.DecimalField(null=True,max_digits=10,decimal_places=0,blank=True)

    def __unicode__(self):
        concerns = ', '.join([str(concern.value) for concern in self.primary_concern.all() ])
        if self.primary_concern_other:
            concerns = concerns + ', ' + self.primary_concern_other

        if self.identity == 'ST':
            # Student filled the form for his/her problems
            return self.student_name + " - " + concerns
        elif self.identity == 'MT':
            if self.on_behalf_of_student == 'Y':
                # Mentor filled the form for student problems
                return self.student_name + " - " + concerns
            else:
                # Mentor filled the form for mentor problems
                return self.mentor_name + " - " + concerns


    def sendNotification(self):

        # Send a notification email to the person signed in
        to_user = self.user.username + '@' + SETTINGS.EMAIL_DOMAIN
        
        context_to_user = {
            "username" : self.user.username
        }

        context_to_psu_email_list = {
            "username" : self.user.username,
            "questionaire" : self,
        }

        # Send email to user
        text_content_to_user = render_to_string('questionaire/notification.txt', context_to_user)
        html_content_to_user = render_to_string('questionaire/notification.html', context_to_user)
        subject_to_user = "[MAPS Webform] Your response is submitted"

        msg_to_user = EmailMultiAlternatives(subject_to_user, text_content_to_user, SETTINGS.EMAIL_FROM, [to_user])
        msg_to_user.attach_alternative(html_content_to_user, "text/html")

        # Send email to PSU Email List
        text_content_psu_email_list = render_to_string('questionaire/notificationToPSU.txt', context_to_psu_email_list)
        html_content_psu_email_list = render_to_string('questionaire/notificationToPSU.html', context_to_psu_email_list)
        subject_to_psu_email_list = "[MAPS Webform] A MAPS Webform is submitted"

        msg = EmailMultiAlternatives(subject_to_psu_email_list, text_content_psu_email_list, SETTINGS.EMAIL_FROM, [SETTINGS.EMAIL_LIST] )
        msg.attach_alternative(html_content_psu_email_list, "text/html")
        return (msg.send() + msg_to_user.send())
    

    class Meta:
        db_table = 'questionaire'
        ordering = ['created_on']

class UserResponse(models.Model):
    """
    A User and response models
    """
    id = models.AutoField(primary_key=True)
    mentor_resolved = models.ForeignKey(User)
    response = models.ForeignKey(Questionaire)

    created_on = models.DateTimeField()
    status = models.BooleanField(default=False, blank=True) # status is used to indicate if the response is resolved by mentor 

    class Meta:
        db_table = 'user_response'