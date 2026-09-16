Configuração do ambiente virtual Python

Abra o terminal na pasta do backend:
cd C:\Projetos\ApprovalIntelligence\backend

Crie o ambiente virtual:
python -m venv .venv

Ative o ambiente virtual:
.\.venv\Scripts\Activate.ps1

Se o PowerShell bloquear a execução do script, execute uma vez:
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

Depois, ative novamente:
.\.venv\Scripts\Activate.ps1

Quando o ambiente estiver ativo, o terminal deverá apresentar algo semelhante a:
(.venv) PS C:\Projetos\ApprovalIntelligence\backend>

Instalação das dependências

Com o ambiente virtual ativo, execute:
python -m pip install --upgrade pip

Instale as dependências do projeto:
python -m pip install -r requirements.txt

Caso seja necessário instalar as ferramentas de teste:
python -m pip install pytest httpx2

Criação das tabelas do banco

O projeto possui duas abordagens para criação e evolução da estrutura do banco:

Criação inicial das tabelas utilizando o script create_tables.py;

Controle de alterações estruturais utilizando Alembic.

Criação inicial das tabelas

Na pasta backend, execute:
python create_tables.py

Esse script utiliza os modelos SQLAlchemy para criar as tabelas necessárias no banco configurado no arquivo .env.

As tabelas principais do MVP são:

candidates
exams
candidate_exams
evidences

Utilização do Alembic

Para verificar a versão atual das migrações:
alembic current

Para aplicar as migrações disponíveis:
alembic upgrade head

Para verificar o histórico de migrações:
alembic history

Durante o desenvolvimento, deve-se utilizar o Alembic para controlar alterações estruturais no banco. O script create_tables.py é útil para a criação inicial em ambientes locais.

Execução da API

A API utiliza FastAPI e Uvicorn.

Acessar a pasta do backend
cd C:\Projetos\ApprovalIntelligence\backend

Ativar o ambiente virtual
.\.venv\Scripts\Activate.ps1

Iniciar a API

Execute:
python -m uvicorn app.main:app --reload

Quando a API iniciar corretamente, o terminal deverá apresentar uma mensagem semelhante a:
Uvicorn running on http://127.0.0.1:8000

Endereços importantes

API:
http://127.0.0.1:8000

Documentação Swagger:
http://127.0.0.1:8000/docs

Documentação alternativa:
http://127.0.0.1:8000/redoc

Health check da aplicação:
http://127.0.0.1:8000/api/health

Health check do banco:
http://127.0.0.1:8000/api/health/database

Principais endpoints disponíveis

Saúde da aplicação
GET /api/health

Saúde da conexão com o banco
GET /api/health/database

Candidatos
GET /candidates
POST /candidates
GET /candidates/{candidate_id}

Provas
GET /exams
POST /exams
GET /exams/{exam_id}

Relacionamento candidato/prova
GET /candidate-exams
POST /candidate-exams
GET /candidate-exams/{candidate_exam_id}

Evidências
POST /candidate-exams/{candidate_exam_id}/evidences
GET /candidate-exams/{candidate_exam_id}/evidences

Análise por dimensões
GET /api/candidate-exams/{candidate_exam_id}/dimensions

Gêmeo Digital
GET /api/candidate-exams/{candidate_exam_id}/digital-twin

Próxima Melhor Ação
GET /api/candidate-exams/{candidate_exam_id}/next-best-action

 Execução dos testes

Os testes automatizados estão localizados em:

backend/tests

Acessar a pasta do backend
cd C:\Projetos\ApprovalIntelligence\backend

Ativar o ambiente virtual
.\.venv\Scripts\Activate.ps1

Executar todos os testes
pytest -q

Executar os testes com mais detalhes
pytest -v

Executar um arquivo específico

Exemplo:
pytest tests/test_digital_twin_service.py -v

Executar um teste específico pelo nome
pytest -k digital_twin -v

Resultado esperado

Um resultado bem-sucedido deverá ser semelhante a:
44 passed, 1 warning

A quantidade de testes poderá aumentar conforme novas funcionalidades forem implementadas.

O warning relacionado ao AnyIO não impede a execução dos testes e não representa, neste momento, uma falha funcional do projeto.

Comandos rápidos

Iniciar a API
cd C:\Projetos\ApprovalIntelligence\backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload

Executar os testes
cd C:\Projetos\ApprovalIntelligence\backend
.\.venv\Scripts\Activate.ps1
pytest -q

Criar tabelas
cd C:\Projetos\ApprovalIntelligence\backend
.\.venv\Scripts\Activate.ps1
python create_tables.py

Aplicar migrações
cd C:\Projetos\ApprovalIntelligence\backend
.\.venv\Scripts\Activate.ps1
alembic upgrade head