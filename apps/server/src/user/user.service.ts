import { Injectable, NotFoundException } from '@nestjs/common';
import { Repository } from 'typeorm';
import { User } from './entity/user.entity';
import { InjectRepository } from '@nestjs/typeorm';
import CreateUserDto from './dto/create-user.dto';

@Injectable()
export class UserService {
  constructor(
    @InjectRepository(User)
    private userRepository: Repository<User>,
  ) {}

  async creatUser(dto: CreateUserDto) {
    const { username, password } = dto;
    // TODO hashing
    const user = this.userRepository.create({ username, password });
    await this.userRepository.save(user);
    return user;
  }

  async getUserByUsername(username: string) {
    const user = await this.userRepository.findOne({ where: { username } });
    if (!user)
      throw new NotFoundException(`Can't find user. username: ${username}`);
    return user;
  }
}
