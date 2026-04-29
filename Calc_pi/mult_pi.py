import random
import sys
import time
from multiprocessing import Pool

# Função isolada (fora da classe/lambda) — obrigatório para multiprocessing no Windows
def calcular_pontos_no_circulo(numero_de_pontos):
    """Cada processo executa isso de forma independente, com seu próprio GIL."""
    pontos_dentro = 0
    # O '_' indica que não nos importamos com o número da iteração atual.
    # Apenas queremos que o bloco de código abaixo se repita 'numero_de_pontos' vezes.
    for _ in range(numero_de_pontos):
        x, y = random.random(), random.random()
        if x**2 + y**2 <= 1:
            pontos_dentro += 1
    return pontos_dentro

def calcular_pi_multiprocess(total_pontos, num_processos):
    pontos_por_processo = total_pontos // num_processos
    tarefas = [pontos_por_processo] * num_processos

    # Ajuste para o resto da divisão no último processo
    tarefas[-1] += total_pontos % num_processos

    # Pool criado UMA vez — aqui está a separação de overhead x cálculo
    with Pool(processes=num_processos) as pool:
        resultados = pool.map(calcular_pontos_no_circulo, tarefas)

    total_dentro = sum(resultados)
    return 4 * total_dentro / total_pontos

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Uso: python calc_pi_mp.py <total_pontos> <num_processos>")
        sys.exit(1)

    total_pontos = int(sys.argv[1])
    num_processos = int(sys.argv[2])

    start_time = time.time()
    pi_estimado = calcular_pi_multiprocess(total_pontos, num_processos)
    end_time = time.time()

    print(f"Aproximação de π: {pi_estimado}")
    print(f"Processos utilizados: {num_processos}")
    print(f"Tempo de execução: {end_time - start_time:.4f} segundos")