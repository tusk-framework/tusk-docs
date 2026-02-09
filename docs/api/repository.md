# Repository API Reference

The Repository pattern provides a clean abstraction for data access.

## Class: `Tusk\Data\Repository\AbstractRepository`

### Basic Usage

```php
use Tusk\Data\Repository\AbstractRepository;
use Tusk\Data\Driver\ConnectionInterface;

class UserRepository extends AbstractRepository
{
    public function __construct(ConnectionInterface $connection)
    {
        parent::__construct($connection);
    }
    
    public function findAll(): array
    {
        $stmt = $this->connection->query('SELECT * FROM users');
        return $stmt->fetchAll(\PDO::FETCH_ASSOC);
    }
    
    public function findById(int $id): ?array
    {
        $stmt = $this->connection->prepare('SELECT * FROM users WHERE id = ?');
        $stmt->execute([$id]);
        return $stmt->fetch(\PDO::FETCH_ASSOC) ?: null;
    }
}
```

---

## CRUD Operations

### Create

```php
public function create(array $data): int
{
    $stmt = $this->connection->prepare(
        'INSERT INTO users (name, email, password) VALUES (?, ?, ?)'
    );
    
    $stmt->execute([
        $data['name'],
        $data['email'],
        password_hash($data['password'], PASSWORD_BCRYPT)
    ]);
    
    return (int) $this->connection->lastInsertId();
}
```

### Read

```php
public function findByEmail(string $email): ?array
{
    $stmt = $this->connection->prepare(
        'SELECT * FROM users WHERE email = ?'
    );
    $stmt->execute([$email]);
    return $stmt->fetch(\PDO::FETCH_ASSOC) ?: null;
}

public function findActive(): array
{
    $stmt = $this->connection->query(
        'SELECT * FROM users WHERE active = 1 ORDER BY created_at DESC'
    );
    return $stmt->fetchAll(\PDO::FETCH_ASSOC);
}
```

### Update

```php
public function update(int $id, array $data): bool
{
    $stmt = $this->connection->prepare(
        'UPDATE users SET name = ?, email = ? WHERE id = ?'
    );
    
    return $stmt->execute([
        $data['name'],
        $data['email'],
        $id
    ]);
}
```

### Delete

```php
public function delete(int $id): bool
{
    $stmt = $this->connection->prepare('DELETE FROM users WHERE id = ?');
    return $stmt->execute([$id]);
}

public function softDelete(int $id): bool
{
    $stmt = $this->connection->prepare(
        'UPDATE users SET deleted_at = NOW() WHERE id = ?'
    );
    return $stmt->execute([$id]);
}
```

---

## Transactions

### Basic Transaction

```php
public function transferFunds(int $fromId, int $toId, float $amount): void
{
    $this->connection->beginTransaction();
    
    try {
        // Deduct from sender
        $stmt = $this->connection->prepare(
            'UPDATE accounts SET balance = balance - ? WHERE id = ?'
        );
        $stmt->execute([$amount, $fromId]);
        
        // Add to receiver
        $stmt = $this->connection->prepare(
            'UPDATE accounts SET balance = balance + ? WHERE id = ?'
        );
        $stmt->execute([$amount, $toId]);
        
        $this->connection->commit();
    } catch (\Exception $e) {
        $this->connection->rollback();
        throw $e;
    }
}
```

---

## Query Building

### Dynamic Filters

```php
public function search(array $filters): array
{
    $sql = 'SELECT * FROM users WHERE 1=1';
    $params = [];
    
    if (isset($filters['name'])) {
        $sql .= ' AND name LIKE ?';
        $params[] = '%' . $filters['name'] . '%';
    }
    
    if (isset($filters['email'])) {
        $sql .= ' AND email = ?';
        $params[] = $filters['email'];
    }
    
    if (isset($filters['active'])) {
        $sql .= ' AND active = ?';
        $params[] = (int) $filters['active'];
    }
    
    $stmt = $this->connection->prepare($sql);
    $stmt->execute($params);
    return $stmt->fetchAll(\PDO::FETCH_ASSOC);
}
```

### Pagination

```php
public function paginate(int $page = 1, int $perPage = 20): array
{
    $offset = ($page - 1) * $perPage;
    
    // Get total count
    $countStmt = $this->connection->query('SELECT COUNT(*) FROM users');
    $total = (int) $countStmt->fetchColumn();
    
    // Get page data
    $stmt = $this->connection->prepare(
        'SELECT * FROM users ORDER BY id DESC LIMIT ? OFFSET ?'
    );
    $stmt->execute([$perPage, $offset]);
    $data = $stmt->fetchAll(\PDO::FETCH_ASSOC);
    
    return [
        'data' => $data,
        'total' => $total,
        'page' => $page,
        'perPage' => $perPage,
        'totalPages' => (int) ceil($total / $perPage)
    ];
}
```

---

