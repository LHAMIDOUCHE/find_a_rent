#!/usr/bin/env bash
dropdb --user postgres app 2>/dev/null
createdb --user postgres app
psql --user postgres app < /var/tmp/app.psql
