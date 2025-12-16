# TypeScript by Framework

TypeScript configurations and best practices for popular frameworks and libraries.

## React

### Configuration
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["DOM", "DOM.Iterable", "ES6"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "module": "ESNext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src"],
  "exclude": ["node_modules"]
}
```

### Component Types
```typescript
import React, { ReactNode, useState, useEffect } from 'react';

// Functional component with props
interface Props {
  title: string;
  count?: number;
  children?: ReactNode;
  onSubmit?: (data: FormData) => void;
}

const Component: React.FC<Props> = ({
  title,
  count = 0,
  children,
  onSubmit
}) => {
  const [localCount, setLocalCount] = useState(count);

  useEffect(() => {
    setLocalCount(count);
  }, [count]);

  return (
    <div>
      <h1>{title}</h1>
      <p>Count: {localCount}</p>
      {children}
    </div>
  );
};

// Generic component
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => ReactNode;
  keyExtractor: (item: T) => string | number;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map(item => (
        <li key={keyExtractor(item)}>
          {renderItem(item)}
        </li>
      ))}
    </ul>
  );
}

// Usage
<List
  items={users}
  renderItem={user => <span>{user.name}</span>}
  keyExtractor={user => user.id}
/>
```

### Hooks with TypeScript
```typescript
// Custom hook with types
function useApi<T>(
  url: string,
  options?: RequestInit
): {
  data: T | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
} {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(url, options);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json() as T;
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [url]);

  return { data, loading, error, refetch: fetchData };
}

// Usage
interface User {
  id: number;
  name: string;
}

const UserProfile: React.FC<{ userId: number }> = ({ userId }) => {
  const { data: user, loading, error } = useApi<User>(`/api/users/${userId}`);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!user) return <div>No user found</div>;

  return <div>{user.name}</div>;
};
```

### Form Handling
```typescript
import { useForm, SubmitHandler } from 'react-hook-form';

interface FormData {
  email: string;
  password: string;
  rememberMe: boolean;
}

const LoginForm: React.FC = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch
  } = useForm<FormData>();

  const password = watch('password');

  const onSubmit: SubmitHandler<FormData> = (data) => {
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        type="email"
        {...register('email', {
          required: 'Email is required',
          pattern: {
            value: /\S+@\S+\.\S+/,
            message: 'Invalid email format'
          }
        })}
      />
      {errors.email && <span>{errors.email.message}</span>}

      <input
        type="password"
        {...register('password', {
          required: 'Password is required',
          minLength: {
            value: 8,
            message: 'Password must be at least 8 characters'
          }
        })}
      />
      {errors.password && <span>{errors.password.message}</span>}

      <label>
        <input type="checkbox" {...register('rememberMe')} />
        Remember me
      </label>

      <button type="submit">Login</button>
    </form>
  );
};
```

## Next.js

### Project Configuration
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/lib/*": ["./src/lib/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

### API Routes
```typescript
// pages/api/users/[id].ts
import { NextApiRequest, NextApiResponse } from 'next';
import { getUserById } from '@/lib/database';

interface User {
  id: number;
  name: string;
  email: string;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<{ user: User } | { error: string }>
) {
  const { id } = req.query;

  if (!id || typeof id !== 'string') {
    return res.status(400).json({ error: 'Invalid user ID' });
  }

  if (req.method === 'GET') {
    try {
      const user = await getUserById(parseInt(id));
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }
      res.status(200).json({ user });
    } catch (error) {
      res.status(500).json({ error: 'Failed to fetch user' });
    }
  } else {
    res.setHeader('Allow', ['GET']);
    res.status(405).json({ error: `Method ${req.method} Not Allowed` });
  }
}
```

### Server-Side Rendering
```typescript
// pages/posts/[id].tsx
import { GetServerSideProps } from 'next';
import { Post, getPostById } from '@/lib/posts';

interface PostPageProps {
  post: Post;
}

const PostPage: React.FC<PostPageProps> = ({ post }) => {
  return (
    <div>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </div>
  );
};

