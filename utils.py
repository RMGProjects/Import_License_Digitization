#####**************************************************************************#####
#####								DESCRIPTION	    						   #####
#####**************************************************************************#####

"""
Set of helper functions for application. 

VALIDATION
The types of check that are being made regularly in the program are:

1. Not blank
2. Not blank and numeric
3. Not blank and alphanumeric
4. Not blank and alpha


There are a number of checks made to the buyer_countries values that are harvested
from the FORM on /order/<uid> but these are highly idiosyncratic, so no function is
prepared for them here. 

Each of the function will accept an argument that is a named tuple of the following
format:

validation_tup = namedtuple('validation', ['fieldname', 'value', 'validation_message'])

The 'fieldname' and 'value' values will be supplied by the function that GETs the
values from the FORM. The validation message will be generated by the functions
written here. 

GET FACTORY NAME
Possibly this is not the best way to pass the factory name to each sheet, but I 
dont want to pass it in the URL. So I use a database access function instea
"""

#consider adding not zero


####********************************************************************************************####
####										  IMPORTS   										####
####********************************************************************************************####
import sqlite3, re, locale, collections
import values # Created for this application
#set locale
locale.setlocale(locale.LC_ALL, '')

####********************************************************************************************####
####								    VALIDATION CHECKS   									####
####********************************************************************************************####
def not_blank(named_tuple):
	named_tuple
	if named_tuple.value.strip() == "":
		named_tuple = named_tuple._replace(validation_message = \
		"Please do not leave the {} blank".format(named_tuple.fieldname))
	else:
		named_tuple = named_tuple._replace(validation_message = "OK")
	return named_tuple
	
def not_blank_integer(named_tuple):
	int_form = re.compile(r'^[1-9][0-9]*$')
	if named_tuple.value.strip() == "":
		named_tuple = named_tuple._replace(validation_message = \
		"Please do not leave the {} blank".format(named_tuple.fieldname))
	elif not named_tuple.value.replace(",", "").isdigit():
		named_tuple = named_tuple._replace(validation_message = \
		"Please only use numbers and commas in {}, no other characters".format(\
		named_tuple.fieldname))
	elif named_tuple.value.replace(",", "").isdigit() \
	and not re.match(int_form, named_tuple.value.replace(",", "")):
		named_tuple = named_tuple._replace(validation_message = \
		"The {} number is not formatted correctly".format(named_tuple.fieldname))
	elif ',' in named_tuple.value:
		compiled = re.compile(r"^[1-9][0-9]{0,2},(\d\d\d,){0,2}[0-9]{3}$")
		if not re.match(compiled, named_tuple.value):
			named_tuple = named_tuple._replace(validation_message = \
			"The {} number is not formatted correctly".format(named_tuple.fieldname))
		else:
			named_tuple = named_tuple._replace(validation_message = "OK")
	else:
		named_tuple = named_tuple._replace(validation_message = "OK")
	return named_tuple
	
def not_blank_float(named_tuple):
	compiled = \
	re.compile(r"(^[1-9][0-9]{0,1}\.\d{2}$)|(^0(?=(\.0(?=(0[1-9]$)|([1-9]{1,2}$)))|(\.[1-9]([0-9]){1,2}$)))")
	if named_tuple.value.strip() == "":
		named_tuple = named_tuple._replace(validation_message = \
		"Please do not leave the {} blank".format(named_tuple.fieldname))
	elif not named_tuple.value.replace(".", "").isdigit():
		named_tuple = named_tuple._replace(validation_message = \
		"Please only use numbers and decimal point in {}, no other characters".format(\
			named_tuple.fieldname))
	elif not re.match(compiled, named_tuple.value):
		named_tuple = named_tuple._replace(validation_message = \
		"The {} number is not formatted correctly".format(named_tuple.fieldname))
	else:
		named_tuple = named_tuple._replace(validation_message = "OK")
	return named_tuple
	
