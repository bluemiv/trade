import React, { FC } from 'react';
import { StyledMain } from './StyledMain';
import { MainProps } from './types';

const Main: FC<MainProps> = ({ children }) => {
    return <StyledMain>{children}</StyledMain>;
};

export default Main;
