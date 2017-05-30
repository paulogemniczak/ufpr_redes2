#----------------------------------------------------------------------------------------
#                          Trabalho de Redes de Computadores II
# Autores:
#           Daniele Harumi Ito      GRR20101243
#           Paulo Ricardo Gemniczak GRR20096237
#
# Este codigo implementa a interface do servidor de um protocolo 2PC ("Two-Phase Commit") 
# em uma versao simplificada que assume que servidores e clientes jamais falham.
#
#                Ciencia da Computacao - Universidade Federal do Parana
#                                  Junho 2015
#----------------------------------------------------------------------------------------

import socket
import sys
import funcoes

#se a linha de comando nao tiver dois argumentos, entao exibe o formato correto e encerra o programa
if len(sys.argv) != 3:
	print "A linha de execucao deve ter o seguinte formato:"
	print "python servidor.py <porta>"
	exit()

#nome do arquivo que contem o log desse servidor
ARQUIVO_LOG = "log_servidor_{}.txt".format(sys.argv[1])

#variavel que armazena o resultado das operacoes
valorArmazenado = 0.0

#mensagem completa recebida do cliente (operacao+valor)
mensagemRecebida = ""

#indica quando o servidor atendeu um cliente e esta esperando seu COMMIT ou ABORT
#inicia com False, pois o servidor nao esta esperando COMMIT ou ABORT quando iniciado
esperandoResposta = False

#tupla <ip, porta> que contem o endereco do cliente cujo o servidor esta esperando um COMMIT ou ABORT 
clienteEsperando = ('',0)

#cria um socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#guarda o ip em que o servidor esta rodando
ip_servidor = sys.argv[2]

#argumento passado na execucao do programa que indica a porta em que o servidor ira "ouvir" 
porta = int(sys.argv[1])

#Faz bind do socket na porta
endereco_servidor = (ip_servidor, porta)
sock.bind(endereco_servidor)

sock.listen(1)

while True:
	#espera uma conexao
	l = "Esperando uma conexao..."
	funcoes.salvar(ARQUIVO_LOG, l)
	conexao, endereco_cliente = sock.accept()

	try:
		l = "Conectei com o cliente: {}".format(str(endereco_cliente[0]))
		funcoes.salvar(ARQUIVO_LOG, l)

		#recebe mensagem do cliente conectado
		dadosRecebidos = conexao.recv(1024)

		#Caso a mensagem tenha tamanho maior que 1, entao o primeiro byte representa a operacao
		#e o restante representa o valor
		if len(dadosRecebidos) > 1:
			l = "Recebi a mensagem: {} {}".format(funcoes.converteCodigoOperacaoParaString(dadosRecebidos[0]), dadosRecebidos[1:])
		else:
			l = "Recebi a mensagem: {}".format(funcoes.converteCodigoOperacaoParaString(dadosRecebidos))
		funcoes.salvar(ARQUIVO_LOG, l)

		#se estava esperando um COMMIT ou ABORT
		if esperandoResposta:
			#se recebeu um COMMIT
			if dadosRecebidos == funcoes.COMMIT:
				valorAntigo = valorArmazenado
				#valor esta do segundo byte em diante da mensagem recebida
				valorRecebido = float(mensagemRecebida[1:])

				dividiuPorZero = False

				#decide qual operacao deve ser realizada
				#operacao esta no primeiro byte da mensagem recebida
				if mensagemRecebida[0] == funcoes.SOMA:
					valorArmazenado += valorRecebido
				elif mensagemRecebida[0] == funcoes.SUBTRACAO:
					valorArmazenado -= valorRecebido
				elif mensagemRecebida[0] == funcoes.MULTIPLICACAO:
					valorArmazenado *= valorRecebido
				elif mensagemRecebida[0] == funcoes.DIVISAO:
					if valorRecebido == 0.0: #caso seja uma divisao e o valor recebido seja zero
						#nao efetua a operacao e exibe mensagem de aviso
						funcoes.salvar(ARQUIVO_LOG, "Nao eh possivel dividir por 0.")
						dividiuPorZero = True
					else:#caso seja diferente de zero, entao realiza a operacao
						valorArmazenado /= valorRecebido

				#Como ja recebeu o COMMIT, entao nao fica mais esperando um COMMIT ou ABORT
				#ou seja, ja pode receber uma operacao de outro cliente
				esperandoResposta = False

				if dividiuPorZero == False:
					#formata o resultado, passando valor antigo, operacao, valor recebido e o resultado, entao registra no log
					l = funcoes.formataResultadoOperacao(valorAntigo, mensagemRecebida[0], valorRecebido, valorArmazenado)
					funcoes.salvar(ARQUIVO_LOG, l)

			#se recebeu um ABORT
			elif dadosRecebidos == funcoes.ABORT:
				#verifica se o cliente que mandou ABORT eh o mesmo que deve me enviar um COMMIT ou ABORT
				if endereco_cliente[0] == clienteEsperando[0]:
					#caso seja o mesmo, entao nao fica mais esperando um COMMIT ou ABORT
					#ou seja, ja pode receber uma operacao de outro cliente
					esperandoResposta = False
			else:
				l = "Estou esperando COMMIT ou ABORT de outro cliente, entao estou enviando NOK"
				funcoes.salvar(ARQUIVO_LOG, l)
				#caso esteja esperando um COMMIT ou ABORT e o que recebi nao eh nenhuma dessas mensagens
				#entao envia NOK
				conexao.sendall(funcoes.NOK)

		#se nao estava esperando COMMIT ou ABORT
		else:
			#se a mensagem recebida eh diferente de ABORT ou COMMIT ou OK ou NOK
			#esse if eh soh para garantir, porque como nao esta esperando COMMIT ou ABORT, a mensagem recebida nao
			#pode ser uma dessas, alem de que OK e NOK o servidor nunca deve receber
			if dadosRecebidos != funcoes.ABORT and dadosRecebidos != funcoes.COMMIT and dadosRecebidos != funcoes.OK and dadosRecebidos != funcoes.NOK:
				funcoes.salvar(ARQUIVO_LOG, "Enviando OK")
				#envia OK para o cliente
				conexao.sendall(funcoes.OK)
				#indica que esta esperando um COMMIT ou ABORT
				esperandoResposta = True
				#guarda o endereco do cliente que devera enviar COMMIT ou ABORT
				clienteEsperando = endereco_cliente
				#armazena a mensagem recebida para que ela seja processada ou descartada apos receber o COMMIT ou ABORT
				mensagemRecebida = dadosRecebidos
	finally:
		#encerra a conexao
		conexao.close()
		l = "Encerrei a conexao com o cliente: {}".format(str(endereco_cliente[0]))
		funcoes.salvar(ARQUIVO_LOG, l)