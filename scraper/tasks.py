from celery import shared_task, Celery
from .scaper import scrape_amazon_brands
app = Celery('tasks')


@shared_task
def scrape():
    print("Here we go")
    scrape_amazon_brands()