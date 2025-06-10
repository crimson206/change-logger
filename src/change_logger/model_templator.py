from .models import (
    ChangelogContext, ParsedCommit
)

context = ChangelogContext()

context.history.released

context.repo_name
context.repo_owner
context.hvcs_type

context.history
context.history.unreleased
context.history.released


context.repo_name
context.history.unreleased.keys()

commit = ParsedCommit()
commit.body