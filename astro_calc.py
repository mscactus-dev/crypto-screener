#!/usr/bin/env python3
"""
Bitcoin Financial Astrology Calculator
Uses accurate ephemeris data from CSV file for planetary positions
Calculates aspects to Bitcoin's natal chart
"""

import math
import csv
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Tuple, Optional
from pathlib import Path

# ==================== CONSTANTS ====================

# Bitcoin Genesis Block (Natal Chart)
BITCOIN_GENESIS = datetime(2009, 1, 3, 18, 15, 5, tzinfo=timezone.utc)

# CSV Ephemeris file path
CSV_PATH = Path(__file__).parent / "CLAUDE Planetary Positions 2025-2035.csv"

# Aspect definitions
ASPECTS = {
    'Conjunction': (0, 8),    # 0° ± 8°
    'Sextile': (60, 6),       # 60° ± 6°
    'Square': (90, 7),        # 90° ± 7°
    'Trine': (120, 8),        # 120° ± 8°
    'Opposition': (180, 8)    # 180° ± 8°
}

MALEFIC_PLANETS = ['Mars', 'Saturn']
BENEFIC_PLANETS = ['Jupiter', 'Venus']
NATAL_POINTS = ['Sun', 'Moon']  # Simplified - in real astrology would include Ascendant

# ==================== CSV EPHEMERIS LOADER ====================

class EphemerisData:
    """Loads and interpolates planetary positions from CSV"""

    def __init__(self, csv_path: Path):
        self.data = []
        self.load_csv(csv_path)

    def load_csv(self, csv_path: Path):
        """Load ephemeris data from CSV file"""
        if not csv_path.exists():
            raise FileNotFoundError(f"Ephemeris file not found: {csv_path}")

        with open(csv_path, 'r') as f:
            # Skip the title row
            f.readline()
            reader = csv.DictReader(f)
            for row in reader:
                # Parse the date
                date_str = row['date_utc']
                dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))

                # Store data
                self.data.append({
                    'datetime': dt,
                    'jd': float(row['JD']),
                    'Sun': float(row['Sun_lon']),
                    'Moon': float(row['Moon_lon']),
                    'Mercury': float(row['Mercury_lon']),
                    'Venus': float(row['Venus_lon']),
                    'Mars': float(row['Mars_lon']),
                    'Jupiter': float(row['Jupiter_lon']),
                    'Saturn': float(row['Saturn_lon']),
                    'Uranus': float(row['Uranus_lon']),
                    'Neptune': float(row['Neptune_lon']),
                    'Ascendant': float(row['Ascendant_deg']),
                    'MC': float(row['MC_deg']),
                    'Mercury_retro': int(row['Mercury_retro']) == 1,
                    'Venus_retro': int(row['Venus_retro']) == 1,
                    'Mars_retro': int(row['Mars_retro']) == 1,
                    'Jupiter_retro': int(row['Jupiter_retro']) == 1,
                    'Saturn_retro': int(row['Saturn_retro']) == 1,
                    'Uranus_retro': int(row['Uranus_retro']) == 1,
                    'Neptune_retro': int(row['Neptune_retro']) == 1,
                })

        print(f"Loaded {len(self.data)} ephemeris entries from {csv_path.name}")

    def get_positions(self, dt: datetime) -> Optional[Dict]:
        """Get planetary positions for a given datetime (with interpolation)"""
        if not self.data:
            return None

        # Check if date is in range
        if dt < self.data[0]['datetime'] or dt > self.data[-1]['datetime']:
            print(f"Warning: Date {dt} is outside ephemeris range")
            return None

        # Find the two surrounding dates
        for i in range(len(self.data) - 1):
            if self.data[i]['datetime'] <= dt <= self.data[i + 1]['datetime']:
                # Linear interpolation
                d1 = self.data[i]
                d2 = self.data[i + 1]

                # Calculate interpolation factor
                total_seconds = (d2['datetime'] - d1['datetime']).total_seconds()
                elapsed_seconds = (dt - d1['datetime']).total_seconds()
                factor = elapsed_seconds / total_seconds if total_seconds > 0 else 0

                # Interpolate positions
                result = {'datetime': dt}

                planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars',
                          'Jupiter', 'Saturn', 'Uranus', 'Neptune']

                for planet in planets:
                    lon1 = d1[planet]
                    lon2 = d2[planet]

                    # Handle 360° wraparound
                    if abs(lon2 - lon1) > 180:
                        if lon2 < lon1:
                            lon2 += 360
                        else:
                            lon1 += 360

                    # Interpolate
                    lon = lon1 + (lon2 - lon1) * factor
                    result[planet] = lon % 360

                # Use retrograde status from closest date
                closest = d1 if factor < 0.5 else d2
                for planet in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']:
                    result[f'{planet}_retro'] = closest[f'{planet}_retro']

                return result

        return None

