% fact_name = record[1]
% fact_adress = record[2]
% URL = "http://localhost:8080/order/" + uid

%include('header')

<div class = "div1" id="about" style="width:300px;height:550px;float:left;margin-right: 40px">
	<p class="s2" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		About The Factory Details Page
	</p>
	<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
	<p class="s3" style="padding-left: 5pt;text-indent: 0pt;text-align: left;">
		This page displays the factory details from the Database of Factories as per the 
		factory name selected from the dropdown menu on the previous page. <br/>
		<br/>
		If the factory selected is not the required factory you can click the "Start Over"
		button on this page to return to the homepage. Alternatively you can begin the digitization of the
		import licence application form by clicking the "Begin Application Digitization" button.<br/>
		<br/> 
		At any time you can access the documentation 
		<a href = "/documentation" target="_blank">here</a><br/>
	</p>
</div>

<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
<p class = 's2'> Factory Details for {{fact_name}}</p>
<table class = 'table1'>
	<tr>
		<td width = 200><b>FIELD</b></td>
		<td width = 200><b>VALUE</td>
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
<p class = 's2'> Please check the above details and choose from one of the following options: </>
<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
<form action="http://localhost:8080/welcome">
	<fieldset>
		<legend class = "s2">Start Over</legend>
		<p class ='s3'> If this is not the factory you were looking for, you can return to the homepage by pressing below:</p>
		<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
			<input type="submit" value="Start Over"></input>
	</fieldset>
</form>
	
<p style="text-indent: 0pt;line-height: 10pt;text-align: left;"><br/></p>
<form action={{URL}}>
	<fieldset>
		<legend class = "s2">Begin Import Application Digitization</legend>
		<p class ='s3'> If this is the factory you were looking for, you can begin the digitization process by pressing below:</p>
		<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
			<input type="submit" value="Begin Application Digitization"></input>
	</fieldset>
</form>	
<body>
<html>