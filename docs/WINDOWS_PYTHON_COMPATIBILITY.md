# Windows / Python 3.14 Compatibility

PhishLens 2.0 is tested around a Python 3.14 Windows setup using binary wheels.
The PostgreSQL driver is pinned to `psycopg[binary]==3.3.6`, which publishes a
CPython 3.14 Windows x86-64 wheel. The launcher installs requirements with
`--only-binary=:all:` so it does not fall back to local C/C++ compilation.
