import { Field, InputType } from 'type-graphql';
import { BaseEntity } from 'typeorm';

@InputType()
class CreateUserInput extends BaseEntity {
    @Field(() => String)
    email: string;

    @Field(() => String)
    password: string;

    @Field(() => String, { nullable: true })
    name: string;
}

export default CreateUserInput;
