# Estimativa de π com Monte Carlo

> Comparação entre implementações: Single Thread, Threading e Multiprocessing

---

## 1. O Método de Monte Carlo

O Método de Monte Carlo é uma técnica estatística que usa números aleatórios para resolver problemas numéricos. A ideia central é simular um processo muitas vezes e usar a frequência dos resultados para estimar um valor.

### Como estimar π

Considere um quadrado de lado 1 e um quarto de círculo de raio 1 inscrito nele. A relação entre as áreas é:

```
Área do quarto de círculo / Área do quadrado = (π × r² / 4) / r² = π / 4
```

Se sortearmos `N` pontos aleatórios dentro do quadrado e contarmos quantos caem dentro do círculo (distância ao centro ≤ 1), podemos estimar:

```
π ≈ 4 × (pontos dentro do círculo / total de pontos)
```

Quanto maior o `N`, mais precisa é a estimativa — e mais processamento é necessário. Daí a necessidade de paralelismo.

---

## 2. O Problema do GIL no Python
<img width="1520" height="652" alt="Captura de tela 2026-04-28 230035" src="https://github.com/user-attachments/assets/6349e66b-c61d-46df-b8ef-d0fd4e58491d" />

O Python possui o **GIL (Global Interpreter Lock)**, que impede que mais de uma thread execute bytecode Python simultaneamente no mesmo processo:

- **Código CPU-bound** (cálculos puros como o nosso): threads **não** rodam em paralelo real. O GIL garante que apenas uma thread executa por vez, tornando o multithreading inútil ou até prejudicial pelo overhead de context switch.
- **Código I/O-bound** (leitura de arquivos, requisições de rede): threads funcionam bem, pois o GIL é liberado enquanto a thread aguarda I/O.

Como a estimativa de π é puramente CPU-bound, a solução ideal é `multiprocessing`, onde cada processo tem seu próprio GIL e roda em um núcleo físico diferente.

---

## 3. Comparação das Implementações

### `calc_pi.py` — Single Thread

A implementação mais simples: um único loop sequencial que sorteia todos os pontos no processo principal.

- ✅ Simples e sem overhead de criação de workers
- ✅ Ideal como baseline de comparação
- ❌ Usa apenas 1 núcleo da CPU
- ❌ Performance deteriora linearmente com o aumento de pontos

```bash
python calc_pi.py <total_pontos>
```

---

### `thread.py` — Threading

Divide o trabalho entre múltiplas threads, separando explicitamente a criação das threads do cálculo.

- ✅ Separa criação de threads (overhead) do cálculo (trabalho real) via `criar_threads()`
- ✅ Distribui tarefas por lista, sem lógica condicional no loop de criação
- ✅ Dispara todas as threads em lote para minimizar defasagem de início
- ❌ Limitado pelo GIL: sem paralelismo real para cálculos puros
- ❌ Pode ser mais lento que single thread pelo overhead de context switch

```bash
python thread.py <total_pontos> <num_threads>
```

---

### `mult_pi.py` — Multiprocessing

Utiliza processos independentes via `multiprocessing.Pool`, onde cada processo tem seu próprio GIL e roda em um núcleo real.

- ✅ Paralelismo real: cada processo roda em um núcleo diferente
- ✅ Pool criado uma única vez, eliminando overhead de criação repetida
- ✅ Speedup próximo ao número de núcleos disponíveis
- ⚠️ Requer `if __name__ == '__main__'` (obrigatório no Windows)
- ❌ Pequeno overhead de comunicação entre processos (IPC), desprezível para N grande

```bash
python mult_pi.py <total_pontos> <num_processos>
```

---

## 4. Tabela Comparativa

| Característica            | `thread.py`                   | `mult_pi.py`                      |
|---------------------------|-------------------------------|-----------------------------------|
| Biblioteca                | `threading`                   | `multiprocessing`                 |
| Paralelismo real          | ❌ Bloqueado pelo GIL          | ✅ Núcleos independentes           |
| Overhead de criação       | Baixo                         | Médio (processos pesam mais)      |
| Overhead separado?        | ✅ (`criar_threads()`)         | ✅ (Pool criado 1x)                |
| Memória compartilhada     | Sim (lista `resultados`)      | Não (IPC via retorno)             |
| Ideal para                | I/O-bound                     | CPU-bound                         |
| Speedup esperado          | Nenhum ou negativo            | Linear com núcleos                |
| Compatibilidade Windows   | Total                         | Requer `if __name__ == '__main__'`|

---

## 5. Como Executar

### Requisitos

- Python 3.8 ou superior
- Sem dependências externas (apenas biblioteca padrão)

### Benchmark sugerido

```bash
# Compare os três lado a lado com 50 milhões de pontos
python calc_pi.py 50000000
python thread.py  50000000 8
python mult_pi.py 50000000 8
```

---

## 6. Conclusão

Para cálculos puramente numéricos como a estimativa de π pelo método de Monte Carlo, o `multiprocessing` é a escolha correta no Python. O `threading`, mesmo com as otimizações de separação de overhead e start em lote, não consegue superar a limitação fundamental do GIL para trabalho CPU-bound.

A versão com `threading` tem seu valor didático: demonstra boas práticas como separação de responsabilidades, distribuição de tarefas e sincronização sem locks. Essas mesmas práticas são aplicações ideais em cenários **I/O-bound**, como scrapers, clientes de API ou leitura de múltiplos arquivos em paralelo.
