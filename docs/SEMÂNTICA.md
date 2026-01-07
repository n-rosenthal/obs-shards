#   Semântica para o projeto `obs-shards.notes`
Devemos buscar respeitar que
1. *Frontmatter* de um documento Markdown é, no máximo, um *estado semântico* para a `Note`; e
2. A representação no banco de dados daquele documento é o *estado operacional* para a `Note`.

Toda nota no Obsidian deve respeitar o *frontmatter canônico mínimo*:

```yaml
---
id: 550e8400-e29b-41d4-a716-446655440000
title: "Título da nota"
type: other
created: 2026-01-07
updated: 2026-01-07
---
```

Note que os campos `created` e `updated` não são mapeados diretamente para o modelo `Note` no backend. Estes são campos de auditoria humana, para migrações e possível recuperação histórica.

Existem também *invariantes sobre notas*, que são informações que não mudam, ou não deveriam mudar, salvo interferência do usuário:

1. `id` deve ser imutável;
2. `doctype` só muda se o usuário assim o fizer;
3. `frontmatter` (ou `metadata`) é a **fonte de verdade *semântica***;
4. banco de dados é a **fonte de verdade *operacional***; e
5. `diff` explícito e campos para `hash` garantem integridade.


##  Modelo `Note`: representação de uma nota do Obsidian
###  $\S 1.$ Semântica de uma `Note`, modelo para nota do Obsidian
Tudo o que possuir sentido em si deverá estar contido no *frontmatter* de uma nota. O *corpo* do documento Markdown é o `content` de uma nota.

Portanto uma nota é definida por seu `frontmatter` ou `metadata`, e por seu `content`.

### $\S 1.1.$ Identidade de uma Nota
Uma `Note` é unicamente definida por um identificador numérico `id` (tipo `UUID`), por seu `title` e pelo `filename`. Esses campos relacionam-se da seguinte forma:

| Frontmatter  | Django       | Tipo   | Observações                              |
| ------------ | ------------ | ------ | ---------------------------------------- |
| `id`         | `id`         | UUID   | **Obrigatório**. Fonte de verdade é o MD |
| `title`      | `title`      | string | Pode divergir do filename                |
| *(filename)* | `vault_path` | string | Inferido pelo sync                       |

> [!NOTE] Regra de Negócio 1: `id` inexistente
> Se `id` não existir no banco de dados, então a nota apontada por `id` é *conflitante*.

### $\S 1.2.$ Tipagem para Notas
Toda `Note` possui um campo `doctype` que deverá ser um dentre uma enumeração de valores (`NoteType`):

```yaml
type: study | journal | project | task | temp | other
```

> [!NOTE] Regra de Negócio 2: tipo inválido
> Se `doctype` não estiver contido na enumeração de tipos possíveis, então a nota é *mal-formada*.

### $\S 1.3.$ Semântica para datas e intervalos de tempo
É possível, mas não obrigatório, usar os campos `date` ou `interval` em notas. Estes campos são reconhecidos pelo `obs-shards.notes` e possuem semântica própria.

| Frontmatter | Django     | Tipo      | Uso             |
| ----------- | ---------- | --------- | --------------- |
| `date`      | `date`     | DateField | Diário, eventos |
| `interval`  | `interval` | JSON      | Blocos de tempo |

para o `Interval`, é necessário respeitar o seguinte contrato:

```yaml
interval:
  start: "08:30"
  end: "10:15"
```

ou também

```yaml
interval:
  start: "2026-01-07T08:30"
  end: "2026-01-07T10:15"
```

então perceba `Interval` é um campo (1) opcional e (2) estruturado.


> [!OBSERVATION] Campo `date` e `mtime` do sistema de arquivos
> O campo `date` dos metadados de uma nota deverá ser inserido pelo usuário durane a criação da nota, e refere-se ao conteúdo semântico desta; não é necessariamente a data de criação ou de última atualização do arquivo.

---
## $\S 2.$ Metadados no Backend
O modelo de dados de uma `Note` é definido a seguir:


Note que `metadata` contém todo o *frontmatter* de uma nota, então nenhuma destas, nem possivelmente outras informações são perdidas, mas sim mantidas no banco de dados.


