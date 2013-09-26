from django.db import models
from django.contrib.auth.models import Group, Permission, User

# Create your models here.

DANCE_STYLE_CHOICES = (
	('IS', 'International Standard'),
	('IL', 'International Latin'),
	('SC', 'Social'),
	('AR', 'American Rhythm'),
	('AS', 'American Smooth'),
	('OR', 'Other')
)

SCHOOL_CHOICES = (
	('HMC', 'Harvey Mudd'),
	('SCR', 'Scripps'),
	('POM', 'Pomona'),
	('PTZ', 'Pitzer'),
	('CMC', 'Claremont McKenna'),
	('CUC', 'Claremont University Consortium'),
	('COM', 'Local Community'),
	('ORT', 'Other')
)

SEMESTER_CHOICES = (
	('SP', 'Spring'),
	('SU', 'Summer'),
	('FA', 'Fall'),
	('WI', 'Winter')
)

ROLE_CHOICES = (
	('L', 'Lead'),
	('F', 'Follow')
)

STATUS_CHOICES = (
	#Current/Alumn(us/ae)/Abroad/LOA
	('CU', 'Current'),
	('AM', 'Alumni'),
	('AB', 'Abroad'),
	('LA', 'Leave of Absence')
)

class AuditionDate(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	date = models.DateTimeField('Date of Audition')
	auditioned_for = models.ForeignKey(Group, related_name='+')

class Class(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	title = models.CharField(max_length=200)
	style = models.CharField(max_length=2, choices=DANCE_STYLE_CHOICES)
	level = models.CharField(max_length=100)
	semester = models.CharField(max_length=2, choices=SEMESTER_CHOICES)
	year = models.IntegerField()

class Training(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	title = models.CharField(max_length=200)
	start_date = models.DateField('Start Date')
	end_date = models.DateField('End Date')
	Description = models.TextField()

class Contribution(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	date = models.DateField()
	hours = models.IntegerField(blank=True)
	dollars = models.IntegerField(blank=True)
	target_team = models.ForeignKey(Group, related_name='contributions')
	notes = models.TextField(blank=True)

	# Person relation through reverse foreign key relation

	approved = models.BooleanField(default=False)
	approved_by = models.ForeignKey('Dancer', related_name='approved_contributions')

class Routine(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	title = models.CharField(max_length=200)
	style = models.CharField(max_length=2, choices=DANCE_STYLE_CHOICES)
	semester = models.CharField(max_length=2, choices=SEMESTER_CHOICES)
	year = models.IntegerField()
	music_url = models.URLField(blank=True)
	video_url = models.URLField(blank=True)
	facebook_group_url = models.URLField(blank=True)

	team = models.ForeignKey(Group, related_name='routines')

class GroupChangeHistory(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	from_group = models.ForeignKey(Group, related_name='+', null=True)
	to_group = models.ForeignKey(Group, related_name='+', null=True)
	audition_date = models.ForeignKey(AuditionDate, related_name='+')
	
	# Person relation through reverse foreign key relation

class Dancer(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	user = models.OneToOneField(User)
	name = models.CharField(max_length=500)
	email = models.EmailField(blank=True)
	phone = models.CharField(max_length=10, blank=True)
	twitter = models.CharField(max_length=100, blank=True)
	facebook_id = models.CharField(max_length=100, blank=True)
	gplus_id = models.CharField(max_length=100, blank=True)
	linkedin_id = models.CharField(max_length=100, blank=True)

	school = models.CharField(max_length=3, choices=SCHOOL_CHOICES)
	graduation_year = models.IntegerField(blank=True)
	role = models.CharField(max_length=1, choices=ROLE_CHOICES)
	status = models.CharField(max_length=2, choices=STATUS_CHOICES)

	interests = models.TextField(blank=True)
	items_checked_out = models.TextField(blank=True)
	leadership_position = models.CharField(max_length=200)

	dues_paid = models.BooleanField(default=False)
	wants_contact = models.BooleanField(default=False)

	contributions = models.ManyToManyField(Contribution, related_name='contributor')
	events_attended = models.ManyToManyField('Event', related_name='attendee')
	audition_dates = models.ManyToManyField(AuditionDate, related_name='auditionee')
	classes_taken = models.ManyToManyField(Class, related_name='student')
	trainings_attended = models.ManyToManyField(Training, related_name='trainee')

class Event(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	url = models.URLField(blank=True)
	tags = models.TextField(blank=True)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()

	organizers = models.ForeignKey(Group)
	rsvps = models.ManyToManyField(Dancer)
	routines = models.ManyToManyField(Routine, related_name='+')

