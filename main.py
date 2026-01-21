"""
Contact Automation System - Main CLI Entry Point
"""
import sys
import argparse
from services.auth_service import configure

def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(
        description='Contact Automation System - Automate beat distribution to artists'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Configure command
    configure_parser = subparsers.add_parser(
        'configure',
        help='Set up Google API authentication'
    )

    # Send beats command (placeholder)
    send_parser = subparsers.add_parser(
        'send-beats',
        help='Send beats to all artists'
    )
    send_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Test run without sending emails'
    )

    # Show history command (placeholder)
    history_parser = subparsers.add_parser(
        'show-history',
        help='Display sending history'
    )

    # List artists command (placeholder)
    artists_parser = subparsers.add_parser(
        'list-artists',
        help='List all artists in vault folder'
    )

    args = parser.parse_args()

    # Handle commands
    if args.command == 'configure':
        success = configure()
        return 0 if success else 1
    elif args.command == 'send-beats':
        print("🚧 send-beats command - Coming soon!")
        print("   This will send beats to all artists.")
        if args.dry_run:
            print("   (Dry run mode - no emails will be sent)")
        return 0
    elif args.command == 'show-history':
        print("🚧 show-history command - Coming soon!")
        print("   This will display email sending history.")
        return 0
    elif args.command == 'list-artists':
        print("🚧 list-artists command - Coming soon!")
        print("   This will list all artists in your vault folder.")
        return 0
    else:
        # No command provided, show help
        parser.print_help()
        return 0

if __name__ == "__main__":
    sys.exit(main())
