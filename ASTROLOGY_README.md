# Bitcoin Financial Astrology Web App

A sophisticated web application that analyzes planetary aspects to Bitcoin's natal chart using pure mathematical calculations based on Kepler's equations.

## Features

- **Real-time Planetary Positions**: Calculates current positions of all planets using astronomical orbital mechanics
- **Bitcoin Natal Chart**: Based on Genesis Block (January 3, 2009, 18:15:05 UTC)
- **Aspect Analysis**:
  - Malefic Aspects: Square, Opposition, Conjunction with Mars/Saturn
  - Benefic Aspects: Trine, Sextile, Conjunction with Jupiter/Venus
- **Special Indicators**:
  - Mercury Retrograde Detection
  - Mars-Uranus Hard Aspect Detection
- **Transit Forecasting**: Predicts major transits for the next 30 days
- **Beautiful UI**: Cosmic-themed, responsive design with zodiac wheel visualization

## Installation

No external dependencies required! Uses only Python standard library.

```bash
# Make scripts executable
chmod +x astro_calc.py server.py
```

## Usage

### Option 1: Command Line Analysis

Run the calculator directly to see a detailed terminal output:

```bash
python3 astro_calc.py
```

This will display:
- Current malefic and benefic aspect counts
- Mercury status (Retrograde/Direct)
- Mars-Uranus hard aspect status
- All current planetary positions
- Bitcoin's natal positions
- All aspects to natal chart
- Upcoming major transits

### Option 2: Web Interface

Start the web server:

```bash
python3 server.py
```

Then open in your browser:
```
http://localhost:8000/bitcoin-astrology.html
```

The web interface provides:
- Visual dashboard with key metrics
- Zodiac wheel visualization
- Interactive aspect listings
- Planetary position tables
- Upcoming transit forecasts
- Astrological interpretation

### Option 3: Standalone HTML (No Server)

Open `bitcoin-astrology.html` directly in a browser. It will use simulated demo data.

## How It Works

### Astronomical Calculations

The app uses **pure mathematical implementation** with no external APIs:

1. **Julian Date Conversion**: Converts current date/time to Julian Date (astronomical time)
2. **Orbital Elements**: Uses J2000.0 epoch orbital elements for each planet
3. **Kepler's Equation**: Solves `M = E - e·sin(E)` iteratively for eccentric anomaly
4. **True Anomaly**: Calculates actual position in orbit
5. **Ecliptic Coordinates**: Transforms to ecliptic longitude (zodiac degrees)

Accuracy: ±1° for inner planets, ±2-3° for outer planets (sufficient for astrology)

### Aspect Detection

Aspects are angular relationships between planets:

- **Conjunction** ☌ (0° ± 8°): Amplification
- **Sextile** ⚹ (60° ± 6°): Harmonious opportunity
- **Square** □ (90° ± 7°): Tension/pressure
- **Trine** △ (120° ± 8°): Strong momentum
- **Opposition** ☍ (180° ± 8°): Polarization

### Bitcoin Natal Chart

**Genesis Block Details:**
- Date: January 3, 2009
- Time: 18:15:05 UTC
- Location: 0°N, 0°E (symbolic - Bitcoin is global)

The natal chart captures planetary positions at Bitcoin's "birth" and transits are compared to these positions.

## Astrological Framework

### Planetary Forces

- ☉ **Sun** - Core vitality, major directional shifts
- ☽ **Moon** - Emotional swings, liquidity tides
- ☿ **Mercury** - Trade flow, market sentiment
- ♀ **Venus** - Value attraction, capital flows
- ♂ **Mars** - Volatility, momentum surges
- ♃ **Jupiter** - Expansion, risk-on appetite
- ♄ **Saturn** - Contraction, regulation
- ♅ **Uranus** - Sudden shocks, disruption
- ♆ **Neptune** - Speculation, confusion
- ♇ **Pluto** - Deep transformation cycles

### Malefic vs Benefic

**Malefic Aspects** (bearish pressure):
- Mars/Saturn forming hard aspects (Square, Opposition, Conjunction)
- Indicates resistance, volatility, corrective pressure

**Benefic Aspects** (bullish support):
- Jupiter/Venus forming harmonious aspects (Trine, Sextile, Conjunction)
- Indicates growth potential, value appreciation

### Special Indicators

**Mercury Retrograde**:
- Occurs ~3 times/year for ~3 weeks
- Associated with: communication failures, technical issues, false signals
- Risk: Increased market confusion

**Mars-Uranus Hard Aspect**:
- Explosive combination
- Mars (aggression) + Uranus (sudden change)
- Indicates: High volatility, unexpected price movements

## File Structure

```
crypto-screener/
├── astro_calc.py              # Core calculation engine
├── bitcoin-astrology.html     # Web interface
├── server.py                  # Local web server
└── ASTROLOGY_README.md        # This file
```

## Technical Details

### Kepler's Equation Solver

The Newton-Raphson iterative method is used:

```
E(n+1) = E(n) - (E - e·sin(E) - M) / (1 - e·cos(E))
```

Converges to ±1e-6 radians in <30 iterations.

### Retrograde Detection

Compares planetary longitude at time T and T+1 day:
- If longitude decreases → Retrograde
- If longitude increases → Direct

### Aspect Calculation

For each transiting planet and natal position:
1. Calculate angular difference
2. Normalize to 0-180° range
3. Check if matches aspect angle ± orb
4. Record aspect with exact orb

## Limitations

1. **Simplified Calculations**: Does not account for:
   - Nutation and precession (tiny effects)
   - Gravitational perturbations (small effects)
   - Full 3D orbital mechanics (mostly 2D ecliptic)

2. **No Ascendant/Houses**: True natal chart requires birth location for house cusps. Bitcoin's "location" is global/symbolic.

3. **Tropical Zodiac**: Uses tropical (seasonal) zodiac, not sidereal (constellation-based).

## Disclaimer

This tool is for **entertainment and research purposes only**. Financial astrology is **not a substitute for proper financial analysis**. Always conduct your own research and consult financial professionals before making investment decisions.

## Future Enhancements

- [ ] Add CSV ephemeris data integration for higher precision
- [ ] Include lunar phases and eclipse detection
- [ ] Add asteroid aspects (Chiron, Juno, Vesta, etc.)
- [ ] Historical backtesting of aspects vs. price movements
- [ ] Support for custom natal charts (altcoins)
- [ ] Vedic/Sidereal zodiac option
- [ ] Arabic parts and midpoints
- [ ] Harmonic aspects (quintile, septile, etc.)

## Credits

Created using:
- Pure Python 3 (no external dependencies)
- Kepler's laws of planetary motion
- VSOP87 orbital element tables
- Traditional astrological aspect theory

## License

Open source - use freely for educational and research purposes.

---

**Note**: The universe doesn't care about your portfolio, but the planets might be worth watching! 🌟🪐📈
