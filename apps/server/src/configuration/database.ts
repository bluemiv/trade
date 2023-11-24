import { TypeOrmModuleOptions } from '@nestjs/typeorm';

export const typeOrmConfiguration: TypeOrmModuleOptions = {
  type: 'postgres',
  host: 'localhost',
  port: 5432,
  username: 'postgres',
  password: 'root',
  database: 'cotra-db',
  autoLoadEntities: true,
  synchronize: true,
};
