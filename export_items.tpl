%import values
%currencies = values.currencies
%categories = values.categories
%clothing_types = values.clothing_types
% URL = "http://localhost:8080/export/" + uid  + "/" + str(export_items) + "/validate"

%include('header')
<div class = "div1" id="about" style="width:300px;height:1150px;float:left;margin-right: 40px">
	<p class="s2" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		About The Export Items Page
	</p>
	<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
	<p class="s3" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		This is the second page of the digitizing of the the import licence application form. <br/>
		<br/>
		On this page there is space for you to add detail for each of the export items
		that you indicated existed as per the Order Page. All fields must be completed<br/>
		<br/>
		By clicking the 'Validate Export Inputs' button at the end of this page you will guided through a 
		process to make sure the fields are correctly completed.<br/>
		<br/>
		At any time you can access the documentation 
		<a href = "/documentation" target="_blank">here</a><br/>
	</p>
</div>

<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
<form method = "post" action = {{URL}} name = "exports">
	<fieldset>
		<legend class = "s2">Add Export Items Detail for {{factory}}</legend>
		%for x in xrange(export_items):
			<fieldset>
				<legend class = "s3"><b>Export Item {{str(x + 1)}}</b></legend>
				<table class = "table2" border = 0 name = "{{'export_item' + str(x +1)}}">
					<tr>
						<td width = 175><b>FIELD</b></td>
						<td><b>INPUT</td>
					</tr>
					<tr>
						<td>Item Category</td>
						<td>
							<select class = "select1" name = "{{'category' + str(x + 1)}}">
							%for category in categories:
								<option value = "{{category}}">{{category}}</option>
							%end
							</select>
						</td>
					</tr>
					<tr>
						<td>Item Type</td>
						<td>
							<select class = "select1" name = "{{'type' + str(x + 1)}}">
							%for type in clothing_types:
								<option value = "{{type}}">{{type}}</option>
							%end
							</select>
						</td>
					</tr>
					<tr>
						<td>Item Description</td>
						<td>
							<input size = 60 type="text" name="{{'description' + str(x + 1)}}" required><br/>
						</td>
					</tr>
					<tr>
						<td>Number of Units</td>
						<td>
							<input size = 20 type="text" name="{{'units' + str(x + 1)}}" required><br/>
						</td>
					</tr>
					<tr>
						<td> Unit FOB Value </td>
						<td>
							<p class = "s3">Currency: 
								<select class = "select2" name = "{{'unit_fob_curr' + str(x + 1)}}">
							</p>
								%for currency in currencies:
									<option value = "{{currency}}">{{currency}}</option>
								%end
								</select>
							<p class = "s3">Amount: <input size = 20 type = "text" name = "{{'unit_fob' + str(x + 1)}}" required><br/></p>
						</td>
					</tr>
					<tr>
						<td> Unit CMP Value </td>
						<td>
							<p class = "s3">Currency: 
								<select class = "select2" name = "{{'unit_cmp_curr' + str(x + 1)}}">
							</p>
								%for currency in currencies:
									<option value = "{{currency}}">{{currency}}</option>
								%end
								</select>
							<p class = "s3">Amount: <input size = 20 type = "text" name = "{{'unit_cmp' + str(x + 1)}}" required><br/></p>
						</td>
					</tr>
				</table>
			</fieldset>
		<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
		%end
		<br/>
	<fieldset>
		<legend class = "s2"> Validate Export Inputs </legend>
		<p class = "s3">When you are ready press the button below to validate the inputs</p>
		<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
		<input type = "submit" value = "Validate Export Inputs">
	</fieldset>
</fieldset>
</form>
</body>
</html>
					
							
					
			