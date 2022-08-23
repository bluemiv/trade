import React, { FC } from 'react';
import { Link } from 'react-router-dom';
import { StyledHeader } from './StyledHeader';
import { HeaderProps } from './types';
import routes from '../../../routes';

const Header: FC<HeaderProps> = ({ title = '', nav = [], active = '' }) => {
    return (
        <StyledHeader>
            <div className="container">
                <Link className="title" to={routes.HOME.path}>
                    {title}
                </Link>
                <ul className="nav">
                    {nav.map(({ key, label, path }, idx) => (
                        <li key={key ? key : idx}>
                            <Link className={active === key ? 'active' : ''} to={path}>
                                {label}
                            </Link>
                        </li>
                    ))}
                </ul>
            </div>
        </StyledHeader>
    );
};

export default Header;
