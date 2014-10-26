%include('header')
% URL = "http://localhost:8080/coefficients/" + uid  + "/" + str(len(items_dict['export_list'])) + '/' + str(len(items_dict['import_list'])) + "/validate"
<div class = "div1" id="about" style="width:300px;height:1150px;float:left;margin-right: 40px">
	<p class="s2" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		About The Validate Export Items Page
	</p>
	<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
	<p class="s3" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		This is the fourth page of the digitizing of the the import licence application form. <br/>
		<br/>
		On this page there is space for you to add detail relating to how much of each import item
		goes into making each export item. The fields are all floating point numbers<br/>
		<br/>
		By clicking the 'Validate Coefficients Inputs' button at the end of this page you will guided through a 
		process to make sure the fields are correctly completed.<br/>
		<br/>	
		At any time you can access the documentation 
		<a href = "/documentation" target="_blank">here</a><br/>
	</p>
</div>

<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
<form method = "post" action = {{URL}} name = "imports">
	<fieldset>
		<legend class = "s2">Add Import Coefficients Detail for {{factory}}</legend>
		<table class = "table2" border = 0 name = "coefficients">
			<tr>
			<td><b>INPUT <br/>DESCIPTION</b></td>
			<td><b>INPUT UNIT</b></td>
			%for item in items_dict['export_list']:
				<td><b>{{item}}</b></td>
			%end
			</tr>
			%for x in xrange(len(items_dict['import_list'])):
				<tr>
				<td>{{items_dict['import_list'][x]}}</td>
				<td>{{items_dict['units_list'][x]}}</td>
				%for y in xrange(len(items_dict['export_list'])):
					<td>
						<input size = 8 type = "text" name="{{str(x+1) + '_' + str(y+1)}}" required><br/>
					</td>
				%end
				</tr>
			%end
		</table>
		<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
		<br/>
		<fieldset>
			<legend class = "s2"> Validate Coefficients </legend>
			<p class = "s3">When you are ready press the button below to validate the inputs</p>
			<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
		<input type = "submit" value = "Validate Coefficients">
		</fieldset>
	</fieldset>
</form>
</body>
</html>
		
			
			
		