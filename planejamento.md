# Planejamento de Implementação para Desenvolvimento de API

## 1. Configuração do Projeto
- Criar novo repositório GitHub para o projeto. (Local)
- Configurar ambiente virtual.
- Instalar as bibliotecas necessárias ( FastAPI, SQLAlchemy, PyJWT, etc.).

## 2. Implementação da Autenticação JWT
- **Implementar Endpoint `/token`:**
  - Codigo para o endpoint que gera credenciais de usuário.


## 3. Definição da Estrutura da API
- **Definir Endpoints:**
  - **POST /token**: Para autenticação de usuário e geração de token JWT.
  - **GET /user**: Rota protegida acessível apenas para usuários com o papel "user".
  - **GET /admin**: Rota protegida acessível apenas para usuários com o papel "admin".
- **Determinar Requisitos de Dados:**
  - Identificar os dados necessários para cada endpoint (por exemplo, credenciais de usuário, papéis).

## 4. Design do Banco de Dados
- Escolher um banco de dados ( SQLite para simplicidade).
- Definir o modelo de usuário com base na estrutura da API para armazenar credenciais e papéis de usuário.
- Criar um esquema de banco de dados que alinhe com os requisitos de dados identificados na estrutura da API.

## 5. Lógica de Autenticação de Usuário
- Implementar lógica para verificar credenciais de usuário contra `fake_users_db`.
- Retornar respostas apropriadas para tentativas de autenticação bem-sucedidas e falhas.

## 6. Lógica de Rotas Protegidas
- Implementar controle de acesso para as rotas `/user` e `/admin` com base nos papéis de usuário.
- Retornar respostas apropriadas para tentativas de acesso não autorizadas.

## 7. Testes
- Escrever testes unitários para o endpoint `/token` para garantir que a geração de JWT funcione corretamente.
- Testar as rotas protegidas (`/user` e `/admin`) usando o JWT gerado.
- Usar uma ferramenta como Postman ou curl para testes manuais.

## 8. Documentação
- Criar um arquivo README no repositório do GitHub.
- Incluir instruções sobre:
  - Como configurar o projeto.
  - Como executar o servidor da API.
  - Como testar os endpoints.
- Documentar os endpoints da API e seus inputs/outputs esperados.

## 9. Considerações de Segurança
- Garantir que as senhas sejam armazenadas de forma segura (por exemplo, hash).
- Implementar tratamento de erros para entradas inválidas e exceções.
- Considerar limitação de taxa para o endpoint de autenticação.

## 10. Implantação (Opcional)
- Se necessário, planejar a implantação em um serviço de nuvem (por exemplo, Heroku, AWS).
- Configurar variáveis de ambiente para informações sensíveis (por exemplo, chaves secretas).

## 11. Revisão e Finalização
- Revisar o código em busca de melhores práticas e segurança.
- Garantir que todos os recursos sejam implementados conforme os requisitos.
- Criar o repositório no GitHub e torná-lo público para avaliação.

## Estimativa de Tempo
- Configuração do Projeto: 30 min
- Implementação da Autenticação JWT: 1h
- Definição da Estrutura da API: 1h
- Design do Banco de Dados: 1h
- Lógica de Autenticação de Usuário: 1h
- Lógica de Rotas Protegidas: 30 min
- Testes: 1h
- Documentação: 40min
- Considerações de Segurança: 1h

Tempo total: ~8h