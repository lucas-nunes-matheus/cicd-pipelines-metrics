"""Operações matemáticas simples usadas como carga de teste do pipeline."""


def somar(a: float, b: float) -> float:
    """Retorna a soma de a e b."""
    return a + b


def subtrair(a: float, b: float) -> float:
    """Retorna a diferença entre a e b."""
    return a - b


def multiplicar(a: float, b: float) -> float:
    """Retorna o produto de a e b."""
    return a * b


def dividir(a: float, b: float) -> float:
    """Retorna a divisão de a por b.

    Levanta ZeroDivisionError com mensagem clara quando b == 0.
    """
    if b == 0:
        raise ZeroDivisionError("divisão por zero não é permitida")
    return a / b


def fatorial(n: int) -> int:
    """Retorna n! para n >= 0.

    Levanta ValueError para n negativo.
    """
    if n < 0:
        raise ValueError("fatorial não é definido para números negativos")
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado


def eh_primo(n: int) -> bool:
    """Retorna True se n é um número primo."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def media(valores: list[float]) -> float:
    """Retorna a média aritmética de uma lista não vazia.

    Levanta ValueError para lista vazia.
    """
    if not valores:
        raise ValueError("não é possível calcular a média de uma lista vazia")
    return sum(valores) / len(valores)


def fibonacci(n: int) -> int:
    """Retorna o n-ésimo número de Fibonacci (fib(0) = 0, fib(1) = 1).

    Levanta ValueError para n negativo.
    """
    if n < 0:
        raise ValueError("fibonacci não é definido para índices negativos")
    anterior, atual = 0, 1
    for _ in range(n):
        anterior, atual = atual, anterior + atual
    return anterior
