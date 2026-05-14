"""Future collection entry point for approved sources only.

This MVP scaffold intentionally does not run automatic collection.
"""

from __future__ import annotations


def main() -> None:
    print(
        "Collection is not enabled in this scaffold. Review sources in "
        "runtime/source_registry.csv and implement only A, B, or carefully "
        "reviewed C collectors."
    )


if __name__ == "__main__":
    main()