def not_blank_price(named_tuple):
	price_form = re.compile(r'^[1-9][0-9]*\.\d\d$')
	if named_tuple.value.strip() == "":
		named_tuple = named_tuple._replace(validation_message = \
		"Please do not leave the {} blank".format(named_tuple.fieldname))
	elif not named_tuple.value.replace(".", "").replace(",", "").isdigit():
		named_tuple = named_tuple._replace(validation_message = \
		"Please only use numbers, commas and decimal point in {}, no other characters".format(\
		named_tuple.fieldname))
	elif not re.match(price_form, named_tuple.value.replace(",", "")):
		named_tuple = named_tuple._replace(validation_message = \
		"The {} number is not formatted correctly".format(named_tuple.fieldname))
	elif ',' in named_tuple.value:
		compiled = re.compile(r"^[1-9][0-9]{0,2},(\d\d\d,){0,2}[0-9]{3}\.\d\d$")
		if not re.match(compiled, named_tuple.value):
			named_tuple = named_tuple._replace(validation_message = \
			"The {} number is not formatted correctly".format(named_tuple.fieldname))
		else:
			named_tuple = named_tuple._replace(validation_message = "OK")
	else:
		named_tuple = named_tuple._replace(validation_message = "OK")
	return named_tuple
	
def not_blank_coefficients(named_tuple):
	compiled = \
	re.compile(r"(^[1-9][0-9]{0,2}\.\d{2}$)|(^0(?=(\.0(?=(0[1-9]$)|([1-9]{1,2}$)))|(\.[1-9]([0-9]){1,2}$)))")
	if named_tuple.value == '0':
		named_tuple = named_tuple._replace(validation_message = "OK")
	elif named_tuple.value.strip() == "":
		named_tuple = named_tuple._replace(validation_message = \
		"Please do not leave the {} blank".format(named_tuple.fieldname))
	elif not named_tuple.value.replace(".", "").isdigit():
		named_tuple = named_tuple._replace(validation_message = \
		"Please only use numbers and decimal point in {}, no other characters".format(\
		named_tuple.fieldname))
	elif not re.match(compiled, named_tuple.value):
		named_tuple = named_tuple._replace(validation_message = \
		"The {} number is not formatted correctly".format(named_tuple.fieldname))
	else:
		named_tuple = named_tuple._replace(validation_message = "OK")
	return named_tuple
		
def not_blank_numeric_code(named_tuple):
	if named_tuple.value.strip() == "":
		named_tuple = named_tuple._replace(validation_message = \
		"Please do not leave the {} blank".format(named_tuple.fieldname))
	elif not named_tuple.value.isdigit():
		named_tuple = named_tuple._replace(validation_message = \
		"Please only use numbers in {}, no other characters".format(named_tuple.fieldname))
	else:
		named_tuple = named_tuple._replace(validation_message = "OK")
	return named_tuple
	
def not_blank_alpha(named_tuple):
	if named_tuple.value.strip() == "":
		named_tuple = named_tuple._replace(validation_message = \
		"Please do not leave the {} blank".format(named_tuple.fieldname))
	elif not named_tuple.value.replace(" ", "").replace(',', '').replace('&', '').replace('-', '').isalpha():
		named_tuple = named_tuple._replace(validation_message = \
		"Please only use letters and the symbols ',', '-', '&', in {} no other characters".format(\
		named_tuple.fieldname))
	else:
		named_tuple = named_tuple._replace(validation_message = "OK")
	return named_tuple
	
def not_blank_alnum(named_tuple):
	if named_tuple.value.strip() == "":
		named_tuple = named_tuple._replace(validation_message = \
		"Please do not leave the {} blank".format(named_tuple.fieldname))
	elif not named_tuple.value.replace(" ", "").replace(',', '').replace('&', '').replace('-', '').replace('%', '').isalnum():
		named_tuple = named_tuple._replace(validation_message = \
		"Please only use letters, numbers, and the symbols ',', '-', '&' in {} no other characters".format(\
		named_tuple.fieldname))
	else:
		named_tuple = named_tuple._replace(validation_message = "OK")
	return named_tuple

