#!/usr/bin/env python3

import cgi
import json
import requests

form = cgi.FieldStorage()

#------------------------------------------------------------------------------------------
#Recebendo dados do SUAP
#------------------------------------------------------------------------------------------

#Login para autenticar ao Chat TCP
matricula = form.getvalue("user")
senha = form.getvalue("pass")

autenticacao = {
    "username": str(matricula),
    "password": str(senha)
}

urls = { "token":"https://suap.ifrn.edu.br/api/v2/autenticacao/token/",
         "dados":"https://suap.ifrn.edu.br/api/v2/minhas-informacoes/meus-dados/"}

#---------------------------------------------------------------------
# Metodo de obtencao do Token no SUAP
#---------------------------------------------------------------------

def getToken():
    response = requests.post(urls['token'], data=autenticacao)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))['token']
    return None

cabecalho={'Authorization': 'JWT {0}'.format(getToken())}

#---------------------------------------------------------------------
# Metodo que obtem as informacoes dos alunos
#---------------------------------------------------------------------

def getInformacoes():
    response = requests.get(urls['dados'], headers=cabecalho)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    return None

informacoes = json.loads(getInformacoes())

foto = str("https://suap.ifrn.edu.br" + informacoes['url_foto_75x100'])
nome = informacoes['vinculo']['nome']
matricula = informacoes['vinculo']['matricula']
campus = informacoes['vinculo']['campus']
email = informacoes['email']

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#HTML
#-------------------------------------------------------------------------------------------------------------------------------------------------------------


###Aluno
if informacoes['tipo_vinculo'] == "Aluno":
	curso = informacoes['vinculo']['curso']

	print("Content-type: text/html\n\n" )
	print("<html>")

	print("<head>")
	print("<title>Login</title>")
	print('<meta charset="UTF-8">')
	print('<meta name="viewport" content="width=device-width, initial-scale=1">')
	print('<link rel="stylesheet" type="text/css" href="css/main.css">')
	print('<link rel="icon" type="image/png" href="images/icons/favicon.png"/>')
	print("</head>")

	print("<body>")


	print('<div class="container-login100">')
	print('<div class="wrap-login100" style="width: auto;">')

	print('<form action="listar.py" method="post" >')
	print('<div class="login100-pic" style="text-align: center;">')
	print('<img  src="' + foto + '"/>')
	print('<input type="hidden" name="foto" value = "' + foto +'">')

	print("</div><br>")

	print('<div class="login100-form">')
	print("<h4>Nome: " + nome + "</h4>")
	print('<input type="hidden" name="nome" value = "' + nome +'">')
	print("<h4>Matricula: " + matricula + "</h4>")
	print('<input type="hidden" name="matricula" value = "' + matricula +'">')
	print("<h4>Email: " + email + "</h4>")
	print('<input type="hidden" name="email" value = "' + email +'">')
	print("<h4>Campus: " + campus + "</h4>")
	print('<input type="hidden" name="campus" value = "' + campus +'">')
	print("<h4>Curso: " + curso + "</h4>")
	print('<input type="hidden" name="curso" value = "' + curso +'">')

	print('<input type="hidden" name="vinculo" value = "' + informacoes['tipo_vinculo'] +'">')

	print('<div class="container-login100-form-btn"><button class="login100-form-btn">adicionar no banco de dados e/ou listar</button></div>')
	print("</div>")
	print("</form>")

	print("</div>")
	print("</div>")
	print("</body>")
	print("</html>")

else:
	diretoria = informacoes['vinculo']['setor_suap']
	disciplina = informacoes['vinculo']['disciplina_ingresso']

	print("Content-type: text/html\n\n" )
	print("<html>")

	print("<head>")
	print("<title>Login</title>")
	print('<meta charset="UTF-8">')
	print('<meta name="viewport" content="width=device-width, initial-scale=1">')
	print('<link rel="stylesheet" type="text/css" href="css/main.css">')
	print('<link rel="icon" type="image/png" href="images/icons/favicon.png"/>')
	print("</head>")

	print("<body>")


	print('<div class="container-login100">')
	print('<div class="wrap-login100" style="width: auto;">')

	print('<form action="listar.py" method="post" >')
	print('<div class="login100-pic" style="text-align: center;">')
	print('<img  src="' + foto + '"/>')
	print('<input type="hidden" name="foto" value = "' + foto +'">')

	print("</div><br>")

	print('<div class="login100-form">')
	print("<h4>Nome: " + nome + "</h4>")
	print('<input type="hidden" name="nome" value = "' + nome +'">')
	print("<h4>Matricula: " + matricula + "</h4>")
	print('<input type="hidden" name="matricula" value = "' + matricula +'">')
	print("<h4>Email: " + email + "</h4>")
	print('<input type="hidden" name="email" value = "' + email +'">')
	print("<h4>Campus: " + campus + "</h4>")
	print('<input type="hidden" name="campus" value = "' + campus +'">')
	print("<h4>Diretoria: " + diretoria + "</h4>")
	print('<input type="hidden" name="diretoria" value = "' + diretoria +'">')
	print("<h4>Disciplina: " + disciplina + "</h4>")
	print('<input type="hidden" name="disciplina" value = "' + disciplina +'">')

	print('<input type="hidden" name="vinculo" value = "' + informacoes['tipo_vinculo'] +'">')

	print('<div class="container-login100-form-btn"><button class="login100-form-btn">adicionar no banco de dados e listar</button></div>')
	print("</div>")
	print("</form>")

	print("</div>")
	print("</div>")
	print("</body>")
	print("</html>")