# Global ephemeris instance
_ephemeris = None

def get_ephemeris():
    """Get or create ephemeris instance"""
    global _ephemeris
    if _ephemeris is None:
        _ephemeris = EphemerisData(CSV_PATH)
    return _ephemeris

# ==================== UTILITY FUNCTIONS ====================

def normalize_angle(angle: float) -> float:
    """Normalize angle to 0-360 range"""
    while angle < 0:
        angle += 360
    while angle >= 360:
        angle -= 360
    return angle

def angle_difference(angle1: float, angle2: float) -> float:
    """Calculate smallest difference between two angles"""
    diff = abs(angle1 - angle2)
    if diff > 180:
        diff = 360 - diff
    return diff

# ==================== FALLBACK: SIMPLIFIED CALCULATIONS ====================

def calculate_pluto_position(dt: datetime) -> float:
    """Calculate approximate Pluto position (not in CSV)"""
    # Very simplified - Pluto moves ~1.5° per year
    days_since_j2000 = (dt - datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc)).days
    years = days_since_j2000 / 365.25

    # Pluto was at ~251° in 2000
    pluto_lon = 251.0 + years * 1.5
    return pluto_lon % 360

def calculate_fallback_positions(dt: datetime) -> Dict[str, Dict]:
    """
    Calculate approximate positions using simplified formulas
    Used for Bitcoin natal chart (2009) which is outside CSV range
    """
    # Days since J2000 epoch
    days_since_j2000 = (dt - datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc)).days

    # Approximate mean motion (degrees per day)
    positions = {}

    # Sun (actually Earth's orbit)
    sun_lon = (280.46 + 0.9856474 * days_since_j2000) % 360
    positions['Sun'] = {'longitude': sun_lon, 'planet': 'Sun', 'retrograde': False}

    # Moon (very approximate)
    moon_lon = (218.316 + 13.176396 * days_since_j2000) % 360
    positions['Moon'] = {'longitude': moon_lon, 'planet': 'Moon', 'retrograde': False}

    # Mercury
    mercury_lon = (252.25 + 4.092338 * days_since_j2000) % 360
    positions['Mercury'] = {'longitude': mercury_lon, 'planet': 'Mercury', 'retrograde': False}

    # Venus
    venus_lon = (181.98 + 1.602131 * days_since_j2000) % 360
    positions['Venus'] = {'longitude': venus_lon, 'planet': 'Venus', 'retrograde': False}

    # Mars
    mars_lon = (355.43 + 0.524039 * days_since_j2000) % 360
    positions['Mars'] = {'longitude': mars_lon, 'planet': 'Mars', 'retrograde': False}

    # Jupiter
    jupiter_lon = (34.35 + 0.083056 * days_since_j2000) % 360
    positions['Jupiter'] = {'longitude': jupiter_lon, 'planet': 'Jupiter', 'retrograde': False}

    # Saturn
    saturn_lon = (50.08 + 0.033459 * days_since_j2000) % 360
    positions['Saturn'] = {'longitude': saturn_lon, 'planet': 'Saturn', 'retrograde': False}

    # Uranus
    uranus_lon = (314.05 + 0.011733 * days_since_j2000) % 360
    positions['Uranus'] = {'longitude': uranus_lon, 'planet': 'Uranus', 'retrograde': False}

    # Neptune
    neptune_lon = (304.88 + 0.005981 * days_since_j2000) % 360
    positions['Neptune'] = {'longitude': neptune_lon, 'planet': 'Neptune', 'retrograde': False}

    # Pluto
    positions['Pluto'] = {
        'longitude': calculate_pluto_position(dt),
        'planet': 'Pluto',
        'retrograde': False
    }

    return positions

