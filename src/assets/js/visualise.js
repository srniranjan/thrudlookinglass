var user_data = null;
var w = 500;
var h = 500;
var padding = 40;

function compare(a,b) {
	var a_vals = String(a.date).split(':');
	var b_vals = String(b.date).split(':');
	var a_month = parseInt(a_vals[0]);
	var a_year = parseInt(a_vals[1]);
	var b_month = parseInt(b_vals[0]);
	var b_year = parseInt(b_vals[1]);
	if(a_year > b_year)//a > b
		return 1;
	if(a_year < b_year)//a < b
		return -1;
    if(a_year == b_year && a_month > b_month)//a > b
		return 1;
    if(a_year == b_year && a_month < b_month)//a < b
		return -1;
	return 0;
}

function populate_dropdown(){
	var dates = $("#dates");
	sorted_dates = user_data.children.sort(compare);
	$.each(sorted_dates, function() {
	    dates.append($("<option />").val(this.date).text(this.date));
	});
}

function handle_date_events(){
	$("#dates").change(function(){
		show_data_for($(this).val())
	});
}

function get_dataset_for(date){
	for(var i = 0; i < user_data.children.length; i++){
		if(user_data.children[i].date == date)
			return user_data.children[i].children;
	}
	return null;
}

function render_axes(xScale, yScale){
	var svg = d3.select("svg");
	var xAxis = d3.svg.axis()
	                   .scale(xScale)
	                   .orient("bottom");
	var yAxis = d3.svg.axis()
	                 .scale(yScale)
	                 .orient("left");
				 
	 if($(".axis").length == 0){
		svg.append("g")
		   .attr("class", "x axis")
		   .attr("transform", "translate(0," + (h - (padding / 2)) + ")")
		   .call(xAxis);
		svg.append("g")
			.attr("class", "y axis")
			.attr("transform", "translate(" + padding + ",0)")
			.call(yAxis);	 	
	 }
	 else{
		 d3.select(".x.axis")
		 	 .transition()
	            .duration(500)
	            .call(xAxis);
		 d3.select(".y.axis")
			 .transition()
	         .duration(500)
	         .call(yAxis);			 
	 }
	
}

function animate_existing_concepts(svg, dataset, concept_names, xScale, yScale, rScale){
	svg.selectAll(".concept")
	   .filter(function(d){
			 return $.inArray(d.name, concept_names) >= 0;
		 })
	   .data(dataset)
	   .transition()
	   .duration(500)
       .attr("cx", function(d) {
	   	return xScale(d.occurances);
	   })
	   .attr("cy", function(d) {
	   	return yScale(d.num_likes);
	   })
	   .attr("r", function(d) {
	   	return rScale(d.len_text);
	   });
}

function remove_old_concepts(svg, concept_names){
	svg.selectAll(".concept")
	   .filter(function(d){
		   return $.inArray(d.name, concept_names) == -1;
	   })
	   .data([])
	   .exit()
	   .remove();
}

function add_new_concepts(svg, dataset, xScale, yScale, rScale){
	var color = d3.scale.category20();
	svg.selectAll("circle")
	 .data(dataset)
	 .enter()
	 .append("circle")
	 .attr("cx", function(d) {
	     return xScale(d.occurances);
	    })
	 .attr("cy", function(d) {
	     return yScale(d.num_likes);
	 })
	 .attr("r", function(d) {
		 return rScale(d.len_text);
	 })
	 .attr("class", "concept")
	 .attr("fill",function(d,i){return color(i);});	
}

function render_circles(xScale, yScale, dataset){
 	var rScale = d3.scale.linear()
                   .domain([0, d3.max(dataset, function(d) { return d.len_text; })])
                   .range([2, 15]);
					   
	var svg = d3.select("svg");
	if($(".concept").length == 0){
		add_new_concepts(svg, dataset, xScale, yScale, rScale);
	}
	else{
		var concept_names = [];
		for(var i = 0; i < dataset.length; i++)
			concept_names.push(dataset[i].name);
		animate_existing_concepts(svg, dataset, concept_names, xScale, yScale, rScale);
		remove_old_concepts(svg, concept_names);
		add_new_concepts(svg, dataset, xScale, yScale, rScale);
	}
}

function show_data_for(date){
	var dataset = get_dataset_for(date);
	
  	var xScale = d3.scale.linear()
                     .domain([0, d3.max(dataset, function(d) { return d.occurances; })])
                     .range([padding, w - padding]);	
   	var yScale = d3.scale.linear()
   	                  .domain([0, d3.max(dataset, function(d) { return d.num_likes; })])
   	                  .range([h - padding, padding]);

	render_axes(xScale, yScale);
	render_circles(xScale, yScale, dataset);
}

function initialize(email){
	handle_date_events();
	
	var svg = d3.select("body")
	          .append("svg")
	          .attr("width", w)
	          .attr("height", h);

	$.getJSON('/visualisation_data?email=' + email, function(data) {
		user_data = data;
		populate_dropdown();
		$("#dates").change();
	});
}