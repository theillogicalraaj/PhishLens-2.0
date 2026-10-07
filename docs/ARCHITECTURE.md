# Architecture

```text
React + TypeScript UI
        |
        | REST + JWT
        v
FastAPI API
  |      |       |
  |      |       +--> PDF reporting
  |      +----------> Behavioral risk model
  v
SQLAlchemy
  |
SQLite (local) / PostgreSQL (Docker)
```

Core domains:

1. Identity and authorization
2. Campaign design
3. Synthetic recipient management
4. Simulation event recording
5. Behavioral analytics
6. Explainable risk scoring
7. Auditability
8. Reporting

The default system is intentionally non-delivery: it prepares and measures simulations inside the application rather than sending messages to external mailboxes.
