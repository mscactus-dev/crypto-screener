#!/usr/bin/env python3
"""
Bitcoin Financial Astrology Calculator
Pure mathematical implementation using Kepler's equations
Calculates planetary positions and aspects to Bitcoin's natal chart
"""

import math
from datetime import datetime, timezone
from typing import Dict, List, Tuple

# ==================== ASTRONOMICAL CONSTANTS ====================

# Julian Date constants
JD_J2000 = 2451545.0  # J2000.0 epoch (Jan 1, 2000, 12:00 TT)

# Orbital elements for planets at J2000.0 epoch
# Format: [a, e, I, L, long_peri, long_node]
# a = semi-major axis (AU), e = eccentricity, I = inclination (deg)
# L = mean longitude (deg), long_peri = longitude of perihelion (deg)
# long_node = longitude of ascending node (deg)

ORBITAL_ELEMENTS = {
    'Sun': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Earth around Sun (we'll invert)
    'Moon': [0.00257, 0.0549, 5.145, 218.316, 318.15, 125.08],  # Approximate
    'Mercury': [0.38710, 0.20563, 7.005, 252.251, 77.456, 48.331],
    'Venus': [0.72333, 0.00677, 3.395, 181.980, 131.563, 76.680],
    'Mars': [1.52368, 0.09340, 1.850, 355.433, 336.060, 49.558],
    'Jupiter': [5.20260, 0.04849, 1.303, 34.351, 14.753, 100.464],
    'Saturn': [9.55491, 0.05551, 2.489, 50.078, 93.057, 113.665],
    'Uranus': [19.21845, 0.04630, 0.773, 314.055, 173.005, 74.006],
    'Neptune': [30.11039, 0.00899, 1.770, 304.880, 48.120, 131.784],
    'Pluto': [39.48169, 0.24881, 17.140, 238.930, 224.067, 110.307]
}

# Orbital element rates (per century from J2000)
ORBITAL_RATES = {
    'Mercury': [0.00000, 0.00002, -0.0001, 149472.6746, 0.1589, -0.1061],
    'Venus': [0.00000, -0.00005, -0.0001, 58517.8149, 0.0529, -0.0278],
    'Mars': [0.00000, 0.00009, -0.0003, 19139.8585, 0.4484, -0.0106],
    'Jupiter': [0.00000, -0.00012, -0.0001, 3034.9056, 0.1703, 0.0328],
    'Saturn': [0.00000, -0.00036, -0.0001, 1222.1138, 0.1302, -0.0492],
    'Uranus': [0.00000, -0.00004, 0.0000, 428.4677, 0.0516, 0.0565],
    'Neptune': [0.00000, 0.00005, 0.0000, 218.4862, -0.0054, -0.0059],
    'Pluto': [0.00000, -0.00006, 0.0000, 145.1847, -0.0044, -0.0099]
}

# Bitcoin Genesis Block (Natal Chart)
BITCOIN_GENESIS = datetime(2009, 1, 3, 18, 15, 5, tzinfo=timezone.utc)

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

# ==================== UTILITY FUNCTIONS ====================

def datetime_to_jd(dt: datetime) -> float:
    """Convert datetime to Julian Date"""
    a = (14 - dt.month) // 12
    y = dt.year + 4800 - a
    m = dt.month + 12 * a - 3

    jdn = dt.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045

    jd = jdn + (dt.hour - 12) / 24.0 + dt.minute / 1440.0 + dt.second / 86400.0

    return jd

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

# ==================== KEPLER'S EQUATION SOLVER ====================

def solve_kepler(M: float, e: float, tolerance: float = 1e-6) -> float:
    """
    Solve Kepler's equation: M = E - e*sin(E)
    M = mean anomaly (radians)
    e = eccentricity
    Returns eccentric anomaly E (radians)
    """
    E = M  # Initial guess

    for _ in range(30):  # Max iterations
        delta = E - e * math.sin(E) - M
        if abs(delta) < tolerance:
            break
        E = E - delta / (1 - e * math.cos(E))

    return E

# ==================== PLANETARY POSITION CALCULATOR ====================

def calculate_planet_position(planet: str, jd: float) -> Dict:
    """
    Calculate heliocentric position of a planet using orbital elements
    Returns dict with longitude, latitude, distance
    """
    if planet not in ORBITAL_ELEMENTS:
        raise ValueError(f"Unknown planet: {planet}")

    # Get orbital elements
    elements = ORBITAL_ELEMENTS[planet].copy()

    # Calculate centuries from J2000
    T = (jd - JD_J2000) / 36525.0

    # Apply rates if available
    if planet in ORBITAL_RATES:
        rates = ORBITAL_RATES[planet]
        for i in range(6):
            elements[i] += rates[i] * T

    a, e, I, L, long_peri, long_node = elements

    # Convert to radians
    I_rad = math.radians(I)
    L_rad = math.radians(L)
    long_peri_rad = math.radians(long_peri)
    long_node_rad = math.radians(long_node)

    # Calculate mean anomaly
    M = L_rad - long_peri_rad
    M = M % (2 * math.pi)

    # Solve Kepler's equation for eccentric anomaly
    E = solve_kepler(M, e)

    # Calculate true anomaly
    nu = 2 * math.atan2(
        math.sqrt(1 + e) * math.sin(E / 2),
        math.sqrt(1 - e) * math.cos(E / 2)
    )

    # Calculate heliocentric distance
    r = a * (1 - e * math.cos(E))

    # Calculate heliocentric longitude
    lon = nu + long_peri_rad
    lon = lon % (2 * math.pi)

    # For simplicity, we'll use 2D ecliptic coordinates
    # Full 3D calculation would include latitude effects

    return {
        'longitude': math.degrees(lon) % 360,
        'distance': r,
        'planet': planet
    }

def calculate_sun_position(jd: float) -> Dict:
    """Calculate geocentric Sun position (Earth around Sun inverted)"""
    # Calculate Earth's position
    elements = [1.00000011, 0.01671022, 0.00005,
                100.46435 + 35999.37306 * ((jd - JD_J2000) / 36525.0),
                102.94719, 0.0]

    a, e, I, L, long_peri, long_node = elements

    L_rad = math.radians(L)
    long_peri_rad = math.radians(long_peri)

    M = L_rad - long_peri_rad
    M = M % (2 * math.pi)

    E = solve_kepler(M, e)

    nu = 2 * math.atan2(
        math.sqrt(1 + e) * math.sin(E / 2),
        math.sqrt(1 - e) * math.cos(E / 2)
    )

    # Sun's apparent longitude (from Earth)
    lon = (nu + long_peri_rad + math.pi) % (2 * math.pi)

    return {
        'longitude': math.degrees(lon) % 360,
        'distance': a,
        'planet': 'Sun'
    }

def calculate_moon_position(jd: float) -> Dict:
    """Simplified Moon position calculation"""
    T = (jd - JD_J2000) / 36525.0

    # Simplified lunar position (good to ~1-2 degrees)
    L0 = 218.316 + 481267.8813 * T  # Mean longitude
    l = 134.963 + 477198.8676 * T   # Mean anomaly
    F = 93.272 + 483202.0175 * T    # Argument of latitude

    # Main perturbations
    lon = L0 + 6.289 * math.sin(math.radians(l))
    lon = lon % 360

    return {
        'longitude': lon,
        'distance': 0.00257,  # AU (average)
        'planet': 'Moon'
    }

def get_all_positions(jd: float) -> Dict[str, Dict]:
    """Calculate positions for all planets at given Julian Date"""
    positions = {}

    # Sun
    positions['Sun'] = calculate_sun_position(jd)

    # Moon
    positions['Moon'] = calculate_moon_position(jd)

    # Planets
    for planet in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']:
        positions[planet] = calculate_planet_position(planet, jd)

    return positions

# ==================== RETROGRADE DETECTION ====================

def is_retrograde(planet: str, jd: float, delta_days: float = 1.0) -> bool:
    """
    Detect if a planet is retrograde by comparing positions
    delta_days: how many days ahead to check
    """
    if planet == 'Sun' or planet == 'Moon':
        return False  # Sun and Moon don't go retrograde

    pos1 = calculate_planet_position(planet, jd)
    pos2 = calculate_planet_position(planet, jd + delta_days)

    lon1 = pos1['longitude']
    lon2 = pos2['longitude']

    # Check if longitude decreased (accounting for 0/360 wraparound)
    if abs(lon2 - lon1) > 180:
        # Wrapped around
        if lon2 < lon1:
            lon2 += 360
        else:
            lon1 += 360

    return lon2 < lon1

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
    now_jd = datetime_to_jd(datetime.now(timezone.utc))
    upcoming = []

    # Check each day
    for day_offset in range(1, days_ahead + 1):
        future_jd = now_jd + day_offset
        future_date = datetime.now(timezone.utc).replace(
            day=datetime.now(timezone.utc).day
        )  # Simplified

        positions = get_all_positions(future_jd)
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
                    'transit': f"{aspect['transit_planet']} {aspect['aspect']} {aspect['natal_planet']}",
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

    # Calculate Bitcoin's natal chart
    genesis_jd = datetime_to_jd(BITCOIN_GENESIS)
    natal_positions = get_all_positions(genesis_jd)

    # Calculate current positions
    now = datetime.now(timezone.utc)
    current_jd = datetime_to_jd(now)
    current_positions = get_all_positions(current_jd)

    # Find all aspects
    aspects = find_aspects_to_natal(current_positions, natal_positions)

    # Count malefic and benefic aspects
    malefic_count = count_malefic_aspects(aspects)
    benefic_count = count_benefic_aspects(aspects)

    # Check Mercury retrograde
    mercury_retrograde = is_retrograde('Mercury', current_jd)

    # Check Mars-Uranus hard aspect
    mars_uranus_hard, mars_uranus_desc = check_mars_uranus_hard_aspect(current_positions)

    # Find upcoming transits
    upcoming_transits = find_upcoming_transits(natal_positions, days_ahead=30)

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
        'upcoming_transits': upcoming_transits
    }

    return result

