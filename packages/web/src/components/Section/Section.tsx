import React, { FC } from 'react';
import { StyledSection } from './StyledSection';
import { SectionProps } from './types';

const Section: FC<SectionProps> = ({ title, width, children }) => {
    return (
        <StyledSection width={width}>
            {title && <h3 className="title">{title}</h3>}
            {children}
        </StyledSection>
    );
};

export default Section;