def review_checks(review_data, check_order, check_exports, check_imports, check_coefficients):
	messages_dict = {'order_messages' 			: [],
					 'export_messages'			: [],
					 'import_messages'			: [],
					 'coefficients_messages'	: []
					}
	#FOB/CMP/CIF Totals Check
	order_data = review_data['order_data']
	export_data = review_data['export_data']
	import_data = review_data['import_data']
	coefficients_data = review_data['coefficients_data']
	if check_order:
		totals = 		[locale.atof(order_data['total_fob']), locale.atof(order_data['total_cmp']),
						locale.atof(order_data['total_cif'])]
		upper_bounds = 	[values.upper_fob_bound, values.upper_cmp_bound, values.upper_cif_bound]
		lower_bounds = 	[values.lower_fob_bound, values.lower_cmp_bound, values.lower_cif_bound]
		keys =  		['FOB', 'CMP', 'CIF']
		for x in xrange(len(keys)):
			if totals[x] < lower_bounds[x]:
				messages_dict['order_messages'].append(\
					"Total {} is lower than suggested lower bound. Please check".format(keys[x]))
			elif totals[x] > upper_bounds[x]:
				messages_dict['order_messages'].append(\
					"Total {} is higher than suggested higher bound. Please check".format(keys[x]))
		if totals[1] < totals[0]/values.fob_cmp_divider_max:
			messages_dict['order_messages'].append(\
			"The ratio between total CMP and total FOB is not as expected. Please check")
		elif totals[1] > totals[0]/values.fob_cmp_divider_min:
			messages_dict['order_messages'].append(\
			"The ratio between total CMP and total FOB is not as expected. Please check")
	else:
		messages_dict['order_messages'].append("Cannot check Order Data due to errors in data")
	
	##Export Items Check
	if check_order and check_exports:
		export_quantity = sum([locale.atoi(export_data['units' + str(x)]) 
								  for x in xrange(1, order_data['export_items'] + 1)])
		if export_quantity != int(order_data['export_quantity']):
			messages_dict['export_messages'].append(\
				"The sum of the export quantities do not match the Total Quantity of Export Items. Please check")
		export_fob_sum = sum([locale.atof(export_data['unit_fob' + str(x)]) * 
							  locale.atoi(export_data['units' + str(x)])
							  for x in xrange(1, order_data['export_items'] + 1)])
		export_cmp_sum = sum([locale.atof(export_data['unit_cmp' + str(x)]) * 
							  locale.atoi(export_data['units' + str(x)])
							  for x in xrange(1, order_data['export_items'] + 1)])
		if int(export_fob_sum) != int(locale.atof(order_data['total_fob'])):
			messages_dict['export_messages'].append(\
			"The sum of the export FOB values * quantities does not match the Total Order FOB Value. Please check")
		if int(export_cmp_sum) != int(locale.atof(order_data['total_cmp' ])):
			messages_dict['export_messages'].append(\
			"The sum of the export CMP values * quantities does not match the Total Order FOB Value. Please check")
	else:
		messages_dict['export_messages'].append("Cannot check Order Data due to errors in data")
		
	##Import Items Check
	if check_order and check_imports:
		import_value_sum = sum([locale.atof(import_data['total_price' + str(x)])
								for x in xrange(1, order_data['import_items'] + 1)])
		if int(import_value_sum) != int(locale.atof(order_data['total_cif'])):
			messages_dict['import_messages'].append(\
				"The total value of the imports does not match the Total Order CIF Value. Please check all import values")
	else:
		messages_dict['import_messages'].append("Cannot check Order Data due to errors in data")
	
	##Coefficients Check
	if check_exports and check_imports and check_coefficients:
		for x in xrange(1, order_data['import_items'] + 1):
			sum_ = int(sum([locale.atof(coefficients_data[str(x) + '_' + str(y)]) * 
						   locale.atoi(export_data['units' + str(y)])
						   for y in xrange(1, order_data['export_items'] + 1)]))
			if sum_ > int(locale.atof(import_data['quantity' + str(x)])):
				messages_dict['coefficients_messages'].append(\
					"The sum of the import coefficients for {} is larger than the quantity ordered. Please check".format(\
					import_data['import_description' + str(x)]))
			elif sum_ < int(locale.atoi(import_data['quantity' + str(x)]) * values.wastage_allowance):
				messages_dict['coefficients_messages'].append(\
					"The sum of the coefficients for {} is {}% lower than the quantity ordered. Please check". format(\
					import_data['import_description' + str(x)], round((1-(float(sum_)/locale.atof(import_data['quantity' + str(x)])))*100, 2)))
	else:
		messages_dict['coefficients_messages'].append("Cannot check Order Data due to errors in data")
	return messages_dict
		
