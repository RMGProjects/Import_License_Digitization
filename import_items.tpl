%import values
%input_types = values.input_types
%input_units = values.input_units
%currencies = values.currencies
% URL = "http://localhost:8080/import/" + uid  + "/" + str(import_items) + "/validate"


%include('header')
<div class = "div1" id="about" style="width:300px;height:1150px;float:left;margin-right: 40px">
	<p class="s2" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		About The Import Items Page
	</p>
	<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
	<p class="s3" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		This is the third page of the digitizing of the the import licence application form. <br/>
		<br/>
		On this page there is space for you to add detail for each of the import items
		that you indicated existed as per the Order Page. All fields must be completed<br/>
		</br>
		By clicking the 'Validate Import Inputs' button at the end of this page you will guided through a 
		process to make sure the fields are correctly completed.<br/>
		<br/>
		At any time you can access the documentation 
		<a href = "/documentation" target="_blank">here</a><br/>
	</p>
</div>
<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
<form method = "post" action = {{URL}} name = "imports">
	<fieldset>
		<legend class = "s2">Add Import Items Detail for {{factory}}</legend>
		<table class = "table2" border = 0 name = "import_items">
			<tr>
				<td><b>SERIAL</b></td>
				<td><b>TYPE</b></td>
				<td><b>DESCRIPTION</b></td>
				<td><b>UNIT OF<br/>MEASURE</b></td>
				<td><b>QUANTITY</b></td>
				<td ><b>TOTAL<br/>CURRENCY</b></td>
				<td><b>TOTAL PRICE</b></td>
			</tr>
			%for x in xrange(import_items):
			<tr>
				<td><p class = "s3"> {{'Import ' + str(x +1)}}</p></td>
				<td>
					<select class = "select2" name = "{{'import_type' + str(x + 1)}}">
					%for type in input_types:
						<option value = "{{type}}">{{type}}</option>
					%end
					</select>
				</td>
				<td>
					<input size = 35 type="text" name="{{'import_description' + str(x + 1)}}" required><br/>
				</td>
				<td>
					<select class = "select2" name = "{{'import_unit' + str(x + 1)}}">
					%for unit in input_units:
						<option value = "{{unit}}">{{unit}}</option>
					%end
				</td>
				<td>
					<input size = 8 type = "text" name = "{{'quantity' + str(x + 1)}}" required><br/>
				<td>
					<select class = "select2" name = "{{'import_item_curr' + str(x + 1)}}">
					%for currency in currencies:
						<option value = "{{currency}}">{{currency}}</option>
					%end
					</select>
				</td>
				<td>
					<input size = 8 type = "text" name = "{{'total_price' + str(x + 1)}}" required><br/>
				</td>
			</tr>
			%end
		</table>
		<br/>
		<fieldset>
			<legend class = "s2"> Validate Import Inputs </legend>
			<p class = "s3">When you are ready press the button below to validate the inputs</p>
			<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
			<input type = "submit" value = "Validate Import Inputs">
		</fieldset>
	</fieldset>
</form>
</body>
</html>