# ==================== GET POSITIONS ====================

def get_all_positions(dt: datetime) -> Dict[str, Dict]:
    """Get positions for all planets at given datetime"""
    positions = {}

    # Try to get from ephemeris CSV
    ephemeris = get_ephemeris()
    ephem_data = ephemeris.get_positions(dt)

    if ephem_data:
        # Use accurate ephemeris data from CSV
        planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars',
                  'Jupiter', 'Saturn', 'Uranus', 'Neptune']

        for planet in planets:
            positions[planet] = {
                'longitude': ephem_data[planet],
                'planet': planet
            }

            # Add retrograde status if available
            if f'{planet}_retro' in ephem_data:
                positions[planet]['retrograde'] = ephem_data[f'{planet}_retro']

        # Add Pluto (not in CSV, use calculation)
        positions['Pluto'] = {
            'longitude': calculate_pluto_position(dt),
            'planet': 'Pluto',
            'retrograde': False  # Not tracking Pluto retrograde
        }
    else:
        # Fallback to calculated positions (for dates outside CSV range, like Bitcoin genesis)
        positions = calculate_fallback_positions(dt)

    return positions

# ==================== ASPECT CALCULATIONS ====================

def check_aspect(lon1: float, lon2: float, aspect_name: str) -> Tuple[bool, float]:
    """
    Check if two longitudes form a specific aspect
    Returns (is_aspect, orb)
    """
    target_angle, max_orb = ASPECTS[aspect_name]

    diff = angle_difference(lon1, lon2)
    orb = abs(diff - target_angle)

    is_aspect = orb <= max_orb

    return is_aspect, orb

def find_aspects_to_natal(current_positions: Dict, natal_positions: Dict) -> List[Dict]:
    """Find all aspects between current transiting planets and natal positions"""
    aspects_found = []

    for transit_planet, transit_data in current_positions.items():
        for natal_planet, natal_data in natal_positions.items():
            transit_lon = transit_data['longitude']
            natal_lon = natal_data['longitude']

            for aspect_name in ASPECTS.keys():
                is_aspect, orb = check_aspect(transit_lon, natal_lon, aspect_name)

                if is_aspect:
                    aspects_found.append({
                        'transit_planet': transit_planet,
                        'natal_planet': natal_planet,
                        'aspect': aspect_name,
                        'orb': round(orb, 2),
                        'transit_longitude': round(transit_lon, 2),
                        'natal_longitude': round(natal_lon, 2)
                    })

    return aspects_found

def count_malefic_aspects(aspects: List[Dict]) -> int:
    """
    Count malefic aspects: Square, Opposition, or Conjunction
    involving Mars or Saturn to natal points
    """
    count = 0
    hard_aspects = ['Square', 'Opposition', 'Conjunction']

    for aspect in aspects:
        if aspect['transit_planet'] in MALEFIC_PLANETS:
            if aspect['aspect'] in hard_aspects:
                if aspect['natal_planet'] in NATAL_POINTS:
                    count += 1

    return count

