# `alembic.ini` and `py.typed`

Sources: [alembic.ini](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/alembic.ini), [py.typed](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/py.typed). Inspected 1.1.4, 2026-10-07.

alembic.ini supplies logging sections only: root INFO with console, sqlalchemy.engine WARNING, alembic INFO, stderr StreamHandler and generic level/name/message formatter. There is no bundled [alembic] database URL or script_location in this file. CLI creates Config from it then sets script_location; migration env obtains URL from DATABASE_URL and calls fileConfig if valid ini path. Verbose option can raise engine logger to INFO afterward. No handlers redact credentials or arbitrary parameter data. These are configuration values, not executable functions or schema revisions.

py.typed is an empty PEP 561 marker communicating that package distributes typing information. It performs no validation/runtime action and declares no API. Generated .pyi files under types/compat provide static signatures, while protobuf generation supplies runtime classes. Marker presence does not mean imports of optional integrations will succeed, and type annotations do not enforce task authorization or wire validity.

The namespace package has no root __init__.py; there are no root README examples beyond the files inventoried here. Bytecode __pycache__ is explicitly excluded. SHA-256 inventory includes ini and empty marker so non-Python files are not silently skipped.
