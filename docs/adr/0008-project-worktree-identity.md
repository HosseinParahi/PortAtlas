# ADR 0008: Project/worktree identity

- **Status:** Accepted
- **Date:** 2026-07-11
- **Scope:** Stable repository, checkout, worktree, and service ownership

## Context

Absolute paths change, linked Git worktrees share repository metadata, independent clones may share a remote, and monorepos contain multiple runnable services. Treating a path as the project identity would lose history after moves and collapse worktree-specific ports. Treating a remote URL as identity would incorrectly merge independent clones.

## Decision

Model logical repositories and runnable checkouts separately:

- A Project is the durable logical repository record.
- A Project has one or more ProjectInstance records.
- Each Git worktree or ordinary checkout is a distinct ProjectInstance with its own canonical root, Git directory, current revision, branch or detached state, scan state, declarations, runtime associations, reservations, and desired assignments.
- Linked worktrees that resolve to the same Git common directory belong to one Project.
- Independent clones are separate Projects by default even when their normalized remotes match. A user may explicitly group them.
- Project and ProjectInstance IDs are persisted opaque IDs. Neither is derived solely from an absolute path, branch name, remote URL, or current commit.
- Discovery records Git common-directory evidence, worktree metadata, normalized remotes, object format, root path, and filesystem evidence to reconcile moves without turning those values into public identifiers.
- Project policy provides defaults; a ProjectInstance can override approved worktree-specific ranges and reservations.
- Services live within a ProjectInstance so two worktrees can run the same logical service on different ports.
- Missing instances become stale before deletion. Ambiguous moves, copied repositories, changed remotes, and broken worktree links require user confirmation rather than automatic merging.
- Non-Git directories receive the same opaque Project and ProjectInstance identities and may be grouped only through explicit user action.

## Alternatives considered

### Absolute path identity

Paths are easy to inspect but change under rename, move, mount, and user-home differences.

### Remote URL identity

Remote URLs can change and credentials may appear in them. Separate clones of one remote can intentionally have independent state.

### Commit hash identity

Commits change continuously, detached worktrees are common, and different worktrees can point at the same commit.

### Treat each worktree as an unrelated project

This preserves runtime separation but loses shared policy, repository history, and the fact that linked worktrees share Git object storage and remotes.

## Consequences

### Positive

- Worktrees can run concurrently without overwriting each other's assignments.
- Shared repository policy and instance-specific runtime state are both representable.
- Moves and renames do not automatically destroy identity.
- Independent clones are not silently conflated.

### Costs and risks

- Reconciliation requires multiple evidence fields and an ambiguous-state workflow.
- Users see two related concepts that need clear UI language.
- A copied Git directory can resemble a moved instance.
- Paths and remotes remain sensitive metadata and require redaction.

## Verification

- Discover a normal repository, add two linked worktrees, and assert one Project with three ProjectInstance records.
- Run the same service from two worktrees and preserve separate declarations, observations, and reservations.
- Test detached HEAD, branch changes, remote URL changes, missing worktrees, repaired worktrees, repository moves, and copied repositories.
- Verify two independent clones of one remote remain separate without user grouping.
- Verify path or remote credentials are redacted from API, logs, MCP, AI context, and diagnostics.
- Add migration tests that preserve opaque IDs across path changes.

## Revisit triggers

- Git changes worktree metadata semantics used for reconciliation.
- Cross-machine synchronization becomes an approved feature.
- Team mode requires a portable repository identity shared between installations.
- User research shows the Project and ProjectInstance distinction cannot be explained clearly.

## Sources

- [Git worktree documentation](https://git-scm.com/docs/git-worktree)
- [Git rev-parse documentation](https://git-scm.com/docs/git-rev-parse)
- [Git repository layout](https://git-scm.com/docs/gitrepository-layout)
