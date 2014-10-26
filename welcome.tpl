% ADD_URL = "http://localhost:8080/add/" + new_uid
%facts = fact_uid_dict.keys()
%facts.sort()

%include('header')

<div class = "div1" id="about" style="width:350px;height:575px;float:left;margin-right: 40px">
	<p class="s2" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		About The Application
	</p>
	<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
	<p class="s3" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		<b>Author</b>: Rory Creedon <br/>
		<b>Contact</b>: rcreedon@poverty-action.org<br/>
		<br/>
		This application is for the digitization of import licence application forms held by the 
		MGMA.<br/>
		<br/>
		On each page of this application a sidebar such as this one explains the function of each page.<br/>
		<br/>
		On this page you can call up a Factory Details from the database. To do this see the 
		"Call Up Factory Details" box. Once the details have been called up the digitization of the 
		import licence application form can begin.<br/>
		<br/>
		If you have an import licence application form that belongs to a factory that does not currently
		exist in the database (i.e. they do not appear in the drop down menu in the "Call Up Factory Details"
		box), then you need to add that factory to the database by referring to the "Add New Factory to Database"
		box.<br/>
		<br/> 
		For more detailed instructions the user documentation can be found 
		<a href = "/documentation" target="_blank">here</a><br/>
	</p>
</div>

<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
<form action="/result" method="post">
	<fieldset>
		<legend class = "s2">Call Up Factory Details</legend>
		<p class="s3">To call up factory details from the DataBase of Factories please select a factory
					  from the drop down box below and press 'Get Details':</p>
		<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
			<p class="s3">Select Factory: <select name="UID"></p><br/>
				%for fact in facts:
					<option value = "{{fact_uid_dict[fact]}}">{{fact}}</option>
				%end
			</select>
		<input value="Get Details" type="submit"></input>
	</fieldset>
</form>
<br/>
<form action = "{{ADD_URL}}" method = "get">
	<fieldset>
		<legend class = "s2">Add New Factory to Database</legend>
		<p class="s3">To add a factory to the Database of Factories please click below:</p>
		<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
		<input type="submit" value="Add Factory">
	</fieldset>
</form>
</div>
</body>
</html>