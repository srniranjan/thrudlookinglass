function initialize(){
	console.log("Here");
	var w = 500;
	var h = 250;
	var padding = 40;
	
	var dataset = [
	                [5, 20], [480, 90], [250, 50], [100, 33], [330, 95],
	                [410, 12], [475, 44], [25, 67], [85, 21], [220, 88]
	              ];
	var svg = d3.select("body")
	          .append("svg")
	          .attr("width", w)
	          .attr("height", h);
			  
  	var xScale = d3.scale.linear()
  	                     .domain([0, d3.max(dataset, function(d) { return d[0]; })])
  	                     .range([padding, w - padding]);	
  	var yScale = d3.scale.linear()
  	                  .domain([0, d3.max(dataset, function(d) { return d[1]; })])
  	                  .range([padding, h - padding]);
	var rScale = d3.scale.linear()
	                   .domain([0, d3.max(dataset, function(d) { return d[1]; })])
	                   .range([2, 5]);

	svg.selectAll("circle")
	 .data(dataset)
	 .enter()
	 .append("circle")
	 .attr("cx", function(d) {
	     return xScale(d[0]);
     })
	 .attr("cy", function(d) {
	     return yScale(d[1]);
	 })
	 .attr("r", function(d) {
		 return rScale(d[1]);
	 });
	 
	 var xAxis = d3.svg.axis()
	                   .scale(xScale)
	                   .orient("bottom");
	svg.append("g")
	   .attr("class", "axis")
	   .attr("transform", "translate(0," + (h - (padding / 2)) + ")")
	   .call(xAxis);
	   
	var yAxis = d3.svg.axis()
	                 .scale(yScale)
	                 .orient("left");
	svg.append("g")
		.attr("class", "axis")
		.attr("transform", "translate(" + padding + ",0)")
		.call(yAxis);
}