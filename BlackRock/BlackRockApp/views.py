import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, AnonymousUser


from django.views.generic import View, TemplateView
from django import forms
from json import loads
from .models import *
from datetime import date, timedelta, datetime


def full_name(user):
    if user.last_name != '' and user.first_name != '':
        return user.first_name+' '+user.last_name
    elif user.first_name != '':
        return user.first_name
    elif user.last_name != '':
        return user.last_name
    else:
        return user.username


def base_context(request, **args):
    context = {}
    django_user = request.user

    context['title'] = 'none'
    context['header'] = 'none'
    context['error'] = 0

    if args != None:
        for arg in args:
            context[arg] = args[arg]


    if len(Users.objects.filter(username=django_user.username)) != 0 and type(request.user) != AnonymousUser:

        user = Users.objects.get(username=django_user.username)
        context['username'] = django_user.username
        context['full_name'] = full_name(user)
        context['user'] = user
    else:
        context['avatar'] = ''
        context['username'] = 'Adminius'
        context['user'] = 'none'

    return context


def get_all_contacts():
    contacts = []
    for contact in Users.objects.all():
        contacts.append((contact.id, contact.name, contact.phone_number))
    return contacts


def beauty_date_interval(date1: datetime, date2: datetime, show_year=False, show_if_this_year=False):
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    result = ''
    result += str(date1.day) + ' '

    if (date1.day, date1.month, date1.year) == (date2.day, date2.month, date2.year):
        result += months[date1.month-1]
    else:
        if date1.month == date2.month:
            result += '- '+str(date2.day) + ' ' + months[date1.month-1]
        else:
            result += months[date1.month-1]+' - ' + \
                str(date2.day) + ' '+months[date2.month-1]

    if show_year:
        if show_if_this_year:
            result += ', '+str(date1.year)
        else:
            if date1.year != datetime.now().year:
                result += ', '+str(date1.year)

    return result


def get_cathegory_path(cathegory):
    cathegory_path = cathegory.name
    curr_cathegory = cathegory
    while curr_cathegory.parent_cathegory != None:
        curr_cathegory = curr_cathegory.parent_cathegory
        cathegory_path = curr_cathegory.name + '/' + cathegory_path
    return cathegory_path


def get_all_free_equipment():
    eq_list = []
    for equipment in Equipment.objects.all():
        eq_list.append((equipment.id,
                        equipment.name,
                        get_cathegory_path(equipment.cathegory),
                        equipment.description,
                        equipment.price,
                        equipment.amount))
        # TODO Append filters to filter only free equipment
    return eq_list


class HomePage(View):
    def get(self, request):
        context = base_context(request, title='Home')
        return render(request, "home.html", context)
    







class Registration(View):
    def get(self, request):

        context = base_context(
            request, title='Sign Up', header='Sign Up', error=0)

        return render(request, "signup.html", context)

    def post(self, request):
        context = {}
        form = request.POST
        user_props = {}
        username = form['username']
        password = form['password']

        # new_post.author = Author.objects.get(id = request.POST.author)
        # new_post.save()
        user = User.objects.filter(username=username)
        if list(user) == []:
            for prop in form:
                if prop not in ('csrfmiddlewaretoken', 'username', 'gender', 'phone_number') and form[prop] != '':
                    user_props[prop] = form[prop]

            # print(user_props)
            User.objects.create_user(
                username=form['username'], **user_props)
            
            custom_user = Users(
                username =form['username'],
                first_name = form['first_name'],
                last_name = form['last_name'],
                email = form['email'],
                phone_number = form['phone_number'],
                confidence_factor = 0,
                profile_approved = False)
            
            custom_user.save()

            user = authenticate(username=username, password=password)
            login(request, user)

            # print(form)
            return HttpResponseRedirect("/")

        else:
            context = base_context(request, title='Sign Up',
                                   header='Sign Up')

            for field_name in form.keys():
                context[field_name] = form[field_name]

            context['error'] = 1
            return render(request, "signup.html", context)
    
class Login(View):

    def __init__(self):
        self.error = 0

    def get(self, request):

        context = base_context(
            request, title='Sign In', header='Sign In', error=0)
        context['error'] = 0

        # context['form'] = self.form_class()
        return render(request, "signin.html", context)

    def post(self, request):
        context = {}
        form = request.POST
        # validation = UserForm(request.POST)
        if True:  # validation.is_valid():
            # print(form)
            username = form['username']
            password = form['password']

            # new_post.author = Author.objects.get(id = request.POST.author)
            # new_post.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    context['name'] = username
                    return HttpResponseRedirect("/")

            else:
                context = base_context(request)
                logout(request)
                context['error'] = 1
                # return Posts.get(self,request)
                return render(request, "signin.html", context)
        else:
            return HttpResponse("Data isn't valid")


class Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")

