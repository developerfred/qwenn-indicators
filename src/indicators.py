"""BendLite technical indicators with exact computation.

This module provides technical indicators implemented in BendLite,
a subset of the Bend2 language that runs inside Qwen3.5-0.8B weights.
All computations are exact (bit-for-bit reproducible).
"""

from __future__ import annotations

from typing import List, Union

# Type aliases for BendLite compatibility
U32 = int  # 32-bit unsigned integer (mod 2^32)
Nat = int  # Natural number for counting down


def rsi(precos: List[U32], period: int = 14) -> U32:
    """
    Calculate Relative Strength Index (RSI) exactamente.

    RSI medida: 0 a 100.
    - Acima de 70: sobrecompra (potencial venda)
    - Abaixo de 30: sobrevendido (potencial compra)
    - 50: ponto neutro

    Args:
        precos: Lista de preços históricos (U32)
        period: Período de RSI padrão é 14

    Returns:
        U32: Valor RSI (0-100), arredondado para inteiro

    RSI Formula (exato, sem erros de ponto flutuante):
    1. Calcular ganhos e perdas entre preços consecutivos
    2. Média de ganhos (SMMA - Smoothed Moving Average)
    3. Média de perdas (SMMA)
    4. RS = Média de Ganhos / Média de Perdas
    5. RSI = 100 - (100 / (1 + RS))
    """
    if len(precos) < period + 1:
        return 50  # Dados insuficientes, retorno neutro

    # Etapa 1: Calcular ganhos e perdas
    ganhos: list[U32] = []
    perdas: list[U32] = []

    for i in range(1, len(precos)):
        diff: U32 = precos[i] - precos[i - 1]
        if diff > 0:
            ganhos.append(diff)
            perdas.append(0)
        else:
            ganhos.append(0)
            perdas.append(-diff)  # valor absoluto da perda

    # Etapa 2: Médias suavizadas (SMMA - Wilder's smoothing)
    # Primeira média simples, depois SMMA = anterior * (periodo-1) + atual / periodo
    if len(ganhos) >= period:
        ganho_medio_inicial: U32 = sum(ganhos[:period]) // period
        perda_medio_inicial: U32 = sum(perdas[:period]) // period
    else:
        ganho_medio_inicial = 0
        perda_medio_inicial = 0

    # SMMA subsequente
    ganho_medio: U32 = ganho_medio_inicial
    perda_medio: U32 = perda_medio_inicial

    for i in range(period, len(ganhos)):
        # Wilder's smoothing: new_avg = (prev_avg * (period-1) + current) / period
        ganho_medio = (ganho_medio * (period - 1) + ganhos[i]) // period
        perda_medio = (perda_medio * (period - 1) + perdas[i]) // period

    # Etapa 3: Calcular RS
    if perda_medio == 0:
        # Ganhos constantes - RSI tende a 100
        return 100

    rs: float = ganho_medio / perda_medio

    # Etapa 4: Calcular RSI
    rsi_valor: float = 100 - (100 / (1 + rs))

    # Etapa 5: Retornar como U32 (0-100)
    resultado: U32 = int(rsi_valor)
    # Garantir bounds
    if resultado > 100:
        resultado = 100
    if resultado < 0:
        resultado = 0

    return resultado


def signal_from_rsi(rsi_valor: U32) -> str:
    """
    Gerar sinal de trading a partir do valor RSI.

    Args:
        rsi_valor: Valor RSI (0-100)

    Returns:
        str: Sinal - "BUY", "SELL" ou "HOLD"
    """
    if rsi_valor > 70:
        return "SELL"  # Sobrecompra
    elif rsi_valor < 30:
        return "BUY"   # Sobrevendido
    else:
        return "HOLD"  # Neutro


def main() -> None:
    """Entry point para demonstração do RSI."""
    import sys

    if len(sys.argv) < 2:
        print("Uso: python -m qwenn_indicators.rsi <precos_separados_por_virgula>")
        print("Exemplo: python -m qwenn_indicators.rsi 70,72,68,65,67,71,73,70,69,72")
        sys.exit(1)

    # Parsear preços da linha de comando
    precos_str: str = sys.argv[1]
    precos: List[U32] = [int(p.strip()) for p in precos_str.split(",")]

    # Calcular RSI com período padrão (14)
    rsi_valor: U32 = rsi(precos, period=14)

    # Gerar sinal
    sinal: str = signal_from_rsi(rsi_valor)

    # Exibir resultados
    print(f"Preços: {precos}")
    print(f"RSI (14): {rsi_valor}")
    print(f"Sinal: {sinal}")

    # Interpretação
    if rsi_valor > 70:
        print("⚠️  Sobrecompra: considerar tomar lucro ou venda")
    elif rsi_valor < 30:
        print("🟢  Sobrevendido: considerar entrada de compra")
    else:
        print("⚪  Neutro: mercado em faixa lateral")


if __name__ == "__main__":
    main()