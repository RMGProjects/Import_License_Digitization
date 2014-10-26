% if all([validation_Odict[key].validation_message == 'OK' for key in validation_Odict]):
	%URL = "http://localhost:8080/add/" + uid + "/validate/commit"
%else:
	%URL = "http://localhost:8080/add/" + uid + "/validate"
%end

%include('header')

<div class = "div1" id="about" style="width:350px;height:575px;float:left;margin-right: 40px">
	<p class="s2" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		About The Validate Factory Page
	</p>
	<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
	<p class="s3" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		This page helps you to validate the inputs entered on the Add Factory page. <br/>
		<br/>
		The Validation column of the table tells you if the input entered
		complied with the expected input rules. If an input complied then this column
		contains the message 'OK'.<br/>
		<br/>
		For those inputs that did not comply a message is displayed as to the error and
		you can fix the input directly on this page. Once modifications have been made
		click the 'Re-validate' button at the bottom of the page.<br/>
		<br/>
		You can also confidently make changes to the fields already verified as these will be 
		re-verified prior to final submission.</br>
		<br/>
		Once all inputs have been validated as 'OK' the button at the bottom of the page will
		read 'Commit to Database'. Press this to permanently add the factory to the database.<br/>
		<br/>		
		At any time you can access the documentation 
		<a href = "/documentation" target="_blank">here</a><br/>
	</p>
</div>

<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
<form method = "post" action = {{URL}} name = 'order'>
<fieldset>
	<legend class = "s2">Validate New Factory Details</legend>
	<fieldset>
		<legend class = "s2">New Factory Details</legend>
		<table class = "table2" border = 0 name = "order_info">
			<tr>
				<td width = 125><b>FIELD</b></td>
				<td><b>INPUT</td>
				<td><b>VALIDATION</td>
			<tr>
			%for key in validation_Odict.keys():
				<tr>
					<td>{{validation_Odict[key].fieldname}}</td>
					<td>
						<input size = 80 type="text" name="{{key}}" value = "{{validation_Odict[key].value}}" required>
					</td>
					<td>
						%if validation_Odict[key].validation_message == 'OK':
							<p class = "s3"> <b>OK</b> </p>
						%else:
							<p class = "s3e"> {{validation_Odict[key].validation_message}} </p></font>
						%end
					</td>
				</tr>
			%end
		</table>
	</fieldset>
	<br/>
	<fieldset>
		<legend class = "s2">Proceed</legend>
		% if all([validation_Odict[key].validation_message == 'OK' for key in validation_Odict.keys()]):
			<input type = "submit" value = "Commit to Database" onclick="return confirm('Are you sure you wish to commit the new factory to the database?')">
		%else:
			<input type = "submit" value = "Re-Validate">
		%end
	</fieldset>
</form>
<body>
<html>