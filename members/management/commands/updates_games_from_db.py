from django.core.management.base import BaseCommand
from django.db import transaction
from members.models import Game, Company  # Import the Company model

class Command(BaseCommand):
    help = 'Updates game information using data from the database'

    def handle(self, *args, **options):
        total_games = Game.objects.count()
        self.stdout.write(f"Updating {total_games} games...")

        with transaction.atomic():
            for game in Game.objects.all():
                # Example: Update all games' ratings
                if game.rating:
                    game.rating = min(game.rating / 10, 10)

                # Assuming you have a way to get the company IDs for the game
                company_ids = [1, 2, 3]  # Replace with actual logic to get company IDs

                # Clear existing companies and set new ones
                game.companies.clear()  # Clear existing companies
                for company_id in company_ids:
                    try:
                        company = Company.objects.get(id=company_id)
                        game.companies.add(company)  # Add the company to the game
                    except Company.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"Company with ID {company_id} does not exist."))

                game.save()  # Save the game after updating

        self.stdout.write(self.style.SUCCESS(f"Successfully updated {total_games} games"))