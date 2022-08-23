import styled from 'styled-components';
import { StyledSectionProps } from './types';

export const StyledSection = styled.section<StyledSectionProps>`
    padding: ${({ theme }) => theme.style.padding.md};
    background-color: #eeeeee;
    box-sizing: border-box;
    height: auto;
    width: ${({ width }) => (width ? `${width}px` : '100%')};

    & > h3.title {
        font-weight: bold;
        margin-bottom: ${({ theme }) => theme.style.padding.md};
    }
`;
