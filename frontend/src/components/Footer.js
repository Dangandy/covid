// 3rd party imports
import React from "react";
import styled from "styled-components";

// Styles
const Footer = styled.p`
  margin: 0;
  grid-gap: 0;
`;
// component
export default () => (
  <Footer>
    Made with{" "}
    <span role="img" aria-label="love">
      ❤️
    </span>
    by <a href="https://github.com/Dangandy">Andy</a> and{" "}
    <a href="https://github.com/anthonyckleung">Anthony</a>
  </Footer>
);
