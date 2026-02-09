# Authentication Guide

Implement authentication and authorization in your Tusk applications.

## JWT Authentication

### Setup

```bash
composer require firebase/php-jwt
```

### JWT Service

```php
<?php

namespace App\Service;

use Firebase\JWT\JWT;
use Firebase\JWT\Key;

class JwtService
{
    private string $secret;
    private string $algorithm = 'HS256';
    
    public function __construct(string $secret)
    {
        $this->secret = $secret;
    }
    
    public function encode(array $payload): string
    {
        $payload['iat'] = time();
        $payload['exp'] = time() + (60 * 60 * 24); // 24 hours
        
        return JWT::encode($payload, $this->secret, $this->algorithm);
    }
    
    public function decode(string $token): object
    {
        return JWT::decode($token, new Key($this->secret, $this->algorithm));
    }
    
    public function verify(string $token): bool
    {
        try {
            $this->decode($token);
            return true;
        } catch (\Exception $e) {
            return false;
        }
    }
}
```

### Auth Service

```php
<?php

namespace App\Service;

use App\Repository\UserRepository;

class AuthService
{
    public function __construct(
        private UserRepository $userRepo,
        private JwtService $jwt
    ) {}
    
    public function login(string $email, string $password): ?string
    {
        $user = $this->userRepo->findByEmail($email);
        
        if (!$user || !password_verify($password, $user['password'])) {
            return null;
        }
        
        return $this->jwt->encode([
            'user_id' => $user['id'],
            'email' => $user['email'],
        ]);
    }
    
    public function verify(string $token): ?array
    {
        try {
            $payload = $this->jwt->decode($token);
            return $this->userRepo->findById($payload->user_id);
        } catch (\Exception $e) {
            return null;
        }
    }
    
    public function register(array $data): int
    {
        $data['password'] = password_hash($data['password'], PASSWORD_BCRYPT);
        return $this->userRepo->create($data);
    }
}
```

---

## Auth Controller

```php
<?php

namespace App\Controller;

use Tusk\Web\Attribute\Route;
use Tusk\Web\Http\Request;
use Tusk\Web\Http\Response;
use App\Service\AuthService;

class AuthController
{
    public function __construct(
        private AuthService $auth
    ) {}
    
    #[Route('/auth/register', methods: ['POST'])]
    public function register(Request $request): Response
    {
        $data = json_decode($request->getBody(), true);
        
        // Validate
        if (!isset($data['email'], $data['password'], $data['name'])) {
            return new Response(400, [], json_encode([
                'error' => 'Missing required fields'
            ]));
        }
        
        // Register user
        try {
            $userId = $this->auth->register($data);
            
            return new Response(201, [], json_encode([
                'id' => $userId,
                'message' => 'User registered successfully'
            ]));
        } catch (\Exception $e) {
            return new Response(500, [], json_encode([
                'error' => 'Registration failed'
            ]));
        }
    }
    
    #[Route('/auth/login', methods: ['POST'])]
    public function login(Request $request): Response
    {
        $data = json_decode($request->getBody(), true);
        
        if (!isset($data['email'], $data['password'])) {
            return new Response(400, [], json_encode([
                'error' => 'Email and password required'
            ]));
        }
        
        $token = $this->auth->login($data['email'], $data['password']);
        
        if (!$token) {
            return new Response(401, [], json_encode([
                'error' => 'Invalid credentials'
            ]));
        }
        
        return new Response(200, [], json_encode([
            'token' => $token
        ]));
    }
    
    #[Route('/auth/me', methods: ['GET'])]
    public function me(Request $request): Response
    {
        $authHeader = $request->getHeader('Authorization');
        
        if (!$authHeader || !str_starts_with($authHeader, 'Bearer ')) {
            return new Response(401, [], json_encode([
                'error' => 'Unauthorized'
            ]));
        }
        
        $token = substr($authHeader, 7);
        $user = $this->auth->verify($token);
        
        if (!$user) {
            return new Response(401, [], json_encode([
                'error' => 'Invalid token'
            ]));
        }
        
        // Remove sensitive data
        unset($user['password']);
        
        return new Response(200, [], json_encode($user));
    }
}
```

---

## Middleware (Future Feature)

