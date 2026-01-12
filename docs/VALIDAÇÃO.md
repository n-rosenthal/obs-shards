#   Validação para `obs-shards.notes`
##  Validação de Notas
### Filosofia para Validadores
1. Validadores nunca corrigem dados, apenas *apontam* a verdade sobre eles. Portanto, os validadores não podem ter estratégias de *auto-fix* ou inferir automaticamente alguma informação não-trivial.

2. Tipos de validação

Validações triviais (de *parsing*): o YAML é válido? existe *frontmatter* no documento? os campos da *frontmatter* são tipados corretamente?

Uma nota que não passa às verificações triviais é dita *mal-formada*.

Validações de *schema*: existe o campo `schema` nos metadados (*frontmatter*)? o `schema` é de uma versão atualmente suportada? os campos apontados pelo `schema` existem todos e são bem tipados?

[Por enquanto?] Uma nota que não passa às validações de *schema* é dita *mal-formada*.

Validações estruturais: o identificador é um `UUID` válido? as datas, se existirem, são formatadas corretamente (ISO)? os intervalos de tempo, se existirem, assumem o contrato adequado?

Uma nota que não passa às verificações estruturais é dita *inconsistente*.

Validações por tipo de nota (`doctype`) são validações específicas e dependem do tipo da nota. A validação de uma nota que é o registro diário é distinta da validação de uma nota que representa uma tarefa a ser feita.

Abaixo, alguns exemplos de erros de validação, marcados com *warning* ou *error* a depender da severidade da situação-problema:

| Situação              | Severidade |
| --------------------- | ---------- |
| `schema` ausente      | ERROR      |
| `id` inválido         | ERROR      |
| `type` desconhecido   | ERROR      |
| `journal` sem `date`  | ERROR      |
| `updated` < `created` | WARNING    |
| `tags` vazias         | WARNING    |
| `interval` ausente    | WARNING    |

note que, até o momento e no que interessa ao aplicativo `obs-shards.notes`, 
1. `ERROR` indica risco de *corrupção* de algum dos sistemas; e
2. `WARNING` indica risco *semântico*, de perda de sentido em algum dos sistemas

### Validação do Schema v1
[a versão inicial do ?] O validador para o `schema v1` é apenas uma verificação dos campos da *frontmatter* de uma nota. Para cada campo do `schema`, verifica-se o dicionário apontado por `frontmatter`; na presença de inconsistência, coleta-se a mensagem de erro ou de aviso, conforme necessário.

```python
def validate_schema_v1(frontmatter):
    """
        Validador para notas com o SchemaV1
    """
    #   Coleção de erros e avisos
    errors = []
    warnings = []

    #   Verificação dos campos
    #   campo `schema` deve ser 1
    if frontmatter.get("schema") != 1:
        errors.append("Invalid or missing schema version")

    #   `id`, `title` e `doctype` devem estar presentes
    if "id" not in frontmatter:
        errors.append("Missing id")

    if not frontmatter.get("title"):
        errors.append("Missing title")

    if frontmatter.get("doctype") not in Note.NoteType.values:
        errors.append("Invalid doctype")

    #   `created` deve estar presente e `updated` pode estar presente
    if "created" not in frontmatter:
        errors.append("Missing created date")

    if "updated" not in frontmatter:
        warnings.append("Missing updated date")

    return errors, warnings
```

### Validação Estrutural
Os validadores estruturais devem ser, por sua natureza, objetos distintos entre si.

```python
def is_valid_uuid(value: str) -> bool:
    """
        Verificador para UUID
    """
    try:
        uuid.UUID(value)
        return True
    except Exception:
        return False

def is_valid_date(value: str) -> bool:
    """
        Verificador para datas.
        Aceita `YYYY-MM-DD` e `YYYY-MM-DDTHH:MM:SS`

        date.fromisoformat(value)
    """
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except Exception:
        try:
            datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
            return True
        except Exception:
            return False
    
    def is_valid_interval(value: dict) -> bool:
        """
            Verificador para intervalos de tempo
        """
        try:
            start, end = date.fromisoformat(value["start"]), date.fromisoformat(value["end"])
            return start < end
        except Exception:
            return False
```

### Pipeline de Validação
```bash
ler arquivo
  ↓
parse frontmatter
  ↓
rodar validadores
  ↓
┌───────────────┐
│ há ERRORS?    │─── sim ──▶ bloquear sync
└───────┬───────┘
        │ não
        ↓
registrar WARNINGS
        ↓
continuar sync
```

### Arquitetura de Diretórios do Sistema de Validação
```sh
notes/
 ├─ validators/
 │   ├─ base.py        # Result, Severity
 │   ├─ schema_v1.py   # regras do schema
 │   ├─ structural.py  # UUID, dates, interval
 │   └─ by_type.py     # journal, task, study
 └─ services/
     └─ sync.py
```

### Tipo Resultado de Validação
```python
ValidationResult(
    errors=[...],
    warnings=[...]
)
```

