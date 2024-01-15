from time import sleep
import keyboard

# gravar após cada interação, evitar mais o erro para o cliente.


lista = list()


def limpar_tela():
    print('\n' * 30)


def buscar_produtos():
    limpar_tela()
    linhas_divisorias()
    print('Procurar produtos'.center(30))
    linhas_divisorias()

    if not lista:
        print('\033[031mNenhum produto encontrado\033[m.')

    while True:
        try:
            nome = int(input('Digite o código do produto [0 cancelar]: '))
            if nome == 0:
                break

            t = encontrar_produto_por_codigo(nome)

            if t:
                linhas_divisorias()
                print(f'\033[32mProduto encontrado!\033[m \nCódigo:{t[0]} \nNome: {t[1]} \nDescrição: {t[2]} \nValor: R${t[3]:.2f} \nVencimento {t[4]}')
            else:
                print('\033[31mProduto não encontrado\033[m.')



        except ValueError:
            print('Erro Somente números.')


def encontrar_produto_por_codigo(substituivel):
    for produto in lista:
        if produto[0] == substituivel:
            return produto
    return None


def excluir_produtos():
    pagina = 0
    produtos_por_pagina = 10

    while True:
        limpar_tela()
        linhas_divisorias()
        print('Excluir produtos'.center(30))
        linhas_divisorias()

        cont = 0
        for c in enumerate(lista[pagina * produtos_por_pagina:(pagina + 1) * produtos_por_pagina]):
            cont += 1

        print(f'Página {pagina + 1} - \033[43:30mQuantidade de produtos {cont}\033[m'.ljust(0))
        print()

        if not lista[pagina * produtos_por_pagina:(pagina + 1) * produtos_por_pagina]:
            print('\033[031mNenhum produto encontrado\033[m.')

        print(f'{"CÓDIGO": <10} {"NOME": <40} {"DESCRIÇÃO": <20} {"VALOR": >12} {"VENCIMENTO": >18}')
        for v in lista[pagina * produtos_por_pagina:(pagina + 1) * produtos_por_pagina]:
            print(f'{v[0]: <10} {v[1]: <40} {v[2]: <20} R$  {v[3]: >8,.2f}  {v[4]: >17}')

        d = 0
        for c, p in enumerate(lista):
            d += 1
        linhas_divisorias()
        print(f'A quantidade de produtos cadastradas é de {d}')
        linhas_divisorias()

        try:
            opc = input('Digite [P próxima pagina / C para continuar]: ').upper()
            if opc == 'C':
                break
            elif opc == 'P':
                pagina += 1
            else:
                print('\033[031mOpção inválida.\033[m.')
        except ValueError:
            print('\033[031mDigite somente números\033[m.')

    while True:
        try:
            linhas_divisorias()
            excluir = int(input('Digite o código do produto para excluir [0 para sair]: '))

            if excluir == 0:
                break

            excluir = encontrar_produto_por_codigo(excluir)

            if excluir:
                decisao = input(f'Deseja excluir o produto "\033[31m{excluir[1]}\033[m"? (S/N): ').strip().lower()[0]

                if decisao == 's':
                    lista.remove(excluir)
                    print(f'\033[31mPRODUTO {excluir[1]} REMOVIDO COM SUCESSO\033[m')
                else:
                    print('\033[32mExclusão cancelada\033[m.')
            else:
                print('\033[031mErro: Código de produto não encontrado\033[m')

        except ValueError as e:
            print(f'{e}')


def carregamento_de_dados():
    try:
        with open("dados-controle-estoque.txt", "r") as arquivo:
            for linha in arquivo:
                codigo, nome_produto, categoria, valor, vencimento = linha.strip().split(";")
                lista.append([int(codigo), nome_produto, categoria, float(valor), vencimento])
    except FileNotFoundError:
        pass


def salvar_produtos():
    with open("dados-controle-estoque.txt", "w") as arquivo:
        for produto in lista:
            arquivo.write(";".join(map(str, produto)) + "\n")


