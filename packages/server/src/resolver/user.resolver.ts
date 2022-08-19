import { Arg, Mutation, Query, Resolver } from 'type-graphql';
import { User } from '../entity';
import { CreateUserInput } from '../inputs';

@Resolver()
class UserResolver {
    @Query((returns) => User)
    async user(@Arg('id') id: string) {
        return await User.findOneBy({ id });
    }

    @Query((returns) => [User])
    async users() {
        return await User.find();
    }

    @Mutation(() => User)
    async createUser(@Arg('user') user: CreateUserInput) {
        const createdUser = User.create(user);
        await createdUser.save();
        return createdUser;
    }
}

export default UserResolver;
