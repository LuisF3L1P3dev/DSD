import random
import sys
import time
import threading

# Função que será executada por cada thread individualmente
def calcular_pontos_no_circulo(numero_de_pontos, resultados, index):
    """Simula o sorteio de pontos. 
    Não usa lock (exclusão mútua) pois cada thread escreve em uma posição única da lista 'resultados'."""
    pontos_dentro = 0 # Contador local da thread
    for _ in range(numero_de_pontos):
        # Gera coordenadas aleatórias entre 0 e 1
        x, y = random.random(), random.random()
        # Se a distância ao centro (0,0) for <= 1, o ponto está dentro do círculo
        if x**2 + y**2 <= 1:
            pontos_dentro += 1
    # Armazena o resultado final desta thread na lista compartilhada
    resultados[index] = pontos_dentro

def criar_threads(num_threads, tarefas, resultados):
    """ETAPA 1: Separação do overhead. 
    Cria os objetos Thread na memória, mas não inicia a execução."""
    threads = []
    for i, pontos in enumerate(tarefas):
        # Instancia a thread passando a função alvo e os argumentos
        t = threading.Thread(
            target=calcular_pontos_no_circulo,
            args=(pontos, resultados, i)
        )
        threads.append(t)
    return threads

def calcular_pi_multithread(total_pontos, num_threads):
    # Lista para coletar os resultados de cada thread sem conflito de escrita
    resultados = [0] * num_threads
    
    # ETAPA 2: Distribuição de tarefas por lista
    pontos_por_thread = total_pontos // num_threads
    tarefas = [pontos_por_thread] * num_threads
    # Adiciona o resto da divisão à última tarefa para não perder pontos
    tarefas[-1] += total_pontos % num_threads

    # Criação das threads (instanciação em lote)
    threads = criar_threads(num_threads, tarefas, resultados)

    # ETAPA 3: Start em lote
    # Dispara todas as threads quase simultaneamente
    for t in threads:
        t.start()
    
    # Aguarda todas as threads terminarem antes de prosseguir
    for t in threads:
        t.join()

    # Soma os resultados parciais e aplica a fórmula de Monte Carlo: (4 * pontos_dentro) / total
    return 4 * sum(resultados) / total_pontos

if __name__ == '__main__':
    # Validação básica de argumentos de linha de comando
    if len(sys.argv) < 3:
        print("Uso: python calc_pi_threads.py <total_pontos> <num_threads>")
        sys.exit(1)

    total_pontos = int(sys.argv[1])
    num_threads = int(sys.argv[2])

    # Medição do tempo total de execução
    start_time = time.time()
    pi_estimado = calcular_pi_multithread(total_pontos, num_threads)
    end_time = time.time()

    print(f"Aproximação de π: {pi_estimado}")
    print(f"Threads utilizadas: {num_threads}")
    print(f"Tempo de execução: {end_time - start_time:.4f} segundos")