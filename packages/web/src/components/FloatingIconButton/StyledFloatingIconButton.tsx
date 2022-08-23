import styled, { css } from 'styled-components';
import { StyledFloatingButtonProps } from './types';

export const StyledFloatingIconButton = styled.button<StyledFloatingButtonProps>`
    position: fixed;
    border: none;
    cursor: pointer;
    transition: 0.1s background-color ease-in-out;
    ${({ theme }) => {
        const { radius, primaryColor, whiteColor } = theme.style;
        return css`
            border-radius: ${radius.circle};
            background-color: ${primaryColor.basic};
            color: ${whiteColor};
        `;
    }}
    ${({ size }) => {
        if (size === 'sm') {
            return css`
                width: 42px;
                height: 42px;
            `;
        }
        if (size === 'md') {
            return css`
                width: 55px;
                height: 55px;
            `;
        }
        return css`
            width: 82px;
            height: 82px;
        `;
    }}
    ${({ top }) =>
        top &&
        css`
            top: ${top}px;
        `}
    ${({ bottom }) =>
        bottom &&
        css`
            bottom: ${bottom}px;
        `}
    ${({ left }) =>
        left &&
        css`
            left: ${left}px;
        `}
    ${({ right }) =>
        right &&
        css`
            right: ${right}px;
        `}

    &:hover {
        background-color: ${({ theme }) => theme.style.primaryColor.dark};
    }
`;
