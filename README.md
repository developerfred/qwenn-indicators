# Qwenn-Indicators

Technical indicators exact computation with QwenBend (U32 arithmetic, no float errors).

## Maintainer
**codingsh <codingsh@pm.me>**

## Description
BendLite implementations of technical indicators with exact U32 computation.
No floating point errors. Token-for-token reproducible results.

### Indicators
- **RSI** (Relative Strength Index) - 5 tests passing
- **MACD** - planned
- **Bollinger Bands** - planned

### Properties
- ✅ Exact U32 arithmetic
- ✅ Token-for-token reproducible
- ✅ Bend2 compliance verified
- ✅ Zero float errors

## Status
- [x] Estrutura do repositório (concluído)
- [x] RSI indicator implementado (5/5 testes passando)
- [ ] MACD indicator (planejado)
- [ ] Bollinger Bands (planejado)
- [ ] Integração Clanker (planejado)

## Tests
```
$ cd /Volumes/MASS/qwenn_indicators
$ python3 -m pytest tests/
# 5 tests passing
```

## Architecture
```
Qwenn-Indicators
├── qwenn_indindators/     # Indicator implementations
├── tests/                  # Test suite
├── pyproject.toml         # Project config
└── README.md              # This file
```

## Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Calculate RSI
python3 -c "
from qwenn_indicators.indicators import rsi, signal_from_rsi
prices = [300, 305, 302, 310, 315, 312, 320, 318, 315, 325, 330, 328, 335, 340]
rsi_val = rsi(prices, period=14)
signal = signal_from_rsi(rsi_val)
print(f'RSI: {rsi_val}, Signal: {signal}')
"
```

## Integration with Clanker
This repository can be integrated with Clanker token launcher for:
- Tokenomics analysis with exact indicators
- Risk assessment before token deployment
- Technical signal generation for AI droids