function showNearbyRestaurants_business(data, businessid) {
    var causes = ["Poor", "Fair", "Good", "Excellent"];

    var margin = {top: 40, right: 25, bottom: 40, left: 50},
        width = 550 - margin.left - margin.right,
        height = 350 - margin.top - margin.bottom;

    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width]);

    var y = d3.scale.linear()
        .rangeRound([height, 0]);

    var z = d3.scale.ordinal()
        .domain(["Poor", "Fair", "Good", "Excellent"])
        .range(["#ca0020", "#f4a582", "#92c5de", "#0571b0"]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom").tickFormat(function (d) {
            return +d.split("-")[1] //
        });

    var x2Axis = d3.svg.axis()
        .scale(x)
        .tickFormat(function (d) {
            return +d.split("-")[0] //"Year1 Year2, etc depending on the tick value - 0,1,2,3,4"
        })
        .orient("top");


    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("right");

    var chart1 = d3.select("#comparisionbody").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var tooltipdiv_comp = d3.select("#comparisionbody").append("tooltipdiv_comp")
        .attr("class", "tooltip")
        .style("opacity", 0);

    var pol_groups_c1 = [];



        for (var i in data) {
            var item = data[i];
            var pol_dict = {};
            var groups = item["pol_groups"];
            for (var pol_var in groups) {
                var pol_item = groups[pol_var];
                pol_dict[pol_item["pol_group"]] = pol_item["prop"]
            }

            pol_groups_c1.push({
                "year": item["_id"]["year"],
                "quarter": item["_id"]["quarter"],
                "Poor": (1 in pol_dict) ? pol_dict["1"] : 0,
                "Fair": (2 in pol_dict) ? pol_dict["2"] : 0,
                "Good": (3 in pol_dict) ? pol_dict["3"] : 0,
                "Excellent": (4 in pol_dict) ? pol_dict["4"] : 0
            });
        }
        var layers = d3.layout.stack()(causes.map(function (c) {
            return pol_groups_c1.map(function (d) {
                return {x: d.year + "-" + d.quarter, y: d[c], name: c};
            });
        }));


        x.domain(layers[0].map(function (d) {
            return d.x;
        }));
        y.domain([0, d3.max(layers[layers.length - 1], function (d) {
            return d.y0 + d.y;
        })]).nice();

        var layer = chart1.selectAll(".layer")
            .data(layers)
            .enter().append("g")
            .attr("class", "layer")
            .style("fill", function (d, i) {
                return z(i);
            });

        layer.selectAll("rect")
            .data(function (d) {
                return d;
            })
            .enter().append("rect")
            .attr("x", function (d) {
                return x(d.x);
            })
            .attr("y", function (d) {
                return y(d.y + d.y0);
            })
            .attr("height", function (d) {
                return y(d.y0) - y(d.y + d.y0);
            })
            .attr("width", x.rangeBand() - 1)

        ;

        layer.selectAll("rect")
            .on("mouseover", function (d) {

                var delta = d.y;
                var xPos = parseFloat(d3.select(this).attr("x"));
                var yPos = parseFloat(d3.select(this).attr("y"));
                var height = parseFloat(d3.select(this).attr("height"))

                d3.select(this).attr("stroke", "red").attr("stroke-width", 0.8);


                tooltipdiv_comp.transition()
                    .duration(200)
                    .style("opacity", .9);
                tooltipdiv_comp.html(d.name + ": " + Math.round(delta) + "%" + "<br/>")
                    .style("left", xPos + "px")
                    .style("top", yPos + "px");

            })
            .on("mouseout", function () {

                d3.select(this).attr("stroke", "white").attr("stroke-width", 0.2);

                tooltipdiv_comp.transition()
                    .duration(200)
                    .style("opacity", 0);

            })
            .on("click", function (d) {
                var dict_rating = {"Poor": 1, "Fair": 2, "Good": 3, "Excellent": 4};
                var pol_value = dict_rating[d.name];
                var year = d.x.split("-")[0];
                var quarter = d.x.split("-")[1];
                var start_year = year+'-01-01';
                var end_year = year+'-12-31';
                //alert(year);
                if(typeof business !== 'undefined')
                {
                    biz_id_bubble = business['business_id'];
                }
                else
                {
                    biz_id_bubble = null
                }
                showBubbleChart(businessid, biz_radius_slider.bootstrapSlider('getValue'),start_year,end_year);
            })


        chart1.append("g")
            .attr("class", "axis-comp axis--x")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        chart1.append("g")
            .attr("class", "axis-comp axis--y")
            .attr("transform", "translate(" + width + ",0)")
            .call(yAxis);

        chart1.append("g")
            .attr("class", "axis-comp axis--x")
            .call(x2Axis)
            .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", function (d) {
                return "rotate(65)"

    });
    var verticalLegend = d3.svg.legend().labelFormat("none").cellPadding(5).orientation("vertical").units("Sentiment").cellWidth(15).cellHeight(10).inputScale(z).cellStepping(10);

    d3.select("#comparisionbody").append("svg").append("g").attr("transform", "translate(20,91)").attr("class", "legend").call(verticalLegend);
}

