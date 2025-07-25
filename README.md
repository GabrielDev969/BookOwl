# BookOwl 🦉

![BookOwl Logo](https://github.com/user-attachments/assets/743d47c6-1f72-4002-9d1a-87f02fba6b67#width=150&height=150)

[![Status](https://img.shields.io/badge/STATUS-EM%20PRODUCAO-green?style=for-the-badge)](https://github.com/GabrielDev969/BookOwl)
[![Version](https://img.shields.io/badge/Versão-1.4.2-green?style=for-the-badge)](https://github.com/GabrielDev969/BookOwl)
[![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)](LICENSE)

Bem-vindo ao **BookOwl**, um sistema intuitivo para gerenciar bibliotecas de igrejas, empresas ou coleções pessoais! Criado com ❤️ para organizar livros e empréstimos de forma simples e eficiente, o BookOwl nasceu de uma necessidade real: ajudar uma irmã da nossa igreja a gerenciar a biblioteca local.

> ⚠️ **Aviso Importante**: O recurso de registro (signup) está temporariamente desativado no serviço online. Para acessar o sistema, entre em contato com o administrador em [gabriel.dev969@gmail.com](mailto:gabriel.dev969@gmail.com) para obter uma conta.

> ℹ **Informações**: 
> Você pode ativar o cadastro no ambiente de desenvolvimento, mudando a view na url de signup para ```view.signup``` .
>
> Em desenvolvimento retire o DATABASE_URL do seu .env para utilizar o banco .sqlite a menos que esteja usando outro tipo de banco. 

## 📚 Objetivo

O BookOwl foi desenvolvido para simplificar o gerenciamento de bibliotecas, com foco em igrejas, pequenas instituições e coleções pessoais. Nosso objetivo é oferecer uma ferramenta prática e acessível que permita organizar livros, acompanhar empréstimos e gerenciar leitores, promovendo o acesso à leitura e ao conhecimento.

## ✨ Funcionalidades

- **Gerenciamento de Livros**: Cadastre, edite e organize livros com título, autor, descrição e status.
- **Controle de Empréstimos**: Monitore empréstimos, datas de devolução e status em tempo real.
- **Gestão de Pessoas**: Administre informações de leitores, incluindo nome, e-mail, telefone e endereço.
- **Interface Moderna**: Design responsivo com uma paleta de cores elegante.
- **Acessibilidade**: Suporte a navegação por teclado e alto contraste para uma experiência inclusiva.

## 🚀 Instalação

Siga os passos abaixo para rodar o BookOwl localmente:

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/GabrielDev969/BookOwl.git
   cd BookOwl
   ```

2. **Crie um ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplique as migrações do banco de dados**:
   ```bash
   python manage.py migrate
   ```

5. **Inicie o servidor**:
   ```bash
   python manage.py runserver
   ```

6. Acesse `http://localhost:8000` no seu navegador.

> **Nota**: Certifique-se de ter o Python 3.8+ instalado. Para criar um superusuário, use `python manage.py createsuperuser`.

## 🤝 Como Contribuir

Quer ajudar a tornar o BookOwl ainda melhor? Sua criatividade é bem-vinda! Siga estas etapas para contribuir:

1. **Fork o repositório** e crie uma branch para sua feature:
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```

2. **Implemente sua funcionalidade**, seguindo as boas práticas do Django.
3. **Adicione testes** para garantir a qualidade do código.
4. **Atualize a documentação** no README ou outros arquivos, se necessário.
5. **Abra um Pull Request** no GitHub, descrevendo suas mudanças.

### Formatos de Commit

Use emojis para manter o histórico organizado:

- `:sparkles:` Novas funcionalidades
- `:bug:` Correção de bugs
- `:wrench:` Ajustes de configuração
- `:memo:` Atualização de documentação
- `:recycle:` Refatoração de código
- `:fire:` Remoção de código ou arquivos
- `:rocket:` Melhorias de performance ou deploy
- `:lipstick:` Ajustes de estilo ou interface

**Exemplo**:
```bash
git commit -m ":sparkles: Adiciona exportação de relatórios em CSV"
```

Explore, crie e ajude a transformar bibliotecas com o BookOwl!

## 📬 Contato

Desenvolvido por **GabrielDev969**, um desenvolvedor apaixonado por criar soluções que facilitam a vida das pessoas. Conecte-se comigo:

- [GitHub](https://github.com/GabrielDev969)
- [LinkedIn](https://www.linkedin.com/in/gabriel-santos-b53632196)
- [Website](https://gabrieldev969.github.io/Portfolio/)

Para dúvidas, sugestões ou suporte, envie um e-mail para [gabriel.dev969@gmail.com](mailto:gabriel.dev969@gmail.com).

---

Feito com ❤️ por pessoas que amam livros e tecnologia!
