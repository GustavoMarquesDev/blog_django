#!/bin/sh
set -e

/scripts/wait_psql.sh
/scripts/collectstatic.sh
/scripts/migrate.sh
/scripts/runserver.sh