####********************************************************************************************####
####								    DATABASE FUNCTIONS	  									####
####********************************************************************************************####
def get_factory_name(uid):
	"""
	uid 	: string
	returns	: string
	
	Function looks up uid in factories.db and returns the corresponding factory name.
	"""
	conn = sqlite3.connect('Factory_Import_Licences.db')
	c = conn.cursor()
	c.execute("SELECT fact_name FROM members WHERE fact_id = (?)", (uid,))
	r = c.fetchone()
	conn.close()
	factory = r[0]
	return factory
	
def get_new_uid():
	"""
	returns	: string
	
	Function returns next UID in series
	"""
	#Create connction with database and get 'last' UID
	conn = sqlite3.connect('Factory_Import_Licences.db')
	c = conn.cursor()
	c.execute("SELECT fact_id FROM members ORDER BY fact_id DESC LIMIT 0, 1")
	last_uid = int(c.fetchall()[0][0].replace('M', ''))
	conn.close()
	#Convert result to integer, modify and reformat to UID type string
	new_uid = str(last_uid + 1)
	while len(new_uid) != 3:
		new_uid = '0' + new_uid
	new_uid = 'M' + new_uid
	return new_uid

def add_record(input_tuple, uid):
	conn = sqlite3.connect('Factory_Import_Licences.db')
	c = conn.cursor()
	c.execute("INSERT INTO members VALUES (?,?,?)", input_tuple)
	conn.commit()
	c.execute("SELECT * FROM members WHERE fact_id = ?", (uid,))
	record = c.fetchone()
	conn.close()
	return record
	
