# Como registrar e armazenar uma *sessão de leitura*?
### definição formal para *sessão de leitura*
> **Sessão de Leitura**
> (Subtipo `reading-session` do tipo `activity-entry`, no sistema de *templates*)
> (Modelo `ReadingSession`, relação um-para-um com o modelo `Activity`, no banco de dados)
> Uma _sessão de leitura_ é uma instância do tipo `activity-entry` com subtipo `reading_session`, representando um intervalo contínuo de tempo dedicado à leitura de um livro, caracterizado por:
> - identificação única (UUID),
> - intervalo temporal,
> - referência bibliográfica,
> - progresso mensurável (páginas),
> - conteúdo textual livre.

---
### implementação
Queremos implementar uma nova funcionalidade para o sistema. Queremos poder registrar a *sessão de leitura* de um usuário, de modo a armazenar dados sobre ela. Estes dados devem seguir os contratos que já temos:

- devem ser armazenados enquanto *frontmatter* YAML de uma nota, além de um campo `content`;
- devem ser registrados no banco de dados;

além disso, é necessário **definir** *sessão de leitura*:
1. uma *sessão de leitura* é uma **atividade** de *subtipo* `reading-session`;
2. uma *sessão de leitura* obedece ao *schema* atual (`schema v1`) e, além dos campos obrigatórios:

```markdown
------
schema: 1
type: activity-entry
subtype: reading-session

id: <% crypto.randomUUID() %>
title: "{{VALUE:title}}"

date: <% tp.date.now("YYYY-MM-DD") %>
start_time: "{{VALUE:start time}}"
end_time: "{{VALUE:end time}}"
duration:

category: "{{VALUE:category}}"
location: "{{VALUE:location}}"
mood: "{{VALUE:mood}}"
people: "{{VALUE:people}}"

# --- reading_session specific ---
book: "{{VALUE:book}}"
author: "{{VALUE:author}}"

pages_start: {{VALUE:pages start}}
pages_end: {{VALUE:pages end}}
pages_read:

related_notes:
  - '"[[<% tp.date.now("YYYY-MM-DD") %>]]"'
  - '"[[<% tp.date.now("YYYY-MM-DD") %> atividades]]"'
  - '"[[{{VALUE:book}}]]"'

tags:
  - activity
  - reading
  - book
  - study

created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
---
# {{VALUE:title}}

## \[`= this.start_time` – `= this.end_time`\]  
### 📖 {{this.book}} ({{this.pages_start}}–{{this.pages_end}})

{{VALUE:entry}}

---
```

3. correspondemos, a esta template do Obsidian, ao modelo de dados `ReadingSession`:

```python
class ReadingSession(models.Model):
    activity = models.OneToOneField(
        Activity,
        on_delete=models.CASCADE,
        related_name="reading_session"
    )

    book = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)

    pages_start = models.PositiveIntegerField()
    pages_end = models.PositiveIntegerField()
    pages_read = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.pages_read:
            self.pages_read = self.pages_end - self.pages_start + 1
        super().save(*args, **kwargs)
```

4. portanto, no banco de dados, uma sessão de leitura é representada por **dois** objetos: uma `Activity` e uma `ReadingSession`.

---
### objetivos do registro de sessões de leitura
#### requisitos
- o *frontmatter* YAML da nota de *sessão de leitura* é a fonte de verdade; e é a partir do *frontmatter* que é feito o registro no banco de dados;
- são criados, no banco de dados, dois objetos para uma sessão de leitura: a atividade em si e a sessão de leitura;
- existe somente uma nota, criada a partir da template `act-reading-session-v1`, que representa a atividade sessão de leitura.

---
#### garantias
- isomorfismo entre o banco de dados e a Vault;
- implementações futuras:
	- somar quantidade de páginas lidas em um dia, em diversas sessões de leitura;
	- agrupar sessões de leitura por livro;
	- correlacionar leitura, humor, horário; e
	- gerar dashboards, relatórios;

---