// imports
import React, { useState, useEffect } from "react";
import styled from "styled-components";

// local
import formatNumber from "../utils/utils";

// styled components
const Block = styled.div`
  padding: 0.25em;
  margin: 0.25em;
  color: dimgray;
  border: none;
  font-size: 1em;
  display: grid;
  grid-template-rows: 1fr;
  justify-content: center;
  align-items: center;
`;

const Number = styled.span`
  color: ${(props) => (props.type ? props.type : "palevioletred")};
  font-size: 2em;
`;

export default function StatsBlock({ type, cur }) {
  // states
  const [direction, setDirection] = useState("dimgray");
  const [value, setValue] = useState(0);

  useEffect(() => {
    setValue(formatNumber(cur));
  }, [cur]);

  useEffect(() => {
    if (type === "Confirmed") {
      setDirection("palevioletred");
    } else if (type === "Recovered") {
      setDirection("palegreen");
    } else {
      setDirection("dimgray");
    }
  }, [cur, type]);

  // return
  return (
    <Block>
      <Number type={direction}>{value}</Number>
      <span>{`${type}`}</span>
    </Block>
  );
}