def final_data_prep(local_datastore):
	order = local_datastore.order_data
	exports = local_datastore.export_data
	imports = local_datastore.import_data
	coefficients = local_datastore.coefficients_data
	
	#Order data
	final_order_data = collections.OrderedDict()
	final_order_data['id']				 = None
	final_order_data['uid']			 	 = order['uid']
	final_order_data['order_id']		 = order['order_id']
	final_order_data['buyer']			 = " ".join(order['buyer'].strip().upper().split())
	final_order_data['sub_date'] 		 = order['sub_date']
	final_order_data['app_date'] 		 = order['app_date']
	final_order_data['ship_date'] 		 = order['ship_date']
	final_order_data['total_fob_curr'] 	 = order['total_fob_curr']
	final_order_data['total_cmp_curr'] 	 = order['total_cmp_curr']
	final_order_data['total_cif_curr'] 	 = order['total_cif_curr']
	final_order_data['total_fob']		 = locale.atof(order['total_fob'])
	final_order_data['total_cmp']		 = locale.atof(order['total_cmp'])
	final_order_data['total_cif']		 = locale.atof(order['total_cif'])
	final_order_data['export_items'] 	 = order['export_items']
	final_order_data['export_quantity']	 = locale.atoi(order['export_quantity'])		
	final_order_data['import_items'] 	 = order['import_items']
	
	#countries data
	final_country_data = collections.OrderedDict()
	final_country_data['buyer_country1']  = order["buyer_country1"]
	final_country_data['buyer_country2']  = order["buyer_country2"]
	final_country_data['buyer_country3']  = order["buyer_country3"]
	
	
	final_export_data = collections.OrderedDict()
	for x in xrange(1, final_order_data['export_items'] + 1):
		final_export_data['export' + str(x)] = collections.OrderedDict()
		final_export_data['export' + str(x)]['category' + str(x)] = exports['category' + str(x)]
		final_export_data['export' + str(x)]['type' + str(x)] = exports['type' + str(x)]
		final_export_data['export' + str(x)]['description' + str(x)] =  \
				" ".join(exports['description' + str(x)].strip().upper().split())
		final_export_data['export' + str(x)]['units' + str(x)] 	= locale.atoi(exports['units' + str(x)])
		final_export_data['export' + str(x)]['unit_fob_curr' + str(x)] 	= exports['unit_fob_curr' + str(x)]
		final_export_data['export' + str(x)]['unit_fob' + str(x)] = locale.atof(exports['unit_fob' + str(x)])
		final_export_data['export' + str(x)]['unit_cmp_curr' + str(x)] = exports['unit_cmp_curr' + str(x)]
		final_export_data['export' + str(x)]['unit_cmp' + str(x)] = locale.atof(exports['unit_cmp' + str(x)])
	
	final_import_data = collections.OrderedDict()
	for x in xrange(1, final_order_data['import_items'] + 1):
		final_import_data['import' + str(x)] = collections.OrderedDict()
		final_import_data['import' + str(x)]['import_type' + str(x)] = imports['import_type' + str(x)]
		final_import_data['import' + str(x)]['import_description'  + str(x)] = \
			" ".join(imports['import_description'  + str(x)].strip().upper().split())
		final_import_data['import' + str(x)]['import_unit' + str(x) ] = imports['import_unit' + str(x)]
		final_import_data['import' + str(x)]['quantity' + str(x)] = locale.atoi(imports['quantity' + str(x)])
		final_import_data['import' + str(x)]['import_item_curr' + str(x)] = imports['import_item_curr' + str(x)]
		final_import_data['import' + str(x)]['total_price' + str(x)] = locale.atof(imports['total_price' + str(x)])
	
	final_coefficients_data = collections.OrderedDict()
	for x in xrange(1, final_order_data['import_items'] + 1):
		for y in xrange(1, final_order_data['export_items'] + 1):
			final_coefficients_data[str(x) + '_' + str(y)] = \
				locale.atof(coefficients[str(x) + '_' + str(y)])
				
	final_data = {'final_order_data' 		: final_order_data,
				  'final_country_data'		: final_country_data,
				  'final_export_data'		: final_export_data,
				  'final_import_data'		: final_import_data,
				  'final_coefficients_data' : final_coefficients_data}
				  
	return final_data
	
def commit_data(final_data):
	order = final_data['final_order_data']
	countries = final_data['final_country_data']
	exports = final_data['final_export_data']
	imports = final_data['final_import_data']
	coefficients = final_data['final_coefficients_data']
	
	conn = sqlite3.connect('Factory_Import_Licences.db')
	c = conn.cursor()
	
	#Insert into Orders table
	c.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
			  tuple(order.values()))
	order_id = c.lastrowid
	
	#Insert into order_countries table
	country_data = [(order_id, value) for value in countries.values() if value != 'N/A']
	c.executemany("INSERT INTO order_countries VALUES (?, ?)", country_data)
	
	#Insert into export_items table
	export_id_map = {}
	for x in xrange(1, order['export_items'] + 1):
		c.execute("INSERT INTO export_items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
			((order_id, None) + tuple(exports['export' + str(x)].values())))
		export_id_map[x] = c.lastrowid
			
	#Insert into import_items table
	import_id_map = {}
	for x in xrange(1, order['import_items'] + 1):
		c.execute("INSERT INTO input_items VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
			((order_id, None) + tuple(imports['import' + str(x)].values())))
		import_id_map[x] = c.lastrowid
		
	#Insert into import_export_lookup table
	for x in xrange(1, order['import_items'] + 1):
		for y in xrange(1, order['export_items'] + 1):
			if coefficients[str(x) + '_' + str(y)] != 0:
				c.execute("INSERT INTO import_export_lookup VALUES (?, ?, ?)",
					(import_id_map[x], export_id_map[y], coefficients[str(x) + '_' + str(y)]))
					
	retrieval_dict = {'uid' 			: order['uid'],
					  'order_id' 		: order_id,
					  'export_id_map'	: export_id_map,
					  'import_id_map'	: import_id_map}
	conn.commit()
	conn.close()			  
	return retrieval_dict
	
