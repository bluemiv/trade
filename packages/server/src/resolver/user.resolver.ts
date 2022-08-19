import { Arg, Query, Resolver } from 'type-graphql';
import { User } from '../entity';

@Resolver()
class UserResolver {
    @Query((returns) => User)
    user(@Arg('id') id: string) {
        return {
            id,
        };
    }

    @Query((returns) => [User])
    users() {
        return [];
    }
}

export default UserResolver;
