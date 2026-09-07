import argparse
import os
from urllib.parse import urlsplit

from alembic.config import Config
from dotenv import load_dotenv

from alembic import command


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recreate the database using the complete Alembic migration chain."
    )
    parser.add_argument(
        "--yes-i-really-mean-it",
        action="store_true",
        help="Confirm that every application table may be deleted.",
    )
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()

    if not args.yes_i_really_mean_it:
        raise SystemExit("Reset cancelled: explicit confirmation flag is required.")

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise SystemExit("Reset cancelled: DATABASE_URL is not configured.")

    hostname = urlsplit(database_url).hostname
    local_hosts = {"localhost", "127.0.0.1", "::1"}
    if hostname not in local_hosts and os.getenv("ALLOW_DATABASE_RESET") != "1":
        raise SystemExit(
            "Reset cancelled: remote databases require ALLOW_DATABASE_RESET=1."
        )

    alembic_config = Config("alembic.ini")
    command.downgrade(alembic_config, "base")
    command.upgrade(alembic_config, "head")


if __name__ == "__main__":
    main()