export const getServerSideProps: GetServerSideProps<PostPageProps> = async (context) => {
  const { id } = context.params;

  if (!id || typeof id !== 'string') {
    return {
      notFound: true
    };
  }

  const post = await getPostById(id);

  if (!post) {
    return {
      notFound: true
    };
  }

  return {
    props: {
      post
    }
  };
};

export default PostPage;
```

### Static Site Generation
```typescript
// pages/blog/[slug].tsx
import { GetStaticPaths, GetStaticProps } from 'next';
import { BlogPost, getAllPostSlugs, getPostBySlug } from '@/lib/blog';

interface BlogPostPageProps {
  post: BlogPost;
}

const BlogPostPage: React.FC<BlogPostPageProps> = ({ post }) => {
  return (
    <article>
      <h1>{post.title}</h1>
      <time>{post.date}</time>
      <div dangerouslySetInnerHTML={{ __html: post.content }} />
    </article>
  );
};

export const getStaticPaths: GetStaticPaths = async () => {
  const paths = await getAllPostSlugs();

  return {
    paths,
    fallback: false
  };
};

export const getStaticProps: GetStaticProps<BlogPostPageProps> = async ({ params }) => {
  const post = await getPostBySlug(params?.slug as string);

  if (!post) {
    return {
      notFound: true
    };
  }

  return {
    props: {
      post
    }
  };
};

export default BlogPostPage;
```

## Express.js

### Basic Setup
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Typed Express Application
```typescript
// src/app.ts
import express, { Request, Response, NextFunction } from 'express';
import helmet from 'helmet';
import cors from 'cors';
import { userRouter } from './routes/users';
import { authRouter } from './routes/auth';

interface AuthenticatedRequest extends Request {
  user?: {
    id: number;
    email: string;
  };
}

const app = express();

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Custom error handler middleware
interface AppError extends Error {
  statusCode?: number;
  status?: string;
}

const errorHandler = (
  err: AppError,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  err.statusCode = err.statusCode || 500;
  err.status = err.status || 'error';

  res.status(err.statusCode).json({
    status: err.status,
    message: err.message
  });
};

// Async error wrapper
const asyncHandler = (fn: Function) => {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};

// Routes
app.use('/api/users', userRouter);
app.use('/api/auth', authRouter);

// 404 handler
app.all('*', (req, res, next) => {
  next(new AppError(`Can't find ${req.originalUrl} on this server!`, 404));
});

app.use(errorHandler);

export default app;
```

### Typed Controllers
```typescript
// src/controllers/userController.ts
import { Request, Response, NextFunction } from 'express';
import { UserService } from '../services/userService';
import { CreateUserRequest, UpdateUserRequest } from '../types/user';

interface AuthenticatedRequest extends Request {
  user?: {
    id: number;
    email: string;
  };
}

export class UserController {
  constructor(private userService: UserService) {}

  getAllUsers = async (
    req: Request,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      const users = await this.userService.getAll();
      res.status(200).json({
        status: 'success',
        results: users.length,
        data: { users }
      });
    } catch (error) {
      next(error);
    }
  };

  createUser = async (
    req: Request<{}, {}, CreateUserRequest>,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      const newUser = await this.userService.create(req.body);
      res.status(201).json({
        status: 'success',
        data: { user: newUser }
      });
    } catch (error) {
      next(error);
    }
  };

  getUser = async (
    req: Request<{ id: string }>,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      const user = await this.userService.getById(parseInt(req.params.id));
      if (!user) {
        return next(new AppError('User not found', 404));
      }
      res.status(200).json({
        status: 'success',
        data: { user }
      });
    } catch (error) {
      next(error);
    }
  };

  updateUser = async (
    req: Request<{ id: string }, {}, UpdateUserRequest>,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      const user = await this.userService.update(
        parseInt(req.params.id),
        req.body
      );
      res.status(200).json({
        status: 'success',
        data: { user }
      });
    } catch (error) {
      next(error);
    }
  };

  deleteUser = async (
    req: AuthenticatedRequest,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      await this.userService.delete(parseInt(req.params.id));
      res.status(204).json({
        status: 'success',
        data: null
      });
    } catch (error) {
      next(error);
    }
  };
}
```

### Typed Services
```typescript
// src/services/userService.ts
import { User, CreateUserRequest, UpdateUserRequest } from '../types/user';
import { Database } from '../database';