def alterar_descri():
    pagina = 0
    produtos_por_pagina = 10

    while True:
        limpar_tela()
        linhas_divisorias()
        print('Alteração de descrição'.center(30))
        linhas_divisorias()

        cont = 0
        for c in enumerate(lista[pagina * produtos_por_pagina:(pagina + 1) * produtos_por_pagina]):
            cont += 1

        print(f'Página {pagina + 1} - \033[43:30mQuantidade de produtos {cont}\033[m'.ljust(0))
        print()

        if not lista[pagina * produtos_por_pagina:(pagina + 1) * produtos_por_pagina]:
            print('\033[031mNenhum produto encontrado\033[m.')

        print(f'{"CÓDIGO": <10} {"NOME": <40} {"DESCRIÇÃO": <20} {"VALOR": >12} {"VENCIMENTO": >18}')
        for v in lista[pagina * produtos_por_pagina:(pagina + 1) * produtos_por_pagina]:
            print(f'{v[0]: <10} {v[1]: <40} {v[2]: <20} R$  {v[3]: >8,.2f}  {v[4]: >17}')

        d = 0
        for c, p in enumerate(lista):
            d += 1
        linhas_divisorias()
        print(f'A quantidade de produtos cadastradas é de {d}')

        linhas_divisorias()
        try:
            opc = input('Digite [P próxima pagina / C para continuar]: ').upper()
            if opc == 'C':
                break #breakSistem.
            elif opc == 'P':
                pagina += 1
            else:
                print('\033[031mOpção inválida.\033[m.')
        except ValueError:
            print('\033[031mDigite somente números\033[m.')

    while True:
        try:
            linhas_divisorias()
            codigo = int(input('Digite o código do produto [0 para parar]: '))
            if codigo == 0:
                break

            descricao = encontrar_produto_por_codigo(codigo)

            if descricao:
                print(f'A descricao atual "{descricao[2]}": ')
                nova_descricao = input('Digite a nova decrição: ').upper().strip()
                confirmacao = input(f'Deseja alterar a descrição do produto "\033[31m{descricao[1]}\033[m"? (S/N): ').strip().upper()[0]

                if confirmacao == 'S':
                    descricao[2] = nova_descricao
                    print('\033[32mNova descrição atualizada com SUCESSO\033[m.')
                else:
                    print('\033[32mOperação cancelada com SUCESSO\033[m.')

            else:
                print('\033[31mCódigo não encontrado no sistema\033[m.')
        except ValueError:
            print('\033[31mErro somente números podem ser digitados\033[m.')


def mudar_precos():
    pagina = 0
    produtos_por_pagina = 10

    while True:
        limpar_tela()
        linhas_divisorias()
        print('Mudar preços.'.center(30))
        linhas_divisorias()

        cont = 0
        for c in enumerate(lista[pagina * produtos_por_pagina:(pagina + 1) * produtos_por_pagina]):
            cont += 1

        print(f'Página {pagina + 1} - \033[43:30mQuantidade de produtos {cont}\033[m'.ljust(0))
        print()

        if not lista[pagina * produtos_por_pagina:(pagina + 1) * produtos_por_pagina]:
            print('\033[031mNenhum produto encontrado\033[m.')

        print(f'{"CÓDIGO": <10} {"NOME": <40} {"DESCRIÇÃO": <20} {"VALOR": >12} {"VENCIMENTO": >18}')
        for v in lista[pagina * produtos_por_pagina:(pagina + 1) * produtos_por_pagina]:
            print(f'{v[0]: <10} {v[1]: <40} {v[2]: <20} R$  {v[3]: >8,.2f}  {v[4]: >17}')

        d = 0
        for c, p in enumerate(lista):
            d += 1
        linhas_divisorias()
        print(f'A quantidade de produtos cadastradas é de {d}')

        linhas_divisorias()
        try:
            opc = input('Digite [P próxima pagina / C para continuar]: ').upper()
            if opc == 'C':
                break
            elif opc == 'P':
                pagina += 1
            else:
                print('\033[031mOpção inválida.\033[m.')
        except ValueError:
            print('\033[031mDigite somente números\033[m.')

    while True:
        try:
            linhas_divisorias()
            palpite = int(input('Digite o código do produto [0 para parar]: '))
            if palpite == 0:
                break

            ded = encontrar_produto_por_codigo(palpite)

            if ded:
                print(f'O preço atual do produto \033[33m{ded[1]}\033[m é R${ded[3]}: ')
                novo_valor = float(input('Digite o novo preço: ').replace(',', '.'))
                confirmacao = input(f'Deseja alterar o preço do produto "\033[31m{ded[1]}\033[m", de R$\033[33m{ded[3]}\033[m, para R$\033[32m{novo_valor:.2f}\033[m? (S/N): ').strip().upper()[0]

                if confirmacao == 'S':
                    ded[3] = novo_valor
                    print('\033[32mNova valor atualizado com SUCESSO\033[m.')
                else:
                    print('\033[32mOperação cancelada com SUCESSO\033[m.')

            else:
                print('\033[31mEscolha um número válido\033[m.')
        except ValueError:
            print('\033[31mErro somente números podem ser digitados\033[m.')


