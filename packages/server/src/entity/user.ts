import { Field, ID, ObjectType } from 'type-graphql';

@ObjectType()
class User {
    @Field(() => ID)
    id: number;

    @Field()
    email: string;

    @Field()
    password: string;

    @Field({ nullable: true })
    name: string;

    @Field({ defaultValue: new Date() })
    createdAt: Date;

    @Field({ defaultValue: new Date() })
    updatedAt: Date;
}

export default User;
