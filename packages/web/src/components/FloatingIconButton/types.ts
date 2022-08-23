import { ReactNode } from 'react';

export interface FloatingButtonProps {
    icon: ReactNode;
    size?: 'sm' | 'md' | 'lg';
    children?: ReactNode;
    top?: number;
    bottom?: number;
    left?: number;
    right?: number;
    onClick?: () => void;
}

export interface StyledFloatingButtonProps {
    readonly size: 'sm' | 'md' | 'lg';
    readonly top?: number;
    readonly bottom?: number;
    readonly left?: number;
    readonly right?: number;
}