def cadastrar_produto():
    global codigo
    global nome_produto
    global categoria
    global valor

    limpar_tela()
    linhas_divisorias()
    print('Cadastro de produto'.center(30))
    linhas_divisorias()

    continuar_operacao = True

    while continuar_operacao:
        try:
            codigo = int(input('Digite o código do produto [Máximo de 8 dígitos, 0 para cancelar]: '))
            if len(str(codigo)) > 8:
                print('\033[31mErro. Código com mais de 8 dígitos\033[m.')
            elif any(coluna[0] == codigo for coluna in lista): # any retorna verdadeiro = se o código dentro da primeira coluna for verdadeiro. print abaixo
                print('\033[31mErro. Código já cadastrado. Escolha outro.\033[m')
            elif codigo == 0:
                print('\033[32mOperação cancelada com SUCESSO\033[m.')
                continuar_operacao = False
            elif codigo < 1:
                print('\033[31mErro, números negativos são inválidos\033[m.')
            else:
                break
        except ValueError:
            print('\033[31mErro. Digite somente números\033[m.')

    if not continuar_operacao:
        return

    while continuar_operacao:
        try:
            nome_produto = str(input('Digite o nome do produto: ')).strip().upper()[:50]
            if nome_produto == '0':
                continuar_operacao = False
            else:
                break
        except Exception as erro:
            print(f'{erro.__cause__}')

    if not continuar_operacao:
        return

    while continuar_operacao:
        try:
            categoria = str(input('Digite a categoria do produto: ')).strip().upper()
            if categoria == '0':
                continuar_operacao = False
            else:
                break
        except Exception as erro:
            print(f'{erro.__cause__}')

    if not continuar_operacao:
        return

    while continuar_operacao:
        try:
            valor = float(input('Digite o valor do produto: ').replace(',', '.'))
            if valor == 0:
                continuar_operacao = False
            elif valor < 1:
                print('\033[31mErro, Valores negativos não são aceitos\033[m')
            else:
                break
        except ValueError:
            print('\033[031mErro. Digite somente valores\033[m.')

    if not continuar_operacao:
        return

    while True:
        try:
            vencimento = input('Digite a data de vencimento[DIA/MÊS/ANO]: ')
            if len(str(vencimento)) == 10 and vencimento[2] == '/' and vencimento[5] == '/':

                dia, mes, ano = map(int, vencimento.split('/'))

                if 1 <= dia <= 31 and 1 <= mes <= 12:
                    formatada = f'{dia: 02d}/{mes: 02d}/{ano: 04d}'
                    print(formatada)
                    break

                else:
                    print('Dia ou mês fora do intervalo.')
        except ValueError:
            print('\033[031mErro. Digite números válidos para dia, mês e ano\033[m.')

    print('\033[032mProduto cadastrado com SUCESSO.\033[m.')
    lista.append([codigo, nome_produto, categoria, valor, formatada])


def mostrar_produtos():
    pagina = 0
    produtos_por_pagina = 10

    while True:
        limpar_tela()
        linhas_divisorias()
        print('Lista de produtos.'.center(30))
        linhas_divisorias()

        cont = 0
        for c in enumerate(lista[pagina * produtos_por_pagina:(pagina + 1) * produtos_por_pagina]):
            cont += 1

        print(f'Página {pagina + 1} - \033[43:30mQuantidade de produtos {cont}\033[m'.ljust(0))
        print()

        if not lista[pagina * produtos_por_pagina:(pagina + 1) * produtos_por_pagina]:
            print('\033[031mNenhum produto encontrado\033[m.')

        print(f'{"CÓDIGO": <10} {"NOME": <40} {"DESCRIÇÃO": <20} {"VALOR": >12} {"VENCIMENTO": >18}')
        for v in lista[pagina * produtos_por_pagina:(pagina + 1) * produtos_por_pagina]:
            print(f'{v[0]: <10} {v[1]: <40} {v[2]: <20} R$  {v[3]: >8,.2f}  {v[4]: >17}')

        d = 0
        for c, p in enumerate(lista):
            d += 1
        linhas_divisorias()
        print(f'A quantidade de produtos cadastradas é de {d}')

        linhas_divisorias()
        try:
            opc = input('Digite [M para mostrar mais / S para sair]: ').upper()
            if opc == 'S':
                break
            elif opc == 'M':
                pagina += 1
            else:
                print('\033[031mOpção inválida.\033[m.')
        except ValueError:
            print('\033[031mDigite somente números\033[m.')


def linhas_divisorias():
    print('=' * 30)


def menu_principal():
    carregamento_de_dados()

    while True:
        limpar_tela()
        linhas_divisorias()
        print('Bem vindo ao Sistema WP'.center(30))
        linhas_divisorias()

        print('''
\033[34m[1]\033[m - Mostrar produtos
\033[34m[2]\033[m - Cadastrar produtos
\033[34m[3]\033[m - Alterar descrição
\033[34m[4]\033[m - Excluir produtos
\033[34m[5]\033[m - Buscar produtos
\033[34m[6]\033[m - Alterar preços
\033[34m[7]\033[m - Sair do sistema
        ''')
        try:
            escolha = int(input('Qual opção deseja realizar? '))
            if escolha not in range(1, 8):
                print('\033[31mErro, escolha um número entre 1 e 6\033[m.')
        except ValueError:
            print('\033[31mSomente números são aceitos. Tente novamente\033[m.')
            continue

        if escolha == 1:
            mostrar_produtos()
        elif escolha == 2:
            cadastrar_produto()
        elif escolha == 3:
            alterar_descri()
        elif escolha == 4:
            excluir_produtos()
        elif escolha == 5:
            buscar_produtos()
        elif escolha == 6:
            mudar_precos()
        elif escolha == 7:
            salvar_produtos()
            break


menu_principal()

linhas_divisorias()
print('Finalizando programa.'.center(30))
sleep(1)
print('Sistemas Wp'.center(30))
