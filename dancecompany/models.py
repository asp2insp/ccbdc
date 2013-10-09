from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from simple_history.models import HistoricalRecords
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

LEVEL_CHOICES = (
	('BR', 'Bronze'),
	('SL', 'Silver'),
	('GD', 'Gold'),
	('NV', 'Novice'),
	('PC', 'Pre-Champion'),
	('CH', 'Champion')
)

class AuditionDate(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	history = HistoricalRecords()

	date = models.DateTimeField('Date of Audition')
	auditioned_for = models.ForeignKey(Group, related_name='+')

	def __unicode__(self):
		return "%s for %s" % (self.date, self.auditioned_for)

class Class(models.Model):
	class Meta:
		verbose_name_plural = "Classes"
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	history = HistoricalRecords()

	title = models.CharField(max_length=200)
	style = models.CharField(max_length=2, choices=DANCE_STYLE_CHOICES)
	level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
	semester = models.CharField(max_length=2, choices=SEMESTER_CHOICES)
	year = models.IntegerField()

	def __unicode__(self):
		return self.title

class Training(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	history = HistoricalRecords()

	title = models.CharField(max_length=200)
	start_date = models.DateField('Start Date')
	end_date = models.DateField('End Date')
	Description = models.TextField()

	def __unicode__(self):
		return self.title

class Contribution(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	history = HistoricalRecords()

	date = models.DateField()
	hours = models.IntegerField(blank=True, null=True)
	dollars = models.IntegerField(blank=True, null=True)
	target_team = models.ForeignKey(Group, related_name='contributions')
	notes = models.TextField(blank=True)

	# Person relation through reverse foreign key relation

	approved = models.BooleanField(default=False)
	approved_by = models.ForeignKey('Dancer', related_name='approved_contributions')

class Routine(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	history = HistoricalRecords()

	title = models.CharField(max_length=200)
	style = models.CharField(max_length=2, choices=DANCE_STYLE_CHOICES)
	semester = models.CharField(max_length=2, choices=SEMESTER_CHOICES)
	year = models.IntegerField()
	music_url = models.URLField(blank=True)
	video_url = models.URLField(blank=True)
	facebook_group_url = models.URLField(blank=True)

	team = models.ForeignKey(Group, related_name='routines')

	def __unicode__(self):
		return self.title

class GroupChangeHistory(models.Model):
	class Meta:
		verbose_name_plural = "Group change histories"
	date = models.DateTimeField(auto_now_add=True, editable=True)
	from_group = models.ForeignKey(Group, related_name='+', null=True)
	to_group = models.ForeignKey(Group, related_name='+', null=True)
	# Person relation through reverse foreign key relation

	def __unicode__(self):
		return "%s -> %s" % (self.from_group, self.to_group)

class Dancer(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	history = HistoricalRecords()

	user = models.OneToOneField(User)
	phone = models.CharField(max_length=10, blank=True)
	twitter = models.CharField(max_length=100, blank=True)
	facebook_id = models.CharField(max_length=100, blank=True)
	gplus_id = models.CharField(max_length=100, blank=True)
	linkedin_id = models.CharField(max_length=100, blank=True)

	school = models.CharField(max_length=3, choices=SCHOOL_CHOICES)
	graduation_year = models.IntegerField(blank=True, null=True)
	role = models.CharField(max_length=1, choices=ROLE_CHOICES)
	status = models.CharField(max_length=2, choices=STATUS_CHOICES)
	level = models.CharField(max_length=2, choices=LEVEL_CHOICES, blank=True)

	weekly_hours = models.IntegerField(blank=True, null=True)
	coach = models.CharField(max_length=200, blank=True)

	interests = models.TextField(blank=True)
	items_checked_out = models.TextField(blank=True)
	leadership_position = models.CharField(max_length=200, blank=True)

	dues_paid = models.BooleanField(default=False)
	wants_contact = models.BooleanField(default=False)

	contributions = models.ManyToManyField(Contribution, related_name='contributor', blank=True)
	events_attended = models.ManyToManyField('Event', related_name='attendee', blank=True)
	audition_dates = models.ManyToManyField(AuditionDate, related_name='auditionee', blank=True)
	classes_taken = models.ManyToManyField(Class, related_name='student', blank=True)
	trainings_attended = models.ManyToManyField(Training, related_name='trainee', blank=True)
	group_history = models.ManyToManyField(GroupChangeHistory, related_name='group_history', blank=True)

	def __unicode__(self):
		return "%s %s" % (self.user.first_name, self.user.last_name)

class Event(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	history = HistoricalRecords()

	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	url = models.URLField(blank=True)
	tags = models.TextField(blank=True)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()

	organizers = models.ForeignKey(Group)
	rsvps = models.ManyToManyField(Dancer)
	routines = models.ManyToManyField(Routine, related_name='+')

	def __unicode__(self):
		return self.title


class Partnership(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	history = HistoricalRecords()

	weekly_hours = models.IntegerField(blank=True, null=True)
	style = models.CharField(max_length=2, choices=DANCE_STYLE_CHOICES)
	level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
	dancers = models.ManyToManyField(Dancer)

	def __unicode__(self):
		return ' and '.join(self.dancers.all())
