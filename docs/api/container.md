# Container API Reference

The `Container` class is the heart of Tusk's dependency injection system.

## Class: `Tusk\Core\Container\Container`

### Methods

#### `set(string $id, callable $factory): void`

Register a service factory in the container.

**Parameters:**
- `$id` (string) - Service identifier (typically the class name)
- `$factory` (callable) - Factory function that returns the service instance

**Example:**

```php
use Tusk\Core\Container\Container;

$container = new Container();

// Register a simple service
$container->set(LoggerInterface::class, function() {
    return new FileLogger('/var/log/app.log');
});

// Register with dependencies
$container->set(UserService::class, function(Container $c) {
    return new UserService(
        $c->get(UserRepository::class),
        $c->get(LoggerInterface::class)
    );
});
```

---

#### `get(string $id): mixed`

Resolve and retrieve a service from the container.

**Parameters:**
- `$id` (string) - Service identifier

**Returns:** The resolved service instance

**Throws:** `ContainerException` if service cannot be resolved

**Example:**

```php
$logger = $container->get(LoggerInterface::class);
$logger->info('Application started');
```

---

#### `has(string $id): bool`

Check if a service is registered in the container.

**Parameters:**
- `$id` (string) - Service identifier

**Returns:** `true` if registered, `false` otherwise

**Example:**

```php
if ($container->has(CacheInterface::class)) {
    $cache = $container->get(CacheInterface::class);
} else {
    // Use fallback
}
```

---

## Auto-Wiring

The container automatically resolves constructor dependencies using reflection.

**Example:**

```php
class UserController
{
    public function __construct(
        private UserRepository $repo,
        private LoggerInterface $logger,
        private EventDispatcher $events
    ) {}
}

// No manual registration needed!
$controller = $container->get(UserController::class);
// Container automatically injects all dependencies
```

### Auto-Wiring Rules

1. **Type-hinted parameters** are resolved by their type
2. **Interfaces** must be explicitly bound to implementations
3. **Scalar values** cannot be auto-wired (use factory functions)
4. **Circular dependencies** will throw an exception

---

## Singleton Pattern

Register services as singletons to reuse the same instance:

```php
$container->set(DatabaseConnection::class, function() {
    static $instance = null;
    if ($instance === null) {
        $instance = new DatabaseConnection('mysql:host=localhost');
    }
    return $instance;
});

// Or use a helper method (if implemented)
$container->singleton(DatabaseConnection::class, function() {
    return new DatabaseConnection('mysql:host=localhost');
});
```

---

## Service Providers

Organize service registration using service providers:

```php
use Tusk\Core\ServiceProviderInterface;

class DatabaseServiceProvider implements ServiceProviderInterface
{
    public function register(Container $container): void
    {
        $container->set(ConnectionInterface::class, function() {
            return new PdoConnection(
                dsn: getenv('DB_DSN'),
                username: getenv('DB_USER'),
                password: getenv('DB_PASS')
            );
        });
        
        $container->set(UserRepository::class, function(Container $c) {
            return new UserRepository($c->get(ConnectionInterface::class));
        });
    }
}

// Register the provider
$provider = new DatabaseServiceProvider();
$provider->register($container);
```

---

## Advanced Patterns

### Factory Pattern

```php
$container->set(EmailServiceFactory::class, function() {
    return new class {
        public function create(string $type): EmailServiceInterface {
            return match($type) {
                'smtp' => new SmtpEmailService(),
                'sendgrid' => new SendGridEmailService(),
                default => throw new \InvalidArgumentException("Unknown type: $type")
            };
        }
    };
});

$factory = $container->get(EmailServiceFactory::class);
$emailService = $factory->create('smtp');
```

### Contextual Binding

```php
// Different logger for different contexts
$container->set(LoggerInterface::class, function(Container $c) {
    // Default logger
    return new FileLogger('/var/log/app.log');
});

$container->set(AuditService::class, function(Container $c) {
    // Audit service gets a special logger
    return new AuditService(
        new FileLogger('/var/log/audit.log')
    );
});
```

---

## Best Practices

1. **Bind interfaces, not implementations** in your application code
2. **Use service providers** to organize related services
3. **Avoid service locator pattern** - inject dependencies via constructor
4. **Register services early** in your bootstrap process
5. **Use singletons sparingly** - only for stateless or expensive-to-create services

---

## Complete Example

```php
<?php
// bootstrap.php

use Tusk\Core\Container\Container;

$container = new Container();

// Configuration
$container->set('config', fn() => require __DIR__ . '/config.php');

// Database
$container->set(ConnectionInterface::class, function(Container $c) {
    $config = $c->get('config');
    return new PdoConnection(
        $config['db']['dsn'],
        $config['db']['user'],
        $config['db']['pass']
    );
});

// Repositories
$container->set(UserRepository::class, function(Container $c) {
    return new UserRepository($c->get(ConnectionInterface::class));
});

// Services
$container->set(AuthService::class, function(Container $c) {
    return new AuthService(
        $c->get(UserRepository::class),
        $c->get(LoggerInterface::class)
    );
});

// Controllers (auto-wired)
// No need to register - container will auto-wire them!

return $container;
```
