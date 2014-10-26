####********************************************************************************************####
####										  IMPORTS											####
####********************************************************************************************####
import bottle as bt
import webbrowser as wb
import pycountry as pyc
import sqlite3 as sql
import re, collections, os, sys, datetime, pickle, urllib
from collections import namedtuple

import utils # Created for this application

#set working directory - SET ACCORDINGLY
os.chdir(r'')

#Create object that will store the partial forms data
datastore_tup = namedtuple('datastore_tup', ['order_data', 'export_data', 
										     'import_data', 'coefficients_data'])

datastore = datastore_tup(None, None, None, None)

####********************************************************************************************####
####										  WELCOME PAGE										####
####********************************************************************************************####
@bt.route('/welcome', method = 'GET')
def welcome():
	"""
	returns : bottle template
	
	Function bound to URL /welcome returns bottle 'welcome' template. Function also sets up the 
	application environment by getting the next factory UID in the series and passing this value
	to the template. The function also creates a dictionary of factories and their associated UIDs
	from the Factory_Import_Licences database which is passed to the template (for use in the drop 
	down menu).
	"""
	conn = sql.connect('Factory_Import_Licences.db')
	c = conn.cursor()
	c.execute("SELECT fact_id, fact_name FROM members ORDER BY fact_name")
	result = c.fetchall()
	conn.close()
	fact_uid_dict = {r[1]: r[0] for r in result}
	new_uid = utils.get_new_uid()
	return bt.template('welcome', new_uid = new_uid, fact_uid_dict = fact_uid_dict)
	

@bt.route('/documentation')
def send_documentation():
	"""
	Function routes user documentation .pdf file to /documentation
	"""
	return bt.static_file('RoryCreedon.pdf',
						   root = r'C:\Users\ipa-lenovo1\Desktop\Application',
						   mimetype = 'application/pdf')
	
####********************************************************************************************####
####										  SEARCH RESULT										####
####********************************************************************************************####
@bt.route('/result', method = 'POST')
def search_result():
	"""
	returns : bottle template
	
	Function bound to URL /result.
	Function get UID value of selected fatctory from /welcome and uses this to access the relevant
	record from the Factory_Import_Licences database, and this record is passed to the template.
	"""
	uid = bt.request.forms.get("UID")
	conn = sql.connect('Factory_Import_Licences.db')
	c = conn.cursor()
	c.execute("SELECT * FROM members WHERE fact_id = ?", (uid,))
	record = c.fetchone()
	conn.close()
	return bt.template("search_result", record = record, uid = uid)

####********************************************************************************************####
####										  ADD RECORD										####
####********************************************************************************************####
@bt.route('/add/<uid>', method = 'GET')
def add_new_record(uid):
	"""
	uid		: string (passed automatically from the dynamic portion of the route)
	returns : bottle template
	
	Function bound to /add/<uid>.
	Function returns template that contains form for adding a new factory to the database. 
	"""
	return bt.template('add_record', uid = uid)

def get_new_record_inputs(uid):
	"""
	uid		: string 
	returns : dict
	
	Function gets values from from on /add/<uid> page and put them in a dict where the values are
	named tuples. This function is called inside the send_new_record_to_validate() function 
	and the commit_new_record() function.
	"""
	validation_tup = namedtuple('validation', ['fieldname', 'value', 'validation_message'])
	uid = uid
	input_dict = {	'uid'			: uid,
					'fact_name' 	: validation_tup('Factory Name', 
									  bt.request.forms.get("fact_name"), None),
					'fact_address'	: validation_tup('Factory Address', 
									  bt.request.forms.get("fact_address"), None),
				 }
	return input_dict
	
@bt.route('/add/<uid>/validate', method = 'POST')
def send_new_record_to_validate(uid):
	"""
	uid		: string (passed automatically from the dynamic portion of the route)
	returns	: function
	
	Function bound to /add/<uid>/validate. 
	Function calls get_new_record_inputs function and passes the resulting dict to the 
	validate_new_record function. 
	"""
	input_dict = get_new_record_inputs(uid)
	return validate_new_record(input_dict)
	
def validate_new_record_inputs(input_dict):
	"""
	input_dict	: dict
	returns		: dict
	
	Function validates the values of the input_dict and creates a validation dict of
	messages that can be displayed to the user. The validation dictionary is an ordered dictionary, 
	and its values are named tuples. Function designed to be called inside the validate_new_record
	function. 
	"""
	validation_Odict = collections.OrderedDict()
	#validate factory name input
	validation_Odict['fact_name'] = utils.not_blank_alnum(input_dict['fact_name'])
	#validate factory address input
	validation_Odict['fact_address'] = utils.not_blank_alnum(input_dict['fact_address'])
	return validation_Odict
	
def validate_new_record(input_dict):
	"""
	input_dict	: dict
	return 		: bottle template
	
	Function calls validate_inputs() function and passes the resulting dictionary to the bottle
	template that helps the user validate the inputs. 
	"""
	uid = input_dict['uid']
	validation_Odict = validate_new_record_inputs(input_dict)
	return bt.template('validate_record', validation_Odict = validation_Odict, uid = uid)
	
@bt.route('/add/<uid>/validate/commit', method = 'POST')
def commit_new_record(uid):
	"""
	uid		: string (passed automatically from the dynamic portion of the route)
	returns	: bottle template
	
	Function bound to /add/<uid>/validate/commit.\n
	Function call the validate_inputs function on the result of the get_new_record_inputs function.
	This is necessary because the user may accidentally make bad changes to verified inputs. If the 
	validation messages are not all of the value 'OK then the validation template is returned,
	otherwise the data are commited to the database."""
	validation_Odict = validate_new_record_inputs(get_new_record_inputs(uid))
	
	if not all([validation_Odict[key].validation_message == 'OK' for key in validation_Odict]):
		return bt.template('validate_record', validation_Odict = validation_Odict, uid = uid)

	#Create Input Tuple
	fact_name = " ".join(validation_Odict["fact_name"].value.strip().upper().split())
	fact_address = " ".join(validation_Odict["fact_address"].value.strip().upper().split())
	input_tuple = (uid, fact_name, fact_address)
	
	#Add record to DB
	record = utils.add_record(input_tuple, uid)
	
	return bt.template("new_record_display", record = record, uid = uid)
	
####********************************************************************************************####
####										  ADD ORDER 										####
####********************************************************************************************####
@bt.route('/order/<uid>', method = 'GET')
def add_order(uid):
	"""
	uid		: string (passed automatically from the dynamic portion of the route)
	returns	: bottle template
	
	Function bound to /order/<uid> 
	Function selects factory name from database based on UID passed as argument and
	returns the template order form, passing the factory name and uid as variables
	to that template. 
	"""
	factory = utils.get_factory_name(uid)
	return bt.template('order', uid = uid, factory = factory)

