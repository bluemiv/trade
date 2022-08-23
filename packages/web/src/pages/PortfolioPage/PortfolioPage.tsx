import React, { FC } from 'react';
import { Section } from '../../components';

const PortfolioPage: FC = () => {
    return (
        <>
            <Section width={250}>섹션 1</Section>
            <Section title="최근 1달 총 자산 내역">섹션 2</Section>
        </>
    );
};

export default PortfolioPage;
