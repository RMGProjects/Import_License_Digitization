%import values
% if all([validation_Idict[key].validation_message == 'OK' for key in validation_Idict]):
	%URL = "http://localhost:8080/import/" + uid + "/" + str(import_items) + "/submit"
%else:
	%URL = "http://localhost:8080/import/" + uid  + "/" + str(import_items) + "/validate"
%end
%input_types = values.input_types
%input_units = values.input_units
%currencies = values.currencies
%fields = ['import_type', 'import_description', 'import_unit', 'quantity', 'import_item_curr', 'total_price']

%include('header')
<div class = "div1" id="about" style="width:300px;height:1150px;float:left;margin-right: 40px">
	<p class="s2" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		About The Validate Import Items Page
	</p>
	<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
	<p class="s3" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		This page helps you to validate the inputs entered on the Import Items page. <br/>
		<br/>
		The Validation column of the table tell you if the input entered
		complied with the expected input rules. If an input complied then this column
		contains the message 'OK'.<br/>
		<br/>
		For those inputs that did not comply a message is displayed as to the error and
		you can fix the input directly on this page. Once modifications have been made
		click the 'Re-validate Import Inputs' button at the bottom of the page.<br/>
		<br/>
		You can also confidently make changes to the fields already verified as these will be 
		re-verified prior to final submission.</br>
		<br/>
		Once all inputs have been validated as 'OK' the button at the bottom of the page will
		read 'Continue to add Import Coefficients'. Press this to move to the next stage.<br/>
		<br/>
		At any time you can access the documentation 
		<a href = "/documentation" target="_blank">here</a><br/>
	</p>
</div>

<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
<form method = "post" action = {{URL}} name = 'import'>
	<fieldset>
		<legend class = "s2">Validate Import Item Details for {{factory}}</legend>
		<table class = "table2" border = 0 name = "import_items">
			<tr>
				<td><b>SERIAL</b></td>
				<td><b>TYPE</b></td>
				<td><b>DESCRIPTION</b></td>
				<td><b>UNIT OF<br/>MEASURE</b></td>
				<td><b>QUANTITY</b></td>
				<td ><b>TOTAL<br/>CURRENCY</b></td>
				<td><b>TOTAL PRICE</b></td>
				<td><b>VALIDATION</b></td>
			</tr>
			%for x in xrange(import_items):
			<tr>
				<td><p class = "s3"> {{'Import ' + str(x +1)}}</p></td>
				<td>
				<select class = "select2" name = "{{'import_type' + str(x + 1)}}">
					%for type in input_types:
						%if type == validation_Idict['import_type' + str(x + 1)].value:
							<option value = "{{type}}" selected>{{type}}</option>
						%else:
							<option value = "{{type}}">{{type}}</option>
						%end
					%end
				</select>
				</td>
				<td>
					<input size = 35 type="text" name="{{'import_description' + str(x + 1)}}" value = "{{validation_Idict['import_description' + str(x + 1)].value}}" required><br/>
				</td>
				<td>
					<select class = "select2" name = "{{'import_unit' + str(x + 1)}}">
					%for unit in input_units:
						%if unit == validation_Idict['import_unit' + str(x + 1)].value:
							<option value = "{{unit}}" selected>{{unit}}</option>
						%else:
							<option value = "{{unit}}">{{unit}}</option>
						%end
					%end
				</select>
				</td>
				<td>
					<input  size = 8 type = "text" name = "{{'quantity' + str(x + 1)}}" value = "{{validation_Idict['quantity' + str(x + 1)].value}}" required>
				</td>
				<td>
					<select class = "select2" name = "{{'import_item_curr' + str(x + 1)}}">
					%for currency in currencies:
						%if currency == validation_Idict['import_item_curr' + str(x + 1)].value:
							<option value = "{{currency}}" selected>{{currency}}</option>
						%else:
							<option value = "{{currency}}">{{currency}}</option>
						%end
					%end
					</select>
				</td>
				<td>
					<input size = 8 type="text" name="{{'total_price' + str(x + 1)}}"  value = "{{validation_Idict['total_price' + str(x + 1)].value}}" required><br/>
				</td>
				<td>
					%if all([validation_Idict[field + str(x+1)].validation_message == 'OK' for field in fields]):
						<p class = "s3">OK</p>
					%else:
						%for field in fields:
							%if validation_Idict[field + str(x + 1)].validation_message != 'OK':
								<p class = "s3e"> {{validation_Idict[field + str(x + 1)].validation_message}}</p>
								<p style="text-indent: 0pt;line-height: 3pt;text-align: left;"><br/></p>
							%end
						%end
					%end
				</td>
			</tr>
			%end
		</table>
		<br/>
		<fieldset>
			<legend class = "s2">Proceed</legend>		
			% if all([validation_Idict[key].validation_message == 'OK' for key in validation_Idict.keys()]):
				<input type = "submit" value = "Continue to Add Import Coefficients" onclick="return confirm('Are you sure you wish to continue?')">
			%else:
				<input type = "submit" value = "Re-Validate Import Inputs">
			%end
		</fieldset>
	</fieldset>
</form>
</body>
</html>

		
	
							
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				