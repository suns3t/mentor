from django.db import models

# Create your models here.
class Counter(models.Model):
	url_id = models.AutoField(primary_key=True)

	# Url of the link that will be redirect to
	# unique_for_date mean Django wouldn't allow the entry of two records
	# with the same url and date
	url = models.CharField(max_length=100, blank=False)	
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'counter'
		