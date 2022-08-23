import styled from 'styled-components';
import { StyledButtonProps } from './types';
import { getButtonBackgroundColor } from './service';

export const StyledButton = styled.button<StyledButtonProps>`
    background-color: ${({ theme, variant }) => getButtonBackgroundColor(theme, variant)};
    color: ${({ theme }) => theme.style.whiteColor};
    border: none;
    border-radius: 5px;
    padding: 12px 24px;
    margin: 0;
    cursor: pointer;
    transition: 0.1s background-color ease-in-out;

    &:hover {
        background-color: ${({ theme, variant }) => getButtonBackgroundColor(theme, variant, true)};
    }
`;
