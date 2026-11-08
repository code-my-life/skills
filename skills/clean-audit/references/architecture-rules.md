# Clean Architecture rules

Distilled from "Clean Architecture" (Robert C. Martin, 2017), studied in full: complete study report in
code-my-life/clean-code-book, `notes/rapport-clean-architecture.md`. Here: the Dependency Rule, the 21 rules
checkable on the dependency graph, the book's metrics, the enforcement hierarchy and the tools per stack.
"Dependency" = source code dependency: import, include, require, qualified name, inheritance, implementation,
instantiation, annotation, referenced type.

## The Dependency Rule and the circles

Four circles, from center to edge: **Entities** (enterprise business rules), **Use Cases** (application business
rules, the interactors), **Interface Adapters** (controllers, presenters, gateways: format conversion), **Frameworks
and Drivers** (web, database, UI, the wiring). The rule: **every source code dependency points inward**. Nothing in an
inner circle mentions the name of anything declared in an outer circle: no function, no class, no data format. The
flow of control crosses the other way thanks to polymorphism: the use case calls an interface it owns (output port),
implemented outside. A policy's level = its distance from the inputs and outputs.

## The 21 graph rules

Each rule: statement, violation signal, verdict (tool / signal / guideline, in the clean-audit sense).

1. **Dependency Rule** (ch. 22): dependencies point inward. Violation: an entities or use cases module imports a
   controller, a framework, a driver, an ORM; outer type as parameter, return, field, annotation; inheriting from a
   framework class. Verdict: tool (with a paths-to-circles mapping).
2. **ADP, no cycles** (ch. 14): the component graph is a DAG. Violation: any detected cycle. The book's remedies: DIP
   (interface owned by the user) or a new common component. Verdict: tool.
3. **SDP, depend toward stability** (ch. 14): I decreases along every edge. Violation: an edge A to B with
   I(A) < I(B). Verdict: tool (the remedy is judged).
4. **SAP, stable therefore abstract** (ch. 14): D = |A+I-1| close to 0. Violation: a concrete, heavily depended-upon
   component (zone of pain, painful if volatile); an abstract component with no dependents (zone of uselessness).
   Verdict: signal (volatility is judged, git churn approximates it).
5. **DIP on the volatile** (ch. 11): depend only on abstractions for whatever is volatile; stable concrete things
   (stdlib, platform) are tolerated. Violation: import, inheritance or new of a volatile concrete class outside
   factories and Main. Verdict: signal (volatility is judged).
6. **Details in the outer circles** (ch. 22, 23, 30, 31, 32): SQL confined to the adapters; no HTTP, no ORM, no
   framework annotations in entities and use cases; data mappers live in the database layer. Violation: an
   SQL/ORM/HTTP/framework import in an inner module. Verdict: tool.
7. **Simple structures cross the boundaries** (ch. 20, 22): never an Entity nor a database row. Violation: a gateway
   returning an ORM type; an Entity passed to the presenter; a request/response model that references an Entity or
   derives from a framework type. Verdict: tool.
8. **Boundaries are crossed through ports** (ch. 22): a use case that calls outward goes through an interface it
   owns. Violation: a direct import of a presenter, a mailer, a concrete HTTP client from a use case. Verdict: tool.
9. **The interface belongs to the user** (ch. 25): the interface is declared in the high-level component that calls
   it, the implementation in the provider. Violation: an interface declared next to its only implementation and
   imported by the high level (the inversion never happened). Verdict: signal.
10. **Injection at Main only** (ch. 26, 32): the injection framework is known only to the composition point, which
    then hands dependencies out normally. Violation: container annotations or lookups in business code; new of
    volatile concrete classes outside Main and factories. Verdict: tool.
11. **Main is a leaf** (ch. 26): nothing depends on Main. Violation: an import of the composition module from any
    other component. Verdict: tool.
12. **ISP/CRP, depend on what you need** (ch. 10, 13): a fat interface whose clients use disjoint subsets gets
    segregated. Measurable violation: used symbols / exposed symbols ratio. Verdict: signal.
13. **CCP/SRP of components** (ch. 7, 13): what changes together lives together. Signal: files systematically
    co-modified across different components (git history); a file modified by different actors for different
    reasons. Verdict: signal.
14. **No physical knowledge of the low level** (ch. 18): no URI, host or path of a low-level service hard-coded in a
    high-level module; configuration gets injected. Verdict: tool.
15. **No undeclared layer skipping** (ch. 34): a web controller never reaches a repository directly. Violation: any
    edge that shortcuts a declared layer. Verdict: tool.
16. **Component encapsulation** (ch. 34): only a component's entry types are public or published. Violation:
    exported implementations; deep imports that bypass the component's interface. Verdict: tool (the language's
    visibility, see the hierarchy).
17. **Tests, the outermost circle** (ch. 28): tests depend inward, nothing depends on them; business rules are
    tested without GUI or infrastructure. Violations: production code importing test code (tool); systematic
    one-test-per-class structural coupling and business-rule tests going through the GUI (signal: fragile tests
    problem).
