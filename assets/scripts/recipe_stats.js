import * as d3 from "d3";

export function createStatsChart() {
    let views;
    let likes;

    try {
        views = parseInt(document.getElementById('recipeViews').innerHTML);
        likes = parseInt(document.getElementById('recipeLikes').innerHTML);
    } catch (e) {
        console.error('No recipe found');
        return false;
    }

    const width = 300;
    const height = 300;
    const margin = 40;

    const radius = Math.min(width, height) / 2 - margin;

    const svg = d3.select("#recipeStatisticChart")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    // Create data
    const data = {
        views: views,
        likes: likes
    };

    // set the color
    const color = d3.scaleOrdinal()
        .domain(data)
        .range(d3.schemeSet2);

    const pie = d3.pie()
        .value(function (d) {
            return d.value;
        });
    const data_ready = pie(d3.entries(data));

    const arcGenerator = d3.arc()
        .innerRadius(0)
        .outerRadius(radius);

    svg
        .selectAll('mySlices')
        .data(data_ready)
        .enter()
        .append('path')
        .attr('d', arcGenerator)
        .attr('fill', function (d) {
            return (color(d.data.value));
        })
        .attr("stroke", "white")
        .style("stroke-width", "2px")
        .style("opacity", 0.7);

    // Add labels
    svg
        .selectAll('mySlices')
        .data(data_ready)
        .enter()
        .append('text')
        .text(function (d) {
            return d.data.value + ' ' + d.data.key;
        })
        .attr("transform", function (d) {
            return "translate(" + arcGenerator.centroid(d) + ")";
        })
        .style("text-anchor", "middle");
}