var margin = { top: 0, right: 0, bottom: 0, left: 0 };
var width, height, outerRadius, innerRadius;

function setDimensions() {

  var margin = {top: 0, right: 0, bottom: 0, left: 0};
  width = 600 - margin.left - margin.right;
  height = 600 - margin.top - margin.bottom;
  outerRadius = Math.min(width, height) / 2; // The outerRadius goes from the middle of the SVG area to the border
  innerRadius = outerRadius/2.4;
  if (window.innerWidth < 600) {
    // Adjust dimensions for mobile
    width = window.innerWidth - margin.left - margin.right;
    height = window.innerWidth - margin.top - margin.bottom;
    outerRadius = Math.min(width, height) / 3; // The outerRadius goes from the middle of the SVG area to the border
    innerRadius = outerRadius/1.6;
  }


}



function loadCircularData() {

  setDimensions(); // Set dimensions before loading data
 // append the svg object

d3.select("#my_dataviz").selectAll("svg").remove();
 fetch('/get_circular_data')
   .then(response => response.json())
   .then(data => {
     // Use data to render your circular bar plot
             // append the svg object
var svg = d3.select("#my_dataviz")
.append("svg")
 .attr("width", width + margin.left + margin.right)
 .attr("height", height + margin.top + margin.bottom)
.append("g")
 .attr("transform", "translate(" + (width / 2 + margin.left) + "," + (height / 2 + margin.top) + ")");

  svg.append("text")
  .attr("x", 0) // center alignment
  .attr("y", height / 2 - margin.bottom - 30) // placing the title above the circular plot
  .attr("text-anchor", "middle")
  .style("font-size", "15px")
  .style("fill", "green")
  .text("Outer Circle: Projects Completed");

  svg.append("text")
  .attr("x", 0) // center alignment
  .attr("y", height / 2 - margin.bottom - 10 ) // placing the title above the circular plot
  .attr("text-anchor", "middle")
  .style("font-size", "15px")
  .style("fill", "red")
  .text("Inner Circle: Projects In Progress");
// X scale: common for 2 data series
var x = d3.scaleBand()
.range([0, 2 * Math.PI])
.align(0)
.domain(data.map(function(d) { return d.Category; }));

// Y scale outer variable
var y = d3.scaleRadial()
.range([innerRadius, outerRadius])
.domain([0, 12]);

// Y scale inner variable
var yinner = d3.scaleRadial()
.range([innerRadius, 70])
.domain([0, d3.max(data, function(d) { return d.InnerValue; })]);

// Add the bars with modified inner radius
svg.append("g")
.selectAll("path")
.data(data)
.enter()
.append("path")
 .attr("fill", "#69b3a2")
 .attr("class", "yo")
 .attr("d", d3.arc()
     .innerRadius(function(d) { return yinner(d.InnerValue); })
     .outerRadius(function(d) { return y(d.Value); })
     .startAngle(function(d) { return x(d.Category); })
     .endAngle(function(d) { return x(d.Category) + x.bandwidth(); })
     .padAngle(0.01)
     .padRadius(innerRadius));

// Add the outer radius values labels
svg.append("g")
.selectAll("g")
.data(data)
.enter()
.append("g")
 .attr("text-anchor", function(d) { return (x(d.Category) + x.bandwidth() / 2 + Math.PI) % (2 * Math.PI) < Math.PI ? "end" : "start"; })
 .attr("transform", function(d) { return "rotate(" + ((x(d.Category) + x.bandwidth() / 2) * 180 / Math.PI - 90) + ")"+"translate(" + (y(d.Value)+10) + ",0)"; })
.append("text")
 .text(function(d){return d.Value;})
 .attr("transform", function(d) { return (x(d.Category) + x.bandwidth() / 2 + Math.PI) % (2 * Math.PI) < Math.PI ? "rotate(180)" : "rotate(0)"; })
 .style("font-size", "11px")
 .style("fill", "white")
 .attr("alignment-baseline", "middle");

// Add the inner radius values labels
svg.append("g")
.selectAll("g")
.data(data)
.enter()
.append("g")
 .attr("text-anchor", function(d) { return (x(d.Category) + x.bandwidth() / 2 + Math.PI) % (2 * Math.PI) < Math.PI ? "end" : "start"; })
 .attr("transform", function(d) { return "rotate(" + ((x(d.Category) + x.bandwidth() / 2) * 180 / Math.PI - 90) + ")"+"translate(" + (yinner(d.InnerValue)-15) + ",0)"; })
.append("text")
 .text(function(d){return d.InnerValue;})
 .attr("transform", function(d) { return (x(d.Category) + x.bandwidth() / 2 + Math.PI) % (2 * Math.PI) < Math.PI ? "rotate(180)" : "rotate(0)"; })
 .style("font-size", "11px")
 .style("fill", "white")
 .attr("alignment-baseline", "middle");

// Add the category labels
svg.append("g")
.selectAll("g")
.data(data)
.enter()
.append("g")
 .attr("text-anchor", function(d) { return (x(d.Category) + x.bandwidth() / 2 + Math.PI) % (2 * Math.PI) < Math.PI ? "end" : "start"; })
 .attr("transform", function(d) { return "rotate(" + ((x(d.Category) + x.bandwidth() / 2) * 180 / Math.PI - 90) + ")"+"translate(" + (y(d.Value)+10) + ",0)"; })
.append("text")
 .text(function(d){return d.Category;})
 .attr("transform", function(d) { return (x(d.Category) + x.bandwidth() / 2 + Math.PI) % (2 * Math.PI) < Math.PI ? "rotate(180)" : "rotate(0)"; })
 .style("font-size", "11px")
 .style("fill", "white")
 .attr("dy", "-1em"); // Adjust the vertical position of the value labels
 

// Add the second series
svg.append("g")
.selectAll("path")
.data(data)
.enter()
.append("path")
 .attr("fill", "red")
 .attr("d", d3.arc()
     .innerRadius(function(d) { return yinner(0); })
     .outerRadius(function(d) { return yinner(d.InnerValue); })
     .startAngle(function(d) { return x(d.Category); })
     .endAngle(function(d) { return x(d.Category) + x.bandwidth(); })
     .padAngle(0.01)
     .padRadius(innerRadius));


   });
}

loadCircularData(); // Call on page load

let previousWidth = window.innerWidth;

function onResize() {
  if (Math.abs(previousWidth - window.innerWidth) > 200) {
    loadCircularData();
  }
  previousWidth = window.innerWidth;
}

window.addEventListener('resize', onResize);


