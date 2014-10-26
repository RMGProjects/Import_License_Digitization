%import values
% if all([validation_Edict[key].validation_message == 'OK' for key in validation_Edict]):
	%URL = "http://localhost:8080/export/" + uid + '/' + str(export_items) + "/submit"
%else:
	%URL = "http://localhost:8080/export/" + uid  + "/" + str(export_items) + "/validate"
%end
%currencies = values.currencies
%categories = values.categories
%clothing_types = values.clothing_types

%include('header')
<div class = "div1" id="about" style="width:300px;height:1150px;float:left;margin-right: 40px">
	<p class="s2" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		About The Validate Export Items Page
	</p>
	<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
	<p class="s3" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		This page helps you to validate the inputs entered on the Export Items page. <br/>
		<br/>
		The Validation column of the table tell you if the input entered
		complied with the expected input rules. If an input complied then this column
		contains the message 'OK'. <br/>
		<br/>
		For those inputs that did not comply a message is displayed as to the error and
		you can fix the input directly on this page. Once modifications have been made
		click the 'Re-validate Export Inputs' button at the bottom of the page.<br/>
		<br/>
		You can also confidently make changes to the fields already verified as these will be 
		re-verified prior to final submission.</br>
		<br/>
		Once all inputs have been validated as 'OK' the button at the bottom of the page will
		read 'Continue to add Import Items'. Press this to move to the next stage.<br/>
		<br/>		
		At any time you can access the documentation 
		<a href = "/documentation" target="_blank">here</a><br/>
	</p>
</div>