## Relationships

### One-to-Many

```php
public function findWithPosts(int $userId): array
{
    // Get user
    $user = $this->findById($userId);
    if (!$user) {
        return null;
    }
    
    // Get posts
    $stmt = $this->connection->prepare(
        'SELECT * FROM posts WHERE user_id = ? ORDER BY created_at DESC'
    );
    $stmt->execute([$userId]);
    $user['posts'] = $stmt->fetchAll(\PDO::FETCH_ASSOC);
    
    return $user;
}
```

### Many-to-Many

```php
public function findWithRoles(int $userId): array
{
    $user = $this->findById($userId);
    if (!$user) {
        return null;
    }
    
    $stmt = $this->connection->prepare('
        SELECT r.* FROM roles r
        INNER JOIN user_roles ur ON ur.role_id = r.id
        WHERE ur.user_id = ?
    ');
    $stmt->execute([$userId]);
    $user['roles'] = $stmt->fetchAll(\PDO::FETCH_ASSOC);
    
    return $user;
}
```

---

## Advanced Patterns

### Specification Pattern

```php
interface SpecificationInterface
{
    public function toSql(): string;
    public function getParameters(): array;
}

class ActiveUserSpecification implements SpecificationInterface
{
    public function toSql(): string
    {
        return 'active = ?';
    }
    
    public function getParameters(): array
    {
        return [1];
    }
}

class UserRepository extends AbstractRepository
{
    public function findBySpecification(SpecificationInterface $spec): array
    {
        $sql = 'SELECT * FROM users WHERE ' . $spec->toSql();
        $stmt = $this->connection->prepare($sql);
        $stmt->execute($spec->getParameters());
        return $stmt->fetchAll(\PDO::FETCH_ASSOC);
    }
}
```

### Query Object Pattern

```php
class UserQuery
{
    private array $where = [];
    private array $params = [];
    private ?int $limit = null;
    private ?int $offset = null;
    
    public function whereActive(): self
    {
        $this->where[] = 'active = ?';
        $this->params[] = 1;
        return $this;
    }
    
    public function whereEmail(string $email): self
    {
        $this->where[] = 'email = ?';
        $this->params[] = $email;
        return $this;
    }
    
    public function limit(int $limit): self
    {
        $this->limit = $limit;
        return $this;
    }
    
    public function toSql(): string
    {
        $sql = 'SELECT * FROM users';
        
        if ($this->where) {
            $sql .= ' WHERE ' . implode(' AND ', $this->where);
        }
        
        if ($this->limit) {
            $sql .= ' LIMIT ' . $this->limit;
        }
        
        return $sql;
    }
    
    public function getParameters(): array
    {
        return $this->params;
    }
}

// Usage
$query = (new UserQuery())
    ->whereActive()
    ->whereEmail('user@example.com')
    ->limit(10);

$stmt = $connection->prepare($query->toSql());
$stmt->execute($query->getParameters());
```

---

## Complete Example

```php
<?php

namespace App\Repository;

use Tusk\Data\Repository\AbstractRepository;
use Tusk\Data\Driver\ConnectionInterface;

class UserRepository extends AbstractRepository
{
    public function __construct(ConnectionInterface $connection)
    {
        parent::__construct($connection);
    }
    
    public function findAll(): array
    {
        $stmt = $this->connection->query('SELECT * FROM users ORDER BY id DESC');
        return $stmt->fetchAll(\PDO::FETCH_ASSOC);
    }
    
    public function findById(int $id): ?array
    {
        $stmt = $this->connection->prepare('SELECT * FROM users WHERE id = ?');
        $stmt->execute([$id]);
        return $stmt->fetch(\PDO::FETCH_ASSOC) ?: null;
    }
    
    public function findByEmail(string $email): ?array
    {
        $stmt = $this->connection->prepare('SELECT * FROM users WHERE email = ?');
        $stmt->execute([$email]);
        return $stmt->fetch(\PDO::FETCH_ASSOC) ?: null;
    }
    
    public function create(array $data): int
    {
        $stmt = $this->connection->prepare('
            INSERT INTO users (name, email, password, created_at)
            VALUES (?, ?, ?, NOW())
        ');
        
        $stmt->execute([
            $data['name'],
            $data['email'],
            password_hash($data['password'], PASSWORD_BCRYPT)
        ]);
        
        return (int) $this->connection->lastInsertId();
    }
    
    public function update(int $id, array $data): bool
    {
        $stmt = $this->connection->prepare('
            UPDATE users 
            SET name = ?, email = ?, updated_at = NOW()
            WHERE id = ?
        ');
        
        return $stmt->execute([
            $data['name'],
            $data['email'],
            $id
        ]);
    }
    
    public function delete(int $id): bool
    {
        $stmt = $this->connection->prepare('DELETE FROM users WHERE id = ?');
        return $stmt->execute([$id]);
    }
}
```
