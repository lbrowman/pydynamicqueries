# PyDynamic Query

## About

PyDynamic Query is a module that facilitates the interaction with databases without having to write any queries.

## Dependencies

The following packages must be installed on your local machine for this to work

    1. pymysql

    2. pyodbc

    3. psycopg2

## USAGE

```python

import pydynamicdb.dbutil.DB

connection_string = {
    "database":"database", "host":"localhost",
    "user":"user", "password":"password"}

QUERY = {
    "select_list":'*',
    "table":"incident",
    "conditions":[{
        "name":"event_id",
        "value":['1', '2', '3']
    }],
    "orderby":"default",
    "order":"desc",
    "groupby":"default",
    "conjunction":None
    }
dbObject = DB(connection_string) # supported connection types are 'mysql','odbc','postgre'

dbObject.select(QUERY)
```

### Expected Return

```python
[(1, 'this is a demo demo demo demo demo demo demo'), (1, 'a bites dog dog bites man back man tells goat'), (6, 'This is powr outage for a long time idk ssss       asdljlaksdjlkj'), (6, 'there has been a power outage for the longest while. Please assist'), (1, 'Fire outsideeee near la penitance. it burns'), (1, 'There is a fire next door.. Send help @!!!!!!!!!')]

```

```python

import pydynamicdb.dbutil.DB

connection_string = {
    "database":"database", "host":"localhost",
    "user":"user", "password":"password"}

QUERY = {
    "select_list":['event_id','description'],
    "table":"incident",
    "conditions":[{
        "name":"event_id",
        "value":['1', '2', '3']
    }],
    "orderby":"default",
    "order":"desc",
    "groupby":"default",
    "conjunction":None
    }
dbObject = DB(connection_string) # supported connection types are 'mysql','odbc','postgre'

dbObject.select(QUERY)
```

### Expected Return

```python

[{'event_id': 1, 'description': 'this is a demo demo demo demo demo demo demo'}, {'event_id': 1, 'description': 'a bites dog dog bites man back man tells goat'}, {'event_id': 6, 'description': 'This is powr outage for a long time idk ssss       asdljlaksdjlkj'}, {'event_id': 6, 'description': 'there has been a power outage for the longest while. Please assist'}, {'event_id': 1, 'description': 'Fire outsideeee near la penitance. it burns'}, {'event_id': 1, 'description': 'There is a fire next door.. Send help @!!!!!!!!!'}]

```