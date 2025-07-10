#!/usr/bin/env python3
"""
Script to get OTF membership data and upload it to Home Assistant as sensor values.
"""

import os
import json
import requests
from typing import Dict, Any, Optional
from otf_membership_info import get_otf_info


def send_to_homeassistant(data: Dict[str, Any], ha_url: str, ha_token: str) -> None:
    """
    Send OTF data to Home Assistant as sensor values.
    
    Args:
        data: Dictionary containing OTF membership data
        ha_url: Home Assistant URL (e.g., http://localhost:8123)
        ha_token: Home Assistant long-lived access token
    """
    headers = {
        'Authorization': f'Bearer {ha_token}',
        'Content-Type': 'application/json'
    }
    
    # Map of sensor names to their values and attributes
    sensors = {
        'otf_active_date': {
            'state': data['active_date'],
            'attributes': {
                'friendly_name': 'OTF Active Date',
                'device_class': 'timestamp',
                'icon': 'mdi:calendar-start'
            }
        },
        'otf_expiration_date': {
            'state': data['expiration_date'],
            'attributes': {
                'friendly_name': 'OTF Expiration Date',
                'device_class': 'timestamp',
                'icon': 'mdi:calendar-end'
            }
        },
        'otf_class_count': {
            'state': data['class_count'],
            'attributes': {
                'friendly_name': 'OTF Class Count',
                'unit_of_measurement': 'classes',
                'icon': 'mdi:counter'
            }
        },
        'otf_classes_remaining': {
            'state': data['classes_remaining'],
            'attributes': {
                'friendly_name': 'OTF Classes Remaining',
                'unit_of_measurement': 'classes',
                'icon': 'mdi:counter'
            }
        },
        'otf_cycle_percentage': {
            'state': data['cycle_percentage'],
            'attributes': {
                'friendly_name': 'OTF Cycle Percentage',
                'unit_of_measurement': '%',
                'icon': 'mdi:percent'
            }
        }
    }
    
    # Handle next booking date (may be None)
    if data['next_booking_date']:
        sensors['otf_next_booking_date'] = {
            'state': data['next_booking_date'],
            'attributes': {
                'friendly_name': 'OTF Next Booking Date',
                'device_class': 'timestamp',
                'icon': 'mdi:calendar-clock'
            }
        }
    
    # Send each sensor to Home Assistant
    for sensor_name, sensor_data in sensors.items():
        url = f"{ha_url}/api/states/sensor.{sensor_name}"
        
        payload = {
            'state': sensor_data['state'],
            'attributes': sensor_data['attributes']
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            print(f"✓ Updated sensor.{sensor_name}: {sensor_data['state']}")
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to update sensor.{sensor_name}: {e}")


def main():
    """Main function to run the script."""
    # Get Home Assistant configuration from environment variables
    ha_url = os.getenv('HA_URL')
    ha_token = os.getenv('HA_TOKEN')
    
    if not ha_url or not ha_token:
        print("Error: HA_URL and HA_TOKEN environment variables must be set")
        print("Example:")
        print("  export HA_URL=http://localhost:8123")
        print("  export HA_TOKEN=your_long_lived_access_token")
        exit(1)
    
    # Remove trailing slash from URL if present
    ha_url = ha_url.rstrip('/')
    
    try:
        # Get OTF membership data
        print("Getting OTF membership data...")
        otf_data = get_otf_info()
        
        print(f"Retrieved data: {json.dumps(otf_data, indent=2)}")
        
        # Send data to Home Assistant
        print("Sending data to Home Assistant...")
        send_to_homeassistant(otf_data, ha_url, ha_token)
        
        print("✓ Successfully updated Home Assistant sensors")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()