Cadastro=True
while Cadastro:

    try:
        #Dados
        cod = int(input("Digite o número do código do produto: "))
        produto = str(input("Digite o nome do produto: "))
        CP = float(input("Digite o custo do produto: "))
        CF = float(input("Digite o custo fixo/administrativo: "))
        CV = float(input("Digite o valor da taxa da comissão de vendas: "))
        IV = float(input("Digite o valor da taxa de impostos sobre a venda do produto: "))
        ML = float(input("Digite o valor da margem de lucro desejada: "))
        PV = CP/(1-((CF+CV+IV+ML)/100))

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

        #Cálculo para obter o valor da porcentagem
        CFC = (PV*CF)/100
        CVC = (PV*CV)/100
        IVC = (PV*IV)/100

        #Tabela
        print("|   CP   |   CF   |   CV   |   IV   |   ML   |      |   PV   |   Lucro   |")
        print("| ",CP," | ",CF," | ",CV," | ",IV," | ",ML," |      | ",PV," | ",classificarLucro(ML)," |")
        print("\n|Descrição                       |Valor                     |%                     |")
        print("|A. Preço de Venda               |",PV,"      |100%                  |")
        print("|B.Custo de Aquisição(Fornecedor)|",CP,"                     |",(CP*100)/PV,"                |")
        print("|C.Receita Bruta(A-B)            |",PV-CP,"     |",((PV-CP)*100)/PV,"   |")
        print("|D.Custo Fixo/Administrativo     |",CFC,"    |",(CFC*100)/PV,"                 |")
        print("|E.Comissão de Vendas            |",CVC,"    |",(CVC*100)/PV,"                 |")
        print("|F.Impostos                      |",IVC,"    |",(IV*100)/PV,"                |")
        print("|G.Outros Custos(D+E+F)          |",CFC+CVC+IVC,"                 |",((CFC+CVC+IVC)*100)/PV,"                 |")
        print("|H.Rentabilidade                 |",(PV-CP)-(CFC+CVC+IVC),"     |",(((PV-CP)-(CFC+CVC+IVC))*100)/PV,"   |")

        #Encerrar o programa ou continuar
        cont=True
        while cont:
            continuar = int(input("Deseja continuar, 1)Sim 2)Não:\n"))
            if continuar == 1:
                cont = False
                Cadastro = True
            elif continuar == 2:
                cont = False
                Cadastro = False
            else:
                cont = True
                print("Selecione uma opção válida!")
    except ValueError:
        print("Insira dados numéricos")