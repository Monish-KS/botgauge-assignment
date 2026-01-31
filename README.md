# Key-Value REST API & Python Client

Key-Value REST API (FastAPI + Django ORM + PostgreSQL) with a Python client (retries, exponential backoff, rate-limit handling).

## Prerequisites

- Python 3.10+
- Docker & Docker Compose
- pip

## Quick Start

```bash
docker-compose up -d
cp .env.example .env
pip install -r requirements.txt
python manage.py makemigrations && python manage.py migrate
uvicorn api.main:app --reload
```

- **API:** http://127.0.0.1:8000  
- **Docs:** http://127.0.0.1:8000/docs

## API

| Method | Endpoint       | Description                          |
|--------|----------------|--------------------------------------|
| POST   | `/items/`      | Create `{ "key", "value" }`          |
| GET    | `/items/{key}` | Get item                             |
| PUT    | `/items/{key}` | Update `{ "value" }`                 |
| DELETE | `/items/{key}` | Delete item                          |
| GET    | `/items/`      | List (`?page=1&page_size=10`)        |

Rate limit: 60 req/min per client. Over limit → **429** with `Retry-After`.

## Python Client

```python
from client import KeyValueClient

client = KeyValueClient("http://127.0.0.1:8000")
client.create_item("mykey", "myvalue")
item = client.get_item("mykey")
client.update_item("mykey", "newvalue")
client.list_items(page=1, page_size=10)
client.delete_item("mykey")
```

Optional: `timeout`, `max_retries`, `base_delay`, `max_delay`. Retries on 429, 5xx, timeouts; uses `Retry-After` when present.

## Testing

With API running: `python examples/test_client.py` and `python examples/test_rate_limit.py`.

## Troubleshooting

- **DB auth failed:** Match `.env` to `docker-compose.yml`; reset with `docker-compose down -v` then `docker-compose up -d`.
- **ModuleNotFoundError:** Run from project root: `python examples/test_client.py`.
