# Tusk Documentation

Official documentation for the Tusk Framework.

## Building the Docs

### Prerequisites

```bash
pip install mkdocs mkdocs-material
```

### Local Development

```bash
cd tusk-docs
mkdocs serve
```

Visit `http://localhost:8000`

### Deploy to GitHub Pages

```bash
mkdocs gh-deploy
```

## Structure

- `docs/` - Markdown documentation files
- `mkdocs.yml` - MkDocs configuration
- `site/` - Generated static site (gitignored)

## Contributing

1. Edit markdown files in `docs/`
2. Preview with `mkdocs serve`
3. Submit PR

## License

MIT
