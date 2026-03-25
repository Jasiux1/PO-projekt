# User Service (Flask)

Prosty serwis HTTP 1.1 w architekturze trójwarstwowej:

- warstwa prezentacji: endpointy Flask w `app/routes.py`
- warstwa logiki biznesowej: `app/service.py`
- warstwa persystencji (in-memory): `app/repository.py`

## Endpointy

- `GET /users`
- `GET /users/<id>`
- `POST /users`
- `PATCH /users/<id>`
- `DELETE /users/<id>`

## Model wejściowy (POST)

```json
{
  "firstName": "Jan",
  "lastName": "Kowalski",
  "birthYear": 1999,
  "group": "user"
}
```

`group` musi być jedną z wartości: `user`, `premium`, `admin`.

## Model wyjściowy

```json
{
  "id": 1,
  "firstName": "Jan",
  "lastName": "Kowalski",
  "age": 27,
  "group": "user"
}
```

## Uruchomienie

1. Zainstaluj zależności:
   - `pip install -r requirements.txt`
2. Uruchom aplikację:
   - `python run.py`

## Testy

- Jednostkowe: `tests/unit/test_user_service.py`
- Integracyjne: `tests/integration/test_users_api.py`

Uruchomienie testów:

- `pytest -q`
