## The Runner (`Tusk\Runtime\Runner`)

The `Runner` is the heart of the PHP worker. It handles the continuous IPC loop with the Go Master Process.

```php
use Tusk\Runtime\Runner;

// Runner::run() starts the blocking NDJSON loop
Runner::run($kernel);
```

### IPC Lifecycle
1. **Wait**: The Runner waits for a newline-delimited JSON string on `stdin`.
2. **Boot**: It parses the request and executes the Kernel.
3. **Flush**: It writes the response as NDJSON to `stdout` and signals readiness for the next request.

## Kernel Integration

The `Kernel` manages the application state across multiple requests. Because workers are persistent, the Kernel can cache containers, DB connections, and pre-compiled templates.

## Process Manager

Cross-platform process management (Windows/Linux compatible).

## Worker Pool

Manage multiple worker processes for parallel task execution.

*Full documentation coming soon.*