class CreateUser(View):
    def get(self, request):
        context = base_context(
            request, title='Новый контакт', header='Добавить нового пользователя')
        return render(request, "add_contact.html", context)

    def post(self, request):

        form = request.POST

        name_input = form['name_input']
        number_input = form['number_input']
        in_club_input = form['in_club_input'] == "on"

        contact = Contact(
            name=name_input,
            phone_number=number_input,
            is_club_member=in_club_input,
        )

        contact.save()

        return HttpResponseRedirect("/new_contact")


class AddEquipment(View):
    def get(self, request):
        context = base_context(
            request, title='Добавить снаряжение', header='Добавить снаряжение')
        # contacts_list = get_all_contacts()
        eq_list = get_all_free_equipment()
        context['eq_list'] = eq_list
        # context['contacts_list'] = contacts_list
        return render(request, "add_equpment.html", context)


class AddGroupAccounting(View):
    def get(self, request):
        context = base_context(
            request, title='Записать снар на группу', header='Запись снаряжения на группу')
        contacts_list = get_all_contacts()
        eq_list = get_all_free_equipment()
        context['eq_list'] = eq_list
        context['contacts_list'] = contacts_list
        return render(request, "new_group_accounting.html", context)

    def post(self, request):
        form = request.POST


        group_composition = GroupComposition(
            realMembers=form['realMembers'],
            students=form['students'],
            newOnes=form['newOnes'],
            others=form['others']
        )
        group_composition.save()


        group_accounting = GroupAccounting(
            lead_name=form['leadName'],
            type_of_hike=form['typeOfHike'],
            responsible_person=Contact.objects.get(
                id=form['responsiblePerson']),
            group_composition = group_composition,
            start_date=form['startDate'],
            end_date=form['endDate'],
            price=form['price'],
            archived=False
        )
        group_accounting.save()


        equipment_json = loads(form['equipmentJSON'])

        for eqId in equipment_json:
            rentedEq = RentedEquipment(
                equipment=Equipment.objects.get(id=eqId),
                amount=equipment_json[eqId],
                type_of_accounting="GroupAccounting",
                group_accounting=group_accounting
            )
            rentedEq.save()

        group_accounting.save()
        return HttpResponseRedirect("/")


class CreateNewRentAccounting(View):
    def get(self, request):
        context = base_context(
            request, title='Арендовать снаряжение', header='Арендовать снаряжение')
        # contacts_list = get_all_contacts()
        eq_list = get_all_free_equipment()
        context['eq_list'] = eq_list
        # context['contacts_list'] = contacts_list
        return render(request, "new_rent_accounting.html", context)

    def post(self, request):
        form = request.POST

        # TODO сделать чёртово добавление записи на участника

        user_accounting = UserAccounting(
            user=Contact.objects.get(
                id=form['responsiblePerson']),
            start_date=form['startDate'],
            end_date=form['endDate'],
            archived=False
        )
        user_accounting.save()
        equipment_json = loads(form['equipmentJSON'])

        for eqId in equipment_json:
            rentedEq = RentedEquipment(
                equipment=Equipment.objects.get(id=eqId),
                amount=equipment_json[eqId],
                type_of_accounting="GroupAccounting",
                group_accounting=user_accounting
            )
            rentedEq.save()

        user_accounting.save()
        return HttpResponseRedirect("/")


class AddNewEquipment(View):
    def post(self, request):
        req = request
        form = request.POST

        result = {}
        result["result"] = "failture"

        if form["requestType"] == "add":
            new_equipment = Equipment()
            new_equipment.name = form['obj[name]']
            new_equipment.path = form['obj[path]']
            new_equipment.description = form['obj[desc]']
            new_equipment.number = form['obj[amount]']
            new_equipment.unique = True if form['obj[amount]'] == '1' else False
            new_equipment.price = float(form['obj[price]'])//1
            new_equipment.price_per_day = float(form['obj[price]'])//10
            new_equipment.price_for_members = float(form['obj[price]'])//20
            new_equipment.save()
            result["result"] = "success"
            result["newId"] = new_equipment.id
            
        elif form["requestType"] == "update":
            try:
                equipment_id = int(form['obj[id]'])
                eq_list = Equipment.objects.filter(id=equipment_id)
                if eq_list:
                    equipment = eq_list[0]
                    equipment.name = form['obj[name]']
                    equipment.path = form['obj[path]']
                    equipment.description = form['obj[desc]']
                    equipment.number = form['obj[amount]']
                    equipment.unique = True if form['obj[amount]'] == '1' else False
                    equipment.price = float(form['obj[price]'])//1
                    equipment.price_per_day = float(form['obj[price]'])//10
                    equipment.price_for_members = float(form['obj[price]'])//20
                    equipment.save()
                    result["result"] = "success"
                else:
                    result["result"] = "failture"
            except:
                pass
        
        elif form["requestType"] == "remove":
            try:
                equipment_id = int(form['obj[id]'])
                Equipment.objects.filter(id=equipment_id).delete()
                result["result"] = "success"
            except:
                pass
            
        return HttpResponse(
            json.dumps(result),
            content_type="application/json"
        )


