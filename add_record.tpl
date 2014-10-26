% URL = "http://localhost:8080/add/" + uid + "/validate"

%include('header')

<div class = "div1" id="about" style="width:350px;height:550px;float:left;margin-right: 40px">
	<p class="s2" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		About The Add Factory Page
	</p>
	<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
	<p class="s3" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		This page helps you to add a new factory to the Database of Factories. <br/>
		<br/>
		In the table enter both fields. Both fields are text, but you may only enter letters,
		numbers, spaces, and the following symbols: ',' '&' '%' '/'<br/>
		<br/>
		By clicking the 'Validate Inputs' button at the end of this page you will 
		guided through a process to make sure the fields are correctly completed.<br/>
		<br/>		
		At any time you can access the documentation 
		<a href = "/documentation" target="_blank">here</a><br/>
	</p>
</div>
<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>

<form method = "post" action = {{URL}} name = "new_record">
<fieldset>
	<legend class = "s2"> Add new factory to the Factory Database</legend>
	<p style="text-indent: 0pt;line-height: 14pt;text-align: left;"><br/></p>
	<p class = "s3"> Factory will be added with UID: {{uid}} </p>
	<p style="text-indent: 0pt;line-height: 14pt;text-align: left;"><br/></p>
	<fieldset>
		<legend class = "s2">New Factory Details</legend>
		<table class = "table2" border = 0 name = "order_info">			
			<tr>
				<td width = 125><b>FIELD</b></td>
				<td><b>INPUT</td>
			</tr>
			<tr>
				<td>Factory Name</td>
				<td>
					<input size = 80 type="text" name="fact_name" required><br/>
				</td>
			</tr>
			<tr>
				<td>Factory Address</td>
				<td>
					<input size = 80 type="text" name="fact_address" required><br/>
				</td>
			</tr>
		</table>
	</fieldset>
	<br/>
	<fieldset>
		<legend class = "s2"> Validate Inputs </legend>
		<p class = "s3">When you are ready press the button below to validate the inputs</p>
		<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
		<input type = "submit" value = "Validate Inputs">
	</fieldset>
</fieldset>
</form>
<body>
<html>