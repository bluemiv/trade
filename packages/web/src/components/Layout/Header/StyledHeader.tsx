import styled from 'styled-components';

export const StyledHeader = styled.header`
    padding: ${({ theme }) => `0 ${theme.style.padding.md}`};

    & > .container {
        height: 80px;
        max-width: 1800px;
        margin: 0 auto;
        display: flex;
        align-items: center;
    }

    & .title {
        flex: 1;
        font-weight: bold;
        font-size: ${({ theme }) => theme.style.fontSize.lg};
        text-decoration: none;
        cursor: pointer;
        color: ${({ theme }) => theme.style.fontColor};

        &:hover {
            color: ${({ theme }) => theme.style.primaryColor.dark};
        }
    }

    & ul.nav {
        list-style: none;
        display: flex;
        column-gap: ${({ theme }) => theme.style.padding.sm};
        li {
            a {
                display: block;
                padding: ${({ theme }) => theme.style.padding.sm};
                text-decoration: none;
                color: ${({ theme }) => theme.style.fontColor};
                border-bottom: 2px solid transparent;

                &:hover {
                    color: ${({ theme }) => theme.style.primaryColor.dark};
                }
            }
            a.active {
                color: ${({ theme }) => theme.style.primaryColor.basic};
                border-bottom: 2px solid ${({ theme }) => theme.style.primaryColor.basic};
            }
        }
    }
`;
