import { ReactNode } from 'react';

export interface SectionProps {
    title?: string;
    width?: number;
    children?: ReactNode;
}

export interface StyledSectionProps {
    readonly width?: number;
}
