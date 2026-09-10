para entrar na .venv: cd C:\Projetos\ApprovalIntelligence> 
.\.venv\Scripts\Activate.ps1

Para subir o servidor python: cd C:\Projetos\ApprovalIntelligence\backend> 
python -m uvicorn app.main:app --reload

Navegador:
    http://127.0.0.1:8000/api/health
    http://127.0.0.1:8000/docs