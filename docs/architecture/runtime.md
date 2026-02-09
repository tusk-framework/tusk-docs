# Runtime (Supervisor)

The `tusk-runtime` component provides process management and supervision.

## Kernel

The `Kernel` class orchestrates application lifecycle.

```php
use Tusk\Runtime\Kernel;
use Tusk\Core\Container\Container;

$container = new Container();
$kernel = new Kernel($container);
$kernel->start();
```

## Supervisor

Manages long-running worker processes with automatic restart on failure.

```php
use Tusk\Runtime\Supervisor;

$supervisor = new Supervisor();
$supervisor->addWorker(new QueueWorker());
$supervisor->run();
```

## Process Manager

Cross-platform process management (Windows/Linux compatible).

## Worker Pool

Manage multiple worker processes for parallel task execution.

*Full documentation coming soon.*
