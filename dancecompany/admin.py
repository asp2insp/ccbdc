from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from simple_history.admin import SimpleHistoryAdmin
from models import *

class ClassAdmin(admin.ModelAdmin):
	pass

class TrainingAdmin(admin.ModelAdmin):
	pass

class ContributionAdmin(admin.ModelAdmin):
	pass

class RoutineAdmin(admin.ModelAdmin):
	pass

class DancerInline(admin.StackedInline):
	model = Dancer
	max_num = 1
	can_delete = False

class UserAdmin(AuthUserAdmin):
	inlines = [DancerInline]
	list_display = ('username', 'first_name', 'last_name')

	def recordGroupHistory(self, obj, gFrom, gTo):
		record = GroupChangeHistory()
		record.from_group = gFrom
		record.to_group = gTo
		record.save()
		obj.dancer.group_history.add(record)
	"""
	def save_model(self, request, obj, form, change):
		#if 'groups' in form.changed_data:
		old_instance = User.objects.get(id=obj.id)
		old_groups = set(old_instance.groups.all())
		new_groups = set() #set(obj.groups.all())
		groups_added = [x for x in new_groups if not x in old_groups]
		groups_removed = [x for x in old_groups if not x in new_groups]

		if (len(groups_added) is 1 and len(groups_removed) is 1):
			self.recordGroupHistory(obj, groups_removed[0], groups_added[0])
		else:
			for group in groups_removed:
				self.recordGroupHistory(obj, group, None)
			for group in groups_added:
				self.recordGroupHistory(obj, None, group)

		super(AuthUserAdmin, self).save_model(request, obj, form, change)
	"""

class EventAdmin(admin.ModelAdmin):
	pass

class PartnershipAdmin(admin.ModelAdmin):
	pass


admin.site.register(Class, ClassAdmin)
admin.site.register(Training, TrainingAdmin)
admin.site.register(Contribution, ContributionAdmin)
admin.site.register(Routine, RoutineAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Partnership, PartnershipAdmin)
# unregister old user admin
admin.site.unregister(User)
# register new user admin
admin.site.register(User, UserAdmin)
