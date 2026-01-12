#   Semântica do Diário
##  Arquitetura de Diretórios

```bash
journal/
├── entries/
│   ├── 2026-01-08T09-32.md
│   ├── 2026-01-08T22-10.md
│   └── 2026-01-09T07-55.md
│
├── days/
│   ├── 2026-01-08.md
│   └── 2026-01-09.md
│
├── weeks/
│   └── 2026-W02.md
│
└── months/
    └── 2026-01.md
```
### Princípios para a Arquitetura de Diretórios

1. Cada *entrada no diário* é uma nota distinta;
2. Um *diário* é uma composição de *entradas no diário*, além de outras informações;
3. Uma *semana* é uma composição de *diários*;
4. Um *mês* é uma composição de *semanas*;
5. Um *ano* é uma composição de *meses*;

| Nível     | Função               |
| --------- | -------------------- |
| **entry** | captura do momento   |
| **day**   | composição narrativa |
| **week**  | análise              |
| **month** | padrões              |

### `Entry`, uma entrada no diário
Uma *entrada no diário* é uma representação de

$$\text{algo vivido, pensado, ou sentido em um intervalo curto e razoavelmente específico de tempo}$$

enquanto nota, é

1. atômica e padronizada (por `_templates/entry.md`);
2. temporalmente localizada (por uma data e por um intervalo de tempo); e
3. semânticamente interessante.

Ver `_templates/entry.md` para o modelo de frontmatter de uma `Entry`.

####    Campos opcionais para `Entry`
#####   `mood`

```json
{
    "mood": {
        "type": enum[string],
        "content": string
    }
}
```

#####   `energy`

```json
{
    "energy": {
        "type": enum[string],
        "value": number
    }
}
```

#####   `sleep`

```json
{
    "sleep": {
        "quality": enum[string],
        "duration": number
    }
}
```

#####   `stress`

```json
{
    "stress": number
}
```


#####   `weather`

```json
{
    "weather": {
        "atmosphere": string,
        "temperature": number
    }
}
```

#####   `location`

```json
{
    "location": string
}
```
#####   `people`

```json
{
    "people": [string]
}
```

#####   `topics`

```json
{
    "topics": [string]
}


#####   `tags`

```bash
tags += [journal]
```

