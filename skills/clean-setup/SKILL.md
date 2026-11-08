---
name: clean-setup
description: "Install the guardrails planned by a validated clean-audit: linters, architecture tests, git hooks, CI checks, agent hooks and guidelines, on any stack. Use when asked to set up or install clean code or clean architecture guardrails, to apply an audit's rollout plan, or to turn audit cards into enforced rules. Requires a validated audit produced with the clean-audit skill."
---

# clean-setup

Turn a validated audit into installed, proven guardrails. The input is an audit document produced with the
clean-audit skill, plus the owner's validation of which cards to install. Without that input, stop: run clean-audit
first, or ask for the audit document and the validated card list. Inventing cards is forbidden: a missing guardrail
goes back to clean-audit.

## References

Shared with clean-audit, installed next to this skill (`../clean-audit/references/`); if missing, read them in
code-my-life/skills:
- `architecture-rules.md`: the enforcement hierarchy and the tools per stack. Load it before step 2.
- `calibration.md`: thresholds, modified-lines scope, escape hatches. Load it before step 2.

## Process

1. **Check the input.** The audit document, its rollout plan, and which cards the owner approved. The step is done
   when the list of cards to install is explicit and each card still matches the project (a card invalidated by a
   code change since the audit goes back to the owner, never silently adapted).
2. **Install in hierarchy order.** Compiler and language visibility first, then architecture tests, then the wiring
   into git hooks and CI, then agent hooks, then guidelines. One card at a time, the smallest change that implements
   it. Extend the project's existing tooling before adding a tool, and never weaken an existing stricter rule. A new
   dependency needs the owner's go when nothing in the project covers the need.
3. **Prove each guardrail, fail first.** Introduce a minimal temporary violation, watch the guardrail catch it,
   remove the violation, watch everything pass. A guardrail that never failed is not proven. Record each proof
   (command and output) for the report.
4. **Respect the card.** Threshold and scope exactly as calibrated in the card (modified lines only where it says
   so); the named escape hatch with its reason; a deviation needs the owner, in both directions: neither silently
   stricter nor silently softer.
5. **Paste the guidelines.** The audit's guidelines section goes into the agent files the owner designated
   (CLAUDE.md, AGENTS.md, rules); a guideline never becomes a gate.
6. **Deliver.** A setup report: per card, what was installed, where it runs, the fail-first proof, and how to disable
   it locally; deviations listed (none without the owner's go). One commit per card or per coherent group, so each
   guardrail is revertable on its own. Production code stays untouched: this skill changes configuration, tooling,
   hooks, CI and agent files only, unless a card explicitly says otherwise.

## Guardrails

- **Verdicts rule the wiring**: only a tool-verdict card may block a commit, a push or a CI; a signal card becomes an
  advisory report; a guideline card becomes agent text.
- **Proof or it does not ship**: a card without its fail-first proof is reported as not installed.
- **Budget honesty**: when a card's real cost exceeds its estimate, stop that card and report, rather than shipping a
  half-wired rule.
- **Leave the keys**: the report says, for every rule, the one command that runs it and the documented way out.
