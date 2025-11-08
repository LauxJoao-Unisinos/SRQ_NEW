# SRQ — Sistema de Reserva de Quadras (Sprint 1)

Esta pasta contém apenas os itens da Sprint 1: UC01, UC02, UC03, UC04, UC05, UC06, UC09.

## Stack
- Django 4.2
- MySQL (via `mysqlclient`) — configure via variáveis de ambiente
- Sem CSS (apenas HTML básico nos templates)

## Configuração rápida
1. Crie um virtualenv e instale dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure o banco via variáveis de ambiente (ou `.env`):
   ```bash
   export DB_NAME=srq
   export DB_USER=root
   export DB_PASSWORD=senha
   export DB_HOST=127.0.0.1
   export DB_PORT=3306
   ```
3. Aplique migrações e crie superusuário:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. Rode o servidor:
   ```bash
   python manage.py runserver
   ```

> As regras de negócio e detalhes adicionais estão descritos nos arquivos `Plano_de_Projeto_SRQ.md` e `Casos_de_Uso_SRQ.md`
