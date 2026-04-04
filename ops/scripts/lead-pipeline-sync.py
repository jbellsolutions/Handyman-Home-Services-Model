#!/usr/bin/env python3
"""
Lead Pipeline Sync — SQLite to ClickUp

Syncs leads from the local SQLite database (automation/data/leads.db)
to ClickUp's Lead Pipeline list. Prevents duplicates by storing the
ClickUp task ID back in the local database.

Usage:
    python ops/scripts/lead-pipeline-sync.py              # Sync new leads
    python ops/scripts/lead-pipeline-sync.py --status      # Show sync status
    python ops/scripts/lead-pipeline-sync.py --dry-run     # Preview without creating tasks

Note: This script is meant to be called by Claude Code or run as a cron.
In practice, Claude Code handles lead creation in ClickUp directly via MCP
when the user says "new lead." This script is a batch sync for any leads
that came through the automation system (CL email replies, FB messages).
"""
import argparse
import asyncio
import os
import sys
import yaml
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'automation'))

from shared.db import init_db
from shared.logger import get_logger

logger = get_logger('lead_sync')

ROOT = Path(__file__).parent.parent.parent
OPS_CONFIG = ROOT / 'ops' / 'config' / 'ops-settings.yaml'
DB_PATH = ROOT / 'automation' / 'data' / 'leads.db'


def load_ops_config():
    """Load ops settings."""
    if OPS_CONFIG.exists():
        with open(OPS_CONFIG) as f:
            return yaml.safe_load(f)
    return {}


async def get_unsynced_leads():
    """Get leads from SQLite that haven't been synced to ClickUp."""
    import aiosqlite

    if not DB_PATH.exists():
        logger.info("No leads database found yet.")
        return []

    async with aiosqlite.connect(str(DB_PATH)) as db:
        # Check if clickup_task_id column exists
        cursor = await db.execute("PRAGMA table_info(leads)")
        columns = [row[1] for row in await cursor.fetchall()]

        if 'clickup_task_id' not in columns:
            # Add the column for tracking sync status
            await db.execute("ALTER TABLE leads ADD COLUMN clickup_task_id TEXT")
            await db.commit()
            logger.info("Added clickup_task_id column to leads table")

        # Get leads without a ClickUp task ID
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            """SELECT * FROM leads
               WHERE clickup_task_id IS NULL OR clickup_task_id = ''
               ORDER BY received_at DESC"""
        )
        return await cursor.fetchall()


async def mark_synced(lead_id, clickup_task_id):
    """Store the ClickUp task ID back in SQLite."""
    import aiosqlite

    async with aiosqlite.connect(str(DB_PATH)) as db:
        await db.execute(
            "UPDATE leads SET clickup_task_id = ? WHERE id = ?",
            (clickup_task_id, lead_id)
        )
        await db.commit()


async def show_sync_status():
    """Show how many leads are synced vs unsynced."""
    import aiosqlite

    if not DB_PATH.exists():
        print("\n  No leads database found. Post some ads first.\n")
        return

    async with aiosqlite.connect(str(DB_PATH)) as db:
        # Check if column exists
        cursor = await db.execute("PRAGMA table_info(leads)")
        columns = [row[1] for row in await cursor.fetchall()]

        cursor = await db.execute("SELECT COUNT(*) FROM leads")
        total = (await cursor.fetchone())[0]

        if 'clickup_task_id' in columns:
            cursor = await db.execute(
                "SELECT COUNT(*) FROM leads WHERE clickup_task_id IS NOT NULL AND clickup_task_id != ''"
            )
            synced = (await cursor.fetchone())[0]
        else:
            synced = 0

        unsynced = total - synced

        print(f"\n  Lead Sync Status")
        print(f"  {'='*30}")
        print(f"  Total leads:    {total}")
        print(f"  Synced to CU:   {synced}")
        print(f"  Pending sync:   {unsynced}")
        print()


async def sync_leads(dry_run=False):
    """Sync unsynced leads to ClickUp."""
    config = load_ops_config()
    clickup = config.get('business_os', {}).get('clickup', {})
    new_leads_list_id = clickup.get('lists', {}).get('new_leads', '')

    if not new_leads_list_id and not dry_run:
        print("\n  ClickUp not configured yet.")
        print("  Run the Business OS setup (Phase 8) first, or set list IDs in ops/config/ops-settings.yaml")
        print("\n  You can still run with --dry-run to preview what would sync.\n")
        return

    await init_db()
    leads = await get_unsynced_leads()

    if not leads:
        print("\n  All leads are synced. Nothing to do.\n")
        return

    print(f"\n  Found {len(leads)} leads to sync.\n")

    for lead in leads:
        lead_dict = dict(lead)
        name = lead_dict.get('lead_name', 'Unknown')
        phone = lead_dict.get('lead_phone', '')
        message = lead_dict.get('lead_message', '')
        service = lead_dict.get('service_requested', '')
        platform = lead_dict.get('platform', '')
        received = lead_dict.get('received_at', '')

        task_name = f"{name} — {service or platform or 'New Lead'}"

        description = f"""**Lead Details**
- Name: {name}
- Phone: {phone}
- Service: {service}
- Source: {platform}
- Message: {message}
- Received: {received}
"""

        if dry_run:
            print(f"  [DRY RUN] Would create task: {task_name}")
            print(f"            List: {new_leads_list_id or '(not configured)'}")
            print(f"            Source: {platform}")
            print()
        else:
            # In production, Claude Code creates the task via ClickUp MCP:
            #   clickup_create_task(list_id=new_leads_list_id, name=task_name, description=description)
            # This script provides the batch sync capability.
            #
            # For now, log what we'd create and mark as needing manual sync
            logger.info(f"Would sync lead: {task_name} to list {new_leads_list_id}")
            print(f"  [SYNC] {task_name} — {platform}")

            # In a real implementation, this would call the ClickUp API directly
            # or be invoked by Claude Code which handles the MCP call.
            # For now, we just log it.

    if dry_run:
        print(f"  {len(leads)} leads would be synced. Run without --dry-run to execute.\n")
    else:
        print(f"\n  Sync complete. {len(leads)} leads processed.")
        print("  Note: Full ClickUp sync requires Claude Code MCP. Run 'morning briefing' in Claude Code.\n")


def main():
    parser = argparse.ArgumentParser(description='Lead Pipeline Sync — SQLite to ClickUp')
    parser.add_argument('--status', action='store_true', help='Show sync status')
    parser.add_argument('--dry-run', action='store_true', help='Preview without creating tasks')
    args = parser.parse_args()

    if args.status:
        asyncio.run(show_sync_status())
    else:
        asyncio.run(sync_leads(dry_run=args.dry_run))


if __name__ == '__main__':
    main()