def get_order_inputs(uid):
	"""
	uid		: string 
	returns	: dict
	
	Function gets values from from on /order/<uid> page and put them in a dict where the values are
	named tuples. This function is called inside the send_order_to_validate() function 
	and the submit_order() function.
	"""
	validation_tup = namedtuple('validation', ['fieldname', 'value', 'validation_message'])
	uid = uid
	order_dict = {'uid'				: uid,
				  'factory'			: validation_tup("Exporter", 
									  bt.request.forms.get("exporter"), "OK"),
				  'order_id' 		: validation_tup("Order ID", 
									  bt.request.forms.get("order_id"), None),
				  'buyer'	 		: validation_tup("Buyer", 
									  bt.request.forms.get("buyer"), None),
				  'buyer_country1' 	: validation_tup("Buyer Country 1", 
									  bt.request.forms.get("buyer_country1"), None),
				  'buyer_country2'	: validation_tup("Buyer Country 2", 
									  bt.request.forms.get("buyer_country2"), None),
				  'buyer_country3'	: validation_tup("Buyer Country 3", 
									  bt.request.forms.get("buyer_country3"), None),
				  'sub_date'		: validation_tup("Submission Date", 
									  bt.request.forms.get("sub_date"), None),
				  'app_date' 		: validation_tup("Approval Date", 
									  bt.request.forms.get("app_date"), None),
				  'ship_date' 		: validation_tup("Shipment Date", 
									  bt.request.forms.get("ship_date"), None),
				  "total_fob_curr"  : validation_tup("Total FOB Currency", 
									  bt.request.forms.get("total_fob_curr"), None),
				  "total_cmp_curr"  : validation_tup("Total CMP Currency", 
									  bt.request.forms.get("total_cmp_curr"), None),
				  "total_cif_curr"  : validation_tup("Total CIF Currency", 
									  bt.request.forms.get("total_cif_curr"), None),
				  "total_fob"       : validation_tup("Total FOB Value", 
									  bt.request.forms.get("total_fob"), None),
				  "total_cmp"       : validation_tup("Total CMP Value",
									  bt.request.forms.get("total_cmp"), None),
				  "total_cif"       : validation_tup("Total CIF Value", 
									  bt.request.forms.get("total_cif"), None),
				  'export_items' 	: validation_tup("Export Items", 
									  int(bt.request.forms.get("export_items")), None),
				  'export_quantity' : validation_tup("Total Quantity of Export Items", 
									  bt.request.forms.get("export_quantity"), None),
				  'import_items' 	: validation_tup("Import Items", 
									  int(bt.request.forms.get("import_items")), None)
				  }
	return order_dict
	
@bt.route('/order/<uid>/validate', method = "POST")
def send_order_to_validate(uid):
	"""
	uid		: string (passed automatically from the dynamic portion of the route)
	returns	: function
	
	Function bound to /order/<uid>/validate. 
	Function calls get_order_inputs function and passes the resulting dict to the 
	validate_order function. 
	"""
	order_dict = get_order_inputs(uid)
	return validate_order(order_dict)
	
def validate_order_inputs(order_dict):
	"""
	order_dict	: dict
	returns		: dict
	
	Function validates the values of the order_dict and creates a validation dict of
	messages that can be displayed to the user. The validation dictionary is an ordered dictionary, 
	and its values are named tuples. Function designed to be called inside the validate_order
	function. 
	"""
	validation_Odict = collections.OrderedDict()
	#validate order id
	validation_Odict['order_id'] = utils.not_blank_numeric_code(order_dict['order_id'])
	#exporter (does not need verification)
	validation_Odict['exporter'] = order_dict['factory']
	#validate buyer
	validation_Odict['buyer'] = utils.not_blank_alnum(order_dict['buyer'])
		
	#validate buyer countries
	non_NAs = [order_dict['buyer_country' + str(x)].value for x in xrange(1, 4) 
			   if order_dict['buyer_country' + str(x)].value != 'N/A']
	if all([order_dict['buyer_country' + str(x)].value == 'N/A' for x in xrange(1, 4)]):
		for x in xrange(1, 4):
			validation_Odict['buyer_country' + str(x)] = \
			order_dict['buyer_country' + str(x)]._replace(validation_message = \
			"Please enter at least one valid buyer country")
	elif order_dict['buyer_country1'].value == 'N/A':
		for x in xrange(1, 4):
			validation_Odict['buyer_country' + str(x)] = \
			order_dict['buyer_country' + str(x)]._replace(validation_message = \
			"Please do not leave country 1 blank")	
	elif len(non_NAs) != len(set(non_NAs)):
		for x in xrange(1, 4):
			validation_Odict['buyer_country' + str(x)] = \
			order_dict['buyer_country' + str(x)]._replace(validation_message = \
			"If entering more than once country, please ensure they are distinct")
	elif order_dict['buyer_country2'].value == 'N/A' and order_dict['buyer_country3'].value !='N/A':
		for x in xrange(1, 4):
			validation_Odict['buyer_country' + str(x)] = \
			order_dict['buyer_country' + str(x)]._replace(validation_message = \
			"Please do not leave the second country country blank if entering a third country")
	else:
		for x in xrange(1, 4):
			validation_Odict['buyer_country' + str(x)] = \
			order_dict['buyer_country' + str(x)]._replace(validation_message = "OK")
	
	#validate fob curr
	validation_Odict["total_fob_curr"] = utils.not_blank(order_dict["total_fob_curr"])
	#validate fob total
	validation_Odict["total_fob"] = utils.not_blank_price(order_dict["total_fob"])
	#validate cmp curr
	validation_Odict["total_cmp_curr"] = utils.not_blank(order_dict["total_cmp_curr"])
	#validate cmp total
	validation_Odict["total_cmp"] = utils.not_blank_price(order_dict["total_cmp"])
	#validate cif curr
	validation_Odict["total_cif_curr"] = utils.not_blank(order_dict["total_cif_curr"])
	#validate cif total
	validation_Odict["total_cif"] = utils.not_blank_price(order_dict["total_cif"])
	#validate submission Date
	validation_Odict['sub_date'] = utils.not_blank(order_dict['sub_date'])
	#validate approval Date
	validation_Odict['app_date'] = utils.not_blank(order_dict['app_date'])
	#validate approval Date
	validation_Odict['ship_date'] = utils.not_blank(order_dict['ship_date'])	

	#validate export Items
	if order_dict['export_items'].value == 0:
		validation_Odict['export_items'] = \
		order_dict['export_items']._replace(validation_message = "Export Items cannot be zero")
	else:
		validation_Odict['export_items'] = \
		order_dict['export_items']._replace(validation_message = "OK")
	
	validation_Odict['export_quantity'] = utils.not_blank_integer(order_dict['export_quantity'])
	#validate import Items
	if order_dict['import_items'].value == 0:
		validation_Odict['import_items'] = \
		order_dict['import_items']._replace(validation_message = "Import Items cannot be zero")
	else:
		validation_Odict['import_items'] = \
		order_dict['import_items']._replace(validation_message = "OK")

	return validation_Odict
	
