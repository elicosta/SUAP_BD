#!/usr/bin/env python3

import cgi
import json
import requests
import psycopg2

form = cgi.FieldStorage()


###Informações do login para armazenar no banco###

vinculo = form.getvalue("vinculo")
matricula = form.getvalue("matricula")
nome = form.getvalue("nome")
email = form.getvalue("email")
foto = form.getvalue("foto")

if vinculo == "Aluno":
	campus = form.getvalue("campus")
	curso = form.getvalue("curso")
else:
	curso = form.getvalue("disciplina")
	campus = form.getvalue("diretoria")


###Comando de conexões ao Banco###
ConexaoDefault  = "dbname=postgres user=postgres host=localhost password=aluno"
ConexaoDBalunos = "dbname=alunos user=postgres host=localhost password=aluno"
SQLCriaDatabase = "CREATE DATABASE alunos"

###coluna curso do banco será curso do aluno e disciplina do servidor
###coluna campus do banco será campus do aluno e diretoria do servidor
SQLCriaTable = "CREATE TABLE alunos (matricula BIGINT PRIMARY KEY, nome VARCHAR(100), email VARCHAR(200), campus VARCHAR(200), curso VARCHAR(200), foto VARCHAR(200), vinculo VARCHAR(200));"


###Funções
def criarBanco():
	from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
	conn = psycopg2.connect(ConexaoDefault)
	conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = conn.cursor()
	cur.execute(SQLCriaDatabase)
	conn = psycopg2.connect(ConexaoDBalunos)
	cur = conn.cursor()
	cur.execute(SQLCriaTable)
	conn.commit()
	cur.close()
	conn.close()

def tabela_existe(NomeTabela):
	strSQL1 = "SELECT EXISTS(SELECT datname FROM pg_database WHERE datname='{0}')".format(NomeTabela)
	strSQL = "SELECT EXISTS(SELECT relname FROM pg_class WHERE relname='{0}')".format(NomeTabela)

	conn = psycopg2.connect(ConexaoDefault)
	curbd = conn.cursor()
	curbd.execute(strSQL1)
	existeBD = curbd.fetchone()[0]

	if(existeBD == True):
		con = psycopg2.connect(ConexaoDBalunos)
		cur = con.cursor()
		cur.execute(strSQL)
		existe = cur.fetchone()[0]
		
		cur.close()
		con.close()
	else:
		existe = False

	curbd.close()
	conn.close()

	return existe

def aluno_existe(Matricula):
	strSQL = "SELECT EXISTS(SELECT matricula FROM alunos WHERE matricula={0})".format(Matricula)

	con = psycopg2.connect(ConexaoDBalunos)
	cur = con.cursor()
	cur.execute(strSQL)
	existePeople = cur.fetchone()[0]	
	cur.close()
	con.close()

	return existePeople

def inserirDados(matricula, nome, email, campus, curso, foto, vinculo):
	conn = psycopg2.connect(ConexaoDBalunos)
	cur = conn.cursor()
	SQLInsereDados = "INSERT INTO alunos (matricula, nome, email, campus, curso, foto, vinculo) VALUES ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(matricula, nome, email, campus, curso, foto, vinculo)
	cur.execute(SQLInsereDados)
	conn.commit()
	cur.close()
	conn.close()





#-----------------------------------------------------------------------------------------------------------------------------------------------------
#Principal
#---------------------------------------------------------------------------------------------------------------------------------------------------

if (tabela_existe("alunos")):
	if(aluno_existe(matricula) == False):
		inserirDados(matricula, nome, email, campus, curso, foto, vinculo)
else:
	criarBanco()
	inserirDados(matricula, nome, email, campus, curso, foto, vinculo)



connConexao = psycopg2.connect(ConexaoDBalunos)
curConexao = connConexao.cursor()
curConexao.execute("select * from alunos")
resultado = curConexao.fetchall()
curConexao = connConexao.cursor()
connConexao.commit()
connConexao.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#HTML
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
print("Content-type: text/html\n\n")
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
print('<div class="wrap-login100" style="width: 900px;">')
print('<span class="login100-form-title">Lista do Banco de Dados</span>')



for aluno in resultado:
	if (aluno[6] == "Aluno"):
		print('<div class="login100-pic" style="text-align: center;">')
		print('<img  src="{0}"/>'.format(aluno[5]))
		print("</div>")
		print('<div class="login100-form">')
		print("<h4>Matrícula: {0}</h4>".format(aluno[0]))
		print("<h4>Nome: {0}</h4>".format(aluno[1]))
		print("<h4>Email: {0}</h4>".format(aluno[2]))
		print("<h4>Campus: {0}</h4>".format(aluno[3]))
		print("<h4>Curso: {0}</h4>".format(aluno[4]))
		print("<h4>Vinculo: {0}</h4>".format(aluno[6]))
		print("</div>")
	else:
		print('<div class="login100-pic" style="text-align: center;">')
		print('<img  src="{0}"/>'.format(aluno[5]))
		print("</div>")
		print('<div class="login100-form">')
		print("<h4>Matrícula: {0}</h4>".format(aluno[0]))
		print("<h4>Nome: {0}</h4>".format(aluno[1]))
		print("<h4>Email: {0}</h4>".format(aluno[2]))
		print("<h4>Diretoria: {0}</h4>".format(aluno[3]))
		print("<h4>Disciplina: {0}</h4>".format(aluno[4]))
		print("<h4>Vinculo: {0}</h4>".format(aluno[6]))
		print("</div>")

print('<a href="index.html" style="margin-top: 25px;" class="login100-form-btn"><button class="login100-form-btn">voltar</button></a>')
print("</div>")
print("</div>")
print("</body>")
print("</html>")
