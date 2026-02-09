# Core (Dependency Injection)

The `tusk-core` component provides the foundation for dependency management.

## Container

The `Container` class is a simple, attribute-based DI container.

### Basic Usage

```php
use Tusk\Core\Container\Container;

$container = new Container();

// Register a service
$container->set(DatabaseConnection::class, function() {
    return new DatabaseConnection('mysql:host=localhost');
});

// Resolve a service
$db = $container->get(DatabaseConnection::class);
```

### Auto-Wiring

The container can automatically resolve constructor dependencies:

```php
class UserService
{
    public function __construct(
        private UserRepository $repo,
        private Logger $logger
    ) {}
}

// Container will automatically inject dependencies
$service = $container->get(UserService::class);
```

## Contracts

Core interfaces that define framework behavior:

- `ContainerInterface` - DI container contract
- `KernelInterface` - Application kernel contract
- `ServiceProviderInterface` - Service registration

## Attributes

PHP 8 attributes for declarative configuration:

- `#[Service]` - Mark a class as a service
- `#[Singleton]` - Register as singleton
- `#[Inject]` - Explicit dependency injection

## Example: Service Provider

```php
use Tusk\Core\Attribute\Service;

#[Service]
class AppServiceProvider
{
    public function register(Container $container): void
    {
        $container->set(LoggerInterface::class, function() {
            return new FileLogger('/var/log/app.log');
        });
    }
}
```
