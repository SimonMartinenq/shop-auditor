import argparse


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="shop-auditor")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("collect", "analyze", "audit"):
        sub.add_parser(name).add_argument("target")
    args = parser.parse_args(argv)
    parser.exit(1, f"{args.command}: not implemented yet\n")


if __name__ == "__main__":
    raise SystemExit(main())
