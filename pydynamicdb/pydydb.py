# -*- coding: utf-8 -*-
"""PyDynamicQueries

This module facilitates the interaction with databases without having to write any queries.

Dependencies:
    1. pymysql
    2. pyodbc

How to use:
    import pydynamicdb.dbutil.DB

    contype = 'mysql' #this can be any structured database except pgAdmin

    db = pydynamicdb.pydydb.DB(connection_params,contype)


"""

import pymysql, pyodbc, psycopg2

class Db(object):
    """ This class houses the connect,insert,select,update and delete queries"""

    def __init__(self, connection_string, connection_type='mysql'):
        """
        Args:
            connection_string (dict):   This is the connection string to the desired database.
                                        It should include the database name,host,user and password.
                                        Examples:
                                        Mysql = {"database":"database", "host":"localhost",
                                                "user":"user", "password":"password"}
                                        ODBC = {
                                                "database":"database", "host":"localhost",
                                                "user":"user", "password":"password",
                                                "driver":"SQL Server", "port":1433
                                                }
            type (str):      This is the connection type.
                                        If it is not specified it will default to  mysql
        """
        self.conn = connection_string
        self.connection_type = connection_type

    def connect(self):
        """ Create connection object to the database"""
        connection = None
        if self.connection_type == 'mysql':
            connection = pymysql.connect(**self.conn)
        elif self.connection_type == 'odbc':
            connection = pyodbc.connect("""
                                        DRIVER={self.conn['driver']};SERVER=self.conn['host'];PORT=self.conn['port'];
                                        DATABASE=self.conn['database'];UID=self.conn['user'];PWD=self.conn['password'];
                                        """)
        elif self.connection_type == 'postgre':
            connection = psycopg2.connect(**self.conn)
        return connection

    def select(self, params):
        """Runs selects based on the below Query Dictionary
           Args:
              params (dict):
                                dict keys:
                                "select_list" - can be '*' or a list of columns you wish to return
                                "table" - the table you wish to QUERY
                                "conditions" - a dictionary array
                                "conjuction" - used to join conditions.e.g. "AND" or "OR" or None
                                "orderby" - either 'default' or a list of columns you wish to return
                                "order" - either asc or dsc
                                "groupby" - either 'default' or a list of columns you wish to return
                                ""
                                Examples
                                QUERY = {
                                    "select_list":['id','event'],
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

                                QUERY = {
                                    "select_list":'*',
                                    "table":"incident",
                                    "conditions":[{
                                        "name":"contact_email",
                                        "value":"contact@mail.com"
                                    },
                                    {
                                        "name":"status_id",
                                        "value":2
                                    }],
                                    "orderby":"event_id",
                                    "order":"desc",
                                    "groupby":"status_id",
                                    "conjunction":None
                                    }

        """
        results = []
        if isinstance(params['select_list'], list) or isinstance(params['select_list'], tuple):
            select_list = ",".join(params['select_list'])
            select = "SELECT {} from {}".format(select_list, params['table'])
        else:
            select = "SELECT * from {}".format(params['table'])
        if 'fields' in params or len(params['conditions']) == 0:
            for index, column in enumerate(params['conditions']):
                select = select+" {} in ({})".format(column['name'], self.parseparam(column))
                if params['conjunction'] or len(params['conditions']) <= index:
                    select = select+" "+params['conjunction']
        if params['orderby'] == 'default' and params['groupby'] == 'default':
            pass
        elif params['groupby'] == 'default':
            select = select+" ORDER by {} {}".format(params['orderby'], params['order'])
        else:
            select = select+" GROUP BY {} ORDER BY {} {}".format(
                params['groupby'], params['orderby'], params['order'])
        con = self.connect()
        with con.cursor() as cur:
            cur.execute(select)
            rows = cur.fetchall()
            if rows:
                for result in rows:
                    if isinstance(params['select_list'], list):
                        dict_result = {}
                        for index, column in enumerate(params['select_list']):
                            print index, column
                            dict_result[column] = result[index]
                        results.append(dict_result)
                    else:
                        results.append(result[0] if len(result) == 1 else result)
        return results

    def parseparam(self, value):
        """Parses the parameter list and returns the paramter in the correct type"""
        fixed_value = ""
        if isinstance(value, list) or isinstance(value, tuple):
            if isinstance(value[0], str):
                if len(value) == 1:
                    fixed_value = "'"+value+"'"
                else:
                    fixed_value = ",".join("'"+val+"'" for val in value)
            elif isinstance(value[0], int):
                if len(value['value']) == 1:
                    fixed_value = value[0]
                else:
                    fixed_value = ",".join(str(val) for val in value)
        elif isinstance(value, int):
            fixed_value = value
        elif isinstance(value, str):
            fixed_value = "'"+value+"'"
        return fixed_value






