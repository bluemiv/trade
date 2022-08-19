import { BaseEntity, Column, Entity, PrimaryGeneratedColumn } from 'typeorm';
import { Field, ID, ObjectType } from 'type-graphql';

@Entity()
@ObjectType()
class User extends BaseEntity {
    @PrimaryGeneratedColumn('increment')
    @Field(() => ID)
    id: string;

    @Column()
    @Field(() => String)
    email: string;

    @Column()
    @Field(() => String)
    password: string;

    @Column({ nullable: true })
    @Field(() => String, { nullable: true })
    name: string;
}

export default User;
