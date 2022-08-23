import { createGlobalStyle, ThemeType } from 'styled-components';
import normalize from 'styled-normalize';

const GlobalStyle = createGlobalStyle<{ theme: ThemeType }>`
  ${normalize}
  body {
    background-color: ${({ theme }) => theme.style.backgroundColor};
    color: ${({ theme }) => theme.style.fontColor};
  }
`;

export default GlobalStyle;
