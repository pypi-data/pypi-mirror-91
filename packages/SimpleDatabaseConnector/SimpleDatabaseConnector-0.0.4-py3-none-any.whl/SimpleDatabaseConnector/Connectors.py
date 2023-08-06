import pyodbc, uuid, os
from datetime import datetime

class SQLConnector:
    def __init__(self,
            username,
            password,
            server,
            database,
            port=1433,
            driver="{ODBC Driver 17 for SQL Server}",
            datetimeUpdateTracking=True
        ):
        self.server = server
        self.database = database
        self.user = username
        self.password = password
        self.port = port
        self.driver = driver
        
        self.trackUpdates = datetimeUpdateTracking

    def execute_file(self, filepath):
        if not os.path.isfile(filepath) or not filepath.lower().endswith(".sql"):
            raise Exception("The give filepath is not a file or is not a SQL file.")

        with open(filepath, 'r') as sqlfile:
            sql = sqlfile.read()

        with pyodbc.connect('DRIVER={};SERVER={};PORT={};DATABASE={};UID={};PWD={}'.format(self.driver, self.server, self.port, self.database, self.user, self.password)) as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)

        return True

    # Base operations
    def execute(self, query, args=None): # Execute without response
        with pyodbc.connect('DRIVER={};SERVER={};PORT={};DATABASE={};UID={};PWD={}'.format(self.driver, self.server, self.port, self.database, self.user, self.password)) as connection:
            with connection.cursor() as cursor:
                if args:
                    cursor.execute(query, args)
                else:
                    cursor.execute(query)
                
    def get_one(self, query, args=None): # Execute with one item as a response
        with pyodbc.connect('DRIVER={};SERVER={};PORT={};DATABASE={};UID={};PWD={}'.format(self.driver, self.server, self.port, self.database, self.user, self.password)) as connection:
            with connection.cursor() as cursor:
                if args:
                    return cursor.execute(query, args).fetchone()
                else:
                    return cursor.execute(query).fetchone()

    def get_all(self, query, args=None): # Execute with all items as a response
        with pyodbc.connect('DRIVER={};SERVER={};PORT={};DATABASE={};UID={};PWD={}'.format(self.driver, self.server, self.port, self.database, self.user, self.password)) as connection:
            with connection.cursor() as cursor:
                if args:
                    return cursor.execute(query, args).fetchall()
                else:
                    return cursor.execute(query).fetchall()

    # Helpers
    def new_uuid(self):
        return str(uuid.uuid4())

    def get_datetime(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def addDefaultInsertColumns(self, columns):
        if 'Id' not in columns:
            columns.insert(0, 'Id')

        if self.trackUpdates:
            columns += ['CreatedAt', 'UpdatedAt']

        return columns

    def addDefaultInsertValues(self, values, id):
        values.insert(0, id)

        if self.trackUpdates:
            values += [self.get_datetime()] * 2

        return values

    def addDefaultUpdateColumns(self, columns):
        if self.trackUpdates:
            columns.append('UpdatedAt')

        return columns

    def addDefaultUpdateValues(self, values, id):
        if self.trackUpdates:
            values.append(self.get_datetime())


        # add ID always last!
        values.append(id)

        return values

    '''
    Basic CRUD operations
    '''
    # Basics
    def get_item(self, tableName, columns, values):
        if len(columns) != len(values):
            raise Exception("Arrays 'columns' and 'values' do not have the same length!")

        seperator = " = ?,"
        query = "SELECT * FROM {} WHERE {} = ?;".format(tableName, seperator.join(columns))
        return self.get_one(query, values)

    def get_all_items(self, tableName):
        query = "SELECT * FROM {};".format(tableName)
        return self.get_all(query)

    def get_items_where(self, tableName, columns, values):
        if len(columns) != len(values):
            raise Exception("Arrays 'columns' and 'values' do not have the same length!")

        seperator = " = ?,"
        query = "SELECT * FROM {} WHERE {} = ?;".format(tableName, seperator.join(columns))
        return self.get_all(query, values)

    def get_item_by_id(self, tableName, id):
        query = "SELECT * FROM {} WHERE Id = ?;".format(tableName)
        return self.get_one(query, [id])

    #Id is auto added but value can be overwriten with customId.
    def insert(self, tableName, columns, values, returnResult=True, customId=None):
        newId = customId if customId != None else self.new_uuid()
    
        # Add default values
        columns = self.addDefaultInsertColumns(columns)
        values = self.addDefaultInsertValues(values, newId)

        # Create base query
        questionMarks = "".join([ " ?," if (idx+1) < len(values) else " ?" for idx, val in enumerate(values)])
        query = "INSERT INTO {} ({}) VALUES ({});".format(tableName, ", ".join(columns), questionMarks)

        # Execute
        self.execute(query, values)

        # Return result
        if returnResult:
            return self.get_item(tableName, ['Id'], [newId])

    def update(self, tableName, id, columns, values, returnResult=True):
        # Add default values
        columns = self.addDefaultUpdateColumns(columns)
        values = self.addDefaultUpdateValues(values, id)

        # Create base query
        setString = "".join([f"{col} = ?, " if (idx+1) < len(columns) else f"{col} = ?" for idx, col in enumerate(columns)])
        query = "UPDATE {} SET {} WHERE Id = ?;".format(tableName, setString)

        # Execute
        self.execute(query, values)

        # Return result
        if returnResult:
            return self.get_item(tableName, ['Id'], [id])

    def delete(self, tableName, id, returnResult=False):
        item = None
        if returnResult:
            item = self.get_item(tableName, ['Id'], [id])

        query = "DELETE FROM {} WHERE Id = ?;".format(tableName)
        args = [id]

        self.execute(query, args)

        return item

    def search(self, tableName, columns, searches, matchOne=True):
        if len(searches) != 1 and len(searches) != len(columns):
            raise Exception("The length of the argument 'searches' has to be 1 or the same as the lenght of 'columns'! Given arrays lengths are: columns = {} and searches = {}".format(len(columns), len(searches)))

        seperator = " LIKE ? OR " if matchOne else " LIKE ? AND "
        query = "SELECT * FROM {} WHERE {} LIKE ?;".format(tableName, seperator.join(columns))

        args = [f"%{searches[0]}%"] * len(columns) if len(searches) == 1 else [f"%{search}%" for search in searches]

        return self.get_all(query, args)