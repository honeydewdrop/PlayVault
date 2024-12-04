from django.utils.dateparse import parse_datetime
from django.core.management.base import BaseCommand
from requests import post
from members.models import Company, Game  # Assuming you also have a Game model
import time

class Command(BaseCommand):
    help = 'Fetches company data from IGDB and stores it in the database'

    def handle(self, *args, **options):
        limit = 100  # Number of records per request
        offset = 0  # Start with the first page
        
        while True:
            # Send the API request for companies
            response = post(
                'https://api.igdb.com/v4/companies',
                headers={
                    # shhhhhhhh!
                },
                data=f'fields change_date,change_date_category,changed_company_id,checksum,country,created_at,description,developed,logo,name,parent,published,slug,start_date,start_date_category,updated_at,url,websites; limit {limit}; offset {offset};'
            )

            if response.status_code != 200:
                self.stderr.write(self.style.ERROR(f"Error: {response.status_code}, {response.text}"))
                return

            companies_data = response.json()
            if not companies_data:
                self.stdout.write(self.style.SUCCESS("No more companies to fetch."))
                break  # No more data to fetch, exit the loop

            self.stdout.write(f"Fetched {len(companies_data)} companies (offset {offset}).")

            for idx, company_data in enumerate(companies_data):
                # Ensure the datetime fields are strings before parsing
                created_at_str = company_data.get('created_at')
                updated_at_str = company_data.get('updated_at')
                start_date_str = company_data.get('start_date')

                # Parse datetime fields if they exist and are valid
                created_at = parse_datetime(created_at_str) if isinstance(created_at_str, str) else None
                updated_at = parse_datetime(updated_at_str) if isinstance(updated_at_str, str) else None
                start_date = parse_datetime(start_date_str) if isinstance(start_date_str, str) else None

                # Create or update the company in the database
                company, created = Company.objects.update_or_create(
                    slug=company_data.get('slug'),  # Use slug as a unique identifier
                    defaults={
                        'name': company_data.get('name'),
                        'description': company_data.get('description'),
                        'country': company_data.get('country'),
                        'logo': company_data.get('logo'),
                        'url': company_data.get('url'),
                        'created_at': created_at,
                        'updated_at': updated_at,
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created company: {company.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Updated company: {company.name}"))

                # Now associate this company with games if needed
                game_data = company_data.get('games', [])  # Assuming you fetch games for this company
                for game_id in game_data:
                    # Fetch the game using the game_id, assuming you have a method for it
                    try:
                        game = Game.objects.get(id=game_id)
                        game.companies.add(company)  # Add the company to the game's ManyToMany field
                        self.stdout.write(self.style.SUCCESS(f"Linked company {company.name} to game {game.name}."))
                    except Game.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"Game with ID {game_id} not found."))

            # Enforce rate limit of 4 requests per second
            time.sleep(1)

            # Increment the offset for the next batch
            offset += limit
