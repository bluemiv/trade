import axios from 'axios';

export const initializeAxios = () => {
    axios.defaults.headers['Content-Type'] = 'application/json; charset=utf-8';
};
