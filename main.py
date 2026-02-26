"""
Contact Automation System - Main CLI Entry Point
"""
import sys
import argparse
from pathlib import Path

from services.auth_service import configure
from services.database_service import DatabaseService
from services.google_drive_service import GoogleDriveService
from services.beat_parser_service import BeatParser
from services.beat_selection_service import BeatSelectionService
from services.email_template_service import EmailTemplateService
from services.gmail_service import GmailService
from utils.logger import setup_logger

logger = setup_logger(__name__)


def cmd_list_artists():
    """Fetch artists from vault folder and display them."""
    print("\n[INFO] Fetching artists from Google Drive vault folder...")
    try:
        drive = GoogleDriveService()
        artists = drive.get_folder_permissions()
    except Exception as e:
        print(f"[ERROR] Failed to fetch artists: {e}")
        return 1

    if not artists:
        print("[WARN] No artists found with access to the vault folder.")
        return 0

    # Sync to database for later use
    db = DatabaseService()
    for a in artists:
        try:
            db.add_artist(a["name"], a["email"])
        except Exception:
            pass  # already exists
    db.close()

    try:
        from tabulate import tabulate
        rows = [[a["name"], a["email"]] for a in artists]
        print(tabulate(rows, headers=["Name", "Email"], tablefmt="simple"))
    except ImportError:
        for a in artists:
            print(f"  {a['name']} <{a['email']}>")

    print(f"\n[OK] Total: {len(artists)} artists")
    return 0


def cmd_show_history(limit: int = 50):
    """Display email sending history."""
    db = DatabaseService()
    history = db.get_email_history(limit=limit)
    db.close()

    if not history:
        print("\n[INFO] No email history yet.")
        return 0

    try:
        from tabulate import tabulate
        rows = []
        for h in history:
            beats_str = ",".join(str(b) for b in h["beats_sent"])
            rows.append([
                h.get("artist_name", ""),
                h.get("artist_email", ""),
                h["timestamp"][:19] if h.get("timestamp") else "",
                h["pack_number"],
                beats_str,
                h["status"],
            ])
        print(tabulate(rows, headers=["Artist", "Email", "Timestamp", "Pack", "Beats", "Status"], tablefmt="simple"))
    except ImportError:
        for h in history:
            print(h)

    print(f"\n[OK] Showing last {len(history)} records")
    return 0


def cmd_check_beats():
    """List all beats in vault and show which need filename formatting."""
    print("\n[INFO] Fetching beat files from vault...")
    try:
        drive = GoogleDriveService()
        files = drive.list_beat_files()
    except Exception as e:
        print(f"[ERROR] Failed to fetch beats: {e}")
        return 1

    if not files:
        print("[WARN] No MP3 files found in vault.")
        return 0

    valid = []
    need_format = []
    required_format = "@zobi - [Beat Name] - [BPM] - [Key] - [Artist/Style].mp3"

    for f in files:
        name = f.get("name", "")
        parsed = BeatParser.parse_filename(name)
        if parsed:
            valid.append(name)
        else:
            # Suggest fix: common issue is Key-BPM order (e.g. "Eb min - 105" should be "105 - Eb min")
            suggested = _suggest_beat_rename(name)
            need_format.append((name, suggested))

    print(f"\n[OK] Total: {len(files)} beats | Valid format: {len(valid)} | Need formatting: {len(need_format)}")
    print(f"\nRequired format: {required_format}")
    print("  Order: Beat Name - BPM (number) - Key - Style\n")

    if valid:
        print("--- Beats with correct format ---")
        for n in sorted(valid):
            print(f"  [OK] {n}")
    if need_format:
        print("\n--- Beats that need formatting (rename in Drive) ---")
        try:
            from tabulate import tabulate
            rows = [[cur, sug or "(fix order: BPM then Key, then Style)"[:40]] for cur, sug in need_format]
            print(tabulate(rows, headers=["Current filename", "Suggested rename"], tablefmt="simple"))
        except ImportError:
            for cur, sug in need_format:
                print(f"  Current: {cur}")
                if sug:
                    print(f"  Suggest: {sug}")
                print()
    return 0


