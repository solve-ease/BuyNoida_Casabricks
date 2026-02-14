"""
Utility functions for calculations
"""
from math import radians, cos, sin, asin, sqrt
from decimal import Decimal
from typing import Literal


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance in meters between two lat/lon points using Haversine formula
    
    Args:
        lat1: Latitude of point 1
        lon1: Longitude of point 1
        lat2: Latitude of point 2
        lon2: Longitude of point 2
        
    Returns:
        Distance in meters
    """
    R = 6371000  # Earth radius in meters
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c


def calculate_price_category(
    price_per_sqft: Decimal,
    avg_price_per_sqft: Decimal
) -> Literal["below_average", "average", "above_average"]:
    """
    Calculate price category by comparing to average
    
    Args:
        price_per_sqft: Price per square foot of the property
        avg_price_per_sqft: Average price per square foot
        
    Returns:
        Category: below_average, average, or above_average
    """
    if avg_price_per_sqft == 0:
        return "average"
    
    difference_pct = abs((price_per_sqft - avg_price_per_sqft) / avg_price_per_sqft * 100)
    
    if difference_pct <= 10:  # Within 10% is average
        return "average"
    elif price_per_sqft < avg_price_per_sqft:
        return "below_average"
    else:
        return "above_average"


def calculate_facing_metrics(facing_direction: str) -> dict:
    """
    Calculate facing direction metrics
    
    Args:
        facing_direction: Direction the property faces
        
    Returns:
        Dict with heat_exposure, vastu_compatibility, natural_light_intensity
    """
    # Simplified scoring based on common beliefs
    metrics = {
        "north": {
            "heat_exposure": 30,
            "vastu_compatibility": 90,
            "natural_light_intensity": 60
        },
        "south": {
            "heat_exposure": 85,
            "vastu_compatibility": 70,
            "natural_light_intensity": 90
        },
        "east": {
            "heat_exposure": 60,
            "vastu_compatibility": 95,
            "natural_light_intensity": 85
        },
        "west": {
            "heat_exposure": 80,
            "vastu_compatibility": 65,
            "natural_light_intensity": 75
        },
        "north_east": {
            "heat_exposure": 45,
            "vastu_compatibility": 100,
            "natural_light_intensity": 75
        },
        "north_west": {
            "heat_exposure": 55,
            "vastu_compatibility": 75,
            "natural_light_intensity": 70
        },
        "south_east": {
            "heat_exposure": 75,
            "vastu_compatibility": 85,
            "natural_light_intensity": 88
        },
        "south_west": {
            "heat_exposure": 80,
            "vastu_compatibility": 80,
            "natural_light_intensity": 82
        }
    }
    
    return metrics.get(facing_direction, {
        "heat_exposure": 50,
        "vastu_compatibility": 50,
        "natural_light_intensity": 50
    })