export class UserService {
  constructor(private db: Database) {}

  async getAll(): Promise<User[]> {
    const query = 'SELECT * FROM users';
    const result = await this.db.query(query);
    return result.rows;
  }

  async getById(id: number): Promise<User | null> {
    const query = 'SELECT * FROM users WHERE id = $1';
    const result = await this.db.query(query, [id]);
    return result.rows[0] || null;
  }

  async create(userData: CreateUserRequest): Promise<User> {
    const { name, email, password } = userData;
    const query = `
      INSERT INTO users (name, email, password)
      VALUES ($1, $2, $3)
      RETURNING *
    `;
    const result = await this.db.query(query, [name, email, password]);
    return result.rows[0];
  }

  async update(id: number, updateData: UpdateUserRequest): Promise<User> {
    const { name, email } = updateData;
    const query = `
      UPDATE users
      SET name = $1, email = $2, updated_at = NOW()
      WHERE id = $3
      RETURNING *
    `;
    const result = await this.db.query(query, [name, email, id]);
    return result.rows[0];
  }

  async delete(id: number): Promise<void> {
    const query = 'DELETE FROM users WHERE id = $1';
    await this.db.query(query, [id]);
  }
}
```

## NestJS

### Typed Module
```typescript
// src/users/users.module.ts
import { Module } from '@nestjs/common';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';
import { TypeOrmModule } from '@nestjs/typeorm';
import { User } from './entities/user.entity';
import { ConfigModule } from '@nestjs/config';

@Module({
  imports: [
    TypeOrmModule.forFeature([User]),
    ConfigModule
  ],
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService]
})
export class UsersModule {}
```

### Typed Controller
```typescript
// src/users/users.controller.ts
import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
  UseGuards,
  Request
} from '@nestjs/common';
import { UsersService } from './users.service';
import { CreateUserDto } from './dto/create-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

interface AuthenticatedRequest extends Request {
  user: {
    userId: number;
    email: string;
  };
}

@Controller('users')
@UseGuards(JwtAuthGuard)
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Post()
  create(@Body() createUserDto: CreateUserDto) {
    return this.usersService.create(createUserDto);
  }

  @Get()
  findAll() {
    return this.usersService.findAll();
  }

  @Get('profile')
  getProfile(@Request() req: AuthenticatedRequest) {
    return this.usersService.findOne(req.user.userId);
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.usersService.findOne(+id);
  }

  @Patch(':id')
  update(@Param('id') id: string, @Body() updateUserDto: UpdateUserDto) {
    return this.usersService.update(+id, updateUserDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.usersService.remove(+id);
  }
}
```

### Typed DTOs
```typescript
// src/users/dto/create-user.dto.ts
import { IsEmail, IsString, MinLength } from 'class-validator';

export class CreateUserDto {
  @IsString()
  @MinLength(2)
  name: string;

  @IsEmail()
  email: string;

  @IsString()
  @MinLength(6)
  password: string;
}

// src/users/dto/update-user.dto.ts
import { PartialType } from '@nestjs/mapped-types';
import { CreateUserDto } from './create-user.dto';

export class UpdateUserDto extends PartialType(CreateUserDto) {}
```

### Typed Service
```typescript
// src/users/users.service.ts
import { Injectable } from '@nestjs/common';
import { CreateUserDto } from './dto/create-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';
import { User } from './entities/user.entity';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';

@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private usersRepository: Repository<User>
  ) {}

  create(createUserDto: CreateUserDto): Promise<User> {
    const user = this.usersRepository.create(createUserDto);
    return this.usersRepository.save(user);
  }

  findAll(): Promise<User[]> {
    return this.usersRepository.find();
  }

  findOne(id: number): Promise<User> {
    return this.usersRepository.findOneBy({ id });
  }

  async update(id: number, updateUserDto: UpdateUserDto): Promise<User> {
    const user = await this.usersRepository.preload({
      id,
      ...updateUserDto
    });
    return this.usersRepository.save(user);
  }

  async remove(id: number): Promise<void> {
    await this.usersRepository.delete(id);
  }

  async findByEmail(email: string): Promise<User | null> {
    return this.usersRepository.findOneBy({ email });
  }
}
```

## Vue.js

### Configuration with Vite
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "preserve",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src/**/*.ts", "src/**/*.tsx", "src/**/*.vue"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### Vue Component with TypeScript
```vue
<!-- src/components/UserProfile.vue -->
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useUserStore } from '@/stores/user';
import type { User } from '@/types/user';

