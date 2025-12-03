## FastAPI Learning Roadmap — Actionable Tasks
## Copy this file as tasks.nd and check off as you go. Each stage builds on the previous one.

## Legend
## [ ] = todo | [x] = done
## Tags: @api @db @auth @docs @tests @perf @ops @files @ws @background @middleware


## Stage 1 — Solid CRUD and Validation (@api)
- [ ] Posts CRUD: GET /posts, GET /posts/{id}, POST /posts, PUT/PATCH /posts/{id}, DELETE /posts/{id}
  - [ ] Use schemas: Post, PostCreate
  - [ ] Set proper status codes (201 on create, 204 on delete)
  - [ ] Use response_model to shape output
- [ ] Users CRUD: minimal endpoints for list/get/create (hide sensitive fields)
- [ ] Validation with Pydantic v2
  - [ ] Constrain title length (e.g., 3..200)
  - [ ] Ensure content non-empty
  - [ ] Add @field_validator to trim strings
- [ ] Error handling
  - [ ] Raise 404 for missing post/user
  - [ ] Global handler: DB IntegrityError -> 409 Conflict

## Stage 2 — Dependencies, Routers, Settings (@api)
- [ ] Add get_db() dependency for DB sessions
- [ ] Add get_current_user() stub (will fill after JWT)
- [ ] Split routes with APIRouter: users, posts; tag and prefix them
- [ ] Introduce versioning: /api/v1
- [ ] Config via BaseSettings (env): DATABASE_URL, JWT_SECRET, ALGORITHM

## Stage 3 — Authentication & Authorization (@auth)
- [ ] OAuth2 Password flow with JWT
  - [ ] POST /auth/token issues JWT
  - [ ] Protect /users/me using OAuth2PasswordBearer
- [ ] Password hashing with passlib/bcrypt
  - [ ] Hash on signup; verify on login
- [ ] Role-based access control
  - [ ] Add roles (e.g., user, admin)
  - [ ] Authors can edit their posts; admins can delete any post

## Stage 4 — Database Mastery (@db)
- [ ] Move to async DB (SQLAlchemy 2.0 async or SQLModel) and async endpoints
- [ ] Alembic migrations
  - [ ] Add fields: published (bool), slug (unique), tags (M2M)
  - [ ] Create/upgrade migration scripts
- [ ] Query features for posts
  - [ ] Filtering by tag
  - [ ] Sorting (e.g., -created_at)
  - [ ] Pagination: page & size params

## Stage 5 — Response Shaping and Docs (@api @docs)
- [ ] Response models/envelopes
  - [ ] Hide sensitive user fields (email/hashed_password)
  - [ ] Add pagination metadata envelope
- [ ] Documentation polish
  - [ ] Add OpenAPI examples and descriptions per endpoint
  - [ ] Add responses metadata (e.g., 400/401/404/409 schemas)

## Stage 6 — Background Work, Files, Real‑Time (@background @files @ws)
- [ ] Background tasks
  - [ ] On signup: send welcome email (stub)
  - [ ] After post create: enqueue search indexing (stub)
- [ ] File uploads
  - [ ] POST /posts/{id}/image with UploadFile; validate type/size
- [ ] WebSockets
  - [ ] /ws to broadcast new post notifications

## Stage 7 — Middleware, Events, Lifespan (@middleware)
- [ ] Middleware
  - [ ] Correlation ID injection and request timing
  - [ ] CORS setup
- [ ] Startup/Shutdown
  - [ ] Lifespan context to warm DB pool on startup and close cleanly on shutdown

## Stage 8 — Caching, Rate Limiting, Performance (@perf)
- [ ] Redis caching for GET /posts list
  - [ ] Tag-based invalidation on create/update/delete
- [ ] Rate limiting (e.g., slowapi)
  - [ ] Throttle write endpoints by IP/user
- [ ] Streaming and conditional responses
  - [ ] StreamingResponse for large export
  - [ ] ETag support for GET /posts/{id}

## Stage 9 — Testing and Quality (@tests)
- [ ] Test setup with pytest
  - [ ] Test DB fixture (transactional)
  - [ ] Override dependencies: get_db, get_current_user
- [ ] Unit tests for schemas/validators
- [ ] Integration tests for key endpoints (auth, posts CRUD, filters)
- [ ] Add linters & type checking: ruff, mypy

## Stage 10 — Observability and Ops (@ops)
- [ ] Structured logging (JSON) with correlation IDs
- [ ] Metrics and tracing
  - [ ] Expose /metrics for Prometheus
  - [ ] Add OpenTelemetry tracing around DB and external calls
- [ ] Packaging and deployment
  - [ ] Dockerfile + docker-compose (Postgres, Redis)
  - [ ] Gunicorn/Uvicorn workers configuration
  - [ ] CI pipeline (GitHub Actions) to run tests and linters


# Concrete mini‑tasks for your current codebase
- [ ] Auto-update updated_at on Post
  - [ ] Set in PUT/PATCH handler or via SQLAlchemy event
- [ ] Slug for posts
  - [ ] Add slug column + unique constraint
  - [ ] Generate from title; ensure idempotent and collision-safe
- [ ] Tagging system
  - [ ] posts_tags join table; filter /posts by tag
- [ ] Ownership checks
  - [ ] Add author_id to Post; enforce only authors can edit
- [ ] Public vs private user schemas
  - [ ] Create UserPublic to avoid leaking email/hashed_password


# Helpful snippets to implement later (reference)
- [ ] DB dependency pattern
- [ ] OAuth2 password flow skeleton
- [ ] Background task usage
