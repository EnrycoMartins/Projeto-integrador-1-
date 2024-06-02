from mysql.connector import connect
connection = connect(
    host  = "localhost",
    port = 3306,
    user = "root",
    password = "Dotedote7!@",
    database = "projint"
)
if connection.is_connected() != True:
    print("Banco não conectado")

cursor = connection.cursor()

#Funções

def inicio():
    print("+-------------------------------------------------------------+")
    print("|              BEM-VINDO AO QUALIFICADOR DE PV                |")
    print("+-------------------------------------------------------------+")
    print("MENU")

def MostrarTabela():
    cursor.execute('''SELECT * FROM projint.estoque;''')
    resultado = cursor.fetchall()
    return resultado

def umTexto (solicitacao, mensagem, valido):
    digitouDireito=False
    while not digitouDireito:
        txt=input(solicitacao)

        if txt not in valido:
            print(mensagem,'- Favor redigitar...')
        else:
            digitouDireito=True

    return txt

def opcaoEscolhida (menu):
    print ()

    opcoesValidas=[]
    posicao=0
    while posicao<len(menu):
        print (posicao+1,') ',menu[posicao],sep='')
        opcoesValidas.append(str(posicao+1))
        posicao+=1

    print()
    return umTexto('Qual é a sua opção? ', 'Opção inválida', opcoesValidas)

def ProcurarCod(connection, cod):
    try:
        cursor = connection.cursor()
        select = "SELECT * FROM Estoque WHERE cod = %s"
        cursor.execute(select, (cod,))
        achou = cursor.fetchone()
        return achou
    except OSError as e:
        print(f"Erro ao buscar o cod: {e}")
        return None



