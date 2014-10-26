% import pycountry as pyc
% import values
% countries = [country.name for country in list(pyc.countries)]
% countries.insert(0, "N/A")
% if all([validation_Odict[key].validation_message == 'OK' for key in validation_Odict]):
	%URL = "http://localhost:8080/order/" + uid + "/submit"
%else:
	%URL = "http://localhost:8080/order/" + uid + "/validate"
%end
%factory = validation_Odict['exporter'].value
%iterable_keys = ['order_id', 'exporter', 'buyer']
%date_keys = ['sub_date', 'app_date', 'ship_date']
%price_keys = ['fob', 'cmp', 'cif']
%export_items = values.export_items
%import_items = values.import_items
%currencies = values.currencies
              
%include('header')
<div class = "div1" id="about" style="width:300px;height:950px;float:left;margin-right: 40px">
	<p class="s2" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		About The Validate Order Page
	</p>
	<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
	<p class="s3" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		This page helps you to validate the inputs entered on the Order page. <br/>
		<br/>
		The Validation column of the  tables tell you if the input entered
		complied with the expected input rules. If an input complied then this column
		contains the message 'OK' <br/>
		<br/>
		For those inputs that did not comply a message is displayed as to the error and
		you can fix the input directly on this page. Once modifications have been made
		click the 'Re-validate Order Inputs' button at the bottom of the page.<br/>
		<br/>
		You can also confidently make changes to the fields already verified as these will be 
		re-verified prior to final submission.</br>
		<br/>
		Once all inputs have been validated as 'OK' the button at the bottom of the page will
		read 'Continue to add Export Items'. Press this to move to the next stage.<br/>
		<br/>		
		At any time you can access the documentation 
		<a href = "/documentation" target="_blank">here</a><br/>
	</p>
</div>

