#!/bin/sh

set -e

git init

touch .git/hooks/pre-commit

chmod +x .git/hooks/pre-commit

echo '''
#!/bin/sh
make pre-commit
''' > .git/hooks/pre-commit
