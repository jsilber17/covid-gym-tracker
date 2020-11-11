import psycopg2 as pg2

class PostgresMonster(object): 

    def __init__(self, user, password, host, port, dbname): 

        """Add comments
        """ 
        self.user = user 
        self.password = password 
        self.host = host 
        self.port = port 
        self.dbname = dbname

    def create_cursor_and_connection(self): 

        """Add comments 
        """ 
        self.connection = pg2.connect(user=self.user,
                                 password=self.password,
                                 host=self.host,
                                 port=self.port,
                                 database=self.dbname) 

        self.cursor = self.connection.cursor() 

        return self.cursor, self.connection

    def insert_rows(self, query_string): 
        
        self.cursor.execute(query_string)
        self.connection.commit() 
        
        return 'Insert query {} has been committed'.format(query_string)

