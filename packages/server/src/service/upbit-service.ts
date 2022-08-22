import * as process from 'process';
import path from 'path';
import dotenv from 'dotenv';
import crypto from 'crypto';
import jwt from 'jsonwebtoken';
import { v4 as uuidv4 } from 'uuid';
import axios from 'axios';

const { NODE_ENV } = process.env;
dotenv.config({ path: path.resolve(__dirname, `../../.env.${NODE_ENV}`) });

const { UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY, UPBIT_BASE_URL, UPBIT_API_VERSION } = process.env;

/**
 * UPBIT API 전체 url을 반환
 * @param subUrl:string sub url
 */
const _getApiUrl = (subUrl: string) => {
    const baseUrl = UPBIT_BASE_URL.endsWith('/') ? UPBIT_BASE_URL : `${UPBIT_BASE_URL}/`;
    const version = UPBIT_API_VERSION.startsWith('/')
        ? UPBIT_API_VERSION.slice(1, UPBIT_BASE_URL.length)
        : UPBIT_API_VERSION;
    const prefix = `${baseUrl}${version}`;

    const url = subUrl.startsWith('/') ? subUrl : `/${subUrl}`;
    return `${prefix}${url}`;
};

/**
 * 인증 토큰을 반환
 * @param query:{} - 쿼리가 있으면, 쿼리를 map 형태로 입력
 * @returns token:string - 인증 토큰
 */
const _getAuthorizeToken = (query: {} | null = null) => {
    const payload = {
        access_key: UPBIT_ACCESS_KEY,
        nonce: uuidv4(),
    };

    if (query !== null) {
        const params = new URLSearchParams(query);
        const hash = crypto.createHash('sha512');
        payload['query_hash'] = hash.update(params.toString(), 'utf-8').digest('hex');
        payload['query_hash_alg'] = 'SHA512';
    }

    const jwtToken = jwt.sign(payload, UPBIT_SECRET_KEY);
    return `Bearer ${jwtToken}`;
};

export const get_upbit_account = async () => {
    const api = axios.create({ headers: { Authorization: _getAuthorizeToken() } });
    const res = await api.get(_getApiUrl('accounts'));
    return res.data;
};
