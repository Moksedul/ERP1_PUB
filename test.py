from organizations.models import Companies
from organizations.models import Persons


def convert_to_demo(request):
    companies = Companies.objects.all()
    persons = Persons.objects.all()

    company_name_str = ''

    for company in companies:
        company.name_of_company =