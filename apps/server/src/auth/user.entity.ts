import { IsString, MaxLength, MinLength } from 'class-validator';
import { Column, Entity, PrimaryGeneratedColumn } from 'typeorm';
import { UserStatus } from './model/UserStatus';

@Entity()
export class User {
  @IsString()
  @MinLength(4)
  @MaxLength(20)
  @PrimaryGeneratedColumn()
  username: string;

  @IsString()
  @Column()
  password: string;

  @Column({ default: UserStatus.ACTIVE })
  status: UserStatus;

  @Column()
  createdAt: string;

  @Column()
  updatedAt: string;
}
