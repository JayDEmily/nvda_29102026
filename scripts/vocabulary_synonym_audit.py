from nvda_desk.vocabulary_synonym_audit import (
    build_report as build_report,
)
from nvda_desk.vocabulary_synonym_audit import (
    main as main,
)
from nvda_desk.vocabulary_synonym_audit import (
    write_report as write_report,
)
from nvda_desk.vocabulary_synonym_audit import (
    write_stamp as write_stamp,
)

__all__ = ["build_report", "main", "write_report", "write_stamp"]

if __name__ == "__main__":
    raise SystemExit(main())