def validate_order(order_dict):
	"""
	order_dict	: dict
	return 		: bottle template
	
	Function calls validate_order_inputs() function and passes the resulting dictionary to the 
	bottle template that helps the user validate the inputs. 
	"""
	validation_Odict = validate_order_inputs(order_dict)
	uid = order_dict['uid']
	return bt.template('validate_order', validation_Odict = validation_Odict, uid = uid)
	
@bt.route('/order/<uid>/submit', method = 'post')
def submit_order_redirect(uid):
	"""
	uid		: string (passed automatically from the dynamic portion of the route)
	returns	: bottle template or None
	
	Function bound to /order/<uid>/submit. 
	Function performs a last data validation check by calling validate_order_inputs() on the 
	result of calling get_order_inputs(). If there are no validation errors, then the data
	are stored in the global datastore, and the browser is redirected to begin the 
	export items form. If there are validation errors then the validation template is returned. 
	"""
	global datastore
	validation_Odict = validate_order_inputs(get_order_inputs(uid))
	if not all([validation_Odict[key].validation_message == 'OK' for key in validation_Odict]):
		return bt.template('validate_order', validation_Odict = validation_Odict, uid = uid)
	order_data = {'uid'				: uid,
				  'order_id' 		: validation_Odict["order_id"].value,
				  'buyer'  			: validation_Odict["buyer"].value,
				  'buyer_country1' 	: validation_Odict["buyer_country1"].value,
				  'buyer_country2' 	: validation_Odict["buyer_country2"].value,
				  'buyer_country3' 	: validation_Odict["buyer_country3"].value,
				  'sub_date' 		: validation_Odict["sub_date"].value,
				  'app_date' 		: validation_Odict["app_date"].value,
				  'ship_date' 		: validation_Odict["ship_date"].value,
				  'total_fob_curr' 	: validation_Odict["total_fob_curr"].value,
				  'total_cmp_curr' 	: validation_Odict["total_cmp_curr"].value,
				  'total_cif_curr' 	: validation_Odict["total_cif_curr"].value,
				  'total_fob' 		: validation_Odict["total_fob"].value,
				  'total_cmp' 		: validation_Odict["total_cmp"].value,
				  'total_cif' 		: validation_Odict["total_cif"].value,
				  'export_items' 	: validation_Odict["export_items"].value,
				  'export_quantity'	: validation_Odict["export_quantity"].value,
				  'import_items' 	: validation_Odict["import_items"].value,
				  }
	datastore = datastore._replace(order_data = order_data)
	bt.redirect('http://localhost:8080/export/' + uid + '/' + str(order_data['export_items']))
	return
####********************************************************************************************####
####									ADD EXPORT ITEMS 										####
####********************************************************************************************####
@bt.route('/export/<uid>/<export_items>', method = 'GET')
def add_export_items(uid, export_items):
	"""
	uid				: string (passed automatically from the dynamic portion of the route)
	export_items	: string (passed automatically from the dynamic portion of the route)
	returns			: bottle template
	
	Function bound to /export/<uid>/<export_items>
	Function selects factory name from database based on UID passed as argument and
	returns the template order form, passing the factory name, uid  and export_items
	as variables to that template. 
	"""
	factory =  utils.get_factory_name(uid)
	return bt.template('export_items', export_items = int(export_items), 
						uid = uid, factory = factory)

def get_export_inputs(uid, export_items):
	"""
	uid				: string 
	export_items	: string 
	returns			: dict
	
	Function gets values from form on /export/<uid>/<export_items> page and put them in a dict where 
	the values are named tuples. This function is called inside the send_export_to_validate() 
	function and the submit_export_redirect() function.
	"""
	validation_tup = namedtuple('validation', ['fieldname', 'value', 'validation_message'])
	uid = uid
	export_dict = {'uid' 		  : uid,
				   'export_items' : int(export_items)}
	for x in xrange(1, int(export_items) + 1):
		export_dict.update({
				'category' + str(x)		: validation_tup("Item Description",
										  bt.request.forms.get("category" + str(x)), None),
				'type' + str(x)			: validation_tup("Item Type",
										  bt.request.forms.get("type" + str(x)), None),
				'description' + str(x) 	: validation_tup("Item Description", 
										  bt.request.forms.get("description" + str(x)), None),
				'units' + str(x) 	   	: validation_tup("Number of Units", 
										  bt.request.forms.get("units" + str(x)), None),
				'unit_fob_curr' + str(x): validation_tup("Unit FOB Currency", 
										  bt.request.forms.get("unit_fob_curr" + str(x)), None),
				'unit_fob' + str(x)		: validation_tup("Unit FOB Amount", 
										  bt.request.forms.get("unit_fob" + str(x)), None),
				'unit_cmp_curr' + str(x): validation_tup("Unit CMP Currency", 
										  bt.request.forms.get("unit_cmp_curr" + str(x)), None),
				'unit_cmp' + str(x)		: validation_tup("Unit CMP Amount", 
										  bt.request.forms.get("unit_cmp" + str(x)), None)
						   })
	return export_dict

@bt.route('/export/<uid>/<export_items>/validate', method = "POST")
def send_export_to_validate(uid, export_items):
	"""
	uid				: string (passed automatically from the dynamic portion of the route)
	export_items	: string (passed automatically from the dynamic portion of the route)
	returns			: function
	
	Function bound to /export/<uid>/<export_items>/validate. 
	Function calls get_export_inputs function and passes the resulting dict to the 
	validate_export() function. 
	"""
	export_dict = get_export_inputs(uid, export_items)
	return validate_export(export_dict)
	
