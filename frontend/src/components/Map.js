import React, { useMemo, memo } from "react";
import { scaleLinear } from "d3-scale";
import {
  ComposableMap,
  Geographies,
  Geography,
  Sphere,
  Graticule,
} from "react-simple-maps";
import styled from "styled-components";
import { style } from "d3";

const geoUrl =
  "https://raw.githubusercontent.com/zcreativelabs/react-simple-maps/master/topojson-maps/world-110m.json";

const ToolTip = styled.div`
  display: flex;
  flex-direction: column;
  line-height: 1.25rem;
  span {
    font-size: 1rem;
  }
`;

const Title = styled.span`
  font-size: 1.25rem;
  font-weight: 600;
`;

const MapChart = ({ max, setTooltipContent, data }) => {
  const colorScale = useMemo(() => {
    return scaleLinear().domain([0, max]).range(["#E6A6A6", "#E60000"]);
  }, [max]);

  return (
    <>
      <ComposableMap
        data-tip=""
        height={500}
        projectionConfig={{
          scale: 150,
        }}
      >
        <Sphere stroke="#E4E5E6" strokeWidth={0.5} />
        <Graticule stroke="#E4E5E6" strokeWidth={0.5} />
        <Geographies geography={geoUrl}>
          {({ geographies }) =>
            geographies.map((geo) => {
              const d = data.find((s) => {
                if (s.country === "US") {
                  return "United States of America" === geo.properties.NAME;
                } else {
                  return s.country === geo.properties.NAME;
                }
              });
              return (
                <Geography
                  key={geo.rsmKey}
                  geography={geo}
                  fill={d ? colorScale(d.confirmed) : "#E6A6A6"}
                  onMouseEnter={() => {
                    if (d) {
                      setTooltipContent(
                        <ToolTip>
                          <Title>{d.country}</Title>
                          <span>Confirmed: {d.confirmed}</span>
                          <span>Recovered: {d.recovered}</span>
                          <span>Deaths: {d.deaths}</span>
                          {d.confirmed_pred ? (
                            <span>Predicted Cases: d.confirmed_pred</span>
                          ) : (
                            ""
                          )}
                        </ToolTip>
                      );
                    }
                  }}
                  onMouseLeave={() => {
                    setTooltipContent("");
                  }}
                  style={{
                    hover: {
                      stroke: "dimgray",
                      strokeWidth: 0.7,
                      outline: "none",
                    },
                    pressed: {
                      stroke: "dimgray",
                      strokeWidth: 1,
                      outline: "none",
                    },
                  }}
                />
              );
            })
          }
        </Geographies>
      </ComposableMap>
    </>
  );
};

export default memo(MapChart);
