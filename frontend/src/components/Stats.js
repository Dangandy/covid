// imports
import React, { useState, useEffect } from "react";
import styled from "styled-components";

// local
import StatsBlock from "./StatsBlock";

// styles
const Section = styled.div`
  display: inline-grid;
  grid-template-columns: 1fr 1fr 1fr;
  min-width: 800px;
`;

export default function Stats({ country }) {
  const [stats, setStats] = useState();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState();
  useEffect(() => {
    const fetchData = async () => {
      await fetch(`/api/stats/${country}`, {
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      })
        .then((res) => res.json())
        .then((d) => {
          setLoading(false);
          setStats(d);
        })
        .catch((err) => setError(err));
    };
    fetchData();
  }, [country]);
  if (loading) return <p>loading..</p>;
  if (error) return <p>error..</p>;
  return (
    <Section>
      <StatsBlock type="Confirmed" cur={stats ? stats.confirmed : 0} />
      <StatsBlock type="Recovered" cur={stats ? stats.recovered : 0} />
      <StatsBlock type="Deaths" cur={stats ? stats.deaths : 0} />
    </Section>
  );
}
