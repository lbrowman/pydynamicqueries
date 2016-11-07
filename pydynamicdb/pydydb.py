# -*- coding: utf-8 -*-
"""PyDynamicQueries

This module enables the use of the pymysql and pyodbc to interact with different databases without having to write any queries.

Dependencies:
    1. pymysql
    2. pyodbc

How to use:
    import pydynamicdb.dbutil.DB

    contype = 'mysql' #this can be any structured database except pgAdmin

    db = pydynamicdb.pydydb.DB(connection_params,contype)


"""

import pymysql, pyodbc

class DB(object):
    """ This class houses the connect,insert,select,update and delete queries"""

    def __init__(self, connection_string, connection_type='mysql'):
        """
        Args:
            connection_string (dict):   This is the connection string to the desired database.
                                        It should include the database name,host,user and password
            type (str):      This is the connection type.
                                        If it is not specified it will default to  mysql
        """
        self.conn = connection_string
        self.connection_type = connection_type

    def connect(self):
        """ Create connection object to the database"""
        try:
            if self.connection_type == 'mysql':
                connection = pymysql.connect(**self.conn)
            else:
                print self.conn['driver']
                connection = pyodbc.connect("""
                                            DRIVER={self.conn['driver']};SERVER=self.conn['host'];PORT=self.conn['port'];
                                            DATABASE=self.conn['database'];UID=self.conn['user'];PWD=self.conn['password'];
                                            """)
            return connection
        except (pymysql.Error, pyodbc.Error) as identifier:
            return identifier

