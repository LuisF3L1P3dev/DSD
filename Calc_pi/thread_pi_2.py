import argparse
import random
import threading
import time


def calcular_pi_paralelo(numero_de_pontos: int, num_threads: int = 6) -> float:
    # Validação inicial: não faz sentido calcular Pi com zero ou menos pontos.
    if numero_de_pontos <= 0:
        raise ValueError('O número de pontos deve ser maior que zero.')

    # Ajuste de segurança: não cria mais threads do que o número de pontos disponíveis.
    num_threads = min(num_threads, numero_de_pontos)
    
    # Distribuição de carga: calcula a base de pontos que cada thread processará.
    pontos_por_thread = [numero_de_pontos // num_threads] * num_threads
    
    # Distribuição do resto: se a divisão não for exata, distribui o resto entre as primeiras threads.
    for i in range(numero_de_pontos % num_threads):
        pontos_por_thread[i] += 1

    # Lista compartilhada para armazenar quantos pontos "caíram" dentro do círculo em cada thread.
    resultados = [0] * num_threads

    # Função interna que define o trabalho de cada thread (Worker).
    def worker(thread_index: int, pontos: int) -> None:
        dentro = 0 # Contador local para evitar contenção de memória
        for _ in range(pontos):
            x = random.random()
            y = random.random()
            # Teorema de Pitágoras: x² + y² <= r². Como r=1, simplificamos para x² + y² <= 1.
            if x * x + y * y <= 1:
                dentro += 1
        # Cada thread escreve seu resultado em um índice exclusivo da lista 'resultados'.
        # Isso elimina a necessidade de Locks (travas), melhorando a performance.
        resultados[thread_index] = dentro

    # Lista para manter as referências dos objetos Thread.
    threads: list[threading.Thread] = []
    
    # Loop de criação e inicialização.
    for index, pontos in enumerate(pontos_por_thread):
        # Cria o objeto thread apontando para a função worker.
        # daemon=True garante que as threads fechem se o programa principal for encerrado.
        thread = threading.Thread(target=worker, args=(index, pontos), daemon=True)
        threads.append(thread)
        thread.start() # Inicia a execução da thread imediatamente.

    # Sincronização: o programa principal espera que TODAS as threads terminem antes de continuar.
    for thread in threads:
        thread.join()

    # Agregação: soma os contadores parciais de todas as threads.
    total_dentro = sum(resultados)
    
    # Fórmula de Monte Carlo: Pi ≈ 4 * (pontos_dentro / total_pontos)
    return 4 * total_dentro / numero_de_pontos


def main() -> None:
    # Configuração do parser de argumentos para permitir uso via linha de comando.
    parser = argparse.ArgumentParser(
        description='Estima o valor de π usando Monte Carlo com threads.'
    )
    parser.add_argument('numero_de_pontos', type=int, help='Quantidade total de pontos a amostrar')
    parser.add_argument(
        '-t', '--threads', # Atalho para definir o número de threads.
        type=int,
        default=4,
        help='Número de threads a utilizar (padrão: 4)'
    )
    args = parser.parse_args()

    start_time = time.time()
    pi_estimado = calcular_pi_paralelo(args.numero_de_pontos, args.threads)
    end_time = time.time()

    print(f'Aproximação de π com {args.numero_de_pontos:,} pontos e {args.threads} threads: {pi_estimado:.8f}')
    print(f'Tempo de execução: {end_time - start_time:.4f} segundos')


if __name__ == '__main__':
    main()
