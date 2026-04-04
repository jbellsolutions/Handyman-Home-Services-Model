#!/usr/bin/env python3
"""
Financial Report Generator — Home Services Business OS

Generates P&L reports, payout calculations, and ROI analysis.
Works with ClickUp Finance lists (via MCP) or standalone from local data.

Usage:
    python ops/scripts/financial-report.py --period current     # Current biweekly period
    python ops/scripts/financial-report.py --period monthly      # This month
    python ops/scripts/financial-report.py --payout              # Calculate biweekly payout
    python ops/scripts/financial-report.py --roi                 # Channel ROI breakdown

Note: This script is primarily used by Claude Code via natural language
("P&L this month", "calculate payout"). It can also run standalone
for manual reporting.
"""
import argparse
import os
import sys
import yaml
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
OPS_CONFIG = ROOT / 'ops' / 'config' / 'ops-settings.yaml'


def load_ops_config():
    """Load ops settings."""
    if OPS_CONFIG.exists():
        with open(OPS_CONFIG) as f:
            return yaml.safe_load(f)
    return {}


def get_period_dates(period_type='current'):
    """Get start and end dates for the reporting period."""
    today = datetime.now()

    if period_type == 'monthly':
        start = today.replace(day=1)
        if today.month == 12:
            end = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        return start, end, f"{today.strftime('%B %Y')}"

    elif period_type == 'current':
        # Biweekly: find the most recent Friday as period start
        days_since_friday = (today.weekday() - 4) % 7
        last_friday = today - timedelta(days=days_since_friday)
        # Go back another week if we're in the first week
        if days_since_friday <= 7:
            period_start = last_friday - timedelta(days=7)
        else:
            period_start = last_friday
        period_end = period_start + timedelta(days=13)
        return period_start, period_end, f"{period_start.strftime('%b %d')} — {period_end.strftime('%b %d, %Y')}"

    elif period_type == 'weekly':
        start = today - timedelta(days=today.weekday())  # Monday
        end = start + timedelta(days=6)
        return start, end, f"Week of {start.strftime('%b %d, %Y')}"

    return today - timedelta(days=30), today, "Last 30 days"


def generate_pnl(revenue_items, expense_items, config, period_label):
    """Generate a P&L report from revenue and expense data."""
    total_revenue = sum(item.get('amount', 0) for item in revenue_items)

    # Break down expenses by category
    expense_categories = {}
    for item in expense_items:
        cat = item.get('category', 'Other')
        expense_categories[cat] = expense_categories.get(cat, 0) + item.get('amount', 0)
    total_expenses = sum(expense_categories.values())

    net_profit = total_revenue - total_expenses

    # Get split percentages
    financials = config.get('business_os', {}).get('financials', {})
    split_marketing = financials.get('split_marketing', 0.35)
    split_field = financials.get('split_field', 0.65)

    marketing_name = config.get('business_os', {}).get('team', {}).get('marketing_ops', {}).get('name', 'Marketing Partner')
    field_name = config.get('business_os', {}).get('team', {}).get('field_lead', {}).get('name', 'Field Partner')

    marketing_share = net_profit * split_marketing
    field_share = net_profit * split_field

    # Revenue by service type
    revenue_by_service = {}
    for item in revenue_items:
        svc = item.get('service_type', 'Unknown')
        revenue_by_service[svc] = revenue_by_service.get(svc, 0) + item.get('amount', 0)

    # Revenue by channel
    revenue_by_channel = {}
    for item in revenue_items:
        ch = item.get('channel', 'Unknown')
        revenue_by_channel[ch] = revenue_by_channel.get(ch, 0) + item.get('amount', 0)

    report = f"""
{'='*60}
  P&L REPORT — {period_label}
{'='*60}

  REVENUE
  {'—'*50}
  Total Revenue:                          ${total_revenue:,.2f}
"""

    if revenue_by_service:
        report += "\n  By Service:\n"
        for svc, amt in sorted(revenue_by_service.items(), key=lambda x: -x[1]):
            report += f"    {svc:<35} ${amt:>10,.2f}\n"

    if revenue_by_channel:
        report += "\n  By Lead Source:\n"
        for ch, amt in sorted(revenue_by_channel.items(), key=lambda x: -x[1]):
            report += f"    {ch:<35} ${amt:>10,.2f}\n"

    report += f"""
  EXPENSES
  {'—'*50}
  Total Expenses:                         ${total_expenses:,.2f}
"""

    for cat, amt in sorted(expense_categories.items(), key=lambda x: -x[1]):
        report += f"    {cat:<35} ${amt:>10,.2f}\n"

    report += f"""
  {'='*50}
  NET PROFIT:                             ${net_profit:,.2f}
  {'='*50}

  PARTNER SPLIT
  {'—'*50}
  {marketing_name} ({split_marketing*100:.0f}%):{'':>20} ${marketing_share:>10,.2f}
  {field_name} ({split_field*100:.0f}%):{'':>20} ${field_share:>10,.2f}

  Jobs completed:                         {len(revenue_items)}
  Average job value:                      ${total_revenue/max(len(revenue_items),1):,.2f}
"""

    return report