18. **Hardware boundary in embedded** (ch. 29): registers and compiler extensions under the HAL, the OS under the
    OSAL, target #ifdefs never repeated. Verdict: tool.
19. **Screaming architecture** (ch. 21): the top-level tree names the domain and the use cases, not the framework.
    The decisive test: every use case runs its tests without a web server or a connected database. Verdict: signal
    (the decisive test: tool, it is a test).
20. **The core ignores its plugins** (ch. 17): UI, database, delivery depend on the business core, never the
    reverse. Violation: an edge from the core to a plugin. Verdict: tool.
21. **LSP, substitutability** (ch. 9): every implementation of an interface (class, module, REST service)
    substitutes for the others without the client noticing. Violation: the client sniffs the concrete type
    (instanceof, downcast, if on the type, if on the provider's URI); an implementation throws "not supported" or
    weakens the contract (square/rectangle). Verdict: signal; becomes tool when a single contract test runs against
    every implementation (property-based or shared suite).

## Where SOLID is checked

| Principle | The book's formulation | Where in the audit | Verdict |
|---|---|---|---|
| SRP | a module answers to one, and only one, actor | rule 13 (git co-modifications, multiple actors); cohesion proxies of the code catalog (ch. 10) | signal |
| OCP | open for extension, closed for modification | rules 1 and 3 (the protected never depends on the protector); G23 (repeated switches) | tool (edge direction), signal (switches) |
| LSP | substitutability of implementations | rule 21 | signal, tool with contract tests |
| ISP | depend on nothing you do not use | rule 12 (fat interfaces, disjoint clients) | signal |
| DIP | depend on abstractions, not volatile concretions | rules 1, 5, 10 (volatile concrete imports, new outside Main and factories) | tool with the layer mapping, signal on volatility |

## The book's metrics (ch. 14)

- **Fan-in**: incoming dependencies; **Fan-out**: outgoing.
- **I (instability) = Fan-out / (Fan-in + Fan-out)**, from 0 (stable) to 1 (unstable).
- **A (abstractness) = Na / Nc**: abstract classes and interfaces over total. Transpose: interfaces and exported types
  without implementation (TypeScript, Python protocols), Go interfaces, Rust traits.
- **D (distance from the main sequence) = |A + I - 1|**: 0 = well placed. The book's usage: examine any component
  whose D drifts from 0; track D per component across releases with a control threshold (the book's example: 0.1).
- The book's own warning: "a metric is not a god"; these metrics steer the examination, they do not condemn.

## The enforcement hierarchy (ch. 34, Simon Brown)

In order of effectiveness; each level catches what the previous one cannot:

1. **The compiler and the language's visibility**: what the code physically cannot violate. Unexported packages (Go
   internal/), package-private (Java), internal (C#, Kotlin), pub(crate) (Rust), package.json exports and project
   references (TypeScript), `__all__` (Python). Without access modifiers, every organization style collapses into
   soft layers: that is Brown's central argument.
2. **Architecture tests**: the graph checked on every CI run. dependency-cruiser or eslint-boundaries (JS/TS),
   import-linter (Python), ArchUnit (Java/Kotlin), NetArchTest (.NET), deptrac (PHP), depguard (Go), cargo-modules
   (Rust); cycle detection: madge, or the tool above.
3. **Git hooks and CI**: the level 1 and 2 rules run before every commit/push and on every PR, plus the code rules
   (linter, formatter, coverage); an agent hook (for example Claude Code's PostToolUse) gives the same verdict while
   the agent codes.
4. **Discipline and guidelines**: CLAUDE.md, AGENTS.md, reviews. The book is explicit: discipline fails under budget
   and deadline pressure; it only carries what cannot be measured.

## Modern transpositions

- **Component**: the unit of build and ownership (monorepo package, pnpm/Cargo workspace, Gradle module, Bazel
  project); the monorepo's declared graph is the graph to control, ADP and SDP apply to it as is.
- **Front end (React, Vue, SwiftUI)**: the Humble Object becomes: pure display components (rendering props), logic in
  hooks, stores or presenters testable without the DOM; the ViewModel of strings and booleans becomes computed props
  and selectors; the testable rule: a screen's logic runs its tests without a browser.
- **ORM**: today's signals for rule 7: Prisma/TypeORM/ActiveRecord/SQLAlchemy entities leaking into use cases or the
  front end; ORM-generated types used as request/response models; a view querying the database.
- **Main**: the framework (Next.js, NestJS, Spring Boot, serverless) owns the entry point; "Main" becomes the
  composition root; framework annotations and hooks stay above the adapters.
- **Services**: services that merely split behavior are expensive function calls; the real boundaries run through the
  services (component-based services, modular monolith). Coupling through shared data survives the network.
- **Database**: the data model is architecturally significant, the database software is a detail; the rule targets the
  code's dependency on the software (SQL, ORM in the inner circles), not the design of the schema.
- **Small project**: the bare minimum (see calibration.md): no cycles, the core free of framework/database/HTTP imports,
  one entry point that wires. Full boundaries (reciprocal ports, DTOs everywhere) are partial boundaries to activate
  at the inflection point, when ignoring costs more than implementing.
