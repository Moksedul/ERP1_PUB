import string

from django.contrib import messages
from django.shortcuts import redirect
import random

from main.views import home
from organizations.models import Companies
from organizations.models import Persons
from faker import Faker


def convert_to_demo(request):
    companies = Companies.objects.all()
    persons = Persons.objects.all()

    company_name_str = ['Corporation', 'Company', 'Limited', 'LTD.', 'Enterprise', 'Trading', '& Co.']
    phone_number_prefix = ['+88012', '+88011', '+88010', '+88109']

    for company in companies:
        random_text = Faker('en_IN')
        company_name = random_text.name() + ' ' + random.choices(company_name_str)[0]
        random_text = Faker('bn_BD')
        company_address = random_text.address()

        company.name_of_company = company_name
        company.company_address = company_address
        company.save()
        print(company)

    for person in persons:
        random_text = Faker('en_IN')
        size = 8
        chars = string.digits
        phone_number_suffix = ''.join(random.choice(chars) for _ in range(size))
        phone_no = random.choices(phone_number_prefix)[0] + phone_number_suffix
        person_name = random_text.name()
        random_text = Faker('bn_BD')
        person_address = random_text.address()

        person.person_name = person_name
        person.address = person_address
        person.contact_number = phone_no
        person.nid_photo = ''
        person.person_photo = 'default.jpg'
        person.save()
        print(person)

    messages.info(request, 'All Required Real Data Converted To Demo Data')

    return redirect(home)
