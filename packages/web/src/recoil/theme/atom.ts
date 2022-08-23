import { atom } from 'recoil';
import { lightTheme } from '../../theme';

export const themeModeAtom = atom({
    key: 'themeMode',
    default: lightTheme,
});
