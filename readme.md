Simple script based on otf-api to pull basic data from your OrangeTheory account. I run this on a cronjob to update my OTF data in Home Assistant.

Instructions:
1. `pip install otf-api` (or skip this to use `uv`)
2. Set the following environment variables:
  - OTF_EMAIL: your OTF email address
  - OTF_PASSWORD: your OTF password
  - HA_TOKEN: Home Assistant long lived access token (for sending to home assistant)
  - HA_URL: Home Assistant URL (for sending to home assistant)
3. Run `python otf_membership_info.py` to get a membership info printed as json
  - Or if you're using uv, run `uv run --with otf-api python3 otf_membership_info.py`
  - The JSON looks like this:
```json
{
  "active_date": "2025-06-25T00:00:00",
  "expiration_date": "2025-07-25T00:00:00",
  "class_count": 8,
  "classes_remaining": 4,
  "next_booking_date": "2025-07-18T16:15:00",
  "cycle_percentage": 50
}
```
4. Run `python otf_to_homeassistant.py` to send info to home assistant using the previously defined environment variables
  - Or with uv, run `uv run --with otf-api python3 otf_to_homeassistant.py`
5. Run this on a crontab to send to home assistant at regular intervals
