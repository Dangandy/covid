// imports
import React, { useState, useEffect, useRef } from "react";
import * as d3 from "d3";

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
        .then((d) => {
          setHistory(d); // res.json() returns a promise.. so.. another then
        })
        .catch((err) => console.log(err));
    }
    fetchHistory();
  }, [country]);

  useEffect(() => {
    async function fetchHistory() {
      console.log("fetching prediction");
      await fetch(`/api/predict/${country}`, {
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      })
        .then((res) => res.json())
        .then((d) => {
          setPrediction(d); // res.json() returns a promise.. so.. another then
        })
        .catch((err) => console.log(err));
    }
    fetchHistory();
  }, [country]);

  useEffect(() => {
    if (history && prediction) {
      console.log("Making d3 plot");
      const height = 420;
      const width = 720;
      const margin = { top: 20, right: 30, bottom: 30, left: 40 };
      // change date
      let { results: data } = history;
      data = data.map(({ date, confirmed }) => {
        return {
          date: new Date(date),
          value: confirmed,
        };
      });

      let { results: pred } = prediction;
      pred = pred.map(({ date, prediction }) => ({
        date: new Date(date),
        value: prediction,
      }));

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
        g.attr("transform", `translate(0,${height - margin.bottom})`).call(
          d3
            .axisBottom(x)
            .ticks(width / 80)
            .tickSizeOuter(0)
        );

      const yAxis = (g) =>
        g
          .attr("transform", `translate(${margin.left},0)`)
          .call(d3.axisLeft(y))
          .call((g) => g.select(".domain").remove())
          .call((g) =>
            g
              .select(".tick:last-of-type text")
              .clone()
              .attr("x", 3)
              .attr("text-anchor", "start")
              .attr("font-weight", "bold")
              .text("Confirmed Cases")
          );

      const line = d3
        .line()
        .defined((d) => !isNaN(d.value))
        .x((d) => x(d.date))
        .y((d) => y(d.value));

      const pLine = d3
        .line()
        .defined((d) => !isNaN(d.value))
        .x((d) => x(d.date))
        .y((d) => y(d.value));

      const svg = d3.select(canvas.current);

      svg.selectAll("path").remove();
      svg.selectAll("g").remove();

      svg
        .attr("width", width)
        .attr("height", height)
        .style("-webkit-tap-highlight-color", "transparent")
        .style("overflow", "visible");

      svg.append("g").call(xAxis);
      svg.append("g").call(yAxis);
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
        .append("path")
        .datum(pred)
        .attr("fill", "none")
        .attr("stroke", "tomato")
        .attr("stroke-width", 1.5)
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")
        .attr("d", pLine);
    }
  }, [history, prediction]);

  // d3 stuff
  return <svg ref={canvas} />;
}
