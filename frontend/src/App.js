// imports
import React, { useState, useEffect } from "react";
import styled, { createGlobalStyle, keyframes } from "styled-components";

// local
import logo from "./virus.svg";
import MultiSelect from "./components/MultiSelect";
import World from "./components/World";
import Footer from "./components/Footer";

// styles
const GlobalStyle = createGlobalStyle`
  body {
    background-color: snow;
    color: dimgray;
    fill: dimgray;
    width: 800
  }
`;

const Wrapper = styled.div`
  display: grid;
  grid-gap: 0.5rem;
  align-items: center;
  justify-content: center;
  padding: 0.5em;
  text-align: center;
  position: relative;
`;

const rotate = keyframes`
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
`;

const Header = styled.header`
  animation: ${rotate} 5s linear infinite;
`;

const Tab = styled.button`
  padding: 10px 30px;
  font-size: 1em;
  background: transparent;
  cursor: pointer;
  border: 0;
  outline: 0;
  border-bottom: 2px solid transparent;
  transition: ease border-bottom 250ms;
  ${({ active }) =>
    active &&
    `
    border-bottom: 2px solid black;
    opacity: 1;
  `}
`;

function TabGroup() {
  const [active, setActive] = useState("World");
  const types = ["World", "Country"];
  const [body, setBody] = useState("");
  const toggle = (
    <div>
      {types.map((type) => (
        <Tab
          key={type}
          active={active === type}
          onClick={() => setActive(type)}
        >
          {type}
        </Tab>
      ))}
    </div>
  );
  useEffect(() => {
    if (active === "World") {
      setBody(<World />);
    } else if (active === "Country") {
      setBody(<MultiSelect />);
    }
  }, [active]);
  return (
    <>
      {toggle}
      {body}
    </>
  );
}

function App() {
  return (
    <>
      <GlobalStyle />
      <Wrapper>
        <Header>
          <img src={logo} alt="cv19" width="100px" height="100px" />
        </Header>
        <TabGroup />
        <Footer />
      </Wrapper>
    </>
  );
}

export default App;
