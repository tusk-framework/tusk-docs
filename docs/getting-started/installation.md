# Installation

## Requirements

- PHP 8.2 or higher
- Composer (for dependency management)
- PDO extension (for database access)

## One-Line Installation (Recommended)

Get Tusk and a portable PHP runtime installed in seconds.

### Linux / macOS
```bash
curl -fsSL https://tusk.sh/install.sh | bash
```

### Windows (PowerShell)
```powershell
iwr -useb https://tusk.sh/install.ps1 | iex
```

These scripts download the `tusk` binary and a pre-configured PHP runtime into `~/.tusk` (or `%USERPROFILE%\.tusk`) and add them to your PATH.

---

## Docker (Containerized)

Tusk provides a ready-to-use Docker image via the GitHub Container Registry (GHCR). This is perfect for CI/CD or production environments.

### Pull the Image
```bash
docker pull ghcr.io/tusk-framework/tusk-engine:main
```

### Run a Local Project
Map your project directory to `/app` inside the container:
```bash
docker run -p 8080:8080 -v $(pwd):/app ghcr.io/tusk-framework/tusk-engine:main
```

---

## Manual Installation

If you prefer to manage your own PHP version:

1. Download the latest `tusk` binary for your platform from [Releases](https://github.com/tusk-framework/tusk-engine/releases).
2. Add the binary to your system PATH.
3. Ensure you have PHP 8.2+ installed.

## Via Composer

For development or contributing to the framework:

```bash
# Clone the monorepo
git clone https://github.com/tusk-framework/tusk-framework.git
cd tusk

# Install dependencies
composer install
```

## Verify Installation

```bash
tusk setup
```

**Output:**
```text
Project Root: /home/user/project
PHP Found: /home/user/.tusk/php/bin/php
Tusk is ready to go!
```

## Next Steps

Continue to [Quick Start](quickstart.md) to create your first project.
