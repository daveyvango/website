#!/bin/bash
rsync -ru /usr/share/nginx/html/django/static/blog/ personalpage/blog/static/blog/ --stats --dry-run | grep 'Number of regular files transferred: 0'
FILES_TRNSFD_COUNT=$?

echo "\"$FILES_TRNSFD_COUNT\""
if [[ "$FILES_TRNSFD_COUNT" == "0" ]]; then
  echo "There are no files to sync"
  exit 0
else
  echo "-----------------------------------"
  echo "Pre-commit hook failed             "
  echo "  - Static iles are out of sync    "
  echo "-----------------------------------"
  echo
  echo "Make sure you sync any uploaded data!"
  echo "Hint:"
  echo
  echo "rsync -ru /usr/share/nginx/html/django/static/blog/ personalpage/blog/static/blog/"
fi
