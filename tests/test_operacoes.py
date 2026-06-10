"""Testes do módulo calculadora.operacoes."""

import pytest

from calculadora import operacoes

# PONTO DE EXPANSÃO (SPEC T3, runs 07-08): a variação "aumento artificial de
# testes" é feita multiplicando os casos deste parametrize (×5 e ×10).
CASOS_SOMA = [
    (1, 2, 3),
    (-1, 1, 0),
    (0, 0, 0),
    (2.5, 2.5, 5.0),
]


@pytest.mark.parametrize(("a", "b", "esperado"), CASOS_SOMA)
def test_somar(a, b, esperado):
    assert operacoes.somar(a, b) == esperado


def test_subtrair():
    # exp(run-05): falha proposital do experimento — reverter no run-06
    assert operacoes.subtrair(10, 4) == 7


def test_multiplicar():
    assert operacoes.multiplicar(3, 7) == 21


def test_dividir():
    assert operacoes.dividir(10, 4) == 2.5


def test_dividir_por_zero():
    with pytest.raises(ZeroDivisionError):
        operacoes.dividir(1, 0)


def test_fatorial():
    assert operacoes.fatorial(5) == 120
    assert operacoes.fatorial(0) == 1


def test_fatorial_negativo():
    with pytest.raises(ValueError):
        operacoes.fatorial(-1)


def test_eh_primo_verdadeiro():
    assert operacoes.eh_primo(2)
    assert operacoes.eh_primo(17)
    assert operacoes.eh_primo(97)


def test_eh_primo_falso():
    assert not operacoes.eh_primo(1)
    assert not operacoes.eh_primo(4)
    assert not operacoes.eh_primo(91)  # 7 * 13


def test_media():
    assert operacoes.media([1, 2, 3, 4]) == 2.5


def test_media_lista_vazia():
    with pytest.raises(ValueError):
        operacoes.media([])


def test_fibonacci():
    assert operacoes.fibonacci(0) == 0
    assert operacoes.fibonacci(1) == 1
    assert operacoes.fibonacci(10) == 55


def test_fibonacci_negativo():
    with pytest.raises(ValueError):
        operacoes.fibonacci(-1)
