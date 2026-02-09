# Kernel API Reference

The Kernel orchestrates the application lifecycle and manages the runtime environment.

## Class: `Tusk\Runtime\Kernel`

### Basic Usage

```php
use Tusk\Runtime\Kernel;
use Tusk\Core\Container\Container;

$container = new Container();
$kernel = new Kernel($container);

// Start the kernel
$kernel->start();

// Kernel runs until terminated
```

---

## Lifecycle Methods

### `start(): void`

Starts the kernel and initializes the application.

**Example:**

```php
$kernel->start();
// Application is now running
```

### `stop(): void`

Gracefully stops the kernel and cleans up resources.

```php
// Register shutdown handler
pcntl_signal(SIGTERM, function() use ($kernel) {
    $kernel->stop();
});

$kernel->start();
```

### `restart(): void`

Restarts the kernel (stops and starts again).

```php
$kernel->restart();
```

---

## Configuration

### Environment Variables

```php
// Load environment configuration
$kernel->loadEnv(__DIR__ . '/.env');

// Access configuration
$dbHost = getenv('DB_HOST');
$appEnv = getenv('APP_ENV') ?: 'production';
```

### Service Registration

```php
$kernel->registerServices([
    DatabaseServiceProvider::class,
    CacheServiceProvider::class,
    LoggingServiceProvider::class,
]);
```

---

## Event Hooks

### Boot Callbacks

```php
$kernel->onBoot(function(Container $container) {
    // Run after kernel boots
    $logger = $container->get(LoggerInterface::class);
    $logger->info('Application started');
});
```

### Shutdown Callbacks

```php
$kernel->onShutdown(function(Container $container) {
    // Run before kernel stops
    $logger = $container->get(LoggerInterface::class);
    $logger->info('Application stopping');
});
```

---

## Process Management

### Worker Processes

```php
use Tusk\Runtime\Worker\WorkerInterface;

class QueueWorker implements WorkerInterface
{
    public function run(): void
    {
        while (true) {
            $job = $this->queue->pop();
            if ($job) {
                $job->handle();
            }
            usleep(100000); // 100ms
        }
    }
}

// Register worker
$kernel->addWorker(new QueueWorker());
```

### Supervisor

```php
use Tusk\Runtime\Supervisor;

$supervisor = new Supervisor();

// Add workers
$supervisor->addWorker(new QueueWorker(), instances: 4);
$supervisor->addWorker(new SchedulerWorker(), instances: 1);

// Run supervisor
$supervisor->run();
```

---

## Signal Handling

### Graceful Shutdown

```php
use Tusk\Runtime\Kernel;

$kernel = new Kernel($container);

// Handle SIGTERM
pcntl_signal(SIGTERM, function() use ($kernel) {
    echo "Received SIGTERM, shutting down gracefully...\n";
    $kernel->stop();
    exit(0);
});

// Handle SIGINT (Ctrl+C)
pcntl_signal(SIGINT, function() use ($kernel) {
    echo "Received SIGINT, shutting down...\n";
    $kernel->stop();
    exit(0);
});

$kernel->start();
```

### Reload Configuration

```php
pcntl_signal(SIGHUP, function() use ($kernel) {
    echo "Received SIGHUP, reloading configuration...\n";
    $kernel->restart();
});
```

---

## Complete Application Bootstrap

```php
<?php
// bootstrap.php

use Tusk\Core\Container\Container;
use Tusk\Runtime\Kernel;
use Tusk\Web\Server\HttpServer;

// Create container
$container = new Container();

// Load environment
if (file_exists(__DIR__ . '/.env')) {
    $lines = file(__DIR__ . '/.env', FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    foreach ($lines as $line) {
        if (strpos($line, '=') !== false && $line[0] !== '#') {
            putenv($line);
        }
    }
}

// Register services
$container->set(ConnectionInterface::class, function() {
    return new PdoConnection(
        getenv('DB_DSN'),
        getenv('DB_USER'),
        getenv('DB_PASS')
    );
});

$container->set(LoggerInterface::class, function() {
    return new FileLogger(getenv('LOG_PATH') ?: '/var/log/app.log');
});

// Create kernel
$kernel = new Kernel($container);

// Register boot callbacks
$kernel->onBoot(function(Container $c) {
    $logger = $c->get(LoggerInterface::class);
    $logger->info('Application booted', [
        'env' => getenv('APP_ENV'),
        'pid' => getmypid()
    ]);
});

// Register shutdown callbacks
$kernel->onShutdown(function(Container $c) {
    $logger = $c->get(LoggerInterface::class);
    $logger->info('Application shutting down');
});

// Setup signal handlers
pcntl_signal(SIGTERM, fn() => $kernel->stop());
pcntl_signal(SIGINT, fn() => $kernel->stop());

return $kernel;
```

---

## HTTP Server Integration

```php
<?php
// public/index.php

use Tusk\Web\Server\HttpServer;
use Tusk\Web\Router\Router;

// Bootstrap
$kernel = require __DIR__ . '/../bootstrap.php';
$container = $kernel->getContainer();

// Create router
$router = new Router($container);
$router->registerControllers([
    \App\Controller\HomeController::class,
    \App\Controller\UserController::class,
]);

// Create HTTP server
$server = new HttpServer('0.0.0.0', 8080, $router);

// Start kernel with HTTP server
$kernel->onBoot(function() use ($server) {
    echo "HTTP Server listening on http://0.0.0.0:8080\n";
    $server->start();
});

$kernel->start();
```

---

## Testing

### Unit Testing

```php
use PHPUnit\Framework\TestCase;
use Tusk\Core\Container\Container;
use Tusk\Runtime\Kernel;

class KernelTest extends TestCase
{
    public function testKernelBoot(): void
    {
        $container = new Container();
        $kernel = new Kernel($container);
        
        $booted = false;
        $kernel->onBoot(function() use (&$booted) {
            $booted = true;
        });
        
        $kernel->start();
        
        $this->assertTrue($booted);
    }
}
```

---

## Best Practices

1. **Single Kernel Instance** - Create only one kernel per application
2. **Signal Handlers** - Always register SIGTERM/SIGINT handlers for graceful shutdown
3. **Environment Variables** - Use `.env` files for configuration
4. **Service Providers** - Organize service registration in providers
5. **Logging** - Log kernel lifecycle events for debugging
6. **Worker Supervision** - Use Supervisor for managing long-running workers
