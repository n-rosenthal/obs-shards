#   `obs-shards` entities
The most important concepts in note-taking, and Obsidian in particular, that are expressed in the system are the entities:

1. `Note`, associated with a `.md` file;
2. `Block`; a paragraph, list, heading, quotation. The `Block` entity will introduce *granularity* to the system.
3. `Tags`;
4. `Link`, backlinks and references to other notes;
5. `Metadata` (YAML frontmatter);
6. `TimeDuration` and `TimeInterval`, for representing temporal intervals.
7. `Context`;

From this set of entities, others may be derived. When designing *journalling notes*, for example, we don't imediatly need a `JournalNote`, but a `Note` with strong temporal semantics may suffice.

The further concept of `doctype` allows for a more fine-grained classification of notes.

```json
{
  "title": "Fourier Analysis and Image Processing",
  "content": "...markdown...",
  "type": "study",
  "date": null,
  "metadata": {
    "course": "Image Processing",
    "difficulty": "HIGH"
  },
  "tags": ["computer-science", "image-processing"]
}
```

## `Note`

```sql
CREATE TABLE notes (
    id              UUID PRIMARY KEY,   // unique identifier
    title           TEXT,               // title of the note
    content         TEXT,               // content of the note (markdown)
    doctype         TEXT,               // enumerated type of the note

    created_at      TIMESTAMP,          // creation timestamp
    updated_at      TIMESTAMP,          // last update timestamp
    deleted_at      TIMESTAMP,          // deletion timestamp

    date            DATE,               // date of the note
    metadata        JSON,               // metadata of the note
)
```

The `doctype` is an enumerated type, with possible values:

```sh
doctype
    - study
    - journal
    - project
    - task
    - temp
```

See `obs-shards/backend/shards/apps/notes/models.py`



##  `Tags`
The tags are normalized bellow:

```sql
//  Tabela de tags
CREATE TABLE tags (
    id              SERIAL PRIMARY KEY, // unique identifier
    name            TEXT NOT NULL,      // name of the tag
)

//  Tags de uma nota
CREATE TABLE note_tags (
    note_id         UUID NOT NULL,      // id da nota
    tag_id          INTEGER NOT NULL,   // id da tag
    PRIMARY KEY (note_id, tag_id),
)
```

## `Links`
References and backlinks for a `Note`:

```sql
CREATE TABLE note_links (
    source_id       UUID REFERENCES notes (id),    // source note
    target_id       UUID REFERENCES notes (id),    // target note
    PRIMARY KEY     (source_id, target_id)
);
```

## `Metadata`

```sql
CREATE TABLE note_metadata (
    note_id         UUID NOT NULL,      // id da nota
    metadata        JSON,               // metadata of the note
    PRIMARY KEY     (note_id)
);
```