# skoob

Full-stack work-in-progress library (book loaning) application built for learning and demo purposes.

The backend stack comprises PostgreSQL, SQLALchemy and FastAPI.

The frontend will be a Nuxt (Vue) app. This will use Vue's composition API and an auto-generated API client derived from the backend's OpenAPI spec.

## Development

Spin up a local stack using Docker Compose as follows:
```bash
docker compose watch
```

## TODO
- [ ] CI/CD
- [ ] Local DB seeding and restoration
- [ ] Alembic
- [ ] Automate API client generation
- [ ] Pagination for API endpoints
- [ ] Tests
- [ ] Improve role-based permissions implementation
- [ ] Ensure roles make sense (e.g. should admins have 'borrowed books'?)
- [ ] API response alignment (e.g. status codes, messages)
- [ ] Error handling
- [ ] Refactor loan service (the current approach has data consistency issues)
- [ ] All of the frontend
