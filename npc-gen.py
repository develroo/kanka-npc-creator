
#!/usr/bin/env python3

import argparse
import os
import sys
from Generator import NpcGenerator
from dotenv import load_dotenv
load_dotenv()

def validate_api_token():
    token = os.getenv("APITOKEN")
    if not token or len(token) < 30:
        sys.exit("❌ Error: API token is missing or looks invalid. Make sure APITOKEN=<token> is set in your .env file.")
    return token


def select_campaign(generator):
    campaigns = generator.get_campaigns().get("data", [])
    if not campaigns:
        sys.exit("❌ No campaigns found.")

    print("\nAvailable campaigns:")
    for idx, campaign in enumerate(campaigns):
        print(f"  [{idx}] {campaign['name']} (ID: {campaign['id']})")

    while True:
        try:
            choice = int(input("\nEnter the number of the campaign to use: "))
            if 0 <= choice < len(campaigns):
                return campaigns[choice]['name']
        except ValueError:
            pass
        print("Invalid choice. Try again.")


def main():
    parser = argparse.ArgumentParser(description="Generate random NPCs in a Kanka campaign.")
    parser.add_argument("--host", help="Set API base URL (e.g., https://kanka.example.com/api/1.0/)")
    parser.add_argument("--campaign", help="Specify campaign name directly")
    parser.add_argument("--count", type=int, help="Number of NPCs to generate", default=None)

    args = parser.parse_args()

    # Set host override if provided
    if args.host:
        os.environ["API_URL"] = args.host

    validate_api_token()
    generator = NpcGenerator()

    # Determine campaign name
    campaign_name = args.campaign or select_campaign(generator)

    # Determine NPC count
    count = args.count
    if count is None:
        try:
            count = int(input("Enter number of NPCs to generate: "))
        except ValueError:
            sys.exit("❌ Invalid number entered.")

    generator.create_npcs(campaign_name, count)


if __name__ == "__main__":
    main()
