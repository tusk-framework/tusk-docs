# Micro (Microservices)

The `tusk-micro` component provides utilities for cloud-native microservices.

## Health Checks

Standard Kubernetes-style health endpoints:

```php
use Tusk\Micro\Health\HealthCheckRegistry;
use Tusk\Micro\Controller\HealthController;

$registry = new HealthCheckRegistry();
$registry->register(new DatabaseCheck());

$controller = new HealthController($registry);
```

**Endpoints:**
- `/health/live` - Liveness probe (always UP)
- `/health/ready` - Readiness probe (checks registry)

## Metrics

Prometheus-compatible metrics:

```php
use Tusk\Micro\Metric\Prometheus;

$metrics = new Prometheus();
$metrics->counter('requests_total')->inc();
```

## RPC Interfaces

Define gRPC-style service contracts:

```php
use Tusk\Micro\Rpc\RpcServiceInterface;

interface UserServiceInterface extends RpcServiceInterface
{
    public function getUser(int $id): User;
}
```

*Full documentation coming soon.*