def validate_export_inputs(export_dict):
	"""
	export_dict	: dict
	returns		: dict
	
	Function validates the values of the export_dict and creates a validation dict of
	messages that can be displayed to the user. The validation dictionary is an ordered dictionary, 
	and its values are named tuples. Function designed to be called inside the validate_export()
	function. 
	"""
	validation_Edict = collections.OrderedDict()
	export_items = export_dict['export_items']
	for x in xrange(1, int(export_items) + 1):
		validation_Edict['category' + str(x)] = \
						 utils.not_blank(export_dict['category' + str(x)])
		validation_Edict['type' + str(x)] = \
						 utils.not_blank(export_dict['type' + str(x)])
		validation_Edict['description' + str(x)] = \
						 utils.not_blank_alpha(export_dict['description' + str(x)])
		validation_Edict['units' + str(x)] = \
						 utils.not_blank_integer(export_dict['units' + str(x)])
		validation_Edict['unit_fob_curr' + str(x)] = \
						 utils.not_blank(export_dict['unit_fob_curr' + str(x)])
		validation_Edict['unit_fob' + str(x)] = \
						 utils.not_blank_float(export_dict['unit_fob' + str(x)])
		validation_Edict['unit_cmp_curr' + str(x)] = \
						 utils.not_blank(export_dict['unit_cmp_curr' + str(x)])
		validation_Edict['unit_cmp' + str(x)] = \
						 utils.not_blank_float(export_dict['unit_cmp' + str(x)])
	return validation_Edict
	
def validate_export(export_dict):
	"""
	order_dict	: dict
	return 		: bottle template
	
	Function calls validate_export_inputs() function and passes the resulting dictionary to the 
	bottle template that helps the user validate the inputs. 
	"""
	factory = utils.get_factory_name(export_dict['uid'])
	uid = export_dict['uid']
	export_items = export_dict['export_items']
	validation_Edict = validate_export_inputs(export_dict)
	return bt.template('validate_export_items', validation_Edict = validation_Edict, uid = uid, 
					   factory = factory, export_items = export_items)
		
@bt.route('/export/<uid>/<export_items>/submit', method = "POST")
def submit_export_redirect(uid, export_items):
	"""
	uid				: string (passed automatically from the dynamic portion of the route)
	export_items	: string (passed automatically from the dynamic portion of the route)
	returns			: bottle template or None
	
	Function bound to /export/<uid>/<export_items>/submit. 
	Function performs a last data validation check by calling validate_export_inputs() on the 
	result of calling get_export_inputs(). If there are no validation errors, then the data
	are stored in the global datastore, and the browser is redirected to begin the 
	import items form. If there are validation errors then the validation template is returned. 
	"""
	global datastore
	factory = utils.get_factory_name(uid)
	export_items = int(export_items)
	validation_Edict = validate_export_inputs(get_export_inputs(uid, export_items))
	if not all([validation_Edict[key].validation_message == 'OK' for key in validation_Edict]):
		return bt.template('validate_export_items', validation_Edict = validation_Edict, uid = uid, 
					   factory = factory, export_items = export_items)
	export_data = {}
	import_items = datastore.order_data['import_items'] #gets number of import items
	for x in xrange(1, export_items + 1):
		export_data.update({
				'category' + str(x)		: validation_Edict['category' + str(x)].value,
				'type' + str(x)			: validation_Edict['type' + str(x)].value,
				'description' + str(x) 	: validation_Edict["description" + str(x)].value,
		        'units' + str(x) 	   	: validation_Edict["units" + str(x)].value,
		        'unit_fob_curr' + str(x): validation_Edict["unit_fob_curr" + str(x)].value,
		        'unit_fob'  + str(x)	: validation_Edict["unit_fob" + str(x)].value,
		        'unit_cmp_curr' + str(x): validation_Edict["unit_cmp_curr" + str(x)].value,
		        'unit_cmp' + str(x)		: validation_Edict["unit_cmp" + str(x)].value,
						  })
	datastore = datastore._replace(export_data = export_data)
	bt.redirect('http://localhost:8080/import/' + uid + '/' + str(import_items))

####********************************************************************************************####
####									ADD IMPORT ITEMS 										####
####********************************************************************************************####
@bt.route('/import/<uid>/<import_items>', method = 'GET')
def add_import_items(uid, import_items):
	"""
	uid				: string (passed automatically from the dynamic portion of the route)
	import_items	: string (passed automatically from the dynamic portion of the route)
	returns			: bottle template
	
	Function bound to /import/<uid>/<import_items>  
	Function selects factory name from database based on UID passed as argument and
	returns the template order form, passing the factory name, uid  and import_items
	as variables to that template. 
	"""
	factory = utils.get_factory_name(uid)
	return bt.template("import_items", uid = uid, import_items = int(import_items), 
						factory = factory)
	
def get_import_inputs(uid, import_items):
	"""
	uid				: string 
	import_items	: string 
	returns			: dict
	
	Function gets values from form on /import/<uid>/<import_items> page and put them in a dict where 
	the values are named tuples. This function is called inside the send_import_to_validation() 
	function and the submit_import_redirect() function.
	"""
	validation_tup = namedtuple('validation', ['fieldname', 'value', 'validation_message'])
	uid = uid
	import_dict = {'uid' 		  : uid,
				   'import_items' : int(import_items)}
	for x in xrange(1, int(import_items) + 1):
		import_dict.update({
			'import_type' + str(x) 		  : validation_tup("Type", 
										    bt.request.forms.get('import_type' + str(x)),
											None),
			'import_description'  + str(x): validation_tup("Description", 
										    bt.request.forms.get('import_description'  + str(x)),
											None),
			'import_unit' + str(x) 		  : validation_tup("Unit of Measure", 
										    bt.request.forms.get('import_unit' + str(x)),
											None),
			'quantity' + str(x)   		  : validation_tup("Quantity", 
										    bt.request.forms.get('quantity' + str(x)),
											None),
			'import_item_curr' + str(x)   : validation_tup("Unit Currency", 
										    bt.request.forms.get('import_item_curr' + str(x)),
											None),
			'total_price' + str(x) 	  	  : validation_tup("Total Price", 
											bt.request.forms.get('total_price' + str(x)),
											None)
						   })
	return import_dict
	
@bt.route('/import/<uid>/<import_items>/validate', method = 'POST')
def send_import_to_validation(uid, import_items):
	"""
	uid				: string (passed automatically from the dynamic portion of the route)
	import_items	: string (passed automatically from the dynamic portion of the route)
	returns			: function
	
	Function bound to /export/<uid>/<import_items>/validate. 
	Function calls get_import_inputs function and passes the resulting dict to the 
	validate_import() function. 
	"""
	import_dict = get_import_inputs(uid, import_items)
	return validate_import(import_dict)

