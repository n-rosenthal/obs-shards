#   `obs-shards`
Projeto de integração bidirecional entre Obsidian e PostgreSQL / Django.

*Event-sourcing pessoal*: sistema de eventos pessoal.

##  Funcionalidades
### Eventos assíncronos com [Celery](https://docs.celeryq.dev/en/latest/index.html)
Usamos Celery para eventos assíncronos (importar e exportar vault, *sync* incremental e processamento de *embeddings* para busca semântica).

Veja: [cron](https://docs.celeryq.dev/en/latest/userguide/cron.html), [Celery Beats](https://docs.celeryq.dev/en/latest/userguide/periodic-tasks.html#beats) e [redis](https://redis.io/).

---