def _suggest_beat_rename(filename: str):
    """Suggest a corrected filename. Returns None if no suggestion."""
    if not filename.startswith("@") or ".mp3" not in filename.lower():
        return None
    base = filename.replace(".mp3", "").replace(".MP3", "").strip()
    parts = [p.strip() for p in base.split(" - ") if p.strip()]
    # Expect: @zobi, BeatName, BPM, Key, Style (5 parts) or 4 if no style
    if len(parts) < 4:
        return None
    prefix = producer if producer.startswith("@") else f"@{producer}"
    # If second part is digits (BPM) and third is not, order might be correct but missing style
    # If second part is not digits and third is, likely Key - BPM - Style -> suggest BPM - Key - Style
    if len(parts) >= 5:
        producer, beat_name, a, b, style = parts[0], parts[1], parts[2], parts[3], parts[4]
        if a.isdigit() and not b.isdigit():
            return None  # Already BPM - Key
        if not a.isdigit() and b.isdigit():
            # Key - BPM order
            return f"{prefix} - {beat_name} - {b} - {a} - {style}.mp3"
    if len(parts) == 4:
        producer, beat_name, a, b = parts[0], parts[1], parts[2], parts[3]
        if a.isdigit() and not b.isdigit():
            return f"{prefix} - {beat_name} - {a} - {b} - [STYLE].mp3"  # Add style
        if not a.isdigit() and b.isdigit():
            return f"{prefix} - {beat_name} - {b} - {a} - [STYLE].mp3"
    return None