interface Props {
  userId: number;
  showEmail?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  showEmail: true
});

const userStore = useUserStore();
const user = ref<User | null>(null);
const loading = ref(true);

const fullName = computed(() => {
  if (!user.value) return '';
  return `${user.value.firstName} ${user.value.lastName}`;
});

onMounted(async () => {
  try {
    user.value = await userStore.fetchUser(props.userId);
  } finally {
    loading.value = false;
  }
});

const emit = defineEmits<{
  update: [user: User];
  delete: [id: number];
}>();

const handleUpdate = async () => {
  if (user.value) {
    const updatedUser = await userStore.updateUser(user.value);
    emit('update', updatedUser);
  }
};
</script>

<template>
  <div v-if="loading">Loading...</div>
  <div v-else-if="user">
    <h2>{{ fullName }}</h2>
    <p v-if="showEmail">{{ user.email }}</p>
    <button @click="handleUpdate">Update</button>
    <button @click="emit('delete', user.id)">Delete</button>
  </div>
  <div v-else>User not found</div>
</template>
```

### Pinia Store with TypeScript
```typescript
// src/stores/user.ts
import { defineStore } from 'pinia';
import type { User } from '@/types/user';
import { userService } from '@/services/userService';

interface UserState {
  users: User[];
  currentUser: User | null;
  loading: boolean;
  error: string | null;
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    users: [],
    currentUser: null,
    loading: false,
    error: null
  }),

  getters: {
    getUserById: (state) => {
      return (id: number): User | undefined =>
        state.users.find(user => user.id === id);
    },

    activeUsers: (state) => {
      return state.users.filter(user => user.isActive);
    }
  },

  actions: {
    async fetchUsers() {
      this.loading = true;
      this.error = null;

      try {
        this.users = await userService.getAll();
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to fetch users';
      } finally {
        this.loading = false;
      }
    },

    async fetchUser(id: number): Promise<User> {
      this.loading = true;
      this.error = null;

      try {
        const user = await userService.getById(id);
        this.currentUser = user;
        return user;
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to fetch user';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async createUser(userData: Omit<User, 'id'>) {
      try {
        const newUser = await userService.create(userData);
        this.users.push(newUser);
        return newUser;
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to create user';
        throw error;
      }
    },

    async updateUser(id: number, updates: Partial<User>) {
      try {
        const updatedUser = await userService.update(id, updates);
        const index = this.users.findIndex(user => user.id === id);
        if (index !== -1) {
          this.users[index] = updatedUser;
        }
        if (this.currentUser?.id === id) {
          this.currentUser = updatedUser;
        }
        return updatedUser;
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to update user';
        throw error;
      }
    },

    async deleteUser(id: number) {
      try {
        await userService.delete(id);
        this.users = this.users.filter(user => user.id !== id);
        if (this.currentUser?.id === id) {
          this.currentUser = null;
        }
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to delete user';
        throw error;
      }
    }
  }
});
```

## Framework-Specific Best Practices

### React
- Use functional components with hooks
- Define component props with interfaces
- Use generic components for reusable logic
- Leverage React Hook Form for type-safe forms

### Next.js
- Use getServerSideProps/getStaticProps with proper typing
- Define API route types with Request/Response
- Leverage path params typing
- Use incremental typing with `next/dynamic`

### Express.js
- Create typed middleware functions
- Use error classes with status codes
- Define request/response types for routes
- Leverage dependency injection

### NestJS
- Use class-validator for DTOs
- Create typed entities with TypeORM
- Leverage dependency injection typing
- Use decorators for metadata

### Vue.js
- Use `<script setup lang="ts">` for composition API
- Define props and emits with interfaces
- Use Pinia with typed stores
- Leverage Vue 3's reactivity system with types

These patterns help you build type-safe applications across different frameworks while maintaining consistency and catching errors at compile-time.