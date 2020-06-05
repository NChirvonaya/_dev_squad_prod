#! /bin/bash

flask db init || true
flask db upgrade
flask db migrate -m 'init' || true \
flask db upgrade

flask run