<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
<form method = "post" action = {{URL}} name = 'order'>
<fieldset>
<legend class = "s2">Validate Order Details for {{factory}} ({{uid}}</legend>
	<fieldset>
		<legend class = "s2">Order Information</legend>
		<table class = "table2" border = 0 name = "order_info">
			<tr>
				<td width = 175><b>FIELD</b></td>
				<td><b>INPUT</td>
				<td><b>VALIDATION</td>
			</tr>
			%for key in iterable_keys:
			<tr>
				<td>{{validation_Odict[key].fieldname}}</td>
				<td>
					<input size = 60 type="text" name="{{key}}" value = "{{validation_Odict[key].value}}" required>
				</td>
				<td>
					%if validation_Odict[key].validation_message == 'OK':
						<p class = "s3">OK</p>
					%else:
						<p class = "s3e"> {{validation_Odict[key].validation_message}} </p>
					%end
				</td>
			</tr>
			%end
				
			%for x in xrange(1, 4):
			<tr>
				<td>{{validation_Odict['buyer_country' + str(x)].fieldname}}</td>
				<td>
					<select name="{{'buyer_country' + str(x)}}">
					%for c in xrange(len(countries)):
						%if countries[c] == validation_Odict['buyer_country' + str(x)].value:
							<option value="{{countries[c]}}" selected>{{countries[c]}}</option>
						%else:
							<option value = "{{countries[c]}}">{{countries[c]}}</option>
						%end
					%end
					</select>
				</td>
				<td>
					%if validation_Odict['buyer_country' + str(x)].validation_message == 'OK':
						<p class = "s3">OK</p>
					%else:
						<p class = "s3e">{{validation_Odict['buyer_country' + str(x)].validation_message}}</p>
					%end
				</td>
			</tr>
			%end
		</table>
	</fieldset>
	</br>
	<fieldset>
		<legend class = "s2">Price Details</legend>
		<table class = "table2" border = 0 name = "price_info">
			<tr>
				<td width = 175><b>FIELD</b></td>
				<td><b>INPUT</td>
				<td><b>VALIDATION</td>
			</tr>
			%for key in price_keys:
			<tr>
				<td>{{validation_Odict['total_' + key + '_curr'].fieldname}}</td>
				<td>
					<select class = "select2" name = "{{'total_' + key + '_curr'}}">
						%for currency in currencies:
							%if currency == validation_Odict['total_' + key + '_curr'].value:
								<option value="{{currency}}" selected>{{currency}}</option>
							%else:
								<option value = "{{currency}}">{{currency}}</option>
							%end
						%end
					</select>
				</td>
				<td>
					%if validation_Odict['total_' + key + '_curr'].validation_message == 'OK':
						<p class = "s3">OK</p>
					%else:
						<p class = "s3e">{{validation_Odict['total_' + key + '_curr'].validation_message}}</p>
					%end
				<td>
			</tr>
			<tr>
				<td>{{validation_Odict['total_' + key].fieldname}}</td>
				<td>
					<input size = 20 type = "text" name = "{{'total_' + key}}" value = "{{validation_Odict['total_' + key].value}}" required><br/>
				</td>
				<td>
					%if validation_Odict['total_' + key].validation_message == 'OK':
						<p class = "s3">OK</p>
					%else:
						<p class = "s3e">{{validation_Odict['total_' + key].validation_message}}</p>
					%end
				<td>
			</tr>
			%end
		</table>
	</fieldset>
	<br/>
	<fieldset>
		<legend class = "s2"> Order Timeline </legend>
		<table class = "table2" border = 0 name = "order_time">
			<tr>
				<td width = 175><b>FIELD</b></td>
				<td><b>INPUT</td>
				<td><b>VALIDATION</td>
			</tr>
			%for x in xrange(len(date_keys)):
			<tr>
				<td>{{validation_Odict[date_keys[x]].fieldname}}</td>
				<td>
					<p class = "s3">Date: <input type="text"  name = "{{date_keys[x]}}" value = "{{validation_Odict[date_keys[x]].value}}"  required></p>
				</td>
				<td>
					%if validation_Odict[date_keys[x]].validation_message == 'OK':
						<p class = "s3">OK</p>
					%else:
						<p class = "s3e"> {{validation_Odict[date_keys[x]].validation_message}} </p>
					%end
				</td>
			</tr>
			%end
		</table>
	</fieldset>
	</br>
	<fieldset>
		<legend class = "s2">Number of Import/Export Items to which the Order Relates</legend>
		%if validation_Odict['export_items'].validation_message == 'OK':
			<p class = "s3">OK</p>
		%else:
			<p class = "s3e"> {{validation_Odict['export_items'].validation_message}}</p>
		%end
		<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
		<p class = "s3">Select Number of Export Items: </p><select name="export_items"><br/>
			%for item in xrange(0, export_items + 1):
				%if item == validation_Odict['export_items'].value:
					<option value="{{item}}" selected>{{str(item) + ' items'}}</option>
				%else:
					<option value = "{{str(item)}}">{{str(item) + ' items'}}</option>
				%end
			%end
		</select><br/>
		<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
		%if validation_Odict['export_quantity'].validation_message == 'OK':
			<p class = "s3">OK</p>
		%else:
			<p class = "s3e"> {{validation_Odict['export_quantity'].validation_message}}</p>
		%end
		<p class = "s3">Total Quantity of Export Items:</p>
			<input size = "12" type = 'text' name = "export_quantity" value = "{{validation_Odict['export_quantity'].value}}" required>
		<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
		%if validation_Odict['import_items'].validation_message == 'OK':
			<p class = "s3">OK</p>
		%else:
			<p class = "s3e"> {{validation_Odict['import_items'].validation_message}}</p>
		%end
		<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
		<p class = "s3">Select Number of Import Items: </p><select name="import_items"><br/>
			%for item in xrange(0, import_items + 1):
				%if item == validation_Odict['import_items'].value:
					<option value="{{item}}" selected>{{str(item) + ' items'}}</option>
				%else:
					<option value = "{{str(item)}}">{{str(item) + ' item'}}</option>
				%end
			%end
		</select><br/>
	</fieldset>
	<br/>
	<fieldset>
		<legend class = "s2">Proceed</legend>		
		% if all([validation_Odict[key].validation_message == 'OK' for key in validation_Odict.keys()]):
			<input type = "submit" value = "Continue to Add Export Items" onclick="return confirm('Are you sure you wish to continue?')">
		%else:
			<input type = "submit" value = "Re-Validate Order Inputs">
		%end
	</fieldset>
</fieldset>
</form>	
<body>
<html>						