# ==================== CLI INTERFACE ====================

if __name__ == '__main__':
    import json

    print("=" * 70)
    print("BITCOIN FINANCIAL ASTROLOGY ANALYSIS")
    print("=" * 70)

    result = analyze_bitcoin_astrology()

    print(f"\nCurrent Date: {result['current_date']}")
    print(f"Bitcoin Genesis: {result['bitcoin_genesis']}")
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
        for aspect in result['all_aspects'][:15]:  # Show first 15
            print(f"{aspect['transit_planet']:10s} {aspect['aspect']:12s} "
                  f"natal {aspect['natal_planet']:10s} (orb: {aspect['orb']:.2f}°)")

    if result['upcoming_transits']:
        print(f"\n{'─' * 70}")
        print("UPCOMING MAJOR TRANSITS (Next 30 Days)")
        print(f"{'─' * 70}")
        for transit in result['upcoming_transits']:
            print(f"{transit['date']:10s}: {transit['transit']} (orb: {transit['orb']:.2f}°)")

    print(f"\n{'─' * 70}")
    print("Analysis complete!")
    print(f"{'─' * 70}\n")

    # Output JSON for web interface
    with open('/tmp/bitcoin_astro.json', 'w') as f:
        json.dump(result, f, indent=2)
    print("JSON data saved to /tmp/bitcoin_astro.json")