def generate_payout(revenue_items, expense_items, config, period_label):
    """Generate biweekly payout calculation."""
    total_revenue = sum(item.get('amount', 0) for item in revenue_items)
    total_expenses = sum(item.get('amount', 0) for item in expense_items)
    net_profit = total_revenue - total_expenses

    financials = config.get('business_os', {}).get('financials', {})
    split_marketing = financials.get('split_marketing', 0.35)
    split_field = financials.get('split_field', 0.65)

    marketing_name = config.get('business_os', {}).get('team', {}).get('marketing_ops', {}).get('name', 'Marketing Partner')
    field_name = config.get('business_os', {}).get('team', {}).get('field_lead', {}).get('name', 'Field Partner')

    report = f"""
{'='*60}
  BIWEEKLY PAYOUT — {period_label}
{'='*60}

  Gross Revenue:        ${total_revenue:>10,.2f}
  Total Expenses:       ${total_expenses:>10,.2f}
  Net Profit:           ${net_profit:>10,.2f}

  PAYOUTS:
  {'—'*40}
  {marketing_name} ({split_marketing*100:.0f}%):   ${net_profit * split_marketing:>10,.2f}
  {field_name} ({split_field*100:.0f}%):   ${net_profit * split_field:>10,.2f}

  Jobs this period: {len(revenue_items)}
"""

    return report


def generate_roi(revenue_items, expense_items, config, period_label):
    """Generate channel ROI analysis."""
    # Marketing spend by channel
    marketing_spend = {}
    for item in expense_items:
        if item.get('category', '').lower() in ('marketing', 'advertising', 'craigslist', 'ads'):
            ch = item.get('channel', 'Marketing')
            marketing_spend[ch] = marketing_spend.get(ch, 0) + item.get('amount', 0)

    # Revenue by channel
    revenue_by_channel = {}
    leads_by_channel = {}
    for item in revenue_items:
        ch = item.get('channel', 'Unknown')
        revenue_by_channel[ch] = revenue_by_channel.get(ch, 0) + item.get('amount', 0)
        leads_by_channel[ch] = leads_by_channel.get(ch, 0) + 1

    report = f"""
{'='*60}
  CHANNEL ROI ANALYSIS — {period_label}
{'='*60}

  {'Channel':<20} {'Leads':>6} {'Revenue':>10} {'Spend':>10} {'ROI':>8}
  {'—'*58}
"""

    all_channels = set(list(revenue_by_channel.keys()) + list(marketing_spend.keys()))
    for ch in sorted(all_channels):
        rev = revenue_by_channel.get(ch, 0)
        spend = marketing_spend.get(ch, 0)
        leads = leads_by_channel.get(ch, 0)
        roi = ((rev - spend) / spend * 100) if spend > 0 else 0
        roi_str = f"{roi:.0f}%" if spend > 0 else "N/A"
        report += f"  {ch:<20} {leads:>6} ${rev:>9,.2f} ${spend:>9,.2f} {roi_str:>8}\n"

    total_rev = sum(revenue_by_channel.values())
    total_spend = sum(marketing_spend.values())
    total_leads = sum(leads_by_channel.values())
    cost_per_lead = total_spend / max(total_leads, 1)

    report += f"""
  {'—'*58}
  {'TOTAL':<20} {total_leads:>6} ${total_rev:>9,.2f} ${total_spend:>9,.2f}

  Cost per lead:    ${cost_per_lead:,.2f}
  Cost per job:     ${total_spend / max(len(revenue_items), 1):,.2f}
"""

    return report


def main():
    parser = argparse.ArgumentParser(description='Financial Report Generator')
    parser.add_argument('--period', choices=['current', 'monthly', 'weekly'], default='current',
                        help='Reporting period')
    parser.add_argument('--payout', action='store_true', help='Generate payout calculation')
    parser.add_argument('--roi', action='store_true', help='Generate channel ROI analysis')
    parser.add_argument('--demo', action='store_true', help='Run with sample data')
    args = parser.parse_args()

    config = load_ops_config()
    start, end, period_label = get_period_dates(args.period)

    if args.demo:
        # Sample data for demonstration
        revenue_items = [
            {'amount': 350, 'service_type': 'Roof Repair', 'channel': 'Craigslist'},
            {'amount': 250, 'service_type': 'Wildlife Removal', 'channel': 'Craigslist'},
            {'amount': 500, 'service_type': 'Handyman', 'channel': 'Facebook'},
            {'amount': 400, 'service_type': 'Property Maintenance', 'channel': 'Nextdoor'},
            {'amount': 300, 'service_type': 'Handyman', 'channel': 'Craigslist'},
            {'amount': 450, 'service_type': 'Roof Repair', 'channel': 'Google'},
            {'amount': 200, 'service_type': 'Wildlife Removal', 'channel': 'Referral'},
        ]
        expense_items = [
            {'amount': 420, 'category': 'Marketing', 'channel': 'Craigslist'},
            {'amount': 15, 'category': 'Marketing', 'channel': 'AvidTrak'},
            {'amount': 350, 'category': 'Materials'},
            {'amount': 800, 'category': 'Labor (Subcontractor)'},
            {'amount': 150, 'category': 'Insurance'},
        ]
    else:
        # In production, these would come from ClickUp via MCP
        # Claude Code calls this script and passes data, or reads from local DB
        print("\nNo data source configured. Run with --demo for sample report.")
        print("In production, Claude Code pulls data from ClickUp and passes it here.")
        print("\nUsage: python ops/scripts/financial-report.py --demo --period monthly")
        return

    if args.payout:
        print(generate_payout(revenue_items, expense_items, config, period_label))
    elif args.roi:
        print(generate_roi(revenue_items, expense_items, config, period_label))
    else:
        print(generate_pnl(revenue_items, expense_items, config, period_label))


if __name__ == '__main__':
    main()