function showComparisionchart(data) {
    //$("#comparisionbody").html("");
    var causes = ["Poor", "Fair", "Good", "Excellent"];

    var margin = {top: 40, right: 25, bottom: 40, left: 50},
        width = 550 - margin.left - margin.right,
        height = 350 - margin.top - margin.bottom;

    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width]);

    var y = d3.scale.linear()
        .rangeRound([height, 0]);

    var z = d3.scale.ordinal()
        .domain(["Poor", "Fair", "Good", "Excellent"])
        .range(["#ca0020", "#f4a582", "#92c5de", "#0571b0"]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom").tickFormat(function (d) {
            return +d.split("-")[1] //
        });

    var x2Axis = d3.svg.axis()
        .scale(x)
        .tickFormat(function (d) {
            return +d.split("-")[0] //"Year1 Year2, etc depending on the tick value - 0,1,2,3,4"
        })
        .orient("top");


    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("right");



    var tooltipdiv_comp = d3.select("#comparisionbody").append("tooltipdiv_comp")
        .attr("class", "tooltip")
        .style("opacity", 0);

    var pol_groups_c2 = [];
    var chart2 = d3.select("#comparisionbody").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");



        for (var i in data) {
            var item = data[i];
            var pol_dict = {};
            var groups = item["pol_groups"];
            for (var pol_var in groups) {
                var pol_item = groups[pol_var];
                pol_dict[pol_item["pol_group"]] = pol_item["prop"]
            }

            pol_groups_c2.push({
                "year": item["_id"]["year"],
                "quarter": item["_id"]["quarter"],
                "Poor": (1 in pol_dict) ? pol_dict["1"] : 0,
                "Fair": (2 in pol_dict) ? pol_dict["2"] : 0,
                "Good": (3 in pol_dict) ? pol_dict["3"] : 0,
                "Excellent": (4 in pol_dict) ? pol_dict["4"] : 0
            });
        }
        var layers = d3.layout.stack()(causes.map(function (c) {
            return pol_groups_c2.map(function (d) {
                return {x: d.year + "-" + d.quarter, y: d[c], name: c};
            });
        }));

        x.domain(layers[0].map(function (d) {
            return d.x;
        }));
        y.domain([0, d3.max(layers[layers.length - 1], function (d) {
            return d.y0 + d.y;
        })]).nice();

        var layer = chart2.selectAll(".layer")
            .data(layers)
            .enter().append("g")
            .attr("class", "layer")
            .style("fill", function (d, i) {
                return z(i);
            });

        layer.selectAll("rect")
            .data(function (d) {
                return d;
            })
            .enter().append("rect")
            .attr("x", function (d) {
                return x(d.x);
            })
            .attr("y", function (d) {
                return y(d.y + d.y0);
            })
            .attr("height", function (d) {
                return y(d.y0) - y(d.y + d.y0);
            })
            .attr("width", x.rangeBand() - 1);

        layer.selectAll("rect")
            .on("mouseover", function (d) {

                // var hoverArray = document.querySelectorAll( ":hover" );
                // var elem = hoverArray[hoverArray.length - 1];
                // var elemUpper = hoverArray[hoverArray.length - 2];
                // var rectObject = elemUpper.getBoundingClientRect();
                //console.log(rectObject);

                var delta = d.y;
                var xPos = parseFloat(d3.select(this).attr("x"));
                var yPos = parseFloat(d3.select(this).attr("y"));
                var height = parseFloat(d3.select(this).attr("height"))

                d3.select(this).attr("stroke", "red").attr("stroke-width", 0.8);

                tooltipdiv_comp.transition()
                    .duration(200)
                    .style("opacity", 0.9);
                tooltipdiv_comp.html(d.name + ": " + Math.round(delta) + "%" + "<br/>")
                    .style("opacity", .9)
                    .style("left", ((xPos+width+350) + "px"))
                    .style("top", ((yPos+50) +"px"));


            })
            .on("mouseout", function () {

                d3.select(this).attr("stroke", "white").attr("stroke-width", 0.2);

                tooltipdiv_comp.transition()
                    .duration(1000)
                    .style("opacity", 0);
            })

        chart2.append("g")
            .attr("class", "axis-comp axis--x")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        chart2.append("g")
            .attr("class", "axis-comp axis--y")
            .attr("transform", "translate(" + width + ",0)")
            .call(yAxis);

        chart2.append("g")
            .attr("class", "axis-comp axis--x")
            .call(x2Axis)
            .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", function (d) {
                return "rotate(65)"
            });



}

var fetchAttributesForComparision = function (businessid, radius) {
    $("#comparisionbody").html("");
    if (businessid == null) {
        businessid = "Sq596PqWNj7J0s-YAQmrQA";
        console.warn('Using sample biz_id = ' + businessid);
    }

    if (radius == null) {
        radius = 1;
        console.warn('Using sample radius =' + radius);
    }

    if (window.jQuery)
        $.ajax({
            type: "GET",
            url: 'http://localhost:5000' + "/getdata/foodqualityvariation/" + businessid,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (response) {
                showNearbyRestaurants_business(response, businessid);
            },
            error: function (xhr, textStatus, errorMessage) {
                console.log(errorMessage);
            }
        });
    else {
        console.warn("Switching to local");
        // paracoordOnTrigger();
    }

    if (window.jQuery)
        $.ajax({
            type: "GET",
            url: 'http://localhost:5000' + "/getdata/foodqualityvariation/" + businessid + "/radius/" + radius,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (response) {
                showComparisionchart(response);
            },
            error: function (xhr, textStatus, errorMessage) {
                console.log(errorMessage);
            }
        });
    else {
        console.warn("Switching to local");
        // paracoordOnTrigger();
    }
}