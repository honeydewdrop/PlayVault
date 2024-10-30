from django.core.management.base import BaseCommand
from requests import post
from members.models import Company

class Command(BaseCommand):
    help = 'Fetches company data from IGDB and stores it in the database'

    def handle(self, *args, **options):
        response = post(
            'https://api.igdb.com/v4/companies',
            headers = {
        'Client-ID': '5fx0c2tdp25zr3fuazhlqmwvezok4f',
        'Authorization': 'Bearer 9xs6a5rq9q9i37q84ca5w82uasrwt9',
            },
            data='fields change_date,change_date_category,changed_company_id,checksum,country,created_at,description,developed,logo,name,parent,published,slug,start_date,start_date_category,updated_at,url,websites;'
        )

        companies_data = response.json()
        self.stdout.write(f"Fetched {len(companies_data)} companies.")

        for company_data in companies_data:
            # Create or update the company in the database
            company, created = Company.objects.update_or_create(
                slug=company_data.get('slug'),  # Use slug as a unique identifier
                defaults={
                    'name': company_data.get('name'),
                    'description': company_data.get('description'),
                    'country': company_data.get('country'),
                    'logo': company_data.get('logo'),
                    'url': company_data.get('url'),
                    'created_at': company_data.get('created_at'),
                    'updated_at': company_data.get('updated_at'),
                    'start_date': company_data.get('start_date'),
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created company: {company.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated company: {company.name}"))