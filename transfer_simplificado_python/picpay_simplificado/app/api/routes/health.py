"""Esse código implementa um Helth Check da nossa API.
Ele permite verificar se a aplicação está respondendo""" 

#Organizar as rotas da aplicação em módulos separados
from fastapi import APIRouter

# Router contém endpoints relacionados á saúde da aplicação
router = APIRouter(tags=["Health"])
# tags Health é utilizado principalmente para organização da documentação automática do FastAPI


# Decorator da Rota
@router.get("/health")
def health(): # Criamos a função que será executada quando alguém acessar.
    return {"status": "ok"} # O FastAPI automaticamente transforma esse dicionário em JSON.

"""Quando alguém fizer uma requisição HTTP GET para /health, execute a função que vem logo abaixo"""