<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
<form method = "post" action = {{URL}} name = 'exports'>
	<fieldset>
		<legend class = "s2">Validate Export Items Detail for {{factory}}</legend>
		%for x in xrange(export_items):
			<fieldset>
				<legend class = "s3"><b>Export Item {{str(x + 1)}}</b></legend>
				<table class = "table2" border = 0 name = "{{'export_item' + str(x +1)}}">
					<tr>
						<td width = 175><b>FIELD</b></td>
						<td><b>INPUT</td>
						<td><b>VALIDATION</td>
					</tr>
					<tr>
						<td>{{validation_Edict['category' + str(x+1)].fieldname}}</td>
						<td>
							<select class = "select1" name = "{{'category' + str(x + 1)}}">
							%for category in categories:
								%if category == validation_Edict['category' + str(x+1)].value:
									<option value="{{category}}" selected>{{category}}</option>
								%else:
									<option value = "{{category}}">{{category}}</option>
								%end
							%end
							</select>
						</td>
						<td>
							%if validation_Edict['category' + str(x + 1)].validation_message == 'OK':
								<p class = "s3">OK</p>
							%else:
								<p class = "s3e"> {{validation_Edict['category' + str(x + 1)].validation_message}} </p>
							%end
						</td>
					</tr>
					<tr>
						<td>{{validation_Edict['type' + str(x+1)].fieldname}}</td>
						<td>
							<select class = "select1" name = "{{'type' + str(x + 1)}}">
							%for type in clothing_types:
								%if type == validation_Edict['type' + str(x+1)].value:
									<option value="{{type}}" selected>{{type}}</option>
								%else:
									<option value = "{{type}}">{{type}}</option>
								%end
							%end
							</select>
						</td>
						<td>
							%if validation_Edict['type' + str(x + 1)].validation_message == 'OK':
								<p class = "s3">OK</p>
							%else:
								<p class = "s3e"> {{validation_Edict['type' + str(x + 1)].validation_message}} </p>
							%end
						</td>
					</tr>
					<tr>
						<td>{{validation_Edict['description' + str(x+1)].fieldname}}</td>
						<td>
							<input size = 60 type="text" name="{{'description' + str(x + 1)}}" value = "{{validation_Edict['description' + str(x+1)].value}}" required><br/>
						</td>
						<td>
							%if validation_Edict['description' + str(x + 1)].validation_message == 'OK':
								<p class = "s3">OK</p>
							%else:
								<p class = "s3e"> {{validation_Edict['description' + str(x + 1)].validation_message}} </p>
							%end
						</td>
					</tr>
					<tr>
						<td>{{validation_Edict['units' + str(x+1)].fieldname}}</td>
						<td>
							<input size = 20 type="text" name="{{'units' + str(x + 1)}}" value = "{{validation_Edict['units' + str(x+1)].value}}" required><br/>
						</td>
						<td>
							%if validation_Edict['units' + str(x + 1)].validation_message == 'OK':
								<p class = "s3">OK</p>
							%else:
								<p class = "s3e"> {{validation_Edict['units' + str(x + 1)].validation_message}} </p>
							%end
						</td>
					</tr>
					<tr>
						<td>{{validation_Edict['unit_fob_curr' + str(x+1)].fieldname}}</td>
						<td>
							<select class = "select2" name = "{{'unit_fob_curr' + str(x + 1)}}">
							%for currency in currencies:
								%if currency == validation_Edict['unit_fob_curr' + str(x + 1)].value:
									<option value="{{currency}}" selected>{{currency}}</option>
								%else:
									<option value = "{{currency}}">{{currency}}</option>
								%end
							%end
							</select>
						</td>
						<td>
							%if validation_Edict['unit_fob_curr' + str(x + 1)].validation_message == 'OK':
								<p class = "s3">OK</p>
							%else:
								<p class = "s3e"> {{validation_Edict['unit_fob_curr' + str(x + 1)].validation_message}} </p>
							%end
						</td>
					</tr>
					<tr>
						<td>{{validation_Edict['unit_fob' + str(x+1)].fieldname}}</td>
						<td>
							<input size = 20 type="text" name="{{'unit_fob' + str(x + 1)}}" value = "{{validation_Edict['unit_fob' + str(x+1)].value}}" required><br/>
						</td>
						<td>
							%if validation_Edict['unit_fob' + str(x + 1)].validation_message == 'OK':
								<p class = "s3">OK</p>
							%else:
								<p class = "s3e"> {{validation_Edict['unit_fob' + str(x + 1)].validation_message}} </p>
							%end
						</td>
					</tr>
					<tr>
						<td>{{validation_Edict['unit_cmp_curr' + str(x+1)].fieldname}}</td>
						<td>
							<select class = "select2" name = "{{'unit_cmp_curr' + str(x + 1)}}">
							%for currency in currencies:
								%if currency  == validation_Edict['unit_cmp_curr' + str(x+1)].value:
									<option value="{{currency}}" selected>{{currency}}</option>
								%else:
									<option value = "{{currency}}">{{currency}}</option>
								%end
							%end
							</select>
						</td>
						<td>
							%if validation_Edict['unit_cmp_curr' + str(x + 1)].validation_message == 'OK':
								<p class = "s3">OK</p>
							%else:
								<p class = "s3e"> {{validation_Edict['unit_cmp_curr' + str(x + 1)].validation_message}} </p>
							%end
						</td>
					</tr>
					<tr>
						<td>{{validation_Edict['unit_cmp' + str(x+1)].fieldname}}</td>
						<td>
							<input size = 20 type="text" name="{{'unit_cmp' + str(x + 1)}}" value = "{{validation_Edict['unit_cmp' + str(x+1)].value}}" required><br/>
						</td>
						<td>
							%if validation_Edict['unit_cmp' + str(x + 1)].validation_message == 'OK':
								<p class = "s3">OK</p>
							%else:
								<p class = "s3e"> {{validation_Edict['unit_cmp' + str(x + 1)].validation_message}} </p>
							%end
						</td>
					</tr>
				</table>
			</fieldset>
			<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
		%end
		<br/>
		<fieldset>
			<legend class = "s2">Proceed</legend>		
			% if all([validation_Edict[key].validation_message == 'OK' for key in validation_Edict.keys()]):
				<input type = "submit" value = "Continue to Add Import Items" onclick="return confirm('Are you sure you wish to continue?')">
			%else:
				<input type = "submit" value = "Re-Validate Export Inputs">
			%end
		</fieldset>
	</fieldset>
</form>
</body>
</html>








