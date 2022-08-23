import React, { FC } from 'react';
import { ButtonProps } from './types';
import { StyledButton } from './StyledButton';

const Button: FC<ButtonProps> = ({ variant = 'primary', onClick = () => {}, children = '' }) => {
    return (
        <StyledButton variant={variant} onClick={onClick}>
            {children}
        </StyledButton>
    );
};

export default Button;
