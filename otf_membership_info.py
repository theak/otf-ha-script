#!/usr/bin/env python3
"""
Script to extract OTF membership and booking information using the OTF API.
"""

import os
import json
from datetime import datetime
from typing import Optional, Dict, Any
from otf_api import Otf, OtfUser


def get_otf_info() -> Dict[str, Any]:
    """
    Retrieve OTF membership and booking information.
    
    Returns:
        Dict containing membership and booking data
    """
    # Get credentials from environment variables
    email = os.getenv('OTF_EMAIL')
    password = os.getenv('OTF_PASSWORD')
    
    if not email or not password:
        raise ValueError("OTF_EMAIL and OTF_PASSWORD environment variables must be set")
    
    # Initialize OTF client
    otf = Otf(user=OtfUser(email, password))
    
    # Get membership information
    membership = otf.members.get_member_membership()
    
    # Get booking information
    bookings = otf.bookings.get_bookings()
    
    # Find the next booking (soonest upcoming booking)
    next_booking_date = None
    if bookings:
        # Filter for future bookings and get the earliest one
        now = datetime.now()
        future_bookings = [
            booking for booking in bookings 
            if booking.otf_class.starts_at > now
        ]
        
        if future_bookings:
            # Sort by start time and get the earliest
            future_bookings.sort(key=lambda b: b.otf_class.starts_at)
            next_booking_date = future_bookings[0].otf_class.starts_at.isoformat()
    
    # Calculate cycle percentage
    cycle_percentage = None
    try:
        now = datetime.now()
        # Remove timezone info for comparison if present
        active_date = membership.active_date.replace(tzinfo=None) if membership.active_date.tzinfo else membership.active_date
        expiration_date = membership.expiration_date.replace(tzinfo=None) if membership.expiration_date.tzinfo else membership.expiration_date
        
        total_days = (expiration_date - active_date).days
        days_elapsed = (now - active_date).days
        
        if total_days > 0:
            cycle_percentage = round((days_elapsed / total_days) * 100)
            # Ensure percentage is between 0 and 100
            cycle_percentage = max(0, min(100, cycle_percentage))
    except Exception:
        cycle_percentage = None
    
    # Prepare output data
    result = {
        "active_date": membership.active_date.isoformat(),
        "expiration_date": membership.expiration_date.isoformat(),
        "class_count": membership.count,
        "classes_remaining": membership.remaining,
        "next_booking_date": next_booking_date,
        "cycle_percentage": cycle_percentage
    }
    
    return result


def main():
    """Main function to run the script."""
    try:
        info = get_otf_info()
        print(json.dumps(info, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
