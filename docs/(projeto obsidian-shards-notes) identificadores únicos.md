# identificadores únicos
Todos os objetos, tanto nas notas da *Vault* do Obsidian quanto os registros no banco de dados, possuem um identificador alfanumérico único. Este identificador é computado por uma função de criptografia.

No Obsidian, este cálculo é feito chamando a função `randomUUID()` do módulo `crypto` da biblioteca padrão do JavaScript. Através do *plugin* Templater, é substituída a chamada da função pelo resultado:

```yaml
id: <% crypto.randomUUID() %>
```

Em Python, obtemos o mesmo resultado fazendo uso da biblioteca `uuid`.

```python
import uuid
id = uuid.uuid4()
```