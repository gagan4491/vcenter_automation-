#!/bin/bash

su - nagios << EOF
rm -rf ~/.ssh/known_hosts
EOF

rm -rf ~/.ssh/known_hosts

exit 0