> [!NOTE] Regra de Negócio 3: manutenção de metadados
> O backend não pode perder campos conhecidos ou desconhecidos dos metadados de uma nota.

## $\S 2.2.$ Outros metadados semânticos ao Obsidian, no backend
Propriedades importantes para notas no Obsidian são preservadas nos metadados do backend, e nesses casos, eles podem ser usados como identificador, ou como outras informações semânticas.

| Frontmatter | Django                |
| ----------- | --------------------- |
| `tags`      | `metadata["tags"]`    |
| `aliases`   | `metadata["aliases"]` |

## $\S 2.3.$ Campos que não devem existir no frontmatter de uma nota

| Django field         |
| -------------------- |
| `content_hash`       |
| `metadata_hash`      |
| `last_synced_hash`   |
| `sync_status`        |
| `last_modified_from` |
| `conflict`           |
| `conflict_data`      |
| `vault_mtime`        |
| `last_sync_at`       |

estes campos devem existir somente no modelo de `Note`, no backend.

## $\S 2.4.$ Campos para *diff* e *hash* explícitos
Os campos

| Django field         |
| -------------------- |
| `content_hash`       |
| `metadata_hash`      |
| `last_synced_hash`   |
| `synsc_status`       |
| `last_modified_from` |

imagine:

```python
content_hash  = sha256(markdown_body)
metadata_hash = sha256(canonical_yaml(frontmatter))
```

### Estados Possíveis

| Estado                           | O que aconteceu         |
| -------------------------------- | ----------------------- |
| `hash_atual == last_synced_hash` | Nada mudou              |
| `hash_atual != last_synced_hash` | Algo mudou              |
| Mudou só no vault                | Editado fora do backend |
| Mudou só no DB                   | Editado via app         |
| Mudou nos dois                   | Conflito real           |

### Fluxo para `diff` explícito

```sh
hash diferente
   ↓
calcular diff (texto + YAML)
   ↓
classificar mudança
   ↓
decidir ação (merge, conflito, aceitar, rejeitar)
```




# $\S 3.$ Parsing para notas no Obsidian
Fluxo de *parsing*:

```sh
.md file
 ├─ YAML frontmatter
 │   ├─ campos mapeados → colunas Django
 │   └─ resto → metadata (JSON)
 └─ markdown body → content
```

# $\S 4.$ `SchemaV1`
O `SchemaV1` representa o esquema de versão 1 do banco de dados de notas.

## Campos Obrigatórios

| Campo     | Tipo              | Observações    |
| --------- | ----------------- | -------------- |
| `schema`  | int               | **Deve ser 1** |
| `id`      | UUID (string)     | Imutável       |
| `title`   | string            | Não vazia      |
| `doctype` | enum              | Ver abaixo     |
| `created` | date (YYYY-MM-DD) | Sem timezone   |

## Campos Opcionais Padrão

| Campo      | Tipo         | Uso                     |
| ---------- | ------------ | ----------------------- |
| `updated`  | date         | Última edição semântica |
| `date`     | date         | Diário / eventos        |
| `interval` | object       | Bloco temporal          |
| `tags`     | list[string] | Obsidian                |
| `aliases`  | list[string] | Obsidian                |

considerando que `enum doctype` é:

```yaml
study
journal
project
task
temp
other
```

e, novamente, considere o contrato para `Interval`:

```yaml
interval:
  start: "HH:MM"
  end: "HH:MM"

interval:
  start: "YYYY-MM-DDTHH:MM"
  end: "YYYY-MM-DDTHH:MM"
```

isto é,
1. `start < end`; e
2. mesmo dia OU ISO completo; e
3. não misturar formatos

Tudo que não está listado acima é:
- permitido;
- preservado;
- armazenado em metadata;
- ignorado pelo `schema v1`

---

### Exemplo de Nota

```markdown
---
schema: 1
id: 550e8400-e29b-41d4-a716-446655440000
title: "Corrida matinal"
type: journal
created: 2026-01-07
updated: 2026-01-07
date: 2026-01-07
interval:
  start: "07:30"
  end: "08:10"
tags: [daily, fitness]
---

# Corrida matinal

Hoje fiz uma corrida leve no parque…


