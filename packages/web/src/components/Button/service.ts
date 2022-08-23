import { ThemeType } from 'styled-components';
import { ButtonVariantType } from './types';

export const getButtonBackgroundColor = (
    theme: ThemeType,
    variant: ButtonVariantType,
    isHover: boolean = false
): string => {
    const { primaryColor, secondaryColor } = theme.style;
    if (isHover) {
        return variant === 'primary' ? primaryColor.dark : secondaryColor.dark;
    }
    return variant === 'primary' ? primaryColor.basic : secondaryColor.basic;
};
