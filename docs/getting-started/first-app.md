# Your First App

Let's build a simple Todo API with database persistence.

## Setup Database

Update `docker-compose.yml` (already included in generated project):

```yaml
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: todos
```

## Create Repository

`src/Repository/TodoRepository.php`:

```php
<?php
namespace App\Repository;

use Tusk\Data\Repository\AbstractRepository;

class TodoRepository extends AbstractRepository
{
    public function findAll(): array
    {
        $stmt = $this->connection->query('SELECT * FROM todos');
        return $stmt->fetchAll(\PDO::FETCH_ASSOC);
    }
    
    public function create(string $title): int
    {
        $stmt = $this->connection->prepare(
            'INSERT INTO todos (title, completed) VALUES (?, 0)'
        );
        $stmt->execute([$title]);
        return (int) $this->connection->lastInsertId();
    }
}
```

## Create Controller

`src/Controller/TodoController.php`:

```php
<?php
namespace App\Controller;

use App\Repository\TodoRepository;
use Tusk\Web\Attribute\Route;
use Tusk\Web\Http\Request;
use Tusk\Web\Http\Response;

class TodoController
{
    public function __construct(
        private TodoRepository $todos
    ) {}
    
    #[Route('/todos', methods: ['GET'])]
    public function list(Request $request): Response
    {
        $todos = $this->todos->findAll();
        return new Response(200, ['Content-Type' => 'application/json'],
            json_encode($todos));
    }
    
    #[Route('/todos', methods: ['POST'])]
    public function create(Request $request): Response
    {
        $data = json_decode($request->getBody(), true);
        $id = $this->todos->create($data['title']);
        
        return new Response(201, ['Content-Type' => 'application/json'],
            json_encode(['id' => $id]));
    }
}
```

## Run Migrations

Create `migrations/001_create_todos.sql`:

```sql
CREATE TABLE todos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Run it:

```bash
docker-compose exec db mysql -uroot -psecret todos < migrations/001_create_todos.sql
```

## Test It

```bash
# List todos
curl http://localhost:8080/todos

# Create todo
curl -X POST http://localhost:8080/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn Tusk"}'
```

Congratulations! You've built a working API with Tusk. 🎉
