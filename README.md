#   `obs-shards`
Projeto de integração bidirecional entre Obsidian e PostgreSQL / Django.

*Event-sourcing pessoal*: sistema de eventos pessoal.

##  Funcionalidades
### Eventos assíncronos com [Celery](https://docs.celeryq.dev/en/latest/index.html)
Usamos Celery para eventos assíncronos (importar e exportar vault, *sync* incremental e processamento de *embeddings* para busca semântica). As *tasks* de entrada e saída definidas devem sempre ser:

1. ter *retry*, caso não for possível realizar a *task* imediatamente;
2. serem idempotentes, isto é, retornar o mesmo resultado para a mesma entrada; e
3. nunca assumir estado global

Veja: [cron](https://docs.celeryq.dev/en/latest/userguide/cron.html), [Celery Beats](https://docs.celeryq.dev/en/latest/userguide/periodic-tasks.html#beats) e [redis](https://redis.io/).

---