import React, { FC } from 'react';
import { StyledFloatingIconButton } from './StyledFloatingIconButton';
import { FloatingButtonProps } from './types';

const FloatingIconButton: FC<FloatingButtonProps> = ({
    icon,
    size = 'md',
    top,
    left,
    bottom,
    right,
    onClick = () => {},
}) => {
    return (
        <StyledFloatingIconButton size={size} top={top} left={left} bottom={bottom} right={right} onClick={onClick}>
            {icon}
        </StyledFloatingIconButton>
    );
};

export default FloatingIconButton;
