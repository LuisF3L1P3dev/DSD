import argparse
import random
import threading
import time


def calcular_pi_paralelo(numero_de_pontos: int, num_threads: int = 7) -> float:
    if numero_de_pontos <= 0:
        raise ValueError('O número de pontos deve ser maior que zero.')

    num_threads = min(num_threads, numero_de_pontos)
    pontos_por_thread = [numero_de_pontos // num_threads] * num_threads
    for i in range(numero_de_pontos % num_threads):
        pontos_por_thread[i] += 1

    resultados = [0] * num_threads

    def worker(thread_index: int, pontos: int) -> None:
        dentro = 0
        for _ in range(pontos):
            x = random.random()
            y = random.random()
            if x * x + y * y <= 1:
                dentro += 1
        resultados[thread_index] = dentro

    threads: list[threading.Thread] = []
    for index, pontos in enumerate(pontos_por_thread):
        thread = threading.Thread(target=worker, args=(index, pontos), daemon=True)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_dentro = sum(resultados)
    return 4 * total_dentro / numero_de_pontos


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Estima o valor de π usando Monte Carlo com threads.'
    )
    parser.add_argument('numero_de_pontos', type=int, help='Quantidade total de pontos a amostrar')
    parser.add_argument(
        '-t', '--threads',
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
