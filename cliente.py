#----------------------------------------------------------------------------------------
#                          Trabalho de Redes de Computadores II
# Autores:
#           Daniele Harumi Ito      GRR20101243
#           Paulo Ricardo Gemniczak GRR20096237
#
# Este codigo implementa a interface do cliente de um protocolo 2PC ("Two-Phase Commit") 
# em uma versao simplificada que assume que servidores e clientes jamais falham.
#
#                Ciencia da Computacao - Universidade Federal do Parana
#                                  Junho 2015
#----------------------------------------------------------------------------------------

import socket
import sys
import time
import funcoes

#Funcao que recebe um endereco de servidor e uma mensagem, envia essa mensagem e retorna a mensagem
#recebida do servidor 
def comunica(endereco_servidor, mensagem):
	#Cria um socket TCP/IP
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	#registra no log que esta conectando ao servidor
	l = "Conectando ao servidor %s na porta %s" % endereco_servidor
	funcoes.salvar(ARQUIVO_LOG, l)

	try:
		#Conecta o socket a porta onde o servidor esta escutando
		sock.connect(endereco_servidor)
	except Exception, e: #caso nao consiga conectar com o servidor, registra no log o erro e retorna None
		l = "Erro ao conectar com o servidor %s na porta %s" % endereco_servidor
		funcoes.salvar(ARQUIVO_LOG, l)
		return None

	retorno = ""
	try:
		#Caso a mensagem tenha tamanho maior que 1, entao o primeiro byte representa a operacao
		#e o restante representa o valor
		if len(mensagem) > 1:
			l = "Enviando a mensagem: {} {}".format(funcoes.converteCodigoOperacaoParaString(mensagem[0]), mensagem[1:])
		else:
			l = "Enviando a mensagem: %s" % funcoes.converteCodigoOperacaoParaString(mensagem)
		funcoes.salvar(ARQUIVO_LOG, l)

		#envia a mensagem
		sock.sendall(mensagem)
		#recebe o retorno do servidor
		retorno = sock.recv(1024)
		l = "Recebi a mensagem: {}".format(funcoes.converteCodigoOperacaoParaString(retorno))
		funcoes.salvar(ARQUIVO_LOG, l)
	finally:
		l = "Fechando socket"
		funcoes.salvar(ARQUIVO_LOG, l)
		#fecha o socket e retorna a mensagem que o servidor retornou
		sock.close()
		return retorno
#----------------------------------------------------------------------------------------

#nome do arquivo que contem o log desse cliente
ARQUIVO_LOG = "log_cliente_{}.txt".format(socket.gethostbyname(socket.gethostbyname("localhost")))

#se a linha de comando nao tiver 8 argumentos, exibir o formato correto e encerra o programa
if len(sys.argv) != 9:
	print len(sys.argv)
	print "A linha de execucao deve ter o seguinte formato:"
	print "python cliente.py <ip_serv_1> <porta_serv_1> <ip_serv_2> <porta_serv_2> <ip_serv_3> <porta_serv_3> <operacao> <valor>"
	print "Operacoes:"
	print "    -> Soma: SOMA"
	print "    -> Subtracao: SUB"
	print "    -> Divisao: DIV"
	print "    -> Multiplicacao: MULT"
	print "Valor:"
	print "    -> Deve ser um numero real utilizando ponto para separar as casas decimais."
	exit()

#endereco de cada servidor eh formado por uma tupla <ip, porta>
endereco_servidor1 = (sys.argv[1], int(sys.argv[2]))
endereco_servidor2 = (sys.argv[3], int(sys.argv[4]))
endereco_servidor3 = (sys.argv[5], int(sys.argv[6]))

#argv[7] deve conter a operacao a ser realizada
operacao = sys.argv[7]

#argv[8] deve conter o valor para realizar a operacao
try: #tenta converter o argumento 'valor' para float
	valor = float(sys.argv[8])
except Exception, e: #caso nao consiga, entao encerra o programa
	print "O argumento 'valor' esta incorreto"
	exit()

mensagem = ""

#mensagem recebe operacao+valor
#primeiro byte da mensagem contem a operacao
#o restante dos bytes contem o valor para realizar a operacao
if operacao == "SOMA":
	mensagem = funcoes.SOMA + str(valor)
elif operacao == "SUB":
	mensagem = funcoes.SUBTRACAO + str(valor)
elif operacao == "DIV":
	mensagem = funcoes.DIVISAO + str(valor)
elif operacao == "MULT":
	mensagem = funcoes.MULTIPLICACAO + str(valor)
else:
	print "Operacao invalida."
	exit()

#comunica com o servidor 1 enviando a mensagem e recebe o retorno do servidor 1
retorno1 = comunica(endereco_servidor1, mensagem)

#time.sleep(5)

#comunica com o servidor 2 enviando a mensagem e recebe o retorno do servidor 2
retorno2 = comunica(endereco_servidor2, mensagem)

#comunica com o servidor 3 enviando a mensagem e recebe o retorno do servidor 3
retorno3 = comunica(endereco_servidor3, mensagem)

#se pelo menos um retorno for None, entao pelo menos em um dos servidores nao foi possivel conectar
if retorno1 == None or retorno2 == None or retorno3 == None:
	exit() #encerra a execucao do programa

#se receber OK dos tres servidores, entao envia COMMIT para os tres
if retorno1 == funcoes.OK and retorno2 == funcoes.OK and retorno3 == funcoes.OK:
	l = "Como recebi tres OK, entao devo enviar COMMIT para os tres servidores."
	funcoes.salvar(ARQUIVO_LOG, l)
	comunica(endereco_servidor1, funcoes.COMMIT)
	comunica(endereco_servidor2, funcoes.COMMIT)
	comunica(endereco_servidor3, funcoes.COMMIT)
#senao, envia ABORT para os tres servidores
else:
	l = "Como nao recebi tres OK, entao devo enviar ABORT para os tres servidores."
	funcoes.salvar(ARQUIVO_LOG, l)
	comunica(endereco_servidor1, funcoes.ABORT)
	comunica(endereco_servidor2, funcoes.ABORT)
	comunica(endereco_servidor3, funcoes.ABORT)

funcoes.salvar(ARQUIVO_LOG, "==============================================================\n");