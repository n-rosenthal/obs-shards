#   Macros para Obsidian
##  Criar nova nota
Usa-se `CTRL + ALT + N` para criar uma nova nota a partir do *schema* (`v1`) e do *template* (`_templates/note.md`).

##  Criar nova entrada no diário
Usa-se `CTRL + ALT + J` para criar uma nova entrada no diário a partir da *template* (`_templates/entry.md`).

Cria uma nova nota, a partir da template `_templates/entry.md`, que garante o contrato do `schema v1`, em `journal/entries/`, cujo nome será `YYYY-MM-DDTHH-MM.md`.

##  Criar novo diário
O diário é criado automaticamente pelo *plugin* para notas diárias, mas também pode ser feito (se não houver ainda nota para o dia atual), pelo macro `CTRL + ALT + D`. Cria uma nova nota, a partir da template `_templates/daily.md`, que garante o contrato do `schema v1`, em `journal/days/`, cujo nome seja `YYYY-MM-DD.md`.

| Tipo       | `doctype` Django | `metadata["type"]` |
| ---------- | ---------------- | ------------------ |
| Conceito   | `STUDY`          | `study-concept`    |
| Fichamento | `STUDY`          | `reading-note`     |
| Referência | `OTHER`          | `reference`        |
| Citação    | `OTHER`          | `quote`            |
