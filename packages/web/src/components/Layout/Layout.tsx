import React, { FC, useEffect, useState } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import Header from './Header';
import Main from './Main';
import { FloatingIconButton } from '../index';
import routes from '../../routes';
import Icons from '../Icons';
import { useRecoilState } from 'recoil';
import { themeModeAtom } from '../../recoil/theme';
import { darkTheme, lightTheme } from '../../theme';

const nav = [{ ...routes.HOME }, { ...routes.PORTFOLIO }];

const renderThemeIcon = (isLightTheme: boolean) => (isLightTheme ? <Icons.Moon /> : <Icons.Sun />);

const Layout: FC = () => {
    const location = useLocation();
    const [active, setActive] = useState<string>('');
    const [themeMode, setThemeMode] = useRecoilState(themeModeAtom);
    const isLightTheme = themeMode.mode === 'light';

    useEffect(() => {
        const rootPathname = location.pathname.split('/').slice(0, 2).join('/');
        const activeNav = Object.values(routes).find((route) => route.path === rootPathname);
        if (!activeNav) return;
        setActive(activeNav.key);
    }, [location.pathname]);

    const onClickToggleTheme = () => {
        const nextTheme = isLightTheme ? darkTheme : lightTheme;
        setThemeMode(nextTheme);
    };

    return (
        <>
            <Header title="COTRA" nav={nav} active={active} />
            <Main>
                <Outlet />
            </Main>
            <FloatingIconButton
                icon={renderThemeIcon(isLightTheme)}
                onClick={onClickToggleTheme}
                bottom={20}
                right={20}
            />
        </>
    );
};

export default Layout;
