Demo-Analytic App

Simple demo analytic app to aggregate data

## How to install

Install dependencies via poetry:

```shell
poetry install
```

or use requirements.txt in the virtual environment:

```shell
pip install -r requirements.txt
```
And create `.env` file from `.env.example` and fill it.

## How to use

Start django server, migrate and load sample data:

```shell
python manage.py runserver
python manage.py migrate
python manage.py loadsampledata
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

1. [http://127.0.0.1:8000/api/insights/?filters={'date_to':'2017-06-01'}&grouping=channel,country&ordering=-clicks](http://127.0.0.1:8000/api/insights/?filters={'date_to':'2017-06-01'}&grouping=channel,country&ordering=-clicks)

2. [http://127.0.0.1:8000/api/insights/?filters={'date_from':'2017-05-01','date_to':'2017-05-31'}&grouping=date&ordering=date](http://127.0.0.1:8000/api/insights/?filters={'date_from':'2017-05-01','date_to':'2017-05-31'}&grouping=date&ordering=date)

3. [http://127.0.0.1:8000/api/insights/?filters={'date_from':'2017-06-01','date_to':'2017-06-01'}&grouping=os&ordering=-revenue](http://127.0.0.1:8000/api/insights/?filters={'date_from':'2017-06-01','date_to':'2017-06-01'}&grouping=os&ordering=-revenue)
4. [http://127.0.0.1:8000/api/insights/?filters={'country':'CA'}&grouping=channel&cpi=true&ordering=-cpi](http://127.0.0.1:8000/api/insights/?filters={'country':'CA'}&grouping=channel&cpi=true&ordering=-cpi)
