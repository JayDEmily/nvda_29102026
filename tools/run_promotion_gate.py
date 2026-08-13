#!/usr/bin/env python3
import argparse
from pathlib import Path

from nvda_desk.architecture.promotion import run_promotion_set

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", default="architecture_kernel")
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    raise SystemExit(run_promotion_set(root, args.set, check_only=args.check_only))
