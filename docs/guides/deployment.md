# Deployment

Guide for deploying Tusk applications to production.

## Docker

Use the generated `docker-compose.yml`:

```bash
docker-compose up -d
```

## Native Server

Run the Tusk native server:

```bash
php tusk.phar run public/index.php
```

For production, use a process manager like systemd or supervisord.

## Nginx Proxy (Optional)

```nginx
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
    }
}
```

## Environment Variables

Configure via `.env`:

```
APP_ENV=production
DB_CONNECTION=mysql://user:pass@db:3306/app
```

*Full deployment guide coming soon.*