Cadastro=True
while Cadastro:
    #Cálculo para obter a classificação do lucro
    def classificarLucro(ML):
            if ML < 0:
                return "Prejuízo"
            elif ML == 0:
                return "Equilíbrio"
            elif ML > 0 and ML <= 10:
                return "Lucro Baixo"
            elif ML > 10 and ML <= 20:
                return "Lucro Médio"
            else:
                return "Alto"
    try:
        #Dados
        def Inserir():
            cod = int(input("Digite o número do código do produto: "))
            produto = str(input("Digite o nome do produto: "))
            descricao = str(input("Digite a decrição do produto: "))
            CP = float(input("Digite o custo do produto: "))
            CF = float(input("Digite o custo fixo/administrativo: "))
            CV = float(input("Digite o valor da taxa da comissão de vendas: "))
            IV = float(input("Digite o valor da taxa de impostos sobre a venda do produto: "))
            ML = float(input("Digite o valor da margem de lucro desejada: "))
            PV = CP/(1-((CF+CV+IV+ML)/100))
            insert = '''INSERT INTO Estoque (cod, nome, descricao, CP, CF, CV, IV, ML)VALUES 
                        (%s, %s, %s, %s, %s, %s, %s, %s)'''
            dados = (cod, produto, descricao, CP, CF, CV, IV, ML)
            cursor.execute(insert, dados)
            connection.commit()

            #Cálculo para obter o valor da porcentagem
            CFC = (PV*CF)/100
            CVC = (PV*CV)/100
            IVC = (PV*IV)/100
            

            #Tabela
            print("|   CP   |   CF   |   CV   |   IV   |   ML   |      |   PV   |   Lucro   |")
            print("| ",round(CP, 2)," | ",round(CF, 2)," | ",round(CV, 2)," | ",round(IV, 2)," | ",round(ML, 2)," |      | ",round(PV,2)," | ",classificarLucro(ML)," |")
            print("\n|Descrição                       |Valor     |%       |")
            print("|A. Preço de Venda               |",round(PV, 2),"   |100%    |")
            print("|B.Custo de Aquisição(Fornecedor)|",round(CP, 2),"    |",round(((CP*100)/PV), 2),"  |")
            print("|C.Receita Bruta(A-B)            |",round((PV-CP), 2),"    |",round((((PV-CP)*100)/PV), 2),"  |")
            print("|D.Custo Fixo/Administrativo     |",round(CFC, 2),"    |",round(((CFC*100)/PV), 2),"  |")
            print("|E.Comissão de Vendas            |",round(CVC, 2),"    |",round(((CVC*100)/PV), 2),"  |")
            print("|F.Impostos                      |",round(IVC, 2),"    |",round(((IVC*100)/PV), 2),"  |")
            print("|G.Outros Custos(D+E+F)          |",round((CFC+CVC+IVC), 2),"     |",round((((CFC+CVC+IVC)*100)/PV), 2),"  |")
            print("|H.Rentabilidade                 |",round(((PV-CP)-(CFC+CVC+IVC)), 2),"    |",round(((((PV-CP)-(CFC+CVC+IVC))*100)/PV), 2),"  |")

            print(cursor.rowcount, "Registro(s) inseridos com sucesso!")

        def Atualizar():
            try:
                cod = int(input("Insira o código do produto que deseja atualizar: "))
            except ValueError:
                print("ID inválido. Tente novamente.")
                return
            
            produto = ProcurarCod(connection, cod)
            if produto is None:
                print(f"Nenhum produto encontrado com o codigo {cod}")
                return
            
            produto = list(produto)

            print(f"Produto encontrado: Codigo - {produto[0]}, Produto - {produto[1]}, Descrição - {produto[2]}, CP - {produto[3]}, CF - {produto[4]}, CV - {produto[5]}, IV - {produto[6]}, ML - {produto[7]}")
            if produto:
                escolha =['Atualizar código',\
                          'Atualizar nome',\
                          'Atualizar descrição',\
                          'Atualizar CP',\
                          'Atualizar CF',\
                          'Atualizar CV',\
                          'Atualizar IV',\
                          'Atualizar ML',\
                          'Finalizar as atualizações']
                opcao = 0
                while opcao != 9:
                    opcao = int(opcaoEscolhida(escolha)) 
                    if opcao == 1:
                        try:
                            codigo = int(input("Digite o novo código: "))
                        except ValueError:
                            print("Digite um código válido")
                        produto[0] = codigo
                    elif opcao == 2:
                        nome = input("Digite o novo nome: ")
                        produto[1] = nome
                    elif opcao == 3:
                        descricao = input("Digite a nova descrição: ")
                        produto[2] = descricao
                    elif opcao == 4:
                        try:
                            CP = int(input("Digite o novo CP: "))
                        except ValueError:
                            print("Digite um valor válido")
                        produto[3] = CP
                    elif opcao == 5:
                        try:
                            CF = int(input("Digite o novo CF: "))
                        except ValueError:
                            print("Digite um valor válido")
                        produto[4] = CF
                    elif opcao == 6:
                        try:
                            CV = int(input("Digite o novo CV: "))
                        except ValueError:
                            print("Digite um valor válido")
                        produto[5] = CV
                    elif opcao == 7:
                        try:
                            IV = int(input("Digite o novo IV: "))
                        except ValueError:
                            print("Digite um valor válido")
                        produto[6] = IV
                    elif opcao == 8:
                        try:
                            ML = int(input("Digite a nova ML: "))
                        except ValueError:
                            print("Digite um valor válido")
                        produto[7] = ML
            
            Update = '''UPDATE Estoque 
                        SET cod = %s, nome = %s, descricao = %s, CP = %s, CF = %s, CV = %s, IV = %s, ML = %s
                        WHERE cod = %s'''
            dados = (produto[0], produto[1], produto[2], produto[3], produto[4], produto[5], produto[6], produto[7], produto[0])

            cursor = connection.cursor()
            try:
                cursor.execute(Update, dados)
                connection.commit()
                print("registro atualizado com sucesso")
            except OSError as e:
                print(f"Erro ao atualizar os dados: {e}")

        def Excluir():
            try:
                cod = int(input("Digite o código do produto que deseja excluir: "))
            except ValueError:
                print("Código inválido")
                return
            
            produto = ProcurarCod(connection, cod)
            if produto is None:
                print(f"Nenhum produto encontrado com o código {cod}")
                return
            
            print(f"Produto encontrado: Codigo - {produto[0]}, Produto - {produto[1]}, Descrição - {produto[2]}, CP - {produto[3]}, CF - {produto[4]}, CV - {produto[5]}, IV - {produto[6]}, ML - {produto[7]}")

            confirmacao = input("Tem certeza que deseja excluir este produto? (s/n): ")
            if confirmacao.lower() != 's':
                print("Exclusão cancelada")
                return
            
            Delete = '''DELETE FROM Estoque
                        WHERE cod = %s'''
            cursor = connection.cursor()
            try:
                cursor.execute(Delete, (cod,))
                connection.commit()
                print("Produto excluído")
            except OSError as e:
                print(f"Erro ao excluir o produto: {e}")

        def Classificar():
            try:
                cod = int(input("Digite o código do produto que deseja excluir: "))
            except ValueError:
                print("Código inválido")
                return
                    
            produto = ProcurarCod(connection, cod)
            if produto is None:
                print(f"Nenhum produto encontrado com o código {cod}")
                return
                    
            print(f"Produto encontrado: Codigo - {produto[0]}, Produto - {produto[1]}, Descrição - {produto[2]}, CP - {produto[3]}, CF - {produto[4]}, CV - {produto[5]}, IV - {produto[6]}, ML - {produto[7]}")

            PV = produto[3]/(1-((produto[4]+produto[5]+produto[6]+produto[7])/100))
            CFC = (PV*produto[4])/100
            CVC = (PV*produto[5])/100
            IVC = (PV*produto[6])/100
            print(produto[0], produto[1], produto[2])
            print("|   CP   |   CF   |   CV   |   IV   |   ML   |      |   PV   |   Lucro   |")
            print("| ",produto[3]," | ",produto[4]," | ",produto[5]," | ",produto[6]," | ",produto[7]," |      | ",round(PV,2)," | ",classificarLucro(produto[7])," |")
            print("\n|Descrição                       |Valor     |%       |")
            print("|A. Preço de Venda               |",round(PV, 2),"   |100%    |")
            print("|B.Custo de Aquisição(Fornecedor)|",produto[3],"    |",round(((produto[3]*100)/PV), 2),"  |")
            print("|C.Receita Bruta(A-B)            |",round((PV-produto[3]), 2),"    |",round((((PV-produto[3])*100)/PV), 2),"  |")
            print("|D.Custo Fixo/Administrativo     |",round(CFC, 2),"    |",round(((CFC*100)/PV), 2),"  |")
            print("|E.Comissão de Vendas            |",round(CVC, 2),"    |",round(((CVC*100)/PV), 2),"  |")
            print("|F.Impostos                      |",round(IVC, 2),"    |",round(((IVC*100)/PV), 2),"  |")
            print("|G.Outros Custos(D+E+F)          |",round((CFC+CVC+IVC), 2),"     |",round((((CFC+CVC+IVC)*100)/PV), 2),"  |")
            print("|H.Rentabilidade                 |",round(((PV-produto[3])-(CFC+CVC+IVC)), 2),"    |",round(((((PV-produto[3])-(CFC+CVC+IVC))*100)/PV), 2),"  |\n")


        def Listar():
            valor = MostrarTabela()
            for todos in valor:
                PV = todos[3]/(1-((todos[4]+todos[5]+todos[6]+todos[7])/100))
                CFC = (PV*todos[4])/100
                CVC = (PV*todos[5])/100
                IVC = (PV*todos[6])/100
                print(todos[0], todos[1], todos[2])
                print("|   CP   |   CF   |   CV   |   IV   |   ML   |      |   PV   |   Lucro   |")
                print("| ",todos[3]," | ",todos[4]," | ",todos[5]," | ",todos[6]," | ",todos[7]," |      | ",round(PV,2)," | ",classificarLucro(todos[7])," |")
                print("\n|Descrição                       |Valor     |%       |")
                print("|A. Preço de Venda               |",round(PV, 2),"   |100%    |")
                print("|B.Custo de Aquisição(Fornecedor)|",todos[3],"    |",round(((todos[3]*100)/PV), 2),"  |")
                print("|C.Receita Bruta(A-B)            |",round((PV-todos[3]), 2),"    |",round((((PV-todos[3])*100)/PV), 2),"  |")
                print("|D.Custo Fixo/Administrativo     |",round(CFC, 2),"    |",round(((CFC*100)/PV), 2),"  |")
                print("|E.Comissão de Vendas            |",round(CVC, 2),"    |",round(((CVC*100)/PV), 2),"  |")
                print("|F.Impostos                      |",round(IVC, 2),"    |",round(((IVC*100)/PV), 2),"  |")
                print("|G.Outros Custos(D+E+F)          |",round((CFC+CVC+IVC), 2),"     |",round((((CFC+CVC+IVC)*100)/PV), 2),"  |")
                print("|H.Rentabilidade                 |",round(((PV-todos[3])-(CFC+CVC+IVC)), 2),"    |",round(((((PV-todos[3])-(CFC+CVC+IVC))*100)/PV), 2),"  |\n")

    except ValueError:
        print("Insira dados numéricos")
        
#Encerrar o programa ou continuar

    inicio()

    menu = ['Incluir produto',\
            'Atualizar produtos',\
            'Excluir produtos',\
            'Classificar lucros',\
            'Listar produtos',\
            'Sair do Programa']
        
    opcao = 0
    while opcao != 6:
        opcao = int(opcaoEscolhida(menu)) 
        if opcao == 1:
            Inserir()
        elif opcao == 2:
            Atualizar()
        elif opcao == 3:
            Excluir()
        elif opcao == 4:
            Classificar()
        elif opcao == 5:
            Listar()
        elif opcao ==6:
            Cadastro = False
                
    