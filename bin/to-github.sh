#!/bin/bash

# Check if an argument was provided
if [ -z "$1" ]; then
  echo "Usage: $0 <username/repository>"
  echo "Example: $0 kriwil/kriwilcom"
  exit 1
fi

# Define the new origin URL
NEW_ORIGIN="git@github.com:$1.git"

# 1. Remove all existing remotes
# We use a loop to ensure every single remote is cleared
remotes=$(git remote)
for remote in $remotes; do
  git remote remove "$remote"
done

# 2. Add the new origin
git remote add origin "$NEW_ORIGIN"

# 3. Success message
echo "All remotes removed."
echo "Added new origin: $NEW_ORIGIN"
git remote -v
