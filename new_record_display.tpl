% fact_name = record[1]
% fact_adress = record[2]
% URL = "http://localhost:8080/order/" + uid

%include('header')

<div class = "div1" id="about" style="width:350px;height:550px;float:left;margin-right: 40px">
	<p class="s2" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		About The Display New Record Page
	</p>
	<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
	<p class="s3" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		This page displays the record you just created in the the Database of Factories. <br/>
		<br/>
		You can now either choose to return to the home page by clicking the "Start Over"
		button on this page or you can begin the digitization of the
		import licence application form for the factory newly entered into the Factory
		Database by clicking the "Begin Application Digitization" button. <br/>
		<br/>		
		At any time you can access the documentation 
		<a href = "/documentation" target="_blank">here</a><br/>
	</p>
</div>

<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
<p class = 's2'> You Successfully Added {{fact_name}} to the Database</p>
<table class = 'table1'>
	<tr>
		<td width = 125><b>FIELD</b></td>
		<td width = 125><b>VALUE</td>
	</tr>
	<tr>
		<td>Factory Name</td>
		<td>{{fact_name}}</td>
	</tr>
	<tr>
		<td>Factory Address</td>
		<td>{{fact_adress}}</td>
	</tr>
</table>
	
<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
<p class = 's2'> Please now choose from one of the following options: </>
<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
<form action="http://localhost:8080/welcome">
	<fieldset>
		<legend class = "s2">Start Over</legend>
		<p class ='s3'> If you would like to return to the homepage you may do so by pressing below</p>
		<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
			<input type="submit" value="Start Over"></input>
	</fieldset>
</form>
	
<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
<form action={{URL}}>
	<fieldset>
		<legend class = "s2">Begin Import Application Digitization</legend>
		<p class ='s3'> You can begin the digitization process by pressing below:</p>
		<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
			<input type="submit" value="Begin Application Digitization"></input>
	</fieldset>
</form>	
<body>
<html>