def retrieve_data(retrieval_dict):
	conn = sqlite3.connect('Factory_Import_Licences.db')
	c = conn.cursor()	
	#Get order (and country) data
	c.execute("SELECT * FROM orders WHERE order_id = (?)", (retrieval_dict['order_id'],))
	order = c.fetchone()
	order_data = {'uid'				: order[1],
				  'order_id' 		: order[2],
    			  'buyer'  			: order[3],
    			  'sub_date' 		: order[4],
    			  'app_date' 		: order[5],
				  'ship_date' 		: order[6],
    			  'total_fob_curr'	: order[7],	
    			  'total_cmp_curr' 	: order[8],
    			  'total_cif_curr' 	: order[9],
    			  'total_fob' 		: order[10],
    			  'total_cmp' 		: order[11],
    			  'total_cif' 		: order[12],
    			  'export_items' 	: order[13],
    			  'export_quantity'	: order[14],
    			  'import_items' 	: order[15]}
				  
	c.execute("SELECT destination_country FROM order_countries WHERE order_id = (?)", 
		(retrieval_dict['order_id'],))
	countries = c.fetchall()
	for x in xrange(1, 4):
		try:
			order_data["buyer_country" + str(x)] = countries[x-1][0]
		except IndexError:
			order_data["buyer_country" + str(x)] = 'N/A'
			
	#Get export data
	c.execute("SELECT * FROM export_items WHERE order_id = (?)", (retrieval_dict['order_id'],))
	export = c.fetchall()
	export_data = {}
	for x in xrange(1, order_data['export_items'] + 1):
		export_data['category' + str(x)] = export[x-1][2]
		export_data['type' + str(x)] = export[x-1][3]
		export_data['description' + str(x)] = export[x-1][4]
		export_data['units' + str(x)] = export[x-1][5]
		export_data['unit_fob_curr' + str(x)] = export[x-1][6]
		export_data['unit_fob' + str(x)] = export[x-1][7]
		export_data['unit_cmp_curr' + str(x)] = export[x-1][8]
		export_data['unit_cmp' + str(x)] = export[x-1][9]
		
	#Get import data
	c.execute("SELECT * FROM input_items WHERE order_id = (?)", (retrieval_dict['order_id'],))
	imports = c.fetchall()
	import_data = {}
	for x in xrange(1, order_data['import_items'] + 1):
		import_data['import_type' + str(x)] = imports[x-1][2]
		import_data['import_description'  + str(x)] = imports[x-1][3]
		import_data['import_unit' + str(x)] = imports[x-1][4]
		import_data['quantity' + str(x)] = imports[x-1][5]
		import_data['import_item_curr' + str(x)] = imports[x-1][6]
		import_data['total_price' + str(x)] = imports[x-1][7]
	
	#get coefficients data
	coefficients_data = {}
	for x in xrange(1, order_data['import_items'] + 1):
		for y in xrange(1, order_data['export_items'] + 1):
			c.execute("SELECT input_coefficient FROM import_export_lookup WHERE \
					  input_item_id = (?) and export_item_id = (?)",
					  (retrieval_dict['import_id_map'][x], retrieval_dict['export_id_map'][y]))
			coef = c.fetchone()
			if coef:
				coefficients_data[str(x) + '_' + str(y)] = coef[0]
			else:
				coefficients_data[str(x) + '_' + str(y)] = 0
	conn.close()
	retrieved_data = {'order_data' 			: order_data,
					  'export_data'			: export_data,
					  'import_data'			: import_data,
					  'coefficients_data'	: coefficients_data}
					  
	return retrieved_data
	