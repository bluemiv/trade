import { Column, Entity, PrimaryGeneratedColumn, UpdateDateColumn, CreateDateColumn, BaseEntity } from 'typeorm';
import { Field, ID, ObjectType } from 'type-graphql';

@Entity()
@ObjectType()
class User extends BaseEntity {
    @PrimaryGeneratedColumn('uuid')
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

    @CreateDateColumn()
    @Field(() => Date, { defaultValue: new Date() })
    createdAt: Date;

    @UpdateDateColumn()
    @Field(() => Date, { defaultValue: new Date() })
    updatedAt: Date;
}

export default User;
