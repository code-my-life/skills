# Calibration

How to apply the two books without dogma. The guardrails come from the books themselves: Martin presents his school
as a school ("don't make the mistake of thinking that we are somehow \"right\" in any absolute sense") and his
numbers as preferences born of experience.

## Thresholds are preferences

- Functions of 2 to 4 lines: "This is not an assertion that I can justify" (Clean Code, ch. 3).
- Files of 200 to 500 lines: "should not be a hard and fast rule" (ch. 5).
- 120 characters: "I personally set my limit at 120" (ch. 5).
- "A metric is not a god; it is merely a measurement against an arbitrary standard" (Clean Architecture, ch. 14).

Consequence for an audit: a threshold is proposed with its measurement on the real code, never as a truth.

## Calibrate on the existing code

1. Measure the current distribution (function length, arguments, nesting, D per component).
2. Set the threshold at the level that blocks regression, not at the book's level: if the 95th percentile of
   functions is 35 lines, the starting threshold is 35, not 20; it will come down as the code comes down.
3. Check added and modified lines only. The existing code does not get rewritten for a guardrail: that is the Boy
   Scout rule (leave it a little cleaner than found), not a rewrite campaign.
4. Plan the escape hatch: every tooled rule says how it gets disabled locally (a named disable comment, with a
   reason), and that disable rate gets watched.

## The bare minimum by size

The book admits it: nobody applies the clean architecture to a 200-line program, and a monolith without components
suits a small team that is starting out. The problem is never paying the debt.

- **Small project (one folder, one person)**: three guardrails: no cycles; the business core free of framework,
  database and HTTP imports; one entry point that wires everything. Plus a formatter and a basic linter.
- **Growing project**: watch the first points of friction (files co-modified in bulk, D drifting, PRs stepping on
  each other) and implement the boundary "right at the inflection point where the cost of implementing becomes less
  than the cost of ignoring" (ch. 25).
- **Large project, several teams**: the full toolkit, in the order of the enforcement hierarchy.

Over-engineering is the symmetric failure: "over-engineering is often much worse than under-engineering"; ROSE died
of its layers (the book's appendix). A boundary costs reciprocal interfaces, DTOs, administration: partial boundaries
(Strategy alone, Facade, "skip the last step") exist for that, with their acknowledged risk of erosion.

## The books' own tolerances

To recall in an audit next to each neighboring rule, so as to judge instead of condemning:

- **Switch**: appropriate where adding functions is more likely than adding types; the rule: one per selection type,
  and it builds polymorphism (G23).
- **Static**: legitimate when all the data comes from the arguments and no polymorphism is plausible (G18).
- **Bare numbers**: tolerated when they read better than their constant (5280; TWO would be absurd) (G25).
- **Feature Envy**: sometimes a necessary evil, to avoid coupling a datum to its output format (G14).
- **Several asserts**: the real rule is one concept per test, not one assert per test (ch. 9).
- **Multiple returns, break, continue**: admitted in a small function (ch. 3).
- **Depending on stable concrete things**: stdlib and platform are consumed as they are; the DIP targets the
  volatile, and its residual violations concentrate in Main (ch. 11).
- **Duplication**: distinguish the true kind (always changes together: unify) from the accidental kind (diverging
  evolutions: leave it); unifying two similar-looking screens by reflex is a mistake (Clean Architecture, ch. 16).
- **Acknowledged compromises**: the book signs some itself (errorMessage in ArgsException: "Frankly, it's a
  compromise"); an audit may accept some, provided they are written down.

## Modern divergences to flag without imposing

The Martin school holds positions that current practice disputes; an audit flags them as team choices, never as
defects: very aggressive extraction into micro-functions and micro-classes (navigation cost; his own fourth simple
design rule serves as the counterweight); wildcard imports (J1); his rejection of final/const on arguments, against
the current preference for declared immutability; event sourcing presented as simple (real costs of versioning and
projections).

## The spirit

The last line of chapter 17: the list "implies a value system"; "Professionalism and craftsmanship come from values
that drive disciplines". An audit passes on the arbitration, not only the rules: the four simple design rules are
ordered (tests, duplication, expression, economy of entities) precisely to decide when they contradict each other.
