import UserResolver from './user.resolver';
import { buildSchemaSync } from 'type-graphql';

const schema = buildSchemaSync({
    resolvers: [UserResolver],
});

export default schema;
