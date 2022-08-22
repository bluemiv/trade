import { DataSource } from 'typeorm';
import { entities } from '../entity';

export const PostgresDataSource = new DataSource({
    entities,
    type: 'postgres',
    host: 'localhost',
    port: 35432,
    username: 'postgres',
    password: 'root',
    database: 'cotra',
    synchronize: true,
    logging: true,
    subscribers: [],
    migrations: [],
});
