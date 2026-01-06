"""
Deterministic electricity price generation.

Generates realistic electricity price curves with:
- Daily patterns (peaks during morning and evening)
- Weekly patterns (weekdays vs weekends)
- Some flat price days
- Some constantly high price days
- Deterministic using fixed seed for reproducibility
"""

import random
from datetime import datetime, timedelta
from typing import List

try:
    from .models import ElectricityPrice
except ImportError:
    from models import ElectricityPrice


# Fixed seed for reproducibility
RANDOM_SEED = 42


def _get_base_price_pattern(hour: int, minute: int) -> float:
    """
    Generate base price pattern based on time of day.
    
    Typical pattern:
    - Night (00:00-06:00): Low prices
    - Morning peak (06:00-09:00): High prices
    - Midday (09:00-17:00): Medium-high prices
    - Evening peak (17:00-20:00): High prices
    - Night (20:00-24:00): Medium prices
    
    Args:
        hour: Hour of day (0-23)
        minute: Minute of hour (0-59)
        
    Returns:
        Base price multiplier (0.5-1.5)
    """
    time_of_day = hour + minute / 60.0
    
    # Night hours (00:00-06:00): Low prices
    if 0 <= time_of_day < 6:
        return 0.5 + (time_of_day / 6) * 0.2  # Gradually increase from 0.5 to 0.7
    
    # Morning peak (06:00-09:00): High prices
    elif 6 <= time_of_day < 9:
        peak_factor = abs(time_of_day - 7.5) / 1.5  # Peak at 7:30
        return 1.2 + (1 - peak_factor) * 0.3  # 1.2 to 1.5
    
    # Midday (09:00-17:00): Medium-high prices
    elif 9 <= time_of_day < 17:
        return 1.0 + (time_of_day - 9) / 8 * 0.2  # 1.0 to 1.2
    
    # Evening peak (17:00-20:00): High prices
    elif 17 <= time_of_day < 20:
        peak_factor = abs(time_of_day - 18.5) / 1.5  # Peak at 18:30
        return 1.2 + (1 - peak_factor) * 0.3  # 1.2 to 1.5
    
    # Night (20:00-24:00): Medium prices
    else:
        return 1.0 - (time_of_day - 20) / 4 * 0.3  # 1.0 to 0.7


def _is_weekend(date: datetime) -> bool:
    """Check if date is a weekend (Saturday or Sunday)."""
    return date.weekday() >= 5


def _get_day_type(date: datetime, day_index: int) -> str:
    """
    Determine day type using deterministic logic.
    
    Args:
        date: Date to check
        day_index: Index of day in the sequence (for deterministic selection)
        
    Returns:
        Day type: 'flat', 'high', 'weekend', or 'normal'
    """
    # Use day index to deterministically select day types
    # Every 7th day is a flat price day
    # Every 11th day is a high price day
    if day_index % 7 == 0:
        return 'flat'
    elif day_index % 11 == 0:
        return 'high'
    elif _is_weekend(date):
        return 'weekend'
    else:
        return 'normal'


def _add_random_variation(base_price: float, seed_value: int) -> float:
    """
    Add small random variation to price for realism.
    
    Args:
        base_price: Base price value
        seed_value: Seed value for deterministic randomness
        
    Returns:
        Price with variation
    """
    # Use seed to create deterministic variation
    random.seed(seed_value)
    variation = random.uniform(-0.05, 0.05)  # ±5% variation
    return base_price * (1 + variation)


def generate_electricity_prices(
    start_time: datetime,
    end_time: datetime,
    base_price_eur_per_mwh: float = 80.0,
) -> List[ElectricityPrice]:
    """
    Generate deterministic electricity prices with realistic patterns.
    
    Args:
        start_time: Start of the time range
        end_time: End of the time range
        base_price_eur_per_mwh: Base price in EUR per MWh (default: 80.0)
        
    Returns:
        List of electricity prices with 15-minute resolution
    """
    prices = []
    current_time = start_time.replace(minute=(start_time.minute // 15) * 15, second=0, microsecond=0)
    
    # Initialize random with fixed seed
    random.seed(RANDOM_SEED)
    
    day_index = 0
    last_date = None
    
    while current_time <= end_time:
        # Track day changes for day type calculation
        current_date = current_time.date()
        if last_date is None or current_date != last_date:
            day_index += 1
            last_date = current_date
        
        # Get day type
        day_type = _get_day_type(current_time, day_index)
        
        # Calculate price based on day type
        if day_type == 'flat':
            # Flat price day: constant price throughout the day
            base_price = base_price_eur_per_mwh * 0.8
        elif day_type == 'high':
            # High price day: constantly high price throughout the day
            base_price = base_price_eur_per_mwh * 1.5
        else:
            # Normal or weekend day: use time-of-day pattern
            hour = current_time.hour
            minute = current_time.minute
            time_multiplier = _get_base_price_pattern(hour, minute)
            
            # Apply weekend discount if applicable
            if day_type == 'weekend':
                day_multiplier = 0.85
            else:
                day_multiplier = 1.0
            
            base_price = base_price_eur_per_mwh * time_multiplier * day_multiplier
        
        # Add deterministic random variation
        # Use timestamp components as seed for variation
        seed_value = RANDOM_SEED + hash((current_time.year, current_time.month, 
                                         current_time.day, current_time.hour, current_time.minute))
        final_price = _add_random_variation(base_price, seed_value)
        
        # Ensure price is positive and within reasonable bounds
        final_price = max(20.0, min(200.0, final_price))
        
        prices.append(ElectricityPrice(
            timestamp=current_time,
            price=round(final_price, 2),
        ))
        
        # Move to next 15-minute interval
        current_time += timedelta(minutes=15)
    
    return prices

