# Container API

The `Container` class provides dependency injection.

## Methods

### `set(string $id, callable $factory): void`

Register a service factory.

```php
$container->set(LoggerInterface::class, fn() => new FileLogger());
```

### `get(string $id): mixed`

Resolve a service from the container.

```php
$logger = $container->get(LoggerInterface::class);
```

### `has(string $id): bool`

Check if a service is registered.

```php
if ($container->has(CacheInterface::class)) {
    // ...
}
```

## Auto-Wiring

The container automatically resolves constructor dependencies.

*Full API reference coming soon.*
