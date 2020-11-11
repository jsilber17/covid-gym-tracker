import psycopg2 as pg2

class PostgresMonster(object):

    """Class that allows for interaction with Postgres database via psycopg2

    Keyword Arguments: 
        user -- Username for Postgres database 
        password -- Password used to login to Postgres database 
        host -- Host for Postgres
        port -- Port where Postgres lives 
        dbname -- Database name on the Postgres server Python hits
    
    Attributes:  
        user -- Username for Postgres database 
        password -- Password used to login to Postgres database 
        host -- Host for Postgres
        port -- Port where Postgres lives 
        dbname -- Database name on the Postgres server Python hits

    """ 

    def __init__(self, user, password, host, port, dbname): 
        self.user = user 
        self.password = password 
        self.host = host 
        self.port = port 
        self.dbname = dbname

    def create_cursor_and_connection(self): 

        """Create the cursor and connection used to query Postgres

        Keyword Arguments: 
            None 
       
       """ 

        self.connection = pg2.connect(user=self.user,
                                 password=self.password,
                                 host=self.host,
                                 port=self.port,
                                 database=self.dbname) 

        self.cursor = self.connection.cursor() 

        return self.cursor, self.connection

    def insert_rows(self, query_string): 
        """Insert rows into a Postgres table

        Keyword Arguments: 
            query_string -- SQL INSERT statement 
        
        """ 
        
        self.cursor.execute(query_string)
        self.connection.commit() 
        
        return 'Insert query {} has been committed'.format(query_string)

