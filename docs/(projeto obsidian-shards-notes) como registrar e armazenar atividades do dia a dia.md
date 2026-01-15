# como registrar e armazenar atividades do dia a dia
## o modelo de dados `Activity`
É definido dessa forma o modelo de dados `Activity`,  que será utilizado no Django/back-end e pelo banco de dados (PostgreSQL):

```python
# backend/apps/activities/models.py

import uuid
from django.db import models


class Activity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    schema = models.PositiveSmallIntegerField(default=1)
    type = models.CharField(max_length=50)          # activity-entry
    subtype = models.CharField(max_length=50)       # reading_session

    title = models.CharField(max_length=255)

    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    category = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    mood = models.CharField(max_length=50, null=True, blank=True)
    people = models.JSONField(default=list, blank=True)

    tags = models.JSONField(default=list)
    related_notes = models.JSONField(default=list)

    content = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["date"]),
            models.Index(fields=["subtype"]),
        ]

```

## o modelo `Activity` é extensível
O modelo de dados `Activity` aceita *subtipos*. Estes subtipos podem ter campos adicionais, mas **são representados por uma tabela a parte**. O primeiro subtipo a ser implementado foi a *sessão de leitura*, ou `reading_session`,  que tem campos próprios:

```yaml
...
# --- reading_session specific ---
book: "{{VALUE:book}}"
author: "{{VALUE:author}}"

pages_start: {{VALUE:pages start}}
pages_end: {{VALUE:pages end}}
pages_read:
...
```

portanto, é necessário que a nota `reading_session` seja representado por **dois** objetos no banco de dados: uma `Activity` e uma `ReadingSession`.

## subtipos: atividades específicas
```bash
Activity
└── ReadingSession
```

--- 