def count_benefic_aspects(aspects: List[Dict]) -> int:
    """
    Count benefic aspects: Trine, Sextile, or Conjunction
    involving Jupiter or Venus to natal Sun or Moon
    """
    count = 0
    soft_aspects = ['Trine', 'Sextile', 'Conjunction']

    for aspect in aspects:
        if aspect['transit_planet'] in BENEFIC_PLANETS:
            if aspect['aspect'] in soft_aspects:
                if aspect['natal_planet'] in NATAL_POINTS:
                    count += 1

    return count

# ==================== SPECIAL ASPECT DETECTION ====================

def check_mars_uranus_hard_aspect(positions: Dict) -> Tuple[bool, str]:
    """Check for hard aspects between Mars and Uranus"""
    mars_lon = positions['Mars']['longitude']
    uranus_lon = positions['Uranus']['longitude']

    hard_aspects = ['Conjunction', 'Square', 'Opposition']

    for aspect_name in hard_aspects:
        is_aspect, orb = check_aspect(mars_lon, uranus_lon, aspect_name)
        if is_aspect:
            return True, f"{aspect_name} (orb: {orb:.2f}°)"

    return False, "None"

# ==================== TRANSIT FORECASTING ====================

def find_upcoming_transits(natal_positions: Dict, days_ahead: int = 30) -> List[Dict]:
    """Find major transits coming up in the next N days"""
    now = datetime.now(timezone.utc)
    upcoming = []

    # Check each day
    for day_offset in range(1, days_ahead + 1):
        future_date = now + timedelta(days=day_offset)

        positions = get_all_positions(future_date)
        if not positions:
            continue

        aspects = find_aspects_to_natal(positions, natal_positions)

        # Look for significant aspects
        for aspect in aspects:
            # Major transits: outer planets to natal Sun/Moon
            outer_planets = ['Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
            major_aspects = ['Conjunction', 'Square', 'Opposition', 'Trine']

            if (aspect['transit_planet'] in outer_planets and
                aspect['natal_planet'] in NATAL_POINTS and
                aspect['aspect'] in major_aspects and
                aspect['orb'] < 2.0):  # Tight orb for upcoming

                upcoming.append({
                    'date': f"Day +{day_offset}",
                    'exact_date': future_date.strftime('%Y-%m-%d'),
                    'transit': f"{aspect['transit_planet']} {aspect['aspect']} natal {aspect['natal_planet']}",
                    'orb': aspect['orb']
                })

    # Remove duplicates and sort
    seen = set()
    unique_upcoming = []
    for t in upcoming:
        key = t['transit']
        if key not in seen:
            seen.add(key)
            unique_upcoming.append(t)

    return unique_upcoming[:10]  # Return top 10

# ==================== MAIN ANALYSIS FUNCTION ====================

def analyze_bitcoin_astrology() -> Dict:
    """Main function to analyze Bitcoin's current astrological situation"""

    # Calculate Bitcoin's natal chart (will use fallback for 2009)
    natal_positions = get_all_positions(BITCOIN_GENESIS)

    # Calculate current positions (will use CSV if in 2025-2035 range)
    now = datetime.now(timezone.utc)
    current_positions = get_all_positions(now)

    # Find all aspects
    aspects = find_aspects_to_natal(current_positions, natal_positions)

    # Count malefic and benefic aspects
    malefic_count = count_malefic_aspects(aspects)
    benefic_count = count_benefic_aspects(aspects)

    # Check Mercury retrograde (from CSV data)
    mercury_retrograde = current_positions.get('Mercury', {}).get('retrograde', False)

    # Check Mars-Uranus hard aspect
    mars_uranus_hard, mars_uranus_desc = check_mars_uranus_hard_aspect(current_positions)

    # Find upcoming transits
    upcoming_transits = find_upcoming_transits(natal_positions, days_ahead=30)

    # Determine data source
    ephemeris = get_ephemeris()
    current_from_csv = ephemeris.get_positions(now) is not None
    natal_from_csv = ephemeris.get_positions(BITCOIN_GENESIS) is not None

    data_source = []
    if current_from_csv:
        data_source.append("Current: CSV Ephemeris (accurate)")
    else:
        data_source.append("Current: Calculated (approximate)")

    if natal_from_csv:
        data_source.append("Natal: CSV Ephemeris")
    else:
        data_source.append("Natal: Calculated (2009 data)")

    # Prepare result
    result = {
        'current_date': now.strftime('%Y-%m-%d %H:%M:%S UTC'),
        'bitcoin_genesis': BITCOIN_GENESIS.strftime('%Y-%m-%d %H:%M:%S UTC'),
        'malefic_aspects': malefic_count,
        'benefic_aspects': benefic_count,
        'mercury_status': 'Retrograde' if mercury_retrograde else 'Direct',
        'mars_uranus_hard_aspect': mars_uranus_desc,
        'current_positions': {k: f"{v['longitude']:.2f}°" for k, v in current_positions.items()},
        'natal_positions': {k: f"{v['longitude']:.2f}°" for k, v in natal_positions.items()},
        'all_aspects': aspects,
        'upcoming_transits': upcoming_transits,
        'data_source': ' | '.join(data_source)
    }

    return result

# ==================== CLI INTERFACE ====================

if __name__ == '__main__':
    import json

    print("=" * 70)
    print("BITCOIN FINANCIAL ASTROLOGY ANALYSIS")
    print("Using Accurate CSV Ephemeris Data")
    print("=" * 70)

    result = analyze_bitcoin_astrology()

    if 'error' in result:
        print(f"\n⚠ ERROR: {result['error']}")
        print(f"Note: {result.get('note', '')}")
        exit(1)

    print(f"\nCurrent Date: {result['current_date']}")
    print(f"Bitcoin Genesis: {result['bitcoin_genesis']}")
    print(f"Data Source: {result['data_source']}")
    print(f"\n{'─' * 70}")
    print(f"MALEFIC ASPECTS (Mars/Saturn hard aspects): {result['malefic_aspects']}")
    print(f"BENEFIC ASPECTS (Jupiter/Venus harmonious): {result['benefic_aspects']}")
    print(f"{'─' * 70}")
    print(f"\nMercury Status: {result['mercury_status']}")
    print(f"Mars-Uranus Hard Aspect: {result['mars_uranus_hard_aspect']}")

    print(f"\n{'─' * 70}")
    print("CURRENT PLANETARY POSITIONS (Tropical Zodiac)")
    print(f"{'─' * 70}")
    for planet, lon in result['current_positions'].items():
        print(f"{planet:12s}: {lon}")

    print(f"\n{'─' * 70}")
    print("BITCOIN NATAL POSITIONS (Jan 3, 2009)")
    print(f"{'─' * 70}")
    for planet, lon in result['natal_positions'].items():
        print(f"{planet:12s}: {lon}")

    if result['all_aspects']:
        print(f"\n{'─' * 70}")
        print("ALL CURRENT ASPECTS TO NATAL CHART")
        print(f"{'─' * 70}")
        for aspect in result['all_aspects'][:20]:  # Show first 20
            print(f"{aspect['transit_planet']:10s} {aspect['aspect']:12s} "
                  f"natal {aspect['natal_planet']:10s} (orb: {aspect['orb']:.2f}°)")

    if result['upcoming_transits']:
        print(f"\n{'─' * 70}")
        print("UPCOMING MAJOR TRANSITS (Next 30 Days)")
        print(f"{'─' * 70}")
        for transit in result['upcoming_transits']:
            print(f"{transit['exact_date']:12s} ({transit['date']:10s}): "
                  f"{transit['transit']} (orb: {transit['orb']:.2f}°)")

    print(f"\n{'─' * 70}")
    print("Analysis complete!")
    print(f"{'─' * 70}\n")

    # Output JSON for web interface
    with open('/tmp/bitcoin_astro.json', 'w') as f:
        json.dump(result, f, indent=2)
    print("JSON data saved to /tmp/bitcoin_astro.json")