def validate_import_inputs(import_dict):
	"""
	import_dict	: dict
	returns		: dict
	
	Function validates the values of the import_dict and creates a validation dict of
	messages that can be displayed to the user. The validation dictionary is an ordered dictionary, 
	and its values are named tuples. Function designed to be called inside the validate_import()
	function. 
	"""
	import_items = import_dict['import_items']
	validation_Idict = collections.OrderedDict()
	for x in xrange(1, int(import_items) + 1):
		validation_Idict['import_type' + str(x)] = \
						 utils.not_blank(import_dict['import_type' + str(x)])
		validation_Idict['import_description' + str(x)] = \
						 utils.not_blank_alnum(import_dict['import_description' + str(x)])
		validation_Idict['import_unit' + str(x)] = \
						 utils.not_blank(import_dict['import_unit' + str(x)])
		validation_Idict['quantity' + str(x)] = \
						 utils.not_blank_integer(import_dict['quantity' + str(x)])
		validation_Idict['import_item_curr' + str(x)] = \
						 utils.not_blank(import_dict['import_item_curr' + str(x)])
		validation_Idict['total_price' + str(x)] = \
						 utils.not_blank_price(import_dict['total_price' + str(x)])
	return validation_Idict

def validate_import(import_dict):
	"""
	import_dict	: dict
	return 		: bottle template
	
	Function calls validate_import_inputs() function and passes the resulting dictionary to the 
	bottle template that helps the user validate the inputs. 
	"""
	factory = utils.get_factory_name(import_dict['uid'])
	uid = import_dict['uid']
	import_items = import_dict['import_items']
	validation_Idict = validate_import_inputs(import_dict)
	return bt.template('validate_import_items', validation_Idict = validation_Idict, uid = uid, 
					   factory = factory, import_items = import_items)
	

@bt.route('/import/<uid>/<import_items>/submit', method = 'POST')
def submit_import_redirect(uid, import_items):
	"""
	uid				: string (passed automatically by dynamic portion of the route)
	import_items	: string (passed automatically from the dynamic portion of the route)
	returns			: bottle template or None
	
	Function bound to /import/<uid>/<import_items>/submit. 
	Function performs a last data validation check by calling validate_import_inputs() on the 
	result of calling get_import_inputs(). If there are no validation errors, then the data
	are stored in the global datastore, and the browser is redirected to begin the 
	coefficients form. If there are validation errors then the validation template is returned. 
	"""
	global datastore
	factory = utils.get_factory_name(uid)
	import_items = int(import_items)
	
	#return validation template if not all validation messages equal 'OK'. 
	validation_Idict = validate_import_inputs(get_import_inputs(uid, import_items))
	if not all([validation_Idict[key].validation_message == 'OK' for key in validation_Idict]):
		return bt.template('validate_import_items', validation_Idict = validation_Idict, uid = uid, 
					   factory = factory, import_items = import_items)
	
	#create dictionary of verified imports data and put in datastore
	import_data = {}
	for x in xrange(1, import_items + 1):
		import_data.update({
			'import_type' + str(x) 		 : validation_Idict['import_type' + str(x)].value,
			'import_description' + str(x): validation_Idict['import_description' + str(x)].value,
			'import_unit' + str(x) 		 : validation_Idict['import_unit' + str(x)].value,
			'quantity' + str(x) 		 : validation_Idict['quantity' + str(x)].value,
			'import_item_curr' + str(x)  : validation_Idict['import_item_curr' + str(x)].value,
			'total_price' + str(x) 		 : validation_Idict['total_price' + str(x)].value,
						  })	
	datastore = datastore._replace(import_data = import_data)
	
	#redirect
	export_items = datastore.order_data['export_items'] # get number export items from export form.
	bt.redirect('http://localhost:8080/coefficients/' + uid + '/' 
				+ str(export_items) + '/' + str(import_items))
	return
####********************************************************************************************####
####									ADD COEFFICIENTS										####
####********************************************************************************************####

def get_items_from_datastore(export_items, import_items):
	"""
	export_items	: int
	import_items	: int
	returns			: dict
	
	Function accessed the global statstore to retrieve information about the export items, import
	items and unit of measure as entered previously on forms at /import/<uid>/<export_items> and
	/import/<uid>/<import_items>. The information is stored in dicts who's values are lists.
	Function is called inside add_coefficients().
	"""
	global datastore
	items_dict = {'export_list' : [datastore.export_data['description' + str(x)] 
								   for x in xrange(1, export_items + 1)],
				  'import_list' : [datastore.import_data['import_description'  + str(x)] 
								   for x in xrange(1, import_items + 1)],
				  'units_list'  : [datastore.import_data['import_unit'  + str(x)] 
								   for x in xrange(1, import_items + 1)]
				  }
	return items_dict

@bt.route('/coefficients/<uid>/<export_items>/<import_items>', method = 'GET')
def add_coefficients(uid, export_items, import_items):
	"""
	uid				: string (passed automatically from the dynamic portion of the route)
	export_items	: string (passed automatically from the dynamic portion of the route)
	import_items	: string (passed automatically from the dynamic portion of the route)
	returns			: bottle template
	
	Function bound to /coefficients/<uid>/<export_items>/<import_items> 
	Function selects factory name from database based on UID passed as argument and
	returns the template coefficients form, passing the factory name, uid, export items,
	and import_items as variables to that template.
	"""
	uid = uid
	factory = utils.get_factory_name(uid)
	export_items = int(export_items)
	import_items = int(import_items)
	items_dict = get_items_from_datastore(export_items, import_items)
	return bt.template('coefficients', uid = uid, items_dict = items_dict, factory = factory)

def get_coefficients_inputs(uid, export_items, import_items):
	"""
	uid				: string 
	export_items	: string 
	import_items	: string 
	returns			: dict
	
	Function gets values from form on /coefficients/<uid>/<export_items>/<import_items> page and put 
	them in a dict where the values are named tuples. This function is called inside the 
	send_coefficients_to_validate() function and the submit_coefficients_redirect() function.
	"""
	validation_tup = namedtuple('validation', ['fieldname', 'value', 'validation_message'])
	uid = uid
	coefficient_dict = {'uid' 		 	: uid,
						'export_items'	: int(export_items),
						'import_items'	: int(import_items)}
	for x in xrange(1, int(import_items) + 1):
		for y in xrange(1, int(export_items) + 1):
			coefficient_dict[str(x) + '_' + str(y)] = validation_tup("Coefficient", 
													  bt.request.forms.get(str(x) + '_' + str(y)),
													  None)
	return coefficient_dict

@bt.route('/coefficients/<uid>/<export_items>/<import_items>/validate', method = "POST")
def send_coefficients_to_validate(uid, export_items, import_items):
	"""
	uid				: string (passed automatically from the dynamic portion of the route)
	export_items	: string (passed automatically from the dynamic portion of the route)
	import_items	: string (passed automatically from the dynamic portion of the route)
	returns			: function
	
	Function bound to /coefficients/<uid>/<export_items>/<import_items>/validate. 
	Function calls get_coefficients_inputs() function and passes the resulting dict to the 
	validate_coefficients() function. 
	"""
	coefficient_dict = get_coefficients_inputs(uid, export_items, import_items)
	return validate_coefficients(coefficient_dict)
	
