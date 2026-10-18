# REA Static-Analysis Notes

Both upstream codebases were passed through REA (Reverse Engineer Anything,
`rea-agents@6.7.0`, `analyze_javascript_application`) before packaging. These
are static, inert-syntax passes — no code was executed.

## uptime-kuma — `server/`

| Field | Value |
| ----- | ----- |
| Input | `/server` JavaScript tree of louislam/uptime-kuma @ main |
| Files | 215 relevant, 215 parsed, 0 parse failures |
| AST nodes | 101,131 |
| Findings | 2,551 |
| Key confirmations | Express + Socket.IO server; SQLite via `better-sqlite3`; no external database dependency |

**Packaging consequence:** Uptime Kuma needs only a data volume — the stack
runs it as a single container with no database service.

## tianji — `src/server/`

| Field | Value |
| ----- | ----- |
| Input | `/src/server` JavaScript tree of msgbyte/tianji @ main |
| Evidence ID | `ev_9f4ab0142d95f4643874d56e35a89fc9fd83ec1e7404b2fcabad6233b` |
| Files | 377 relevant, 371 parsed, 1 parse failure |
| AST nodes | 271,682 |
| Findings | 6,175 |
| Key confirmations | Server-side `DATABASE_URL` (PostgreSQL), `JWT_SECRET` session signing, `ALLOW_REGISTER` / `ALLOW_OPENAPI` toggles |

**Packaging consequence:** the stack carries PostgreSQL 15 and wires
`DATABASE_URL` / `JWT_SECRET` from `.env`, with the Postgres service
health-gated before Tianji starts.

## Limitations

Static analysis parses source as inert text; it does not prove runtime
behavior. Coverage of dynamic imports and obfuscated paths is incomplete by
design (see the limitations block in each Evidence record). The conclusions
above were used only to decide which services and environment wiring the
combined stack needs.
