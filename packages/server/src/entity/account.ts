import {
    BaseEntity,
    Column,
    CreateDateColumn,
    Double,
    Entity,
    PrimaryGeneratedColumn,
    UpdateDateColumn,
} from 'typeorm';
import { Field, Float, ID, ObjectType } from 'type-graphql';

@Entity()
@ObjectType()
class Account extends BaseEntity {
    @PrimaryGeneratedColumn('uuid')
    @Field(() => ID)
    id: string;

    @Column('varchar', { length: 100 })
    @Field(() => String)
    currency: string;

    @Column()
    @Field(() => String)
    balance: string;

    @Column()
    @Field(() => String)
    locked: string;

    @Column()
    @Field(() => String)
    avgBuyPrice: string;

    @Column()
    @Field(() => Boolean)
    avgBuyPriceModified: boolean;

    @Column()
    @Field(() => String)
    unitCurrency: string;

    @CreateDateColumn()
    @Field(() => Date, { defaultValue: new Date() })
    createdAt: Date;

    @UpdateDateColumn()
    @Field(() => Date, { defaultValue: new Date() })
    updatedAt: Date;
}

export default Account;
