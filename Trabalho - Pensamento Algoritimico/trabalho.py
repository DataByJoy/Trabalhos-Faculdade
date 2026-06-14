import os
import csv

class Imovel:
    def __init__(self, tipo, aluguel, maximo_parcelas):
        self.tipo = tipo
        self.aluguel = aluguel
        self.maximo_parcelas = maximo_parcelas

    def __str__(self):
        nomes_chaves = {
            'tipo': 'Tipo',
            'aluguel': 'Valor do Aluguel Base',
            'parcelas_selecionadas': 'Parcelas Selecionadas',
            'quartos': 'Quantidade de Quartos',
            'vaga_garagem': 'Vagas de Garagem',
            'filho': 'Possui Filhos'
        }
        
        linhas = []
        for chave, valor in self.__dict__.items():
            if chave == 'maximo_parcelas':
                continue
                
            if isinstance(valor, bool):
                valor = "Sim" if valor else "Não"
            
            nome_exibicao = nomes_chaves.get(chave, chave.capitalize())
            linhas.append(f"{nome_exibicao}: {valor}")
            
        return "\n".join(linhas)

class Apartamento(Imovel):
    def __init__(self, quartos, vaga_garagem, child):
        super().__init__('Apartamento', 700, 5)
        self.quartos = quartos
        self.vaga_garagem = vaga_garagem
        self.filho = child

    def valor_aluguel(self):
        total = self.aluguel
        especificacoes = [f'Valor base: R$ {self.aluguel:.2f}']

        if self.quartos == 2:
            total += 200
            especificacoes.append('Acréscimo 2º quarto: R$ 200,00')

        if self.vaga_garagem:
            total += 300
            especificacoes.append('Vaga de garagem: R$ 300,00')

        if not self.filho:
            desconto = total * 0.05
            total -= desconto
            especificacoes.append(f'Desconto por não ter filhos (5%): -R$ {desconto:.2f}')

        return {'total': total, 'especificacoes': especificacoes}

class Casa(Imovel):
    def __init__(self, quartos, vaga_garagem):
        super().__init__('Casa', 900, 5)
        self.quartos = quartos
        self.vaga_garagem = vaga_garagem

    def valor_aluguel(self):
        total = self.aluguel
        especificacoes = [f'Valor base: R$ {self.aluguel:.2f}']

        if self.quartos == 2:
            total += 250
            especificacoes.append('Acréscimo 2º quarto: R$ 250,00')

        if self.vaga_garagem:
            total += 300
            especificacoes.append('Vaga de garagem: R$ 300,00')

        return {'total': total, 'especificacoes': especificacoes}

class Estudio(Imovel):
    def __init__(self, vaga_garagem):
        super().__init__('Estudio', 1200, 5)
        self.vaga_garagem = vaga_garagem

    def valor_aluguel(self):
        total = self.aluguel
        especificacoes = [f'Valor base: R$ {self.aluguel:.2f}']

        if self.vaga_garagem > 0:
            total += 250
            especificacoes.append('Até 2 vagas de garagem: R$ 250,00')

        if self.vaga_garagem > 2:
            adicional_vaga = self.vaga_garagem - 2
            valor_extra = adicional_vaga * 60
            total += valor_extra
            especificacoes.append(f'{adicional_vaga} vagas extras: R$ {valor_extra:.2f}')

        return {'total': total, 'especificacoes': especificacoes}
    
class Orcamento(Imovel):
    def __init__(self, imovel, maximo_parcelas):
        self.imovel = imovel
        self.maximo_parcelas = min(maximo_parcelas, 5)
        self.valor_contrato = 2000

    def resumo(self):
        dados_aluguel = self.imovel.valor_aluguel()
        valor_parcela = self.valor_contrato / self.maximo_parcelas

        return {
            "Aluguel": dados_aluguel,
            "Valor da parcela": valor_parcela,
            "Quantidade de parcelas": self.maximo_parcelas
        }

    def __str__(self):
        dados = self.resumo()
        aluguel_info = dados["Aluguel"]
        
        aluguel_fixo = aluguel_info['total']
        valor_parcela = dados['Valor da parcela']
        qtd_parcelas = dados['Quantidade de parcelas']
        
        linhas = [
            "                                        ",
            "          RESUMO DO ORÇAMENTO           ",
            "----------------------------------------",
            f"{str(self.imovel)}",
            "========================================",
            "COMPOSIÇÃO DO ALUGUEL:",
        ]
        
        for item in aluguel_info["especificacoes"]:
            linhas.append(f" • {item}")
            
        linhas.extend([
            f"  > Total do Aluguel: R$ {aluguel_fixo:.2f}",
            "========================================",
            "PAGAMENTO DO CONTRATO:",
            f" • Valor do Contrato: R$ {self.valor_contrato:.2f}",
            f" • Parcelamento: {qtd_parcelas}x de R$ {valor_parcela:.2f}",
            "----------------------------------------",
            "PROJEÇÃO DE PAGAMENTO (12 MESES):",
            "----------------------------------------"
        ])
        
        for mes in range(1, 13):
            if mes <= qtd_parcelas:
                valor_mes = aluguel_fixo + valor_parcela
                detalhe = "(Aluguel + Contrato)"
            else:
                valor_mes = aluguel_fixo
                detalhe = "(Apenas Aluguel)"
                
            linhas.append(f" Mês {mes:02d} | R$ {valor_mes:8.2f}  {detalhe}")

        linhas.extend([
            "========================================",
            "                                        "
        ])
        return "\n".join(linhas)

