# Data (Repository)

The `tusk-data` component provides database abstraction and repository pattern.

## PdoConnection

Resilient PDO wrapper with automatic reconnection:

```php
use Tusk\Data\Driver\Pdo\PdoConnection;

$db = new PdoConnection('mysql:host=localhost;dbname=app', 'user', 'pass');
```

## AbstractRepository

Base class for clean data access:

```php
use Tusk\Data\Repository\AbstractRepository;

class UserRepository extends AbstractRepository
{
    public function findByEmail(string $email): ?array
    {
        $stmt = $this->connection->prepare('SELECT * FROM users WHERE email = ?');
        $stmt->execute([$email]);
        return $stmt->fetch(\PDO::FETCH_ASSOC) ?: null;
    }
}
```

## Transactions

```php
$db->beginTransaction();
try {
    // ... operations
    $db->commit();
} catch (\Exception $e) {
    $db->rollback();
}
```

*Full documentation coming soon.*
