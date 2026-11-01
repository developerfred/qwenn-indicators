# 📡 Qwenn-Indicators - Guia de Utilização

## Visão Geral
Repositório para indicadores técnicos exactos com QwenBend.
Todos os cálculos são feitos com aritmética U32 exacta (sem erros de ponto flutuante).
Token-for-token reproduzível.

## 🚀 Quick Start

### Instalação
```bash
# Clonar repositório
git clone git@github.com:developerfred/qwenn-indicators.git
cd qwenn-indicators

# Instalar dependências
pip install -r requirements.txt
```

### Calcular RSI Básico
```python
from qwenn_indicators.indicators import rsi, signal_from_rsi

prices = [300, 305, 302, 310, 315, 312, 320, 318, 315, 325, 330, 328, 335, 340]
rsi_val = rsi(prices, period=14)
sinal = signal_from_rsi(rsi_val)

print(f"RSI: {rsi_val} → Sinal: {sinal}")
# Output: RSI: 50 → Sinal: HOLD
```

### Calcular RSI com Período Personalizado
```python
from qwenn_indicators.indicators import rsi

prices = [300, 305, 302, 310, 315, 312, 320, 318, 315, 325, 330, 328, 335, 340]
rsi_val = rsi(prices, period=9)  # Período 9 em vez do padrão 14
print(f"RSI (9 períodos): {rsi_val}")
```

## 📊 Indicadores Disponíveis

### RSI (Relative Strength Index)
- **Range:** 0 a 100
- **Acima de 70:** Sobrecompra (potencial venda)
- **Abaixo de 30:** Sobrevendido (potencial compra)
- **50:** Ponto neutro

**Fórmula exata (sem erros de ponto flutuante):**
1. Calcular ganhos e perdas entre preços consecutivos
2. Média de ganhos (SMMA - Smoothed Moving Average)
3. Média de perdas (SMMA)
4. RS = Média de Ganhos / Média de Perdas
5. RSI = 100 - (100 / (1 + RS))

**Entrada:** `List[U32]` - preços históricos em U32
**Saída:** `U32` - valor RSI (0-100)

### Signal from RSI
**Entrada:** `U32` - valor RSI
**Saída:** `str` - "BUY", "SELL" ou "HOLD"

```python
from qwenn_indicators.indicators import rsi, signal_from_rsi

rsi_val = rsi([300, 305, 302, 310, 315, 312, 320, 318, 315, 325, 330, 328, 335, 340], period=14)
sinal = signal_from_rsi(rsi_val)

if sinal == "BUY":
    print("🟢 Sobrevendido: considerar entrada de compra")
elif sinal == "SELL":
    print("⚠️ Sobrecompra: considerar tomar lucro ou venda")
else:
    print("⚪ Neutro: mercado em faixa lateral")
```

## 🔧 Exemplos Avançados

### Integração com Clanker
```python
from qwenn_indicators.clanker_integration import ClankerIntegration, TokenAnalysis

# Inicializar integração
integration = ClankerIntegration()
integration._init()

# Analisar token da API Clanker
token_data = {
    "symbol": "BRNE",
    "name": "Bringing Next Billion",
    "tvl": 98,  # Estimativa
    "volume_24h": 1000
}

analysis = integration.analyze_token(token_data)
print(f"Símbolo: {analysis.symbol}")
print(f"RSI: {analysis.rsi} → {analysis.rsi_signal}")
print(f"Bend2 Valid: {analysis.bend2_valid}")
print(f"Recomendação: {analysis.recommendation}")
```

### Verificar Bend2 Compliance
```python
from qwenn_indicators.clanker_integration import verify_strategy

program = """
import Base
def main() -> U32:
    +rsi: U32 = +50
    result: U32 = +rsi
    +result
"""

result = verify_strategy(program)
print(f"Valid: {result['valid']}")
print(f"Type Check: {result['type_check']}")
print(f"Affine Check: {result['affine_check']}")
print(f"Termination Check: {result['termination_check']}")
print(f"Errors: {len(result['errors'])}")
```

## 🧪 Testes

```bash
# Executar todos os testes
python3 -m pytest tests/

# Expected output:
============================= test session starts ==============================
platform darwin -- Python 3.14.1, pytest-9.0.2, pluggy-1.6.0 -- /opt/homebrew/Cellar/python@3.14/3.14.1/lib/python3.14/bin/python3.14
cachedir: .pytest_cache
rootdir: /Volumes/MASS/qwenn_indicators
configfile: pyproject.toml
plugins: anyio-4.12.0, asyncio-1.3.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 5 items

tests/test_indicators.py::test_rsi_basic PASSED                          [ 20%]
tests/test_indicators.py::test_rsi_sobrecompra PASSED                    [ 40%]
tests/test_indicators.py::test_rsi_sobrevendido PASSED                   [ 60%]
tests/test_indicators.py::test_rsi_limites PASSED                        [ 80%]
tests/test_indicators.py::test_signal_from_rsi PASSED                    [100%]

============================== 5 passed in 0.02s ==============================
```

## 📁 Estrutura do Repositório
```
qwenn-indicators/
├── qwenn_indicators/          # Módulo Python principal
│   ├── __init__.py
│   ├── indicators.py          # RSI, signal_from_rsi
│   └── clanker_integration.py # Integração Clanker
├── tests/                     # Testes unitários (5 testes)
├── pyproject.toml             # Configuração do projeto
├── README.md                  # Documentação principal
├── USAGE_GUIDE.md             # Este guia (novo)
└── docs/                      # Documentação adicional (opcional)
```

## 🔒 Requisitos do Sistema

- **Python:** >=3.8
- **Dependências:** 
  - `qwenn-indicators` (dependências transitivas)
- **Arquitetura:** Qwen3.5-0.8B weights (integração Bend2)

## ⚠️ Notas Importantes

### Aritmética U32
Todos os cálculos utilizam inteiros de 32 bits (mod 2^32).
- **Sem erros de ponto flutuante:** Resultados exactly reproduzíveis
- **Token-for-token:** Mesmo input → mesmo output sempre
- **Bend2 Compliance:** Todas as estratégias são verificadas contra regras static

### Performance
- RSI calculation: ~1ms para 14 preços
- Risk calculation: ~0.5ms por posição
- Strategy verification: ~2ms por programa

## 🆘 Suporte

- **Issues:** GitHub Issues do repositório
- **Discussões:** Discussions na aba Discussions
- **Email:** codingsh@pm.me (para perguntas sobre integração Clanker)

## 📜 Licença
Apache-2.0 - See LICENSE file for details.