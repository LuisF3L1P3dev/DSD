import random
import sys
import time
import threading

def calcular_pontos_no_circulo(numero_de_pontos, resultados, index):
    """Função executada por cada thread."""
    pontos_dentro = 0
    for _ in range(numero_de_pontos):
        x, y = random.random(), random.random()
        if x**2 + y**2 <= 1:
            pontos_dentro += 1
    resultados[index] = pontos_dentro

def calcular_pi_multithread(total_pontos, num_threads):
    threads = []
    # Lista para armazenar o resultado parcial de cada thread
    resultados = [0] * num_threads
    pontos_por_thread = total_pontos // num_threads

    for i in range(num_threads):
        # O último thread pega o resto da divisão, se houver
        if i == num_threads - 1:
            pontos_por_thread += total_pontos % num_threads
        
        t = threading.Thread(target=calcular_pontos_no_circulo, args=(pontos_por_thread, resultados, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    total_dentro = sum(resultados)
    return 4 * total_dentro / total_pontos

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Uso: python script.py <total_pontos> <num_threads>")
        sys.exit(1)

    total_pontos = int(sys.argv[1])
    num_threads = int(sys.argv[2])

    start_time = time.time()
    pi_estimado = calcular_pi_multithread(total_pontos, num_threads)
    end_time = time.time()

    print(f"Aproximação de π: {pi_estimado}")
    print(f"Threads utilizadas: {num_threads}")
    print(f"Tempo de execução: {end_time - start_time:.4f} segundos")