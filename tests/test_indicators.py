"""Tests for Qwenn-Indicators RSI implementation."""

from qwenn_indicators.indicators import rsi, signal_from_rsi


def test_rsi_basic():
    """Test RSI with basic price series."""
    # Preços apenas subindo -> RSI deve ser alto (sobrecompra)
    precos_subida = [50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64]
    rsi_valor = rsi(precos_subida, period=14)
    assert rsi_valor > 50, f"RSI em tendência de alta deveria ser > 50, got {rsi_valor}"

    # Preços apenas caindo -> RSI deve ser baixo (sobrevendido)
    precos_queda = [64, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 50]
    rsi_valor_baixo = rsi(precos_queda, period=14)
    assert rsi_valor_baixo < 50, f"RSI em tendência de baixa deveria ser < 50, got {rsi_valor_baixo}"

    # Preços laterais (sem variação) -> RSI = 50 (neutro)
    precos_laterais = [55] * 20
    rsi_lateral = rsi(precos_laterais, period=14)
    assert rsi_lateral == 50, f"RSI em preços constantes deveria ser 50, got {rsi_lateral}"


def test_rsi_sobrecompra():
    """Test RSI em cenário de sobrecompra."""
    # Preços fortes de alta
    precos_alta = [
        100, 102, 101, 103, 105, 104, 106, 108, 107, 109,
        110, 111, 112, 113, 114, 115, 116, 117, 118, 119
    ]
    rsi_valor = rsi(precos_alta, period=14)
    assert rsi_valor > 70, f"RSI em forte alta deveria ser > 70, got {rsi_valor}"
    sinal = signal_from_rsi(rsi_valor)
    assert sinal == "SELL", f"Sinal de sobrecompra deveria ser SELL, got {sinal}"


def test_rsi_sobrevendido():
    """Test RSI em cenário de sobrevendido."""
    # Preços fortes de queda
    precos_baixa = [
        119, 118, 117, 116, 115, 114, 113, 112, 111, 110,
        109, 108, 107, 106, 105, 104, 103, 102, 101, 100
    ]
    rsi_valor = rsi(precos_baixa, period=14)
    assert rsi_valor < 30, f"RSI em forte queda deveria ser < 30, got {rsi_valor}"
    sinal = signal_from_rsi(rsi_valor)
    assert sinal == "BUY", f"Sinal de sobrevendido deveria ser BUY, got {sinal}"


def test_rsi_limites():
    """Test que RSI está sempre nos limites 0-100."""
    # Caso extremo: apenas ganhos (preços monotonamente crescentes)
    precos_apenas_ganhos = list(range(20))  # 0, 1, 2, ..., 19
    rsi_valor = rsi(precos_apenas_ganhos, period=14)
    assert 0 <= rsi_valor <= 100, f"RSI deveria estar em [0, 100], got {rsi_valor}"

    # Caso extremo: apenas perdas (preços monotonamente decrescentes)
    precos_apenas_perdas = list(range(19, -1, -1))  # 19, 18, ..., 0
    rsi_valor = rsi(precos_apenas_perdas, period=14)
    assert 0 <= rsi_valor <= 100, f"RSI deveria estar em [0, 100], got {rsi_valor}"


def test_signal_from_rsi():
    """Test função de sinal a partir de RSI."""
    # Sobrecompra: RSI >= 70
    assert signal_from_rsi(80) == "SELL"
    assert signal_from_rsi(75) == "SELL"
    assert signal_from_rsi(71) == "SELL"
    assert signal_from_rsi(70) == "SELL"  # borderline, >= 70

    # Sobrevendido: RSI <= 30
    assert signal_from_rsi(25) == "BUY"
    assert signal_from_rsi(30) == "BUY"  # borderline, <= 30
    assert signal_from_rsi(10) == "BUY"

    # Neutro: 30 < RSI < 70
    assert signal_from_rsi(50) == "HOLD"
    assert signal_from_rsi(55) == "HOLD"
    assert signal_from_rsi(31) == "HOLD"  # inside neutral range
    assert signal_from_rsi(69) == "HOLD"  # inside neutral range

    # Limites absolutos
    assert signal_from_rsi(100) == "SELL"
    assert signal_from_rsi(0) == "BUY"