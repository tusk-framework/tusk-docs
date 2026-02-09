# Testing Guide

Learn how to test your Tusk applications effectively.

## Unit Testing

### Testing Controllers

```php
use PHPUnit\Framework\TestCase;
use Tusk\Web\Http\Request;
use App\Controller\UserController;

class UserControllerTest extends TestCase
{
    private UserController $controller;
    private UserRepository $mockRepo;
    
    protected function setUp(): void
    {
        $this->mockRepo = $this->createMock(UserRepository::class);
        $this->controller = new UserController($this->mockRepo);
    }
    
    public function testListUsers(): void
    {
        // Arrange
        $this->mockRepo
            ->expects($this->once())
            ->method('findAll')
            ->willReturn([
                ['id' => 1, 'name' => 'Alice'],
                ['id' => 2, 'name' => 'Bob'],
            ]);
        
        $request = new Request('GET', '/users', [], [], '');
        
        // Act
        $response = $this->controller->list($request);
        
        // Assert
        $this->assertEquals(200, $response->getStatusCode());
        $data = json_decode($response->getBody(), true);
        $this->assertCount(2, $data);
    }
    
    public function testShowUser(): void
    {
        // Arrange
        $this->mockRepo
            ->expects($this->once())
            ->method('findById')
            ->with(1)
            ->willReturn(['id' => 1, 'name' => 'Alice']);
        
        $request = new Request('GET', '/users/1', [], [], '');
        
        // Act
        $response = $this->controller->show($request, 1);
        
        // Assert
        $this->assertEquals(200, $response->getStatusCode());
    }
}
```

### Testing Repositories

```php
use PHPUnit\Framework\TestCase;
use Tusk\Data\Driver\ConnectionInterface;
use App\Repository\UserRepository;

class UserRepositoryTest extends TestCase
{
    private UserRepository $repo;
    private ConnectionInterface $mockConnection;
    
    protected function setUp(): void
    {
        $this->mockConnection = $this->createMock(ConnectionInterface::class);
        $this->repo = new UserRepository($this->mockConnection);
    }
    
    public function testFindById(): void
    {
        // Arrange
        $mockStmt = $this->createMock(\PDOStatement::class);
        $mockStmt->expects($this->once())
            ->method('execute')
            ->with([1]);
        $mockStmt->expects($this->once())
            ->method('fetch')
            ->willReturn(['id' => 1, 'name' => 'Alice']);
        
        $this->mockConnection
            ->expects($this->once())
            ->method('prepare')
            ->with('SELECT * FROM users WHERE id = ?')
            ->willReturn($mockStmt);
        
        // Act
        $user = $this->repo->findById(1);
        
        // Assert
        $this->assertEquals(1, $user['id']);
        $this->assertEquals('Alice', $user['name']);
    }
}
```

---

## Integration Testing

### Database Testing

```php
use PHPUnit\Framework\TestCase;
use Tusk\Data\Driver\Pdo\PdoConnection;
use App\Repository\UserRepository;

class UserRepositoryIntegrationTest extends TestCase
{
    private PdoConnection $connection;
    private UserRepository $repo;
    
    protected function setUp(): void
    {
        // Use SQLite in-memory database for testing
        $this->connection = new PdoConnection('sqlite::memory:');
        
        // Create schema
        $this->connection->exec('
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ');
        
        $this->repo = new UserRepository($this->connection);
    }
    
    public function testCreateAndFind(): void
    {
        // Create user
        $id = $this->repo->create([
            'name' => 'Alice',
            'email' => 'alice@example.com'
        ]);
        
        // Find user
        $user = $this->repo->findById($id);
        
        $this->assertEquals('Alice', $user['name']);
        $this->assertEquals('alice@example.com', $user['email']);
    }
    
    public function testUpdate(): void
    {
        $id = $this->repo->create([
            'name' => 'Alice',
            'email' => 'alice@example.com'
        ]);
        
        $this->repo->update($id, [
            'name' => 'Alice Smith',
            'email' => 'alice.smith@example.com'
        ]);
        
        $user = $this->repo->findById($id);
        $this->assertEquals('Alice Smith', $user['name']);
    }
}
```

---

## HTTP Testing

### Testing Routes

```php
use PHPUnit\Framework\TestCase;
use Tusk\Web\Router\Router;
use Tusk\Web\Http\Request;
use Tusk\Core\Container\Container;

class RouterTest extends TestCase
{
    private Router $router;
    
    protected function setUp(): void
    {
        $container = new Container();
        $this->router = new Router($container);
        $this->router->registerControllers([
            \App\Controller\UserController::class,
        ]);
    }
    
    public function testGetUsers(): void
    {
        $request = new Request('GET', '/users', [], [], '');
        $response = $this->router->dispatch($request);
        
        $this->assertEquals(200, $response->getStatusCode());
    }
    
    public function testPostUser(): void
    {
        $request = new Request('POST', '/users', 
            ['Content-Type' => 'application/json'],
            [],
            json_encode(['name' => 'Alice', 'email' => 'alice@example.com'])
        );
        
        $response = $this->router->dispatch($request);
        
        $this->assertEquals(201, $response->getStatusCode());
    }
    
    public function test404NotFound(): void
    {
        $this->expectException(\Tusk\Web\Exception\RouteNotFoundException::class);
        
        $request = new Request('GET', '/nonexistent', [], [], '');
        $this->router->dispatch($request);
    }
}
```

---

## Test Fixtures

### Database Fixtures

```php
class DatabaseFixtures
{
    public static function loadUsers(ConnectionInterface $connection): void
    {
        $users = [
            ['name' => 'Alice', 'email' => 'alice@example.com'],
            ['name' => 'Bob', 'email' => 'bob@example.com'],
            ['name' => 'Charlie', 'email' => 'charlie@example.com'],
        ];
        
        $stmt = $connection->prepare('
            INSERT INTO users (name, email) VALUES (?, ?)
        ');
        
        foreach ($users as $user) {
            $stmt->execute([$user['name'], $user['email']]);
        }
    }
}

// Usage in tests
protected function setUp(): void
{
    parent::setUp();
    DatabaseFixtures::loadUsers($this->connection);
}
```

---

## Test Configuration

### PHPUnit Configuration

```xml
<!-- phpunit.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<phpunit bootstrap="vendor/autoload.php"
         colors="true"
         verbose="true">
    <testsuites>
        <testsuite name="Unit">
            <directory>tests/Unit</directory>
        </testsuite>
        <testsuite name="Integration">
            <directory>tests/Integration</directory>
        </testsuite>
    </testsuites>
    
    <coverage>
        <include>
            <directory suffix=".php">src</directory>
        </include>
    </coverage>
</phpunit>
```

### Running Tests

```bash
# Run all tests
./vendor/bin/phpunit

# Run specific suite
./vendor/bin/phpunit --testsuite Unit

# Run with coverage
./vendor/bin/phpunit --coverage-html coverage/
```

---

## Best Practices

1. **Test Isolation** - Each test should be independent
2. **Mock External Dependencies** - Don't hit real databases/APIs in unit tests
3. **Use In-Memory Databases** - SQLite for integration tests
4. **Descriptive Test Names** - `testCreateUserWithValidData()`
5. **Arrange-Act-Assert** - Structure tests clearly
6. **Test Edge Cases** - Not just happy paths
7. **Keep Tests Fast** - Unit tests should run in milliseconds
