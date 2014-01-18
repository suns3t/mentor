from django.contrib import admin
from mentor.counter.models import Counter 
# Register your models here.

class CounterAdmin(admin.ModelAdmin):

	# This changes CounterAdmin list form
	list_display = ('url','timestamp')
	list_filter = ['timestamp']

	date_hierarchy = 'timestamp'
	# This changes CounterAdmin detail form

admin.site.register(Counter, CounterAdmin)