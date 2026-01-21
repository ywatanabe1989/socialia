#!/usr/bin/env python3
"""
Example 04: Google Analytics Integration

Demonstrates:
- Tracking custom events
- Querying page views
- Getting traffic sources

Usage:
    python 04_analytics.py

Environment:
    SOCIALIA_GOOGLE_ANALYTICS_MEASUREMENT_ID  - Required for tracking
    SOCIALIA_GOOGLE_ANALYTICS_API_SECRET      - Required for tracking
    SOCIALIA_GOOGLE_ANALYTICS_PROPERTY_ID     - Optional, for Data API queries
"""

from socialia import GoogleAnalytics


def main():
    ga = GoogleAnalytics()

    print("=== Google Analytics Demo ===\n")

    # 1. Track a custom event
    print("1. Tracking custom event...")
    result = ga.track_event(
        "example_demo",
        params={
            "demo_type": "analytics",
            "source": "socialia_examples",
        },
    )
    if result["success"]:
        print("   Event tracked successfully")
    else:
        print(f"   Event tracking failed: {result.get('error', 'Unknown')}")

    # 2. Get page views (requires Data API setup)
    print("\n2. Querying page views...")
    result = ga.get_page_views(start_date="7daysAgo", end_date="today")
    if result["success"]:
        print(f"   Date range: {result['date_range']}")
        pages = result.get("pages", [])
        if pages:
            print("   Top pages:")
            for page in pages[:5]:
                print(f"     {page['path']}: {page['page_views']} views")
        else:
            print("   No page data available")
    else:
        print(f"   Query failed: {result.get('error', 'Unknown')}")

    # 3. Get traffic sources
    print("\n3. Querying traffic sources...")
    result = ga.get_traffic_sources(start_date="7daysAgo", end_date="today")
    if result["success"]:
        sources = result.get("sources", [])
        if sources:
            print("   Top sources:")
            for src in sources[:5]:
                print(
                    f"     {src['source']}/{src['medium']}: {src['sessions']} sessions"
                )
        else:
            print("   No source data available")
    else:
        print(f"   Query failed: {result.get('error', 'Unknown')}")

    print("\n=== Demo Complete ===")
    return 0


if __name__ == "__main__":
    exit(main())
