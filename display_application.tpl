%include('header')


<div class = "div1" style=height:450px;float:left;margin-right:1000px">
<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
<table class = "table2" border = 0 name = "order_info">
	<caption class = "s2">Order Information</caption>
	<tr>
		<td width = 175><b>FIELD</b></td>
		<td width = 275><b>VALUE</td>
	</tr>
	<tr>
		<td>Order ID Number</td>
		<td>{{retrieved_data['order_data']['order_id']}}</td>
	</tr>
	<tr>
		<td>Exporter</td>
		<td>{{factory}}	</td>
	</tr>
	<tr>
		<td>Buyer Name</td>
		<td>{{retrieved_data['order_data']['buyer']}}</td>
	</tr>
	<tr>
		<td>Buyer Country of Origin</td>
		<td>{{retrieved_data['order_data']['buyer_country1']}}, {{retrieved_data['order_data']['buyer_country2']}}, {{retrieved_data['order_data']['buyer_country3']}}</td>
	</tr>
</table>
<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>


<table class = "table2" border = 0 name = "price_info">
	<caption class = "s2">Price Information</caption>
	<tr>
		<td width = 175><b>FIELD</b></td>
		<td width = 275><b>VALUE</td>
	</tr>
	<tr>
		<td> Total FOB Value </td>
		<td>{{retrieved_data['order_data']['total_fob_curr']}} {{retrieved_data['order_data']['total_fob']}}</td>
	</tr>
	<tr>
		<td> Total CMP Value </td>
		<td>{{retrieved_data['order_data']['total_cmp_curr']}} {{retrieved_data['order_data']['total_cmp']}}</td>
	</tr>
	<tr>
		<td> Total CIF Value </td>
		<td>{{retrieved_data['order_data']['total_cif_curr']}} {{retrieved_data['order_data']['total_cif']}}</td>
	</tr>
</table>
<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
</div>

<div class = "div1" style=height:450px>
<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
<table class = "table2" border = 0 name = "order_time">
	<caption class = "s2">Order Timeline</caption>
	<tr>
		<td width = 175><b>FIELD</b></td>
		<td width = 275><b>VALUE</td>
	</tr>
	<tr>
		<td>Submission Date</td>
		<td>{{retrieved_data['order_data']['sub_date']}}</td>
	</tr>
	<tr>
		<td>ApprovalDate</td>
		<td>{{retrieved_data['order_data']['app_date']}}</td>
	</tr>
	<tr>
		<td>Shipment Date</td>
		<td>{{retrieved_data['order_data']['ship_date']}}</td>
	</tr>
</table>
<p style="text-indent: 0pt;line-height: 30pt;text-align: left;"><br/></p>

<table class = "table2" border = 0 name = "imp_exp">
	<caption class = "s2">Order Import & Export Items</caption>
	<tr>
		<td width = 175><b>FIELD</b></td>
		<td width = 275><b>VALUE</td>
	</tr>
	<tr>
		<td>Number of Export Items</td>
		<td>{{retrieved_data['order_data']['export_items']}}</td>
	</tr>
	<tr>
		<td>Total Quantity Export Items</td>
		<td>{{retrieved_data['order_data']['export_quantity']}}</td>
	</tr>
	<tr>
		<td>Number of Import Items</td>
		<td>{{retrieved_data['order_data']['import_items']}}</td>
	</tr>
</table>
<p style="text-indent: 0pt;line-height: 14pt;text-align: left;"><br/></p>
</div>
<p style="text-indent: 0pt;line-height: 28pt;text-align: left;"><br/></p>

<div class = "div1">
<p class = "s2">Export Items</p></tr>
<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
<table class = "table2" border = 0 name = "export_items">
	<tr>
		<td><b>Category</b></td>
		<td><b>Type</b></td>
		<td><b>Description</b></td>
		<td><b>Number of Units</b></td>
		<td><b>FOB Value</b></td>
		<td><b>CMP Value</b></td>
	</tr>
	%for x in xrange(retrieved_data['order_data']['export_items']):
		<tr>
			<td>{{retrieved_data['export_data']['category' + str(x+1)]}}</td>
			<td>{{retrieved_data['export_data']['type' + str(x+1)]}}</td>
			<td>{{retrieved_data['export_data']['description' + str(x+1)]}}</td>
			<td>{{retrieved_data['export_data']['units' + str(x+1)]}}</td>
			<td>{{retrieved_data['export_data']['unit_fob_curr' + str(x+1)]}} {{retrieved_data['export_data']['unit_fob' + str(x+1)]}}</td>
			<td>{{retrieved_data['export_data']['unit_cmp_curr' + str(x+1)]}} {{retrieved_data['export_data']['unit_cmp' + str(x+1)]}}</td>
		</tr>
	%end
</table>
<p style="text-indent: 0pt;line-height: 14pt;text-align: left;"><br/></p>
</div>
<p style="text-indent: 0pt;line-height: 28pt;text-align: left;"><br/></p>

<div class = "div1">
<p class = "s2">Import Items</p></tr>
<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
<table class = "table2" border = 0 name = "import_items">
	<tr>
		<td><b>Type</b></td>
		<td><b>Description</b></td>
		<td><b>Units of Measure</b></td>
		<td><b>Quantity</b></td>
		<td><b>Value</b></td>
	</tr>
	%for x in xrange(retrieved_data['order_data']['import_items']):
		<tr>
			<td>{{retrieved_data['import_data']['import_type' + str(x +1)]}}</td>
			<td>{{retrieved_data['import_data']['import_description' + str(x +1)]}}</td>
			<td>{{retrieved_data['import_data']['import_unit' + str(x +1)]}}</td>
			<td>{{retrieved_data['import_data']['quantity' + str(x +1)]}}</td>
			<td>{{retrieved_data['import_data']['import_item_curr' + str(x +1)]}} {{retrieved_data['import_data']['total_price' + str(x +1)]}}</td>
		</tr>
	%end
</table>
<p style="text-indent: 0pt;line-height: 14pt;text-align: left;"><br/></p>
</div>
<p style="text-indent: 0pt;line-height: 28pt;text-align: left;"><br/></p>

<div class = "div1">
<p class = "s2">Import Export Coefficients</p></tr>
<p style="text-indent: 0pt;line-height: 7pt;text-align: left;"><br/></p>
<table class = "table2" border = 0 name = "coefficients">
	<tr>
		<td><b>INPUT <br/>DESCIPTION</b></td>
		<td><b>INPUT UNIT</b></td>
		%for x in xrange(retrieved_data['order_data']['export_items']):
			<td><b>{{retrieved_data['export_data']['description' + str(x+1)]}}</b></td>
		%end
	</tr>
	%for x in xrange(retrieved_data['order_data']['import_items']):
		<tr>
			<td>{{retrieved_data['import_data']['import_description' + str(x +1)]}}</td>
			<td>{{retrieved_data['import_data']['import_unit' + str(x +1)]}}</td>
			%for y in xrange(retrieved_data['order_data']['export_items']):
				<td>{{retrieved_data['coefficients_data'][str(x +1) + '_' + str(y +1)]}}</td>
			%end
		</tr>
	%end
</table>
</div>


