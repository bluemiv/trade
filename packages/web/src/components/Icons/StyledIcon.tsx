import styled from 'styled-components';
import { StyledIconProps } from './types';

const sizeMap = {
    sm: 12,
    md: 18,
    lg: 32,
};

export const StyledIcon = styled.div<StyledIconProps>`
    display: inline-block;
    width: ${({ size }) => `${sizeMap[size]}px`};
    height: ${({ size }) => `${sizeMap[size]}px`};
`;
