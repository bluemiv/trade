import { commonStyle } from './theme';

declare module 'styled-components' {
    type CommonStyle = typeof commonStyle;
    export interface ThemeType {
        mode: 'light' | 'dark';
        style:
            | commonStyle
            | {
                  backgroundColor: string;
                  fontColor: string;
              };
    }
}
