%import collections
%import values
%from collections import namedtuple
%currencies = values.currencies
%input_units = values.input_units
%order_data = review_data['order_data']
%export_data = review_data['export_data']
%import_data = review_data['import_data']
%coefficients_data = review_data['coefficients_data']
%URL1 = "http://localhost:8080/review/" + uid + '/' + str(order_data['export_items']) + '/' + str(order_data['import_items']) + "/validate"
%URL2 = "http://localhost:8080/review/" + uid + '/' + str(order_data['export_items']) + '/' + str(order_data['import_items']) + "/submit"

%include('header')
<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
<p class = "s2"> Review Data for {{factory}} ({{uid}}) </p>
<p style="text-indent: 0pt;line-height: 14pt;text-align: left;"><br/></p>
<form method = "post" name = "order">
<fieldset>
<legend class = "s2">Final Check</legend>
	<fieldset>
		<legend class = "s2">Order Price Information</legend>
		<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
		%if messages_dict['order_messages']:
			<p class = "s3e"> There are the following potential issues with the Order Data, please review:</p>
			<ul>
				%for message in messages_dict['order_messages']:
					<li class = "s3"> {{message}}</li>
				%end
			</ul>
		%else:
			<p class = "s3"> There are no known issues with the Order Data</p>
		%end
		
		<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
		%if not all([validation_dict['order_validation'][key].validation_message == "OK" for key in validation_dict['order_validation']]):
			<p class = "s3e"> There are the following Input Errors in the data</p>
			<ul>
				%for key in validation_dict['order_validation']:
					%if validation_dict['order_validation'][key].validation_message != "OK":
						<li class = "s3"> {{validation_dict['order_validation'][key].validation_message}}</li>
					%end
				%end
			</ul>
		%end
		<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>		
				
		<table class = "table2" border = 0 name = "order_info">
			<tr>
				<td width = 175><b>FIELD</b></td>
				<td><b>INPUT</td>
			</tr>
			<tr>
				<td> Total FOB Value </td>
				<td>
					<p class = "s3">FOB Currency: <select class = "select2" name = "total_fob_curr"></p>
						%for currency in currencies:
							%if currency == order_data['total_fob_curr']:
								<option value="{{currency}}" selected>{{currency}}</option>
							%else:
								<option value = "{{currency}}">{{currency}}</option>
							%end
						%end
					</select>
					<p class = "s3">FOB Amount: <input size = 20 type = "text" name = "total_fob" value = "{{order_data['total_fob']}}" required><br/></p>
				</td>
			</tr>
			<tr>
				<td> Total CMP Value </td>
				<td >
					<p class = "s3">CMP Currency: <select class = "select2"  name = "total_cmp_curr"></p>
						%for currency in currencies:
							%if currency == order_data['total_cmp_curr']:
								<option value="{{currency}}" selected>{{currency}}</option>
							%else:
								<option value = "{{currency}}">{{currency}}</option>
							%end
						%end
					</select>
					<p class = "s3">CMP Amount: <input size = 20 type = "text" name = "total_cmp" value = "{{order_data['total_cmp']}}" required><br/></p>
				</td>
			</tr>
			<tr>
				<td> Total CIF Value </td>
				<td>
					<p class = "s3">CIF Currency: <select class = "select2"  name = "total_cif_curr"></p>
						%for currency in currencies:
							%if currency == order_data['total_cif_curr']:
								<option value="{{currency}}" selected>{{currency}}</option>
							%else:
								<option value = "{{currency}}">{{currency}}</option>
							%end
						%end
					</select>
					<p class = "s3">CIF Amount: <input size = 20 type = "text" name = "total_cif" value = "{{order_data['total_cif']}}" required><br/></p>
				</td>
			</tr>
			<tr>
				<td> Total Quantity of Export Items </td>
				<td> 
					<input size = "12" type = 'text' name = "export_quantity" value = "{{order_data['export_quantity']}}" required>
				</td>
			</tr>
		</table>
	</fieldset>
	<br/>
	<fieldset>
		<legend class = "s2">Export Information</legend>
		<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
		%if messages_dict['export_messages']:
			<p class = "s3e"> There are the following potential issues with the Export Data, please review:</p>
			<ul>
				%for message in messages_dict['export_messages']:
					<li class = "s3"> {{message}}</li>
				%end
			</ul>
		%else:
			<p class = "s3"> There are no known issues with the Export Data</p>
		%end
		<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
		%if not all([validation_dict['export_validation'][key].validation_message == "OK" for key in validation_dict['export_validation']]):
			<p class = "s3e"> There are the following Input Errors in the data</p>
			<ul>
				%for key in validation_dict['export_validation']:
					%if validation_dict['export_validation'][key].validation_message != "OK":
						<li class = "s3"> {{validation_dict['export_validation'][key].validation_message}}</li>
					%end
				%end
			</ul>
		%end
		<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>	
		<table class = "table2" border = 0 name = "export_info">
			<tr>
				<td><b>EXPORT ITEM</b></td>
				<td><b>NUMBER OF UNITS</b></td>
				<td><b>UNIT FOB <br/>CURRENCY</b></td>
				<td><b>UNIT FOB <br/>VALUE</b></td>
				<td><b>UNIT CMP <br/>CURRENCY</b></td>
				<td><b>UNIT CMP <br/>VALUE</b></td>
			</tr>
			%for x in xrange(int(order_data['export_items'])):
				<td><p class = "s3">{{export_data['description' + str(x + 1)]}}</p></td>
				<td>
					<input size = 20 type="text" name="{{'units' + str(x + 1)}}" value = "{{export_data['units' + str(x + 1)]}}" required><br/>
				</td>
				<td>
					<select class = "select2" name = "{{'unit_fob_curr' + str(x + 1)}}">
						%for currency in currencies:
							%if currency == export_data['unit_fob_curr' + str(x + 1)]:
								<option value="{{currency}}" selected>{{currency}}</option>
							%else:
									<option value = "{{currency}}">{{currency}}</option>
							%end
						%end
					</select>
				</td>
				<td>
					<input size = 20 type="text" name="{{'unit_fob' + str(x + 1)}}" value = "{{export_data['unit_fob' + str(x+1)]}}" required><br/>
				</td>
				<td>
					<select class = "select2" name = "{{'unit_cmp_curr' + str(x + 1)}}">
						%for currency in currencies:
							%if currency == export_data['unit_cmp_curr' + str(x + 1)]:
								<option value="{{currency}}" selected>{{currency}}</option>
							%else:
									<option value = "{{currency}}">{{currency}}</option>
							%end
						%end
					</select>
				</td>
				<td>
					<input size = 20 type="text" name="{{'unit_cmp' + str(x + 1)}}" value = "{{export_data['unit_cmp' + str(x+1)]}}" required><br/>
				</td>
			</tr>
			%end
		</table>
	</fieldset>
	<br/>
	<fieldset>
		<legend class = "s2">Import Information</legend>
		<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
		%if messages_dict['import_messages']:
			<p class = "s3e"> There are the following potential issues with the Import Data, please review:</p>
			<ul>
				%for message in messages_dict['import_messages']:
					<li class = "s3"> {{message}}</li>
				%end
			</ul>
		%else:
			<p class = "s3"> There are no known issues with the Import Data</p>
		%end
				<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
		%if not all([validation_dict['import_validation'][key].validation_message == "OK" for key in validation_dict['import_validation']]):
			<p class = "s3e"> There are the following Input Errors in the data</p>
			<ul>
				%for key in validation_dict['import_validation']:
					%if validation_dict['import_validation'][key].validation_message != "OK":
						<li class = "s3"> {{validation_dict['import_validation'][key].validation_message}}</li>
					%end
				%end
			</ul>
		%end
		<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>	
		<table class = "table2" border = 0 name = "import_info">
			<tr>
				<td><b>DESCRIPTION</b></td>
				<td><b>UNIT OF<br/>MEASURE</b></td>
				<td><b>QUANTITY</b></td>
				<td ><b>TOTAL<br/>CURRENCY</b></td>
				<td><b>TOTAL PRICE</b></td>
			</tr>
			%for x in xrange(int(order_data['import_items'])):
				<tr>
					<td><p class = "s3">{{import_data['import_description'  + str(x + 1)]}}</p></td>
					<td>
						<select class = "select2" name = "{{'import_unit' + str(x + 1)}}">
						%for unit in input_units:
							%if unit == import_data['import_unit' + str(x + 1)]:
								<option value = "{{unit}}" selected>{{unit}}</option>
							%else:
								<option value = "{{unit}}">{{unit}}</option>
							%end
						%end
						</select>
					</td>
					<td>
						<input size = 8 type = "text" name = "{{'quantity' + str(x + 1)}}" value = "{{import_data['quantity' + str(x + 1)]}}" required>
					</td>
					<td>
					<select class = "select2" name = "{{'import_item_curr' + str(x + 1)}}">
					%for currency in currencies:
						%if currency == import_data['import_item_curr' + str(x + 1)]:
							<option value = "{{currency}}" selected>{{currency}}</option>
						%else:
							<option value = "{{currency}}">{{currency}}</option>
						%end
					%end
					</select>
					</td>
					<td>
						<input size = 8 type="text" name="{{'total_price' + str(x + 1)}}"  value = "{{import_data['total_price' + str(x + 1)]}}" required><br/>
					</td>
				</tr>
			%end
		</table>
	</fieldset>
	<br/>
	<fieldset>
		<legend class = "s2">Coefficients Detail</legend>
		<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
		%if messages_dict['coefficients_messages']:
			<p class = "s3e"> There are the following potential issues with the Coefficients Data, please review:</p>
			<ul>
				%for message in messages_dict['coefficients_messages']:
					<li class = "s3"> {{message}}</li>
				%end
			</ul>
		%else:
			<p class = "s3"> There are no known issues with the Coefficients Data</p>
		%end
		<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
		%if not all([validation_dict['coefficients_validation'][key].validation_message == "OK" for key in validation_dict['coefficients_validation']]):
			<p class = "s3e"> There are the following Input Errors in the data</p>
			<ul>
				%for key in validation_dict['coefficients_validation']:
					%if validation_dict['coefficients_validation'][key].validation_message != "OK":
						<li class = "s3"> {{validation_dict['coefficients_validation'][key].validation_message}}</li>
					%end
				%end
			</ul>
		%end
		<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>	
		<table class = "table2" border = 0 name = "coefficients">
			<tr>
				<td><b>INPUT <br/>DESCIPTION</b></td>
				<td><b>INPUT UNIT</b></td>
				%for x in xrange(int(order_data['export_items'])):
					<td><b>{{export_data['description' + str(x + 1)]}}</b></td>
				%end
			</tr>
			%for x in xrange(int(order_data['import_items'])):
				<tr>
					<td>{{import_data['import_description'  + str(x + 1)]}}</td>
					<td>{{import_data['import_unit'  + str(x + 1)]}}</td>
					%for y in xrange(int(order_data['export_items'])):
						<td>
							<input size = 8 type = "text" name="{{str(x+1) + '_' + str(y+1)}}" value = "{{coefficients_data[str(x+1) + '_' + str(y+1)]}}" required><br/>
						</td>
					%end
				</tr>
			%end
		</table>
	</fieldset>
	<fieldset>
		<legend class = "s2">Validate Changes</legend>
		<p class ='s3'> If you made changes to any of the data then click here to validate:</p>
		<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
			<input type="submit" value="Validate Changes" formaction = "{{URL1}}" ></input>
	</fieldset>
	<fieldset>
		<legend class = "s2">Submit Form</legend>
		<p class ='s3'> If you have finished making changes and wish to submit the data the click here:</p>
		<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
			<input type="submit" value="Final Submit" formaction = "{{URL2}}"></input>
	</fieldset>
</fieldset>
</form>
</body>
</html>