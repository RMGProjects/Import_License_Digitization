
% URL = "http://localhost:8080/order/" + uid + "/validate"
% import pycountry as pyc
% import values
% countries = [country.name for country in list(pyc.countries)]
% countries.insert(0, "N/A")
%export_items = values.export_items
%import_items = values.import_items
%currencies = values.currencies

%include('header')

<div class = "div1" id="about" style="width:300px;height:1150px;float:left;margin-right: 40px">
	<p class="s2" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		About The Order Page
	</p>
	<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
	<p class="s3" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		This is the first of several pages that will guide you through the process
		of digitizing the import licence application form. This page allows you to enter 
		information about the total order found in the Import Licence Application Form<br/>
		<br/>
		All fields must be completed By clicking the 
		'Validate Order Inputs' button at the end of this page you will guided through a 
		process to make sure the fields are correctly completed.<br/>
		<br/>
		At any time you can access the documentation 
		<a href = "/documentation" target="_blank">here</a><br/>
	</p>
</div>

<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
<form method = "post" action = {{URL}} name = "order">
<fieldset>
	<legend class = "s2">Add Order Detail for {{factory}}</legend>
	<fieldset>
		<legend class = "s2">Order Information</legend>
		<table class = "table2" border = 0 name = "order_info">
			<tr>
				<td width = 175><b>FIELD</b></td>
				<td><b>INPUT</td>
			</tr>
			<tr>
				<td>Order ID Number</td>
				<td>
				<input size = 60 type="text" name="order_id" required><br/>
				</td>
			</tr>
			<tr>
				<td>Exporter</td>
				<td>
				<input size = 60 type="text" value = "{{factory}}" name="exporter" readonly><br/>	
				</td>
			</tr>
			<tr>
				<td>Buyer Name</td>
				<td>
					<input size = 60 type="text" name="buyer" required><br/>
				</td>
			</tr>
			<tr>
				<td>Buyer Country of Origin (Select up to 3)</td>
				<td>
				%for x in xrange(1, 4):						
					<select class = "select1" name="{{'buyer_country' + str(x)}}">
						%for country in countries:
							<option value = "{{country}}">{{country}}</option>
						%end
					</select>
				%end
				</td>
			</tr>
		</table>
	</fieldset>
	</br>
	<fieldset>
		<legend class = "s2">Price Details</legend>
		<table class = "table2" border = 0 name = "price_info">
			<tr>
				<td width = 175><b>FIELD</b></td>
				<td><b>INPUT</td>
			</tr>
			<tr>
				<td> Total FOB Value </td>
				<td>
					<p class = "s3">FOB Currency: <select class = "select2" name = "total_fob_curr"></p>
						%for currency in currencies:
							<option value = "{{currency}}">{{currency}}</option>
						%end
					</select>
					<p class = "s3">FOB Amount: <input size = 20 type = "text" name = "total_fob" required><br/></p>
				</td>
			</tr>
			<tr>
				<td> Total CMP Value </td>
				<td >
					<p class = "s3">CMP Currency: <select class = "select2"  name = "total_cmp_curr"></p>
						%for currency in currencies:
							<option value = "{{currency}}">{{currency}}</option>
						%end
					</select>
					<p class = "s3">CMP Amount: <input size = 20 type = "text" name = "total_cmp" required><br/></p>
				</td>
			</tr>
			<tr>
				<td> Total CIF Value </td>
				<td>
					<p class = "s3">CIF Currency: <select class = "select2"  name = "total_cif_curr"></p>
						%for currency in currencies:
							<option value = "{{currency}}">{{currency}}</option>
						%end
					</select>
					<p class = "s3">CIF Amount: <input size = 20 type = "text" name = "total_cif" required><br/></p>
				</td>
			</tr>
		</table>
	</fieldset>
	<br/>
	<fieldset>
		<legend class = "s2"> Order Timeline </legend>
		<table class = "table2" border = 0 name = "order_time">
			<tr>
				<td width = 175><b>FIELD</b></td>
				<td ><b>Input</td>
			</tr>
			<tr>
				<td>Submission Date</td>
				<td>
					<p class = "s3">Date: 
						<input type="text" name = "sub_date" required>
					</p>
				</td>
			</tr>
			<tr>
				<td>Approval Date</td>
				<td>
					<p class = "s3">Date: 
						<input type="text"  name = "app_date" required>
					</p>
				</td>
			</tr>
			<tr>
				<td>Shipment Date</td>
				<td>
					<p class = "s3">Date: 
						<input type="text" name = "ship_date"  required>
					</p>
				</td>
			</tr>
		</table>
	</fieldset>
	</br>
	<fieldset>
		<legend class = "s2">Number of Import/Export Items to which the Order Relates</legend>
		<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
		<p class = "s3">Select Number of Export Items:</p>
		<select class = "select2" name="export_items"><br/>
			%for item in xrange(0, export_items + 1):
				<option value = "{{str(item)}}">{{str(item) + ' items'}}</option>
			%end
		</select><br/>
		<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
		<p class = "s3">Total Quantity of Export Items:</p>
			<input size = "12" type = 'text' name = "export_quantity" required>
		<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
		<p class = "s3">Select Number of Import Items:</p>
		<select class = "select2" name="import_items"><br/>
			%for item in xrange(0, import_items + 1):
				<option value = "{{str(item)}}">{{str(item) + ' items'}}</option>
			%end
		</select><br/>
	</fieldset>
	<br/>
	<fieldset>
		<legend class = "s2"> Validate Order Inputs </legend>
		<p class = "s3">When you are ready press the button below to validate the inputs</p>
		<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
		<input type = "submit" value = "Validate Order Inputs">
	</fieldset>
</fieldset>
</form>
</body>
</html>