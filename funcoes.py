#----------------------------------------------------------------------------------------
#                          Trabalho de Redes de Computadores II
# Autores:
#           Daniele Harumi Ito      GRR20101243
#           Paulo Ricardo Gemniczak GRR20096237
#
# Este codigo implementa funcoes utilizadas nos codigos do cliente e servidor.
#
#                Ciencia da Computacao - Universidade Federal do Parana
#                                  Junho 2015
#----------------------------------------------------------------------------------------

import datetime
import os
import socket

#cada operacao tem tamanho igual a 1byte
#aqui elas sao definidas apenas para facilitar a programacao e leitura do codigo
NOK = '0'
OK = '1'
ABORT = '2'
COMMIT = '3'
SOMA = '4'
SUBTRACAO = '5'
DIVISAO = '6'
MULTIPLICACAO = '7'

cabecalho = "============================================================================================\n"
cabecalho += "Inicio da execucao do cliente {}: programa implementa protocolo 2PC.\n".format(socket.gethostbyname(socket.gethostbyname("localhost")))
cabecalho += "Daniele Harumi Ito & Paulo Ricardo Gemniczak - Universidade Federal do Parana\n"
cabecalho += "============================================================================================\n\n"

#Funcao imprime a operacao e o resultado no seguinte formato:
#<valor_antigo> <op> <valor_recebido> = <resultado>
def formataResultadoOperacao(valorAntigo, operacao, valorRecebido, resultado):
	op = ""
	if operacao == SOMA:
		op = " + "
	elif operacao == SUBTRACAO:
		op = " - "
	elif operacao == MULTIPLICACAO:
		op = " * "
	elif operacao == DIVISAO:
		op = " / "

	return str(valorAntigo) + op + str(valorRecebido) + " = " + str(resultado)
#----------------------------------------------------------------------------------------

# Funcao implementada apenas para auxiliar no registro do log. Assim as mensagens sao regis-
# tradas com seu real significado, e nao com o codigo de cada operacao.
def converteCodigoOperacaoParaString(codigo):
	if codigo == OK:
		return "OK"
	elif codigo == NOK:
		return "NOK"
	elif codigo == COMMIT:
		return "COMMIT"
	elif codigo == ABORT:
		return "ABORT"
	elif codigo == SOMA:
		return "SOMA"
	elif codigo == SUBTRACAO:
		return "SUBTRACAO"
	elif codigo == DIVISAO:
		return "DIVISAO"
	elif codigo == MULTIPLICACAO:
		return "MULTIPLICACAO"
#----------------------------------------------------------------------------------------

# Funcao salva em um arquivo uma mensagem, ambos passados por parametro.
def salvar(arquivo, mensagem):
	if os.path.isfile(arquivo) == False:
		f = open(arquivo, "w")
		f.write(cabecalho)
	else:
		f = open(arquivo, "a")

	mensagem = str(datetime.datetime.now()) + " -> " + mensagem

	f.write(mensagem)
	f.write("\n")
	f.close()
#----------------------------------------------------------------------------------------