```php
<?php

namespace App\Middleware;

use Tusk\Web\Http\Request;
use Tusk\Web\Http\Response;
use App\Service\AuthService;

class AuthMiddleware
{
    public function __construct(
        private AuthService $auth
    ) {}
    
    public function handle(Request $request, callable $next): Response
    {
        $authHeader = $request->getHeader('Authorization');
        
        if (!$authHeader || !str_starts_with($authHeader, 'Bearer ')) {
            return new Response(401, [], json_encode([
                'error' => 'Unauthorized'
            ]));
        }
        
        $token = substr($authHeader, 7);
        $user = $this->auth->verify($token);
        
        if (!$user) {
            return new Response(401, [], json_encode([
                'error' => 'Invalid token'
            ]));
        }
        
        // Attach user to request
        $request->setAttribute('user', $user);
        
        return $next($request);
    }
}
```

---

## Protected Routes

### Manual Check

```php
#[Route('/users/{id}', methods: ['PUT'])]
public function update(Request $request, int $id): Response
{
    // Get authenticated user
    $authHeader = $request->getHeader('Authorization');
    if (!$authHeader) {
        return new Response(401, [], json_encode(['error' => 'Unauthorized']));
    }
    
    $token = substr($authHeader, 7);
    $user = $this->auth->verify($token);
    
    if (!$user) {
        return new Response(401, [], json_encode(['error' => 'Invalid token']));
    }
    
    // Check authorization
    if ($user['id'] !== $id && !$user['is_admin']) {
        return new Response(403, [], json_encode(['error' => 'Forbidden']));
    }
    
    // Update user
    $data = json_decode($request->getBody(), true);
    $this->userRepo->update($id, $data);
    
    return new Response(200, [], json_encode(['message' => 'Updated']));
}
```

---

## Role-Based Access Control (RBAC)

### User Roles

```php
class UserRepository extends AbstractRepository
{
    public function findWithRoles(int $userId): array
    {
        $user = $this->findById($userId);
        
        $stmt = $this->connection->prepare('
            SELECT r.name FROM roles r
            INNER JOIN user_roles ur ON ur.role_id = r.id
            WHERE ur.user_id = ?
        ');
        $stmt->execute([$userId]);
        
        $user['roles'] = array_column($stmt->fetchAll(\PDO::FETCH_ASSOC), 'name');
        
        return $user;
    }
    
    public function hasRole(int $userId, string $role): bool
    {
        $stmt = $this->connection->prepare('
            SELECT COUNT(*) FROM user_roles ur
            INNER JOIN roles r ON r.id = ur.role_id
            WHERE ur.user_id = ? AND r.name = ?
        ');
        $stmt->execute([$userId, $role]);
        
        return (int) $stmt->fetchColumn() > 0;
    }
}
```

### Authorization Helper

```php
class AuthorizationService
{
    public function __construct(
        private UserRepository $userRepo
    ) {}
    
    public function can(int $userId, string $permission): bool
    {
        $stmt = $this->connection->prepare('
            SELECT COUNT(*) FROM permissions p
            INNER JOIN role_permissions rp ON rp.permission_id = p.id
            INNER JOIN user_roles ur ON ur.role_id = rp.role_id
            WHERE ur.user_id = ? AND p.name = ?
        ');
        $stmt->execute([$userId, $permission]);
        
        return (int) $stmt->fetchColumn() > 0;
    }
}
```

---

## Session-Based Authentication

### Session Service

```php
class SessionService
{
    public function start(): void
    {
        if (session_status() === PHP_SESSION_NONE) {
            session_start();
        }
    }
    
    public function set(string $key, mixed $value): void
    {
        $_SESSION[$key] = $value;
    }
    
    public function get(string $key, mixed $default = null): mixed
    {
        return $_SESSION[$key] ?? $default;
    }
    
    public function has(string $key): bool
    {
        return isset($_SESSION[$key]);
    }
    
    public function remove(string $key): void
    {
        unset($_SESSION[$key]);
    }
    
    public function destroy(): void
    {
        session_destroy();
    }
}
```

---

## Complete Example

```php
<?php
// Register services in bootstrap.php

$container->set(JwtService::class, function() {
    return new JwtService(getenv('JWT_SECRET'));
});

$container->set(AuthService::class, function(Container $c) {
    return new AuthService(
        $c->get(UserRepository::class),
        $c->get(JwtService::class)
    );
});

// Usage in client
// POST /auth/register
{
    "name": "Alice",
    "email": "alice@example.com",
    "password": "secret123"
}

// POST /auth/login
{
    "email": "alice@example.com",
    "password": "secret123"
}
// Response: { "token": "eyJ0eXAiOiJKV1QiLCJhbGc..." }

// GET /auth/me
// Headers: Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
// Response: { "id": 1, "name": "Alice", "email": "alice@example.com" }
```
