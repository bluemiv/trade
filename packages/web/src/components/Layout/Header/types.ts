export interface HeaderProps {
    title?: string;
    nav?: { key?: number | string; label: string; path: string }[];
    active?: string;
}
