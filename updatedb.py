import sqlite3
import sys
import os

class UpdateSqlite3Db:
    def __init__(self, db):
        self.connection = sqlite3.connect( db )
        self.cursor = self.connection.cursor()

    def add_field( self, table, field, definition ):
        # see if the field already exists
        sql_cmd = ( "select sql from sqlite_master where type='table' and name='%s' and sql LIKE '%%\"%s %%'" % ( table, field ) );
        result = self.cursor.execute( sql_cmd )

        if self.cursor.fetchone():
            # field already exists
            return False

        sql_cmd = ( "alter table main.'%s' add column %s %s" % ( table, field, definition ) )

        print "sql: %s" % sql_cmd

        self.cursor.execute( sql_cmd )
        self.connection.commit()
       
def main(): 
    
    if len( sys.argv ) < 2:
        sys.exit(1)

    updatedb = UpdateSqlite3Db( sys.argv[ 1 ] )

    # Add contact number and  previous ngo work to mentor application
    updatedb.add_field( 'user_mentorapplication', 'contact_no', 'varchar(32) NOT NULL default ""' )
    updatedb.add_field( 'user_mentorapplication', 'prev_ngo', 'text NOT NULL default ""' )

if __name__ == '__main__':
    main() 
