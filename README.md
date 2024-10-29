# Amazon Product Scraper by Brand

This project is a web application based on Django that scrapes product data from Amazon's search results by brand using BeautifulSoup4. It stores the collected data in a database and provides an API for access.

## Getting Started

To set up the project locally, follow these steps:

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ahmednoureldeen/amazon-products-scraper.git
```
2. Change into the project directory:

```bash
cd amazon-products-scraper
```
3. Create and activate a virtual environment:

```bash
virtualenv env_name
source env_name/bin/activate
```

4. Install the required packages:

```bash
pip install -r requirements.txt
```

5. Apply database migrations:

```bash
python manage.py migrate
```
6. Create an admin user(Because we need to add some brands from admin panel before we can run the scraping):

```bash
python manage.py createsuperuser
```
*Here you will need to provide username,email(optional),password etc...

7. Start the development server:

```bash
python manage.py runserver
```

8. Go to the server admin panel and login as admin:

```bash
http://127.0.0.1:8000/admin
```

9. Under the Brands model add as brands as you want to scrap the products.


10. That's it we are ready to run our scraping.

***The application should now be running at http://127.0.0.1:8000/ (Unless you specified a different port).***

## Run the Scraping using command line
We have created a custom command in django so we can start the scraping manually using django manage.py.
```python
python manage.py run_scraper
```
**This will scrap through all the keywords in the DB one by one **

## Using API Endpoints
We also have API endpoint to fetch all the scraped data and we can filter data based on brands and product data(name, asin and sku)
```python
#Endpoint to fetch all data
http://127.0.0.1:8000/api/products/
```
```python
#query filter to filter products by brand.
http://127.0.0.1:8000/api/products/?brand=1
```
```python
#or search in product fields.
http://127.0.0.1:8000/api/products/?search=laptop
```


## Run Task Scheduler using Celery and RabbitMQ
We have a feature to scrape data four times a day (every six hours), which can be modified by editing the `main/celery.py` file.
```python
app.conf.beat_schedule = {
    'trigger-scraper-every-24-hours': {
        'task': 'scraper.tasks.scrape',
        'schedule': timedelta(hours=6),
    },
}
```
To run this we will need RabbitMQ setup. Follow this link: https://www.rabbitmq.com/download.html to setup it as per device requirements.
Once we have the RabbitMQ running we can trigger the server using these commands.
```python
#navigate to your project directory and start the Celery worker
celery -A main worker --loglevel=info
```
```python
#In another terminal window, start the Celery beat
celery -A main beat --loglevel=info
```
Make sure to run the commands in separate terminal windows, as they need to run concurrently. The first command starts the Celery worker, which processes the tasks. The second command starts the Celery beat, which schedules tasks to be executed by the worker at specified intervals.