def validate_coefficients_input(coefficient_dict):
	"""
	coefficient_dict	: dict
	returns				: dict
	
	Function validates the values of the coefficient_dict and creates a validation dict of
	messages that can be displayed to the user. The validation dictionary is an ordered dictionary, 
	and its values are named tuples. Function designed to be called inside the validate_coefficients
	function. 
	"""
	import_items = coefficient_dict['import_items']
	export_items = coefficient_dict['export_items']
	validation_Cdict = collections.OrderedDict()
	for x in xrange(1, import_items + 1):
		for y in xrange(1, export_items + 1):
			validation_Cdict[str(x) + '_' + str(y)] = \
			utils.not_blank_coefficients(coefficient_dict[str(x) + '_' + str(y)])
	return validation_Cdict

def validate_coefficients(coefficient_dict):
	"""
	coefficient_dict	: dict
	return 				: bottle template
	
	Function calls validate_coefficients_input() function and passes the resulting dictionary to the 
	bottle template that helps the user validate the inputs. 
	"""
	uid = coefficient_dict['uid']
	export_items = coefficient_dict['export_items']
	import_items = coefficient_dict['import_items']
	items_dict = get_items_from_datastore(export_items, import_items)
	factory = utils.get_factory_name(uid)
	validation_Cdict = validate_coefficients_input(coefficient_dict)
	return bt.template("validate_coefficients", uid = uid, validation_Cdict = validation_Cdict,
						items_dict = items_dict, factory = factory) 
						
@bt.route('/coefficients/<uid>/<export_items>/<import_items>/submit', method = 'POST')
def submit_coefficients_redirect(uid, export_items, import_items):
	"""
	uid				: string (passed automatically from the dynamic portion of the route)
	exportt_items	: string (passed automatically from the dynamic portion of the route)
	import_items	: string (passed automatically from the dynamic portion of the route)
	returns			: bottle template or None
	
	Function bound to /coefficients/<uid>/<export_items>/<import_items>/submit. 
	Function performs a last data validation check by calling validate_coefficients_input() on the 
	result of calling get_coefficients_inputs(). If there are no validation errors, then the data
	are stored in the global datastore, and the browser is redirected to begin the 
	final review form. If there are validation errors then the validation template is returned. 
	"""
	global datastore
	uid = uid
	export_items = int(export_items)
	import_items = int(import_items)
	items_dict = get_items_from_datastore(export_items, import_items)
	factory = utils.get_factory_name(uid)
	#return validation template if not all validation messages equal 'OK'. 
	validation_Cdict = validate_coefficients_input(get_coefficients_inputs(uid, export_items, 
																		   import_items))
	if not all([validation_Cdict[key].validation_message == 'OK' for key in validation_Cdict]):
		return bt.template("validate_coefficients", uid = uid, validation_Cdict = validation_Cdict,
							items_dict = items_dict, factory = factory)
	
	#create dictionary of verified coefficients data and put in datastore
	coefficients_data = {}
	for x in xrange(1, import_items + 1):
		for y in xrange(1, export_items + 1):
			coefficients_data[str(x) + '_' + str(y)] = validation_Cdict[str(x) + '_' + str(y)].value
	datastore = datastore._replace(coefficients_data = coefficients_data)
	
	#redirect
	bt.redirect('http://localhost:8080/review/' + uid + '/' + str(export_items) + '/' + str(import_items))
	return

####********************************************************************************************####
####										REVIEW		        								####
####********************************************************************************************####
@bt.route('/review/<uid>/<export_items>/<import_items>', method = 'GET')
def review_data(uid, export_items, import_items):
	"""
	uid				: string (passed automatically from the dynamic portion of the route)
	export_items	: string (passed automatically from the dynamic portion of the route)
	import_items	: string (passed automatically from the dynamic portion of the route)
	returns			: bottle template
	
	Function bound to /review/<uid>/<export_items>/<import_items>.
	Function retrieves the data stored so far in the data store and puts it in the review_data
	dict. Function calls utils.review_checks function to create messages_dict which contains
	messages as to where key data points do not sum up etc. The review_data and the messages_dict
	are passed to the template this function returns.
	"""
	global datastore
	review_data = {	'order_data' 		: datastore.order_data,
					'export_data'		: datastore.export_data,
					'import_data'		: datastore.import_data,
					'coefficients_data'	: datastore.coefficients_data}
	uid = uid
	factory = utils.get_factory_name(uid)
	messages_dict = utils.review_checks(review_data, True, True, True, True)
	return bt.template('review', review_data = review_data, uid = uid, factory = factory, 
					   messages_dict = messages_dict)
						
