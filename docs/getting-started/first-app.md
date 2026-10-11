# Your First App

The project skeleton includes a small typed product API at
`/api/products`. It demonstrates JSON input validation and returning an HTTP
response through the Framework and RoadRunner.

Start the application from its project directory:

```sh
tusk doctor
tusk start
```

In another terminal, create a product:

```sh
curl -i \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{"name":"Notebook","sku":"NOTE-1"}' \
  http://127.0.0.1:8080/api/products
```

The example stores products in process memory. It is intended to demonstrate
the request path, not persistence: workers do not share their in-memory state,
and that state is lost when a worker restarts. Use a database-backed repository
for application data that must persist or be shared across workers.

The application bootstrap is `bootstrap/app.php`; routes and controllers live
in the application source. See the [Framework API guides](../api/router.md)
when extending the example.
