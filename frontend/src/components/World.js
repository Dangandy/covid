// imports
import React, { useEffect, useState } from "react";
import ReactTooltip from "react-tooltip";
import styled from "styled-components";

// local
import Stats from "./Stats";
import Map from "./Map";

const Wrapper = styled.div`
  grid-gap: 0;
  margin: 0;
  padding: 0;
`;

const MyComponent = () => {
  const [content, setContent] = useState("");
  const [data, setData] = useState([]);
  const [max, setMax] = useState();

  useEffect(() => {
    const fetchData = async () => {
      await fetch(`/api/plot/World`, {
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      })
        .then((res) => res.json())
        .then(({ result }) => {
          setData(result);

          const m = result.reduce(
            (prev, current) =>
              prev.confirmed > current.confirmed ? prev : current,
            1
          );
          setMax(m.confirmed);
        });
    };
    fetchData();
  }, []);
  return (
    <Wrapper>
      <Stats country="World" />
      <Map max={max} data={data} setTooltipContent={setContent} />
      <ReactTooltip>{content}</ReactTooltip>
    </Wrapper>
  );
};

export default MyComponent;
