import UserResolver from './user-resolver';
import { buildSchemaSync } from 'type-graphql';
import AccountResolver from './account-resolver';

const schema = buildSchemaSync({
    resolvers: [UserResolver, AccountResolver],
});

export default schema;
