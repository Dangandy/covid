// 3rd party imports
import React, { useState, useEffect, useRef } from "react";
import * as d3 from "d3";

// local imports
import formatNumber from "../utils/utils";

// Components
export default function History({ country }) {
  const [history, setHistory] = useState();
  const [prediction, setPrediction] = useState();
  const canvas = useRef(null);

  useEffect(() => {
    async function fetchHistory() {
      console.log("fetching history");
      await fetch(`/api/plot/${country}`, {
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      })
        .then((res) => res.json())
        .then(({ result }) => {
          console.log("retrieved plot info");
          const hist = result.filter((res) => res.confirmed);
          const pred = result.filter((res) => res.confirmed_pred);
          setHistory(hist); // res.json() returns a promise.. so.. another then
          setPrediction(pred);
        })
        .catch((err) => console.log(err));
    }
    fetchHistory();
  }, [country]);

  useEffect(() => {
    if (history && prediction) {
      console.log("Making d3 plot");
      const height = 400;
      const width = 720;
      const margin = { top: 20, right: 30, bottom: 50, left: 50 };
      // change date
      let data = history.map(({ date, confirmed }) => {
        const d = new Date(date);
        return {
          date: d.setHours(d.getHours() + 4),
          value: confirmed,
        };
      });

      let pred = prediction.map(({ date, confirmed_pred }) => {
        const d = new Date(date);
        return {
          date: d.setHours(d.getHours() + 4),
          value: confirmed_pred,
        };
      });

      // add data and pred together to get full size..
      const combine = [...data, ...pred];

      const x = d3
        .scaleUtc()
        .domain(d3.extent(combine, (d) => d.date))
        .range([margin.left, width - margin.right]);

      const y = d3
        .scaleLinear()
        .domain([0, d3.max(combine, (d) => d.value)])
        .nice()
        .range([height - margin.bottom, margin.top]);

      const xAxis = (g) =>
        g
          .attr("transform", `translate(0,${height - margin.bottom})`)
          .call(
            d3
              .axisBottom(x)
              .ticks(width / 80)
              .tickSizeOuter(0)
          )
          .call((g) => g.select(".domain").remove());

      const yAxis = (g) =>
        g
          .attr("transform", `translate(${margin.left},0)`)
          .call(d3.axisLeft(y))
          .call((g) => g.select(".domain").remove());

      const line = d3
        .line()
        .defined((d) => !isNaN(d.value))
        .x((d) => x(d.date))
        .y((d) => y(d.value));

      // Define the div for the tooltip
      var tooltip = d3
        .select("body")
        .append("div")
        .attr("class", "tooltip")
        .style("position", "absolute")
        .style("z-index", "10")
        .style("visibility", "hidden")
        .style("background", "azure");
      var formatTime = d3.timeFormat("%B %e");

      const svg = d3.select(canvas.current);

      svg.selectAll("path").remove();
      svg.selectAll("g").remove();
      svg.selectAll("text").remove();

      svg
        .attr("width", width)
        .attr("height", height)
        .style("-webkit-tap-highlight-color", "transparent")
        .style("overflow", "visible");

      svg.append("g").call(xAxis);
      svg
        .append("text")
        .attr("text-anchor", "middle") // this makes it easy to centre the text as the transform is applied to the anchor
        .attr("transform", `translate(${width / 2 + 40},${height - 15})`) // centre below axis
        .text("Date");

      svg.append("g").call(yAxis);
      svg
        .append("text")
        .attr("text-anchor", "middle") // this makes it easy to centre the text as the transform is applied to the anchor
        .attr("transform", "translate(0," + height / 2 + ")rotate(-90)") // text is drawn off the screen top left, move down and out and rotate
        .text("# Confirmed Cases");
      svg
        .append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 1.5)
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")
        .attr("d", line);

      svg
        .append("g")
        .selectAll("dot")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", function (d) {
          return x(d.date);
        })
        .attr("cy", function (d) {
          return y(d.value);
        })
        .attr("r", 3)
        .attr("fill", "steelblue")
        .on("mouseover", function (d) {
          return tooltip.style("visibility", "visible");
        })
        .on("mousemove", function (d) {
          return tooltip
            .html(formatTime(d.date) + "<br/>Cases: " + formatNumber(d.value))
            .style("top", d3.event.pageY - 10 + "px")
            .style("left", d3.event.pageX + 10 + "px");
        })
        .on("mouseout", function () {
          return tooltip.style("visibility", "hidden");
        });

      // Add the points
      svg
        .append("g")
        .selectAll("dot")
        .data(pred)
        .enter()
        .append("circle")
        .attr("cx", function (d) {
          return x(d.date);
        })
        .attr("cy", function (d) {
          return y(d.value);
        })
        .attr("r", 3)
        .attr("fill", "tomato")
        .on("mouseover", function (d) {
          return tooltip.style("visibility", "visible");
        })
        .on("mousemove", function (d) {
          return tooltip
            .html(
              formatTime(d.date) + "<br/>Prediction: " + formatNumber(d.value)
            )
            .style("top", d3.event.pageY - 10 + "px")
            .style("left", d3.event.pageX + 10 + "px");
        })
        .on("mouseout", function () {
          return tooltip.style("visibility", "hidden");
        });
    }
  }, [history, prediction]);

  // d3 stuff
  return <svg ref={canvas} />;
}
