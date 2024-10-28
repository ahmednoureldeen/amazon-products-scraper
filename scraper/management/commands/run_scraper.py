from django.core.management.base import BaseCommand
from scraper.scaper import scrape_amazon_brands




class Command(BaseCommand):
    help = 'Runs the Amazon scraper for brands exists in the Brands table'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting the scraper...'))
        scrape_amazon_brands()
        self.stdout.write(self.style.SUCCESS('Scraper finished successfully.'))