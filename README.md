Demo-Analytic App

Simple demo analytic app to aggregate data from FB based on the Django

## How to install

Create `.env` file from `.env.example` in the main directory and fill it.

## How to use

Start django server, migrate and load sample data:

```shell
make run
make migrate
docker-compose exec app python manage.py loadsampledata
```

Endpoint to fetch insight data:

```shell
/api/insights/
```

## Query params

filtering by `date_from`, `date_to`, `channel`, `country` and `os`: 
```shell
filters={"date_from":'2017-06-10','date_to':'2017-06-17","channel": "vungle", "country": "GB", "os": "ios"}
```

grouping by `channel`, `country`, `os` and dates (`date`, `date__month`, `date__quarter`, `date__year`):
```shell
grouping=channel,date__year,os
```

calculate cpi field:
```shell
cpi=true
```

ordering by any fields using django style:
```shell
ordering=-date,cpi
ordering=-channel,date,os
```

### API example cases

1. Show the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order.

[http://0.0.0.0:8000/api/insights/?filters={%27date_to%27:%272017-06-01%27}&grouping=channel,country&ordering=-clicks](http://0.0.0.0:8000/api/insights/?filters={%27date_to%27:%272017-06-01%27}&grouping=channel,country&ordering=-clicks)

2. Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order.

[http://0.0.0.0:8000/api/insights/?filters={%27date_from%27:%272017-05-01%27,%27date_to%27:%272017-05-31%27}&grouping=date&ordering=date](http://0.0.0.0:8000/api/insights/?filters={%27date_from%27:%272017-05-01%27,%27date_to%27:%272017-05-31%27}&grouping=date&ordering=date)

3. Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order.

[http://0.0.0.0:8000/api/insights/?filters={%27date_from%27:%272017-06-01%27,%27date_to%27:%272017-06-01%27}&grouping=os&ordering=-revenue](http://0.0.0.0:8000/api/insights/?filters={%27date_from%27:%272017-06-01%27,%27date_to%27:%272017-06-01%27}&grouping=os&ordering=-revenue)

4. Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order. Please think carefully which is an appropriate aggregate function for CPI.

[http://0.0.0.0:8000/api/insights/?filters={%27country%27:%27CA%27}&grouping=channel&cpi=true&ordering=-cpi](http://0.0.0.0:8000/api/insights/?filters={%27country%27:%27CA%27}&grouping=channel&cpi=true&ordering=-cpi)