def get_review_inputs(uid, export_items, import_items):
	"""
	uid 			: string
	export_items	: string
	import_items	: string
	returns			: dict
	
	Function gets values from form on /review/<uid>/<export_items>/<import_items>, and places them
	in the review_dict which is returned. The dictionary has values that are named tuples. One of 
	named tuple fields (as in previous functions) is 'filedname'. In previous functions this was
	simply the input field from the form to which the data relate. The system changes here such that
	the fieldname also referecnes the export/import to which the field relates. For this reason the
	export and import data from the datastore are accessed such that the fieldnames can be formatted
	with specific imports/exports. The necessity of doing this is that the fieldnames and validation
	messages on the /review/<uid>/<export_items>/<import_items>/validate page are presented as the
	were previously (in the table to which the data belong) but above the relevant table. 
	Function is called within get_review_inputs funtion and submit_form function. 
	"""
	global datastore
	export_data = datastore.export_data
	import_data = datastore.import_data
	coefficients_data = datastore.coefficients_data
	
	validation_tup = namedtuple('validation', ['fieldname', 'value', 'validation_message'])
	uid = uid
	export_items = int(export_items)
	import_items = int(import_items)
	review_dict = { 
			"uid" 			 			: uid,
			"export_items"				: export_items,
			"import_items"				: import_items,
			"total_fob_curr"  			: validation_tup("Total FOB Currency", 
										  bt.request.forms.get("total_fob_curr"), None),
			"total_cmp_curr"  			: validation_tup("Total CMP Currency", 
										  bt.request.forms.get("total_cmp_curr"), None),
			"total_cif_curr"  			: validation_tup("Total CIF Currency", 
										  bt.request.forms.get("total_cif_curr"), None),
			"total_fob"      	 		: validation_tup("Total FOB Value", 
										  bt.request.forms.get("total_fob"), None),
			"total_cmp"       			: validation_tup("Total CMP Value",
										  bt.request.forms.get("total_cmp"), None),
			"total_cif"       			: validation_tup("Total CIF Value", 
										  bt.request.forms.get("total_cif"), None),
			"export_quantity" 			: validation_tup("Total Quantity of Export Items",
										  bt.request.forms.get("export_quantity"), None)}
	
	for x in xrange(1, int(export_items) + 1):
		review_dict.update({
			"units" + str(x) 	   		: validation_tup("Number of Units ({})".format(\
										  export_data['description' + str(x)]), 
										  bt.request.forms.get("units" + str(x)), None),
			"unit_fob_curr" + str(x)	: validation_tup("Unit FOB Currency ({})".format(\
										  export_data['description' + str(x)]), 
										  bt.request.forms.get("unit_fob_curr" + str(x)), None),
			"unit_fob" + str(x)			: validation_tup("Unit FOB Amount ({})".format(\
										  export_data['description' + str(x)]), 
										  bt.request.forms.get("unit_fob" + str(x)), None),
			"unit_cmp_curr" + str(x)	: validation_tup("Unit CMP Currency ({})".format(\
										  export_data['description' + str(x)]), 
										  bt.request.forms.get("unit_cmp_curr" + str(x)), None),
			"unit_cmp" + str(x)			: validation_tup("Unit CMP Amount ({})".format(\
										  export_data['description' + str(x)]), 
										  bt.request.forms.get("unit_cmp" + str(x)), None)})
									
	for x in xrange(1, int(import_items) + 1):
		review_dict.update({
			"import_unit" + str(x) 		  : validation_tup("Unit of Measure ({})".format(\
											import_data['import_description'  + str(x)]), 
										    bt.request.forms.get("import_unit" + str(x)),
											None),
			"quantity" + str(x)   		  : validation_tup("Quantity ({})".format(\
											import_data['import_description'  + str(x)]), 
										    bt.request.forms.get("quantity" + str(x)),
											None),
			"import_item_curr" + str(x)   : validation_tup("Unit Currency ({})".format(\
											import_data['import_description'  + str(x)]), 
										    bt.request.forms.get("import_item_curr" + str(x)),
											None),
			"total_price" + str(x) 	  	  : validation_tup("Total Price ({})".format(\
											import_data['import_description'  + str(x)]), 
											bt.request.forms.get("total_price" + str(x)),
											None)})								   
	
	for x in xrange(1, int(import_items) + 1):
		for y in xrange(1, int(export_items) + 1):
			review_dict[str(x) + '_' + str(y)] = validation_tup("Coefficient ({}, {})".format(\
													  import_data['import_description'  + str(x)],
													  export_data['description' + str(y)]),
													  bt.request.forms.get(str(x) + '_' + str(y)),
													  None)
	return review_dict

@bt.route('/review/<uid>/<export_items>/<import_items>/validate', method = "POST")
def send_review_to_validate(uid, export_items, import_items):
	"""
	uid				: string (passed automatically from the dynamic portion of the route)
	export_items	: string (passed automatically from the dynamic portion of the route)
	import_items	: string (passed automatically from the dynamic portion of the route)
	returns			: function
	
	Function bound to /review/<uid>/<export_items>/<import_items>/validate. 
	Function calls get_review_inputs() function and passes the resulting dict to the 
	validate_review() function. 
	"""
	review_dict = get_review_inputs(uid, export_items, import_items)
	return validate_review(review_dict)
	
def validate_review_inputs(review_dict):
	"""
	review_dict	: dict
	returns		: dict
	
	Function validates the values of the review_dict and creates a validation dict of
	messages that can be displayed to the user. Unlike previous functions the validation_dict has
	values that are themselves dictionaries. These dictionaries pertain to each field in the 
	datastore. 
	"""
	export_items = int(review_dict['export_items'])
	import_items = int(review_dict['import_items'])
	order_validation = collections.OrderedDict()
	export_validation = collections.OrderedDict()
	import_validation = collections.OrderedDict()
	coefficients_validation = collections.OrderedDict()
	
	order_validation["total_fob_curr"] = utils.not_blank(review_dict["total_fob_curr"])
	order_validation["total_fob"] = utils.not_blank_price(review_dict["total_fob"])
	order_validation["total_cmp_curr"] = utils.not_blank(review_dict["total_cmp_curr"])
	order_validation["total_cmp"] = utils.not_blank_price(review_dict["total_cmp"])
	order_validation["total_cif_curr"] = utils.not_blank(review_dict["total_cif_curr"])
	order_validation["total_cif"] = utils.not_blank_price(review_dict["total_cif"])
	order_validation['export_quantity'] = utils.not_blank_integer(review_dict['export_quantity'])

	for x in xrange(1, export_items + 1):
		export_validation['units' + str(x)] = \
					utils.not_blank_integer(review_dict['units' + str(x)])
		export_validation['unit_fob_curr' + str(x)] = \
					utils.not_blank(review_dict['unit_fob_curr' + str(x)])
		export_validation['unit_fob' + str(x)] = \
					utils.not_blank_float(review_dict['unit_fob' + str(x)])
		export_validation['unit_cmp_curr' + str(x)] = \
					utils.not_blank(review_dict['unit_cmp_curr' + str(x)])
		export_validation['unit_cmp' + str(x)] = \
					utils.not_blank_float(review_dict['unit_cmp' + str(x)])
					
	for x in xrange(1, import_items + 1):
		import_validation['import_unit' + str(x)] = \
					 utils.not_blank(review_dict['import_unit' + str(x)])
		import_validation['quantity' + str(x)] = \
					 utils.not_blank_integer(review_dict['quantity' + str(x)])
		import_validation['import_item_curr' + str(x)] = \
					 utils.not_blank(review_dict['import_item_curr' + str(x)])
		import_validation['total_price' + str(x)] = \
						 utils.not_blank_price(review_dict['total_price' + str(x)])
	
	for x in xrange(1, import_items + 1):
		for y in xrange(1, export_items + 1):
			coefficients_validation[str(x) + '_' + str(y)] = utils.not_blank_coefficients(review_dict[str(x) + '_' + str(y)])
	
	validation_dict = {	'order_validation'			: order_validation, 
						'export_validation'			: export_validation,
						'import_validation'			: import_validation,
						'coefficients_validation'	: coefficients_validation}
	return validation_dict

	
def update_review_data(validation_dict, review_dict):
	"""
	validation_dict	: dict (as created by validate_review_inputs())
	review_dict		: dict as created by get_review_inputs())
	returns			: dict
	
	Function retrieves data from the global datastore and updates each dictionary with data as 
	pulled from the form on /review/<uid>/<export_items>/<import_items> by the get_review_inputs()
	function. Places all dictionaries of data in the review_data dictionary which the function 
	returns.
	"""
	#Get data from datastore
	global datastore
	order_data = datastore.order_data
	export_data = datastore.export_data
	import_data = datastore.import_data
	coefficients_data = datastore.coefficients_data
	
	#update data from review_dict
	for key in validation_dict['order_validation']:
		order_data[key]  		= review_dict[key].value
	for key in validation_dict['export_validation']:
		export_data[key] 		= review_dict[key].value
	for key in validation_dict['import_validation']:
		import_data[key] 		= review_dict[key].value
	for key in validation_dict['coefficients_validation']:
		coefficients_data[key] 	= review_dict[key].value
		
	review_data = {	'order_data' 		: datastore.order_data,
					'export_data'		: datastore.export_data,
					'import_data'		: datastore.import_data,
					'coefficients_data'	: datastore.coefficients_data}
	return review_data
	
def check_validation_messgaes(validation_dict):
	"""
	validation_dict	: dict
	returns			: list
	
	Function returns list of four boolean values that indicate whether all the validation_message
	field of the named tuples contained in each of the nested dictionaries of the validation_dict
	are equal to "OK". This is necessary both for the utils.review_checks() function and also for
	determining when validation messages will be dispalyed to the user on the review validation
	page. Function is called in the validate_review() function and the submit_form() function.
	"""
	check_order 		= all([validation_dict['order_validation'][key].validation_message == 'OK' 
							  for key in validation_dict['order_validation']])
	check_export 		= all([validation_dict['export_validation'][key].validation_message == 'OK' 
							  for key in validation_dict['export_validation']])
	check_import 		= all([validation_dict['import_validation'][key].validation_message == 'OK' 
							  for key in validation_dict['import_validation']])
	check_coefficients	= all([validation_dict['coefficients_validation'][key].validation_message == 'OK' 
							  for key in validation_dict['coefficients_validation']])
	
	validation_bools = [check_order, check_export, check_import, check_coefficients]
	return validation_bools
	
	
def validate_review(review_dict):
	"""
	review_dict	: dict
	return 		: bottle template
	
	Function calls validate_review_inputs() function to create the validation_review_dict. Also
	passes the review dict passed as argument to the update_review_data() function to create the 
	validation_dict. Additionally the validation_dict is passed to the check_validation_messgaes()
	function in order to create the validation_bools list and hence the messages dict. All of these
	object are then passed the bottle template that helps the user validate the inputs.
	"""
	global datastore
	uid = review_dict['uid']
	factory = utils.get_factory_name(uid)
	export_items = int(review_dict['export_items'])
	import_items = int(review_dict['import_items'])
	validation_dict = validate_review_inputs(review_dict)
	review_data = update_review_data(validation_dict, review_dict)
	validation_bools = check_validation_messgaes(validation_dict)
	check_order, check_export, check_import, check_coefficients = validation_bools
	messages_dict = utils.review_checks(review_data, check_order, check_export, 
										check_import, check_coefficients)
	
	return bt.template('validate_review', review_data = review_data, uid = uid, factory = factory, 
						messages_dict = messages_dict, validation_dict = validation_dict,
						validation_bools = validation_bools)

def pickle_data(final_data, name):
	"""
	final_data	: dict
	name		: string
	returns		: None
	
	Function pickles the final data. Called inside the submit_form() function.
	"""
	path = r'' # Change to PICKLES File
	filename = path + '\\' + name
	pickle.dump(final_data, open(filename, 'wb'))
	return

@bt.route('/review/<uid>/<export_items>/<import_items>/submit', method = 'POST')
def submit_form(uid, export_items, import_items):
	"""
	uid				: string (passed automatically from the dynamic portion of the route)
	exportt_items	: string (passed automatically from the dynamic portion of the route)
	import_items	: string (passed automatically from the dynamic portion of the route)
	returns			: bottle template or None
	
	Function bound to /review/<uid>/<export_items>/<import_items>/submit. 
	Function performs a last data validation check by calling validate_review_inputs() on the 
	result of calling get_review_inputs(). If there are no validation errors, then the data
	are stored in the global datastore, and the browser is redirected to begin the 
	display order page, and the routine for updating the database is gone through. If there are 
	validation errors then the validation template is returned. 
	"""
	uid = uid
	factory = utils.get_factory_name(uid)
	review_dict = get_review_inputs(uid, export_items, import_items)
	validation_dict = validate_review_inputs(review_dict)
	review_data = update_review_data(validation_dict, review_dict)
	validation_bools = check_validation_messgaes(validation_dict)
	if not all(validation_bools):
		check_order, check_export, check_import, check_coefficients = validation_bools
		messages_dict = utils.review_checks(review_data, check_order, check_export, 
										check_import, check_coefficients)
		return bt.template('validate_review', review_data = review_data, uid = uid, factory = factory, 
						messages_dict = messages_dict, validation_dict = validation_dict,
						validation_bools = validation_bools)
	global datastore
	datastore = datastore._replace(order_data = review_data['order_data'])
	datastore = datastore._replace(export_data = review_data['export_data'])
	datastore = datastore._replace(import_data = review_data['import_data'])
	datastore = datastore._replace(coefficients_data = review_data['coefficients_data'])
	local_datastore = datastore
	final_data = utils.final_data_prep(local_datastore)
	pickle_data(final_data, uid + '_' + str(datetime.datetime.now()).replace(':', '_'))
	return commit_and_display(final_data)
	
def save_html(retrieval_dict, retrieved_data, factory):
	path = r'' #Change path to HTML Files
	name = retrieval_dict['uid'] + '_id(' + str(retrieval_dict['order_id']) + ')_' + \
		   str(datetime.datetime.now().date()) + '.html'
	filename = path + '\\' + name
	html = bt.template('display_application', retrieved_data = retrieved_data, factory = factory)
	html_file = open(filename, 'w')
	html_file.write(html)
	html_file.close()
	return
		
def commit_and_display(final_data):
	"""
	final_data	: dict
	returns		: bottle template
	
	Function passed the final_data dict to the utils function that will commit it to the database.
	The result of this utils.commit_data function is a dictionary of database ids that can be used
	to then extract the same data back out of the database. This is achieved with the 
	utils.retrieve_data() function. The result of this function is then passed to the bottle
	template. 
	"""
	retrieval_dict = utils.commit_data(final_data)
	retrieved_data = utils.retrieve_data(retrieval_dict)
	factory = utils.get_factory_name(retrieved_data['order_data']['uid'])
	save_html(retrieval_dict, retrieved_data, factory)
	return bt.template('display_application', retrieved_data = retrieved_data, factory = factory)	
####********************************************************************************************####
####										  RUN METHOD										####
####********************************************************************************************####	
	
def main():
	wb.open('http://localhost:8080/welcome')
	bt.run(host = 'localhost', port = 8080, debug = True)
	
if __name__ == '__main__':
	main()