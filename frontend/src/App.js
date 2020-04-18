// imports
import React from "react";
import styled, { createGlobalStyle, keyframes } from "styled-components";

// local
import Stats from "./components/Stats";
import logo from "./virus.svg";
import MultiSelect from "./components/MultiSelect";

// styles
const GlobalStyle = createGlobalStyle`
  body {
    background-color: snow;
  }
`;

const Wrapper = styled.div`
  display: grid;
  grid-gap: 0.5rem;
  align-items: center;
  justify-content: center;
  padding: 0.5em;
  color: dimgray;
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

function App() {
  return (
    <>
      <GlobalStyle />
      <Wrapper>
        <Header>
          <img src={logo} alt="cv19" width="100px" height="100px" />
        </Header>
        <h3>World Stats</h3>
        <Stats country="World" />
        <MultiSelect />
      </Wrapper>
    </>
  );
}

export default App;
