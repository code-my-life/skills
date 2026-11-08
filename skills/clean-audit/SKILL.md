---
name: clean-audit
description: "Audit a project against Clean Code and Clean Architecture (Robert C. Martin), on any stack: measurements, findings cited by heuristic, prioritized guardrail plan. Use when asked to audit code quality or architecture, to find what a project lacks in clean code or clean architecture, or to prepare quality gates (linters, architecture tests, hooks, CI) before installing them."
---

# clean-audit

Produce an audit document that says where a project departs from Clean Code and Clean Architecture, with evidence,
and which guardrail to install for each gap. The audit is read-only: installation follows from the owner's validation
of this document, never from the audit itself.

Every finding carries a **verdict**, which decides its future:
- **tool**: a program returns the same verdict for the same inputs; candidate for a linter, an architecture test, a
  hook, a CI check;
- **signal**: a program detects, a human decides; candidate for an advisory report, never for a blocking CI without
  human triage;
- **guideline**: pure judgment; candidate for a line in CLAUDE.md, AGENTS.md or a skill, never for a gate.

## References

- `references/clean-code-heuristics.md`: the 66 coded heuristics of chapter 17, the numeric thresholds and the
  chapter rules, each with its verdict. Load it for the code pass (step 3).
- `references/architecture-rules.md`: the 21 dependency-graph rules (SOLID included), the I/A/D metrics, the
  enforcement hierarchy and the tools per stack. Load it for the architecture pass (step 4) and for the plan (step 5).
- `references/calibration.md`: thresholds as preferences, calibration on the existing code, the bare minimum for a
  small project, the books' own tolerances. Load it before writing the plan (step 5).

## Process

1. **Observe.** The stack (languages, frameworks, package manager), the tooling in place (formatter, linter,
   typecheck, tests, git hooks, CI, agent instructions: CLAUDE.md, AGENTS.md, rules), the folder structure and the
   project size. The step is done when the inventory of the tooling in place is written: the audit completes what
   exists, it does not rediscover it as duplicates.
2. **Measure.** Function and file sizes, nesting depth, argument counts, duplication, coverage when it exists, and
   the dependency graph: cycles, edge direction between layers, I/A/D per component when the project has components.
   Every number comes from a reproducible command, written next to it. The step is done when every measurement in the
   report has its command.
3. **Code findings.** Walk the code with the heuristics catalog. A finding cites: the heuristic code (G5, F1, N5...),
   an example as file:line, the measurement when there is one, the verdict. The step is done when every tool or
   signal heuristic of the catalog has been considered on this project: violated with evidence, respected, or not
   applicable to this stack.
4. **Architecture findings.** Apply the 21 graph rules, same format: rule number, offending edge or module, verdict.
   On a project without declared layers, the first card of the plan is the layer declaration: the paths-to-circles
   mapping, validated by the owner.
5. **Plan.** One card per guardrail, prioritized by effect on the project then by cost, in the order of the
   enforcement hierarchy (compiler, architecture tests, hooks and CI, guidelines). A card holds six lines:
   - Source: book, chapter or heuristic code;
   - Rule: the precise statement, threshold calibrated on the step 2 measurements;
   - Tool: the program that checks it, and its configuration rule;
   - Where: editor, agent hook, pre-commit, pre-push, CI;
   - Expected false positives: what the rule will wrongly catch, and the planned escape hatch;
   - Cost: estimated setup effort and daily noise.
   Findings with a guideline verdict go in a section of their own: the text ready to paste into CLAUDE.md or
   AGENTS.md, one line per guideline.
6. **Deliver.** The audit document follows the format below, and ends with the list of what the audit deliberately
   sets aside (dismissed dogma, rules without object), so the owner also sees what was judged. Nothing gets
   installed: the rollout waits for their validation, card by card.

## Audit document format

1. **Context**: stack, size, domain, what the project does.
2. **Tooling in place**: the step 1 inventory.
3. **Measurements**: the step 2 numbers, each with its command.
4. **Code findings**: by heuristic family, most severe first.
5. **Architecture findings**: by rule, with the graph or excerpt that shows it.
6. **Rollout plan**: the prioritized cards.
7. **Guidelines**: the ready-to-paste text for what cannot be measured.
8. **Set aside**: what the audit judged without object or dogmatic for this project, and why.

## Guardrails

- **Calibrate, never impose**: a threshold is set from the measurement of the existing code and blocks regression on
  modified lines; rewriting the existing code is outside the scope of a guardrail (see calibration.md).
- **Respect the verdicts**: a signal goes into an advisory report, a guideline into agent text; only a tool-verdict
  rule may block a commit or a CI.
- **Bare minimum first**: on a small project, three cards are often enough: no cycles, the business core free of
  framework, database and HTTP imports, one entry point that wires everything.
- **Cite**: a finding without a heuristic code, a file:line or a command does not enter the audit.
