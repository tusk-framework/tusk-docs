# Installation

## Requirements

- PHP 8.2 or higher
- Composer (for dependency management)
- PDO extension (for database access)

## Using the PHAR (Recommended)

The easiest way to get started is with the standalone PHAR executable:

```bash
# Download the latest release
wget https://github.com/tusk-framework/tusk/releases/latest/download/tusk.phar

# Make it executable (Linux/Mac)
chmod +x tusk.phar

# Move to your PATH (optional)
sudo mv tusk.phar /usr/local/bin/tusk
```

Now you can use `tusk` (or `php tusk.phar`) globally.

## Via Composer

For development or contributing to the framework:

```bash
# Clone the monorepo
git clone https://github.com/tusk-framework/tusk.git
cd tusk

# Install dependencies
composer install
```

## Verify Installation

```bash
# Check version
php tusk.phar

# Output:
# 🐘 Tusk Framework v0.1.0
# Available commands:
#   init [name]  - Create a new Tusk project
#   run [file]   - Run a Tusk application
```

## Next Steps

Continue to [Quick Start](quickstart.md) to create your first project.
