# Contributing

Thank you for helping shape this project. The current repository is a pre-implementation documentation baseline, so contributions should preserve the accepted scope and traceability model.

## Before proposing a change

1. Read [AGENTS.md](AGENTS.md), the [product charter](docs/product/project-charter.md), and the relevant ADRs.
2. Use an issue to describe the problem, affected requirement IDs, expected tests, privacy impact, and managed-versus-unmanaged assurance impact.
3. Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md); never include secrets, tokens, private project contents, or exploit details in an issue.

## Pull requests

- Keep changes focused and link their product, requirement, ADR, and test references.
- Include verification evidence and update documentation in the same change.
- Confirm that examples and diagnostic output are redacted.
- Run `python3 scripts/validate_docs.py` and `git diff --check`.
- Preserve accessibility, offline behavior, and degradation guarantees.

## Developer Certificate of Origin

Contributions use the [Developer Certificate of Origin 1.1](https://developercertificate.org/). Add a sign-off to every commit:

```text
Signed-off-by: Your Name <your-address@example.com>
```

Create it with `git commit --signoff`. The sign-off certifies that you have the right to submit the contribution under the project license. The project does not require a relicensing contributor license agreement.

## License

Contributions accepted into this repository are licensed under Apache-2.0. Commercial use is permitted without payment under that license. Sponsorship is voluntary and does not affect usage permission.
