# API Routes

Base URL: `http://127.0.0.1:8000` (when running locally)

**Rate limit:** All `/items/*` routes are limited to **60 requests per minute per client**. Exceeding returns **HTTP 429** with a `Retry-After` header (seconds). Root `/` is not rate-limited.

---

## Routes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Root / health |
| POST | `/items/` | Create item |
| GET | `/items/{key}` | Get item by key |
| PUT | `/items/{key}` | Update item value |
| DELETE | `/items/{key}` | Delete item |
| GET | `/items/` | List items (paginated) |

---

### GET `/`

Root endpoint. Not rate-limited.

**Response:** `200 OK`

```json
{ "message": "Key-Value API" }
```

---

### POST `/items/`

Create a new key-value item.

**Request body (JSON):**

| Field | Type | Required |
|-------|------|----------|
| key   | string | yes |
| value | string | yes |

**Example:** `{ "key": "mykey", "value": "my value" }`

**Response:** `200 OK` — item object (key, value, created_at, updated_at)

**Errors:**

- `409 Conflict` — key already exists
- `422 Unprocessable Entity` — invalid or missing body
- `429 Too Many Requests` — rate limit exceeded (`Retry-After` header)

---

### GET `/items/{key}`

Get a single item by key.

**Path:** `key` — string

**Response:** `200 OK` — item object (key, value, created_at, updated_at)

**Errors:**

- `404 Not Found` — item not found
- `429 Too Many Requests` — rate limit exceeded

---

### PUT `/items/{key}`

Update the value for an existing key.

**Path:** `key` — string

**Request body (JSON):**

| Field | Type | Required |
|-------|------|----------|
| value | string | yes |

**Example:** `{ "value": "updated value" }`

**Response:** `200 OK` — item object (key, value, created_at, updated_at)

**Errors:**

- `404 Not Found` — item not found
- `422 Unprocessable Entity` — invalid or missing body
- `429 Too Many Requests` — rate limit exceeded

---

### DELETE `/items/{key}`

Delete an item by key.

**Path:** `key` — string

**Response:** `200 OK`

```json
{ "message": "deleted" }
```

**Errors:**

- `404 Not Found` — item not found
- `429 Too Many Requests` — rate limit exceeded

---

### GET `/items/`

List items with pagination.

**Query parameters:**

| Param     | Type | Default | Constraints |
|-----------|------|---------|-------------|
| page      | int  | 1       | ≥ 1         |
| page_size | int  | 10      | 1–100       |

**Example:** `GET /items/?page=1&page_size=10`

**Response:** `200 OK`

```json
{
  "items": [
    { "key": "...", "value": "...", "created_at": "...", "updated_at": "..." }
  ],
  "total": 42,
  "page": 1,
  "page_size": 10
}
```

**Errors:**

- `429 Too Many Requests` — rate limit exceeded

---

## Item object

All item responses use this shape:

| Field      | Type   |
|------------|--------|
| key        | string |
| value      | string |
| created_at | string (ISO datetime) |
| updated_at | string (ISO datetime) |

---

## OpenAPI docs

When the API is running: **http://127.0.0.1:8000/docs** (Swagger UI)
