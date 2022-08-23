import { ReactNode } from 'react';

export type ButtonVariantType = null | 'primary' | 'secondary';

export interface ButtonProps {
    variant: ButtonVariantType;
    children?: ReactNode;
    onClick?: () => void;
}

export interface StyledButtonProps {
    readonly variant: ButtonVariantType;
    readonly onClick: () => void;
}
