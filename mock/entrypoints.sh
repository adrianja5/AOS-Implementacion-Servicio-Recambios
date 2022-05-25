#!/bin/sh

node dist/index.js mock --cors -h 0.0.0.0 "/recambios/openapi.yaml" &

rc-service nginx start

wait -n

fg %1