import React from 'react';
import { GlobalStyle, Layout } from './components';
import { Route, Routes } from 'react-router-dom';
import { HomePage, PortfolioPage } from './pages';
import routes from './routes';
import { ThemeProvider } from 'styled-components';
import { useRecoilValue } from 'recoil';
import { themeModeAtom } from './recoil/theme';

function App() {
    const themeMode = useRecoilValue(themeModeAtom);

    return (
        <ThemeProvider theme={themeMode}>
            <GlobalStyle />
            <Routes>
                <Route element={<Layout />}>
                    <Route index element={<HomePage />} />
                    <Route path={routes.HOME.path} element={<HomePage />} />
                    <Route path={routes.PORTFOLIO.path} element={<PortfolioPage />} />
                </Route>
            </Routes>
        </ThemeProvider>
    );
}

export default App;