def cmd_send_beats(dry_run: bool = False):
    """Send beat packs to all artists."""
    print("\n" + "=" * 60)
    print("Contact Automation - Send Beats")
    print("=" * 60)

    if dry_run:
        print("[DRY RUN] No emails will be sent.\n")

    try:
        drive = GoogleDriveService()
        db = DatabaseService()
        beat_selector = BeatSelectionService.from_config(db)
        email_tpl = EmailTemplateService()
        config_path = Path(__file__).parent / "config" / "config.yaml"
        import yaml
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        subject_tpl = config["email"]["subject_template"]
        agreement_path = Path(__file__).parent / config["email"]["agreement_path"]
    except Exception as e:
        print(f"[ERROR] Initialization failed: {e}")
        return 1

    # 1. Fetch artists
    print("[1/5] Fetching artists...")
    try:
        artists = drive.get_folder_permissions()
    except Exception as e:
        print(f"[ERROR] Failed to fetch artists: {e}")
        return 1
    if not artists:
        print("[WARN] No artists found. Exiting.")
        return 0

    for a in artists:
        try:
            db.add_artist(a["name"], a["email"])
        except Exception:
            pass
    print(f"      Found {len(artists)} artists.")

    # 2. Fetch and sync beats
    print("[2/5] Fetching beats from vault...")
    try:
        drive_files = drive.list_beat_files()
    except Exception as e:
        print(f"[ERROR] Failed to list beats: {e}")
        return 1
    if not drive_files:
        print("[ERROR] No MP3 files found in vault.")
        return 1

    file_id_by_name = {f["name"]: f["id"] for f in drive_files}
    for f in drive_files:
        parsed = BeatParser.parse_filename(f["name"])
        if parsed:
            try:
                db.add_beat(
                    filename=f["name"],
                    beat_name=parsed["beat_name"],
                    bpm=BeatParser.parse_bpm(parsed["bpm"]),
                    key=parsed.get("key"),
                    style_category=parsed.get("style_category"),
                    file_type=parsed.get("file_type", "mp3"),
                    file_size=int(f["size"]) if f.get("size") else None,
                )
            except Exception:
                pass
    print(f"      Found {len(drive_files)} beats.")

    # 3. Load agreement
    print("[3/5] Loading Beat Agreement...")
    if not agreement_path.exists():
        print(f"[WARN] Agreement file not found: {agreement_path}")
        agreement_content = b""
    else:
        agreement_content = agreement_path.read_text(encoding="utf-8").encode("utf-8")
    print("      Done.")

    # 4. Gmail service (only if not dry run)
    gmail = None
    if not dry_run:
        try:
            gmail = GmailService.from_config()
        except Exception as e:
            print(f"[ERROR] Gmail init failed: {e}")
            return 1

    # 5. Send to each artist
    print("[4/5] Preparing and sending emails...")
    results = []
    for i, a in enumerate(artists):
        artist = db.get_artist_by_email(a["email"])
        if not artist:
            continue
        artist_id = artist["id"]
        pack_number = artist["last_pack_number"] + 1
        beat_ids = beat_selector.select_beats_for_artist(artist_id)
        if not beat_ids:
            results.append((a["name"], a["email"], "SKIP", "No beats selected"))
            continue

        beats_data = db.get_beats_by_ids(beat_ids)
        beat_names = [b["beat_name"] for b in beats_data]
        body = email_tpl.generate_body(a["name"], beat_names)
        subject = subject_tpl.replace("{pack_number}", str(pack_number))

        if dry_run:
            results.append((a["name"], a["email"], "DRY", f"Pack #{pack_number}, {len(beat_ids)} beats"))
            continue

        # Build attachments: agreement + beat files
        attachments = [{"filename": "Beat_Usage_Agreement.txt", "content": agreement_content}]
        for b in beats_data:
            fn = b["filename"]
            fid = file_id_by_name.get(fn)
            if fid:
                try:
                    content = drive.download_file(fid)
                    attachments.append({"filename": fn, "content": content})
                except Exception as ex:
                    logger.warning(f"Could not download {fn}: {ex}")

        sent_id = gmail.send_email(to=a["email"], subject=subject, body=body, attachments=attachments)
        if sent_id:
            db.add_email_history(artist_id, pack_number, beat_ids, "sent")
            for bid in beat_ids:
                db.add_artist_beat_history(artist_id, bid)
            db.update_artist_pack_number(artist_id, pack_number)
            results.append((a["name"], a["email"], "SENT", f"Pack #{pack_number}"))
        else:
            db.add_email_history(artist_id, pack_number, beat_ids, "failed", "Send failed")
            results.append((a["name"], a["email"], "FAIL", "Send failed"))

        gmail.apply_rate_limit(i)

    db.close()

    # Summary
    print("[5/5] Summary")
    print("-" * 60)
    try:
        from tabulate import tabulate
        print(tabulate(results, headers=["Artist", "Email", "Status", "Detail"], tablefmt="simple"))
    except ImportError:
        for r in results:
            print(f"  {r[0]} | {r[1]} | {r[2]} | {r[3]}")
    sent_count = sum(1 for r in results if r[2] == "SENT")
    print(f"\n[OK] Sent: {sent_count}, Total: {len(results)}")
    return 0


def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(
        description="Contact Automation System - Automate beat distribution to artists"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("configure", help="Set up Google API authentication")
    send_parser = subparsers.add_parser("send-beats", help="Send beats to all artists")
    send_parser.add_argument("--dry-run", action="store_true", help="Test run without sending emails")
    history_parser = subparsers.add_parser("show-history", help="Display sending history")
    history_parser.add_argument("-n", "--limit", type=int, default=50, help="Max records to show")
    subparsers.add_parser("list-artists", help="List all artists in vault folder")
    subparsers.add_parser("check-beats", help="List beats that need filename formatting")

    args = parser.parse_args()

    if args.command == "configure":
        success = configure()
        return 0 if success else 1
    if args.command == "list-artists":
        return cmd_list_artists()
    if args.command == "show-history":
        return cmd_show_history(limit=getattr(args, "limit", 50))
    if args.command == "send-beats":
        return cmd_send_beats(dry_run=getattr(args, "dry_run", False))
    if args.command == "check-beats":
        return cmd_check_beats()
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
