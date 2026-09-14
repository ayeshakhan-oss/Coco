#!/usr/bin/env bash
# Deploy the Coco webapp to Railway, stamped with the commit it is serving.
#
# GitHub auto-deploy is not connected to this service: pushing to main builds
# nothing. Deploys go through the Railway CLI, which sets no git environment
# variables, so /healthz could not report which commit was live and "is it
# deployed?" had no answer. This writes the SHA into webapp/BUILD_SHA first,
# which `railway up` uploads with the rest of the build context.
#
# Usage:  bash scripts/deploy_webapp.sh
set -euo pipefail

cd "$(dirname "$0")/.."

SERVICE="elegant-benevolence"
URL="https://coco-production-bcc8.up.railway.app"

SHA="$(git rev-parse --short HEAD)"
DIRTY=""
if ! git diff --quiet || ! git diff --cached --quiet; then
  DIRTY="+dirty"
  echo "WARNING: the working tree has uncommitted changes. 'railway up' ships the"
  echo "         WORKING TREE, not the commit, so what goes live will not match $SHA."
fi

# Set the SHA as a service VARIABLE, not a file. `railway up` honours
# .gitignore, so a generated file that is (correctly) gitignored never reaches
# the builder - which is exactly how the first attempt at this silently failed.
railway variables --set "GIT_COMMIT_SHA=$SHA$DIRTY" --service "$SERVICE" --skip-deploys >/dev/null

echo "Deploying $SHA$DIRTY to $SERVICE ..."
railway up --detach --service "$SERVICE"

echo "Waiting for $SHA$DIRTY to serve ..."
for i in $(seq 1 40); do
  served="$(curl -s -m 15 "$URL/healthz" 2>/dev/null | sed -n 's/.*"commit":"\([^"]*\)".*/\1/p')"
  if [ "$served" = "$SHA$DIRTY" ]; then
    echo "LIVE after ~$((i * 15))s: $(curl -s -m 15 "$URL/healthz")"
    curl -s -m 15 "$URL/readyz"; echo
    exit 0
  fi
  sleep 15
done

echo "TIMED OUT after 10 minutes. Still serving: ${served:-<no commit field>}"
echo "The old build is still live. Check the Railway dashboard."
exit 1