def gerar_csv_orcamento(orcamento):
    dados = orcamento.resumo()
    valor_aluguel = dados["Aluguel"]["total"]
    valor_parcela = dados["Valor da parcela"]
    qtd_parcelas = dados["Quantidade de parcelas"]
    nome_arquivo = "orcamento_gerado.csv"

    # utf-8-sig para o Excel ler os acentos
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8-sig') as arquivo:
        escritor = csv.writer(arquivo, delimiter=';')
        escritor.writerow(['Mês', 'Valor Aluguel', 'Parcela Contrato', 'Total do Mês'])
        
        for mes in range(1, 13):
            if mes <= qtd_parcelas:
                total_mes = valor_aluguel + valor_parcela
                escritor.writerow([mes, f"R$ {valor_aluguel:.2f}", f"R$ {valor_parcela:.2f}", f"R$ {total_mes:.2f}"])
            else:
                total_mes = valor_aluguel
                escritor.writerow([mes, f"R$ {valor_aluguel:.2f}", "R$ 0.00", f"R$ {total_mes:.2f}"])
                
    print(f"\n[SUCESSO] Arquivo '{nome_arquivo}' salvo na pasta atual!")

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def encerrar_sistema():
    limpar_terminal()
    print("Sistema encerrado.")
    print("R.M IMÓVEIS Agradece pela confiança!")

def sanitizacao_resposta(pergunta):
    while True:
        resposta = input(pergunta).strip().upper()
        if resposta in ['S', 'N']:
            return resposta == 'S'
        print("Entrada inválida. Digite apenas 'S' para Sim ou 'N' para Não.")

def iniciar_sistema():
    while True:
        limpar_terminal()
        print("---------------------------------------")
        print("R.M IMÓVEIS - Obrigado pela preferência")
        print("---------------------------------------")
        print("Selecione o tipo de imóvel:")
        print("1 - Apartamento")
        print("2 - Casa")
        print("3 - Estúdio")
        print("0 - Sair")
        print("---------------------------------------")
        
        opcao = input("Opção desejada: ").strip()
        
        if opcao == '0':
            encerrar_sistema()
            break
            
        if opcao not in ['1', '2', '3']:
            input("\nOpção inválida. Pressione [ENTER] para tentar novamente.")
            continue

        try:
            print("----------------------------------------")
            if opcao == '1':
                while True:
                    quartos = int(input("Quantidade de quartos (1 ou 2): "))
                    if quartos in [1, 2]:
                        break
                    print("Opção inválida. Trabalhamos apenas com opções de 1 ou 2 quartos para este imóvel.")
                
                vagas = sanitizacao_resposta("Possui vaga de garagem? (S/N): ")
                tem_filhos = sanitizacao_resposta("Possui filhos? (S/N): ")
                imovel_selecionado = Apartamento(quartos, vagas, tem_filhos)

            elif opcao == '2':
                # Loop para garantir 1 ou 2 quartos
                while True:
                    quartos = int(input("Quantidade de quartos (1 ou 2): "))
                    if quartos in [1, 2]:
                        break
                    print("Opção inválida. A R.M Imóveis trabalha apenas com opções de 1 ou 2 quartos para este imóvel.")
                    
                vagas = sanitizacao_resposta("Possui vaga de garagem? (S/N): ")
                imovel_selecionado = Casa(quartos, vagas)

            elif opcao == '3':
                vagas = int(input("Quantidade de vagas de garagem (0 para nenhuma): "))
                imovel_selecionado = Estudio(vagas)

            print("----------------------------------------")
            
            # Loop de validação das parcelas (1 a 5)
            while True:
                parcelas = int(input("Parcelamento do contrato (1 a 5 vezes): "))
                if 1 <= parcelas <= 5:
                    break
                print("Opção inválida. Temos opções de parcelamento apenas em 1, 2, 3, 4 ou 5 vezes.")
            
            orcamento_final = Orcamento(imovel_selecionado, parcelas)
            limpar_terminal()
            print(orcamento_final)
            
            # geração do CSV se o usuário desejar
            exportar = sanitizacao_resposta("\nDeseja gerar o orçamento em arquivo CSV? (S/N): ")
            if exportar:
                gerar_csv_orcamento(orcamento_final)
            
        except ValueError:
            input("\nErro de digitação. Utilize apenas números inteiros onde solicitado. Pressione [ENTER] para recomeçar.")
            continue
            
        continuar = sanitizacao_resposta("\nDeseja realizar uma nova simulação? (S/N): ")
        if not continuar:
            encerrar_sistema()
            break

if __name__ == "__main__":
    iniciar_sistema()