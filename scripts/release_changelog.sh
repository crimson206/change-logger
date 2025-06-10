#!/bin/bash

# @description: Create GitHub release with entire CHANGELOG.md as release notes
# @arg version: Release version (e.g., v1.0.0, 1.2.3)
# @option changelog,c [default=CHANGELOG.md]: Path to changelog file
# @option prerelease,p [flag]: Mark as pre-release
# @option draft,d [flag]: Create as draft release
# @option assets,a [optional]: Glob pattern for assets to attach (e.g., "dist/*")
# @option title,t [optional]: Custom release title (defaults to version)

# USER SETTING
# Customize these settings as needed
DEFAULT_BRANCH="main"
REPO_ROOT="."

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI (gh) is not installed"
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not in a git repository"
    exit 1
fi

# Normalize version (add 'v' prefix if not present)
if [[ "$VERSION" =~ ^[0-9] ]]; then
    VERSION="v$VERSION"
fi

# Check if changelog file exists
if [ ! -f "$CHANGELOG" ]; then
    echo "Error: Changelog file '$CHANGELOG' not found"
    exit 1
fi

# Set release title
RELEASE_TITLE="${TITLE:-$VERSION}"

# Prepare release command
RELEASE_CMD="gh release create \"$VERSION\""
RELEASE_CMD="$RELEASE_CMD --title \"$RELEASE_TITLE\""
RELEASE_CMD="$RELEASE_CMD --notes-file \"$CHANGELOG\""

# Add flags if specified
if [ "$PRERELEASE" = "1" ]; then
    RELEASE_CMD="$RELEASE_CMD --prerelease"
fi

if [ "$DRAFT" = "1" ]; then
    RELEASE_CMD="$RELEASE_CMD --draft"
fi

# Add assets if specified
if [ -n "$ASSETS" ]; then
    RELEASE_CMD="$RELEASE_CMD $ASSETS"
fi

# Check if tag already exists
if git tag -l | grep -q "^$VERSION$"; then
    echo "Warning: Tag '$VERSION' already exists"
    read -p "Do you want to continue and create release for existing tag? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted"
        exit 1
    fi
else
    # Create and push tag
    echo "Creating tag '$VERSION'..."
    git tag -a "$VERSION" -m "Release $VERSION"
    
    echo "Pushing tag to origin..."
    git push origin "$VERSION"
fi

# Show what we're about to do
echo "Creating GitHub release:"
echo "  Version: $VERSION"
echo "  Title: $RELEASE_TITLE"
echo "  Changelog: $CHANGELOG"
echo "  Prerelease: $PRERELEASE"
echo "  Draft: $DRAFT"
if [ -n "$ASSETS" ]; then
    echo "  Assets: $ASSETS"
fi
echo

# Confirm before proceeding
if [ "$DRAFT" != "1" ]; then
    read -p "Proceed with creating the release? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted"
        exit 1
    fi
fi

# Execute the release command
echo "Creating release..."
eval $RELEASE_CMD

if [ $? -eq 0 ]; then
    echo "✅ Release '$VERSION' created successfully!"
    echo "🔗 View at: https://github.com/$(gh repo view --json owner,name -q '.owner.login + "/" + .name')/releases/tag/$VERSION"
else
    echo "❌ Failed to create release"
    exit 1
fi