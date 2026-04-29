import random
import sys
import time
from multiprocessing import Pool # Importa a classe Pool do módulo multiprocessing para criar um pool de processos.

# Função isolada (fora da classe/lambda) — obrigatório para multiprocessing no Windows
def calcular_pontos_no_circulo(numero_de_pontos):
    """Cada processo executa isso de forma independente, com seu próprio GIL."""
    pontos_dentro = 0 # Inicializa o contador de pontos que caem dentro do círculo.
    # O '_' indica que não nos importamos com o número da iteração atual no loop.
    # Apenas queremos que o bloco de código abaixo se repita 'numero_de_pontos' vezes.
    for _ in range(numero_de_pontos): # Loop para gerar 'numero_de_pontos' aleatórios.
        x, y = random.random(), random.random() # Gera coordenadas x e y aleatórias entre 0.0 e 1.0.
        # random.random() retorna um float no intervalo [0.0, 1.0).
        
        # Verifica se o ponto (x, y) está dentro do círculo de raio 1 centrado na origem.
        # A equação do círculo é x^2 + y^2 = r^2. Como r=1, é x^2 + y^2 <= 1.
        if x**2 + y**2 <= 1: 
            pontos_dentro += 1 # Incrementa o contador se o ponto estiver dentro do círculo.
    return pontos_dentro # Retorna o total de pontos que caíram dentro do círculo para este processo.

def calcular_pi_multiprocess(total_pontos, num_processos):
    # Calcula quantos pontos cada processo deve simular.
    pontos_por_processo = total_pontos // num_processos 
    # Cria uma lista 'tarefas' onde cada elemento é o número de pontos para um processo.
    # Inicialmente, todos os processos recebem uma parte igual.
    tarefas = [pontos_por_processo] * num_processos 

    # Ajuste para o resto da divisão no último processo
    # Se 'total_pontos' não for divisível igualmente por 'num_processos',
    # o resto é adicionado ao último processo para garantir que todos os pontos sejam simulados.
    tarefas[-1] += total_pontos % num_processos

    # Pool criado UMA vez — aqui está a separação de overhead x cálculo
    # Cria um pool de processos. O 'with' garante que o pool seja fechado corretamente.
    with Pool(processes=num_processos) as pool:
        # Mapeia a função 'calcular_pontos_no_circulo' para cada item na lista 'tarefas'.
        # Cada item de 'tarefas' (número de pontos) é passado como argumento para uma chamada
        # separada de 'calcular_pontos_no_circulo' em um processo diferente.
        # 'resultados' será uma lista contendo o retorno de cada chamada da função.
        resultados = pool.map(calcular_pontos_no_circulo, tarefas)

    total_dentro = sum(resultados) # Soma os resultados de todos os processos para obter o total de pontos dentro do círculo.
    # Calcula a aproximação de Pi. A área do círculo é Pi*r^2, a área do quadrado é (2r)^2.
    # Para um quarto de círculo em um quadrado de lado 1, a proporção é (Pi*1^2/4) / 1^2 = Pi/4.
    # Então, Pi = 4 * (pontos_dentro / total_pontos).
    return 4 * total_dentro / total_pontos 

if __name__ == '__main__':
    # Este bloco é executado apenas quando o script é chamado diretamente (não importado como módulo).
    
    # Verifica se o número correto de argumentos de linha de comando foi fornecido.
    # Espera-se: python mult_pi.py <total_pontos> <num_processos>
    if len(sys.argv) < 3:
        print("Uso: python calc_pi_mp.py <total_pontos> <num_processos>")
        sys.exit(1) # Sai do programa com código de erro se os argumentos estiverem incorretos.

    # Converte os argumentos da linha de comando para inteiros.
    total_pontos = int(sys.argv[1]) # Primeiro argumento: número total de pontos a serem simulados.
    num_processos = int(sys.argv[2]) # Segundo argumento: número de processos a serem utilizados.

    start_time = time.time() # Registra o tempo de início da execução.
    pi_estimado = calcular_pi_multiprocess(total_pontos, num_processos) # Chama a função principal para calcular Pi.
    end_time = time.time() # Registra o tempo de término da execução.

    # Imprime os resultados.
    print(f"Aproximação de π: {pi_estimado}") # Valor estimado de Pi.
    print(f"Processos utilizados: {num_processos}") # Número de processos usados.
    print(f"Tempo de execução: {end_time - start_time:.4f} segundos") # Tempo total de execução formatado para 4 casas decimais.