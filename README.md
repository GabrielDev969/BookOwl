# BookOwl

![Badge em Produção](http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge)
![Badge em Versão](http://img.shields.io/static/v1?label=Versão&message=1.0.0&color=GREEN&style=for-the-badge)

Bem-vindo ao **BookOwl**! Este projeto foi criado para gerenciar uma biblioteca de livros da igreja, atualmente ele vai ser feito com ferramentas simples apenas para ter um bom gerenciamento.

## Objetivo

O objetivo é ser uma ferramenta que ajude outras pessoas que desejam organizar a biblioteca da sua igreja, empresa ou pessoal.

## Instalação

Siga os passos abaixo para instalar e rodar o projeto localmente:

1. **Clone o repositório:**
    ```
    git clone https://github.com/GabrielDev969/BookOwl.git
    cd BookOwl
    ```

2. **Crie um ambiente virtual:**
    ```
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3. **Instale as dependências:**
    ```
    pip install -r requirements.txt
    ```

4. **Aplique as migrações do banco de dados:**
    ```
    python manage.py migrate
    ```

5. **Inicie o servidor:**
    ```
    python manage.py runserver
    ```

6. Acesse `http://localhost:8000` no seu navegador.

## Como contribuir ou implementar melhorias

Quer adicionar novas funcionalidades ou melhorar o FinanceApp? Siga estas dicas:

- **Fork o repositório** e crie uma branch para sua feature ou correção.
- **Implemente sua funcionalidade** seguindo as boas práticas do Django.
- **Adicione testes** para garantir a qualidade do código.
- **Atualize a documentação** se necessário.
- **Abra um Pull Request** explicando suas mudanças.

### Formatos de commit

Para manter o histórico organizado, utilize os seguintes formatos de commit:

- `:sparkles:` Novidades, novas funcionalidades
- `:bug:` Correção de bugs
- `:wrench:` Ajustes de configuração ou manutenção
- `:memo:` Atualização de documentação
- `:recycle:` Refatoração de código
- `:fire:` Remoção de código ou arquivos
- `:rocket:` Melhorias de performance ou deploy
- `:lipstick:` Ajustes de estilo ou interface

Exemplo:
```
git commit -m ":sparkles: Adiciona funcionalidade de exportação de relatórios"
```

Sua criatividade é o limite! Sinta-se à vontade para contribuir e tornar o BookOwl ainda melhor.

---

Feito com ❤ por pessoas que amam livros!
