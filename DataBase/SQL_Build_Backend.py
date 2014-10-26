#####**************************************************************************#####
#####								DESCRIPTION	    						   #####
#####**************************************************************************#####
"""Pre-testing of methods for the Export Records Digitization Project, in particular
the back end database.

Issues to to be worked out:
+ getting info from a csv file
+ creating the database

"""

import sqlite3, os, csv
os.chdir(r'E:\MGMA Application Digitization Setup\Setup\Application\DataBase')

####******************************Getting Data From CSV File*********************### 
data_tuples = [] # container for my tuples

with open('MGMA_Members.csv', 'rb') as csvfile:
	csvreader = csv.reader(csvfile, dialect = 'excel')
	for line in csvreader:
		data_tuples.append(tuple([entry.replace('\r', "").replace('\n', '').replace('\xa0', '').upper() 
                                  for entry in line]))

data_tuples[:5]
#
#Test that all tuples are len 5
all([len(tup) == 3 for tup in data_tuples])
#Test that there are no None values
all(test for test in [(val is not None) for tup in data_tuples for val in tup])


####******************************Creating the Database**************************###
#create database:
conn = sqlite3.connect('Factory_Import_Licences.db')
c = conn.cursor()

#Members Table
c.execute("CREATE TABLE members \
    (fact_id TEXT PRIMARY KEY,\
	fact_name TEXT NOT NULL,\
	fact_address TEXT NOT NULL)")
c.executemany('INSERT INTO members VALUES (?,?,?)', data_tuples)


#Order Table
c.execute("CREATE TABLE orders \
	(order_id INTEGER PRIMARY KEY AUTOINCREMENT, \
	 fact_id TEXT FOREIGN_KEY REFERENCES members(fact_id), \
	 mgma_order_id TEXT NOT NULL, \
	 buyer TEXT NOT NULL, \
	 sub_date TEXT NOT NULL, \
	 app_date TEXT NOT NULL, \
	 ship_date TEXT NOT NULL, \
	 order_fob_curr TEXT NOT NULL,\
	 order_cmp_curr TEXT NOT NULL, \
	 order_cif_curr TEXT NOT NULL, \
	 order_total_fob REAL NOT NULL, \
	 order_total_cmp REAL NOT NULL, \
	 order_total_cif REAL NOT NULL,\
	 num_export_items INTEGER NOT NULL,\
	 total_export_quantity INTEGER NOT NULL,\
	 num_import_items INTEGER NOT NULL)")
		   
#Order Countries
c.execute("CREATE TABLE order_countries \
	(order_id INTEGER FOREIGN_KEY REFERENCES orders(order_id), \
	 destination_country TEXT NOT NULL)")

#Export Items
c.execute("CREATE TABLE export_items \
	(order_id INTEGER FOREIGN_KEY REFERENCES orders(order_id), \
	 export_item_id INTEGER PRIMARY KEY AUTOINCREMENT, \
	 export_category TEXT NOT NULL, \
	 export_type TEXT NOT NULL, \
	 export_description TEXT NOT NULL, \
	 export_units INTEGER NOT NULL,\
	 export_fob_curr TEXT NOT NULL, \
	 export_cmp_curr TEXT NOT NULL,\
	 export_fob_value REAL NOT NULL, \
	 export_cmp_value REAL NOT NULL)")

#Import Items
c.execute("CREATE TABLE input_items \
	(order_id INTEGER FOREIGN_KEY REFERENCES orders(order_id), \
	 input_item_id INTEGER PRIMARY KEY AUTOINCREMENT, \
	 input_type TEXT NOT NULL,\
	 input_descript TEXT NOT NULL,\
	 input_unit TEXT NOT NULL, \
	 input_quantity INTERGER NOT NULL,\
	 input_curr TEXT NOT NULL, \
	 input_value REAL NOT NULL)")
		   
#Import/Export Lookup
c.execute("CREATE TABLE import_export_lookup \
	(input_item_id INTEGER FOREIGN_KEY REFERENCES input_items(input_item_id),\
 	 export_item_id INTEGER FOREIGN_KEY REFERENCES export_items(export_item_id),\
	 input_coefficient REAL NOT NULL)")

#save database
conn.commit()
conn.close()