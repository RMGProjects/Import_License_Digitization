""",
This file contains the dropdown menu options that are used throughout the entire application.
Im order to add to a dropdown menu, simply insert the new value at the end of the relevant list.
This lists are sorted so as to be alphabetical, but the sort occurs on the list after the list has
been created. In other words the order of the list as it appears on this page is immaterial as 
sort function is applied afterwards.

When adding a value be sure that the value is enclosed in quotation marks and there is a comma
between the new value and the last value previously in the list.
"""

#Modify these numbers to allow for an increase in the number of export/import items
export_items = 25
import_items = 75

#Modify this list if a currency needs to be added
currencies = sorted(['', 'USD', 'EUR', 'GBP', 'MMK', 'RMB', 'JPY'])

#Modify this list if a type of import needs to b added
input_types = sorted(['', 'Fabric', 'Lining', 'Thread', 'Belt', 'Tape', 
			   'Cord', 'Label', 'Packaging', 'Down', 'Bag', 'Button', 
			   'Interlining', 'Eyelet', 'String', 'Tag', 'Zipper', 'Other'])

#Modify this list if a unit of measure for imports needs to be added
input_units = sorted(['', 'Units', 'Metres', 'Kgs', 'Pack', 'Other', 'Cone'])

#Modify this list if a category of export needs to be added
categories = sorted(['', "Men", "Women", "Kids", 'Baby', 'Boys', 'Girls', 'Unisex', "Unknown", "Other"])

#Modify this list if a type of export item needs to be added
clothing_types = sorted(['', "Jumper", "Padding", "Brief", "T-Shirt", "Underwear", "Coat", "Vest",
						 "Shirt", "Jacket", "Skirt", "Blouse", "Unknown", "Trousers", "Pants", "Other",
						 'Bag', 'Blazer', 'Brassiere', 'Dress', 'Fleece', 'Glove', 'Hoody', 'Legging', 
						 'Nightdress', 'Pyjamas', 'Pant', 'Polo Shirt', 'Shorts', 'Suit',])

#These upper/lower bounds CMP are entirely arbitrary, so change if necessary
lower_cmp_bound = 5000
upper_cmp_bound = 100000

#These upper/lower bounds FOB are entirely arbitrary, so change if necessary
lower_fob_bound = 50000
upper_fob_bound = 1000000

#These upper/lower bounds CIF are entirely arbitrary, so change if necessary
lower_cif_bound = 50000
upper_cif_bound = 500000

fob_cmp_divider_max = 13
fob_cmp_divider_min = 6

wastage_allowance = 0.95

