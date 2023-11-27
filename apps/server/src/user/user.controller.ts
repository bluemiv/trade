import {
  Body,
  Controller,
  Delete,
  Get,
  Param,
  Post,
  Put,
} from '@nestjs/common';
import { UserService } from './user.service';
import CreateUserDto from './dto/create-user.dto';

@Controller('user')
export class UserController {
  constructor(private userService: UserService) {}

  @Post()
  createUser(@Body() createUserDto: CreateUserDto) {
    return this.userService.creatUser(createUserDto);
  }

  @Get('/:username')
  getUser(@Param('username') username: string) {
    return this.userService.getUserByUsername(username);
  }

  @Put()
  modifyUser() {}

  @Delete()
  deleteUser() {}
}
