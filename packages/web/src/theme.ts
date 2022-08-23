const padding = {
    xs: '8px',
    sm: '14px',
    md: '24px',
    lg: '18px',
};

const radius = {
    sm: '8px',
    md: '12px',
    lg: '18px',
    circle: '100%',
};

const fontSize = {
    xm: '0.8rem',
    sm: '0.9rem',
    md: '1rem',
    lg: '1.25rem',
    xl: '1.75rem',
};

const primaryColorForLightTheme = {
    light: '#edf2ff',
    basic: '#4263eb',
    dark: '#364fc7',
};

const primaryColorForDarkTheme = {
    light: '#dbe4ff',
    basic: '#5c7cfa',
    dark: '#4263eb',
};

const secondaryColor = {
    light: '#ffdeeb',
    basic: '#d6336c',
    dark: '#a61e4d',
};

const warningColor = {
    light: '#ffe8cc',
    basic: '#ff922b',
    dark: '#e8590c',
};

export const commonStyle = {
    padding,
    radius,
    fontSize,
    secondaryColor,
    warningColor,
    whiteColor: '#ffffff',
};

export const lightTheme = {
    mode: 'light',
    style: {
        ...commonStyle,
        backgroundColor: '#ffffff',
        fontColor: '#343a40',
        primaryColor: primaryColorForLightTheme,
    },
};

export const darkTheme = {
    mode: 'dark',
    style: {
        ...commonStyle,
        backgroundColor: '#343a40',
        fontColor: '#f8f9fa',
        primaryColor: primaryColorForDarkTheme,
    },
};
