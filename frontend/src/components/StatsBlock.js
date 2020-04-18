// imports
import React, { useState, useEffect } from "react";
import styled, { keyframes } from "styled-components";

// styled components
const Block = styled.div`
  padding: 0.5em;
  margin: 0.5em;
  color: dimgray;
  background: ${(props) => props.blockColor};
  border: none;
  border-radius: 12px;
  font-size: 1em;
  display: flex;
  grid-template-rows: 1fr;
  justify-content: center;
  align-items: center;
  border: 1px solid dimgray;
`;

const fadeIn = keyframes`
0% {
opacity: 0;
}
100% {
opacity: 1;
}
`;

const Flash = styled.span`
  animation: ${fadeIn} 2s ease-out infinite;
`;

export default function StatsBlock({ type, cur, prev }) {
  // states
  const [direction, setDirection] = useState("snow");

  useEffect(() => {
    if (cur > prev) {
      setDirection("mistyrose");
    } else if (cur < prev) {
      setDirection("honeydew");
    }
  }, [cur, prev]);

  // return
  return (
    <Block blockColor={direction}>
      <span>{`${type}: `}</span>
      <Flash>{cur}</Flash>
    </Block>
  );
}
