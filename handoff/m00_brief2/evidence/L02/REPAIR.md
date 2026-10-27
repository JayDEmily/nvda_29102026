# L02 requirement-relative repair

Baseline clean9e4977c strict m00_brief2 generation1:19passed/1failed, only N18; full original baseline-red.log preserved. The public valid UTCdatetime carrier was admitted by D139 API but failed SQLite append in _encode_native_value; valid projection and reopen were unreachable. The missing-carrier absence branch and all36/155 positives passed.

Minimal repair adds codec tag z for already-lawful UTC datetime, ASCII exact isoformat payload with existing length prefix, validated UTC/canonical decode. All existing tags and native payload bytes are unchanged. No record field, temporal law, identity law or provider-native time is invented; time.receipt remains collector-added. Existing same-ID native equality already compares datetime.isoformat exactly.

PostgreSQL implication inspected statically: _postgres.py has its own historical native codec and is not a user of changed _native_codec.py; its original supported-value code remains unchanged. It likewise lacks datetime encoding, a retained known limitation for future PostgreSQL deployment; no PostgreSQL parity or runtime certification is claimed. This SQLite-only repair does not worsen its existing supported representations. Historical native-type storage proof must be rerun once because the shared SQLite codec changed; no unrelated D signal suite.

Recovery uses same immutable Brief2 gen1 tests, not changed expectations. Independent reviewer must review exact source diff and run the same strict aggregate after material repair; original failure retained. A separate original raw SQLite aggregate run is justified only by codec's impact on original fidelity guarantees.
