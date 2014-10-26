%include('header')
% if all([validation_Cdict[key].validation_message == 'OK' for key in validation_Cdict]):
	%URL = "http://localhost:8080/coefficients/" + uid  + "/" + str(len(items_dict['export_list'])) + '/' + str(len(items_dict['import_list'])) + "/submit"
%else:
	%URL = "http://localhost:8080/coefficients/" + uid  + "/" + str(len(items_dict['export_list'])) + '/' + str(len(items_dict['import_list'])) + "/validate"
%end	
<div class = "div1" id="about" style="width:175px;height:1150px;float:left;margin-right: 40px">
	<p class="s2" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		About The Validate Export Items Page
	</p>
	<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
	<p class="s3" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		This page helps you to validate the inputs entered on the Export Items page. <br/>
		<br/>
		The Validation column of the below tables tell you if the input entered
		complied with the expected input rules. If an input complied then this column
		contains the message 'OK'. In such circumstances the input field appears in the
		table as a 'readonly' value. That is it cannot be changed on this page. Should you 
		wish to change values that have been accepted please use the back button of your
		browser. <br/>
		<br/>
		For those inputs that did not comply a message is displayed as to the error and
		you can fix the input directly on this page. Once modifications have been made
		click the 'Re-validate' button at the bottom of the page.<br/>
		<br/>
		Once all inputs have been validated the button at the bottom of the page will
		read 'Continue to add Import Items'. Press this to move to the next stage.<br/>
		<br/>		
		At any time you can access the documentation 
		<a href = "/documentation" target="_blank">here</a><br/>
	</p>
</div>

<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
<p class = "s2"> Add Coefficients for {{factory}} ({{uid}}) </p>
<p style="text-indent: 0pt;line-height: 14pt;text-align: left;"><br/></p>
<form method = "post" action = {{URL}} name = "imports">
	<fieldset>
		<legend class = "s2">Coefficients Detail</legend>
		<table class = "table2" border = 0 name = "coefficients">
			<tr>
			<td><b>INPUT <br/>DESCIPTION</b></td>
			<td><b>INPUT UNIT</b></td>
			%for item in items_dict['export_list']:
				<td><b>{{item}}</b></td>
				<td width = 35><b>VALIDATION</b></td>
			%end
			</tr>
			%for x in xrange(len(items_dict['import_list'])):
				<tr>
				<td>{{items_dict['import_list'][x]}}</td>
				<td>{{items_dict['units_list'][x]}}</td>
				%for y in xrange(len(items_dict['export_list'])):
					<td>
						<input size = 8 type = "text" name="{{str(x+1) + '_' + str(y+1)}}" value = "{{validation_Cdict[str(x+1) + '_' + str(y+1)].value}}" required><br/>
					</td>
					<td>
						%if validation_Cdict[str(x+1) + '_' + str(y+1)].validation_message == 'OK':
							<p class = "s3">OK</p>
						%else:
							<p class = "s3e"> {{validation_Cdict[str(x+1) + '_' + str(y+1)].validation_message}} </p>
						%end
					</td>
				%end
				</tr>
			%end
		</table>
		<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
		<br/>
		<fieldset>
			<legend class = "s2">Proceed</legend>		
			% if all([validation_Cdict[key].validation_message == 'OK' for key in validation_Cdict.keys()]):
				<input type = "submit" value = "Submit Application" onclick="return confirm('Are you sure you wish to continue?')">
			%else:
				<input type = "submit" value = "Re-Validate">
			%end
		</fieldset>
	</fieldset>
</form>
</body>
</html>
