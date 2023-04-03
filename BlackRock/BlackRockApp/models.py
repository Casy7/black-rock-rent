from django.db import models
from django.contrib.auth.models import User


class Equipment(models.Model):
	name = models.CharField(max_length=250, default='карабин')
	path = models.CharField(max_length=50, default='горное')
	unique = models.BooleanField(default=True)
	number = models.IntegerField(default=1, blank=True)
	price_per_day = models.IntegerField(default=0, blank=True)
	price = models.IntegerField(default=0, blank=True)
	price_for_members = models.IntegerField(default=0, blank=True)
	description = models.CharField(max_length=1000, default='', null=True)


class Contact(models.Model):
	name = models.CharField(max_length=250, default='Смерека')
	is_club_member = models.BooleanField(default=False)
	phone_number = models.CharField(max_length=30, blank=True)


TYPE_OF_HIKE = [
	("ПВД", "noncategoried"),
	("Лыжный", "лыжный"),
	("Горный", "горный"),
	("Водный", "водный"),
	("Пеший", "пеший"),
	("Спелео", "спелео"),
	("Вело", "вело"),
]

TYPE_OF_ACCOUNTING = [
	("UesrAccounting", "GroupAccounting"),
	("GroupAccounting", "GroupAccounting")
]


class GroupComposition(models.Model):
	realMembers = models.IntegerField(default=0)
	students = models.IntegerField(default=0)
	newOnes = models.IntegerField(default=0)
	others = models.IntegerField(default=0)


class GroupAccounting(models.Model):
	lead_name = models.CharField(max_length=250, default='Смерека')
	type_of_hike = models.CharField(
		max_length=15, choices=TYPE_OF_HIKE, default="ПВД")
	responsible_person = models.ForeignKey(
		Contact, null=True, default=None, related_name="responsible_person", on_delete=models.CASCADE)
	group_composition = models.ForeignKey(GroupComposition, null=True, default=None, related_name="group", on_delete=models.CASCADE)
	start_date = models.DateField(default="2021-01-02")
	end_date = models.DateField(default="2021-01-02")
	equipment = models.ManyToManyField(Equipment)
	price = models.IntegerField(default=0, null=False)
	archived = models.BooleanField(default=False)


class UserAccounting(models.Model):
	equipment = models.ManyToManyField(Equipment)
	user = models.ForeignKey(
		Contact, null=True, default=None, related_name="user", on_delete=models.CASCADE)
	start_date = models.DateField(default="2021-01-02")
	end_date = models.DateField(default="2021-01-02")
	archived = models.BooleanField(default=False)


class RentedEquipment(models.Model):
	equipment = models.ForeignKey(Equipment, null=True, default=None, related_name="equipment", on_delete=models.CASCADE)
	amount = models.IntegerField(default=1, blank=True)
	type_of_accounting = models.CharField(max_length=15, choices=TYPE_OF_ACCOUNTING, default="GroupAccounting")
	user_accounting = models.ForeignKey(
		UserAccounting, null=True, default=None, on_delete=models.CASCADE)
	group_accounting = models.ForeignKey(
		GroupAccounting, null=True, default=None, on_delete=models.CASCADE)        
