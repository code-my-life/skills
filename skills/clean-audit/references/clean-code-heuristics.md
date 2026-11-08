# Clean Code heuristics

Distilled from "Clean Code" (Robert C. Martin, 2008), studied in full: complete study reports in
code-my-life/clean-code-book, `notes/rapport-clean-code.md`. Every entry carries its verdict:
**tool** (checkable by a program), **signal** (a program detects, a human decides),
**guideline** (pure judgment, to pass on as agent text).

## The book's numeric thresholds

These are preferences born of experience, not laws (see calibration.md): the book says so itself.

| Measure | The book | Reasonable audit threshold |
|---|---|---|
| Function length | "hardly ever be 20 lines long", shown ideal: 2 to 4 | alert beyond 20 lines |
| Nesting inside a function | one or two levels at most | alert beyond 2 |
| Function arguments | 0 ideal, 3 "to avoid", more than 3 refused | alert at 3, refuse beyond |
| File length | typically ~200 lines, upper limit 500 | alert beyond 500 |
| Line width | 80 arbitrary, 100-120 acceptable, Martin: 120 | the project's formatter decides |
| Asserts per test | minimize; one concept per test | one concept per test |
| Return/break/continue | several admitted in a small function | no "single return" rule |

## The chapter 17 catalog (66 codes)

### Comments (C)

| Code | Name | Prescription | Verdict |
|---|---|---|---|
| C1 | Inappropriate Information | History, author, date belong to the VCS and the tracker, not to comments. | signal |
| C2 | Obsolete Comment | A stale comment gets updated or deleted. | signal |
| C3 | Redundant Comment | A comment that restates the code gets deleted; it must say what the code cannot. | signal |
| C4 | Poorly Written Comment | A comment worth writing is written well: brief, precise, grammatical. | guideline |
| C5 | Commented-Out Code | Commented-out code gets deleted; the VCS remembers it. | tool |

### Environment (E)

| Code | Name | Prescription | Verdict |
|---|---|---|---|
| E1 | Build Requires More Than One Step | The build fits in one command. | tool |
| E2 | Tests Require More Than One Step | All tests run with one command. | tool |

### Functions (F)

| Code | Name | Prescription | Verdict |
|---|---|---|---|
| F1 | Too Many Arguments | Zero arguments ideal; more than three gets refused. | tool |
| F2 | Output Arguments | A function that changes state changes its own object's state, not an argument's. | signal |
| F3 | Flag Arguments | A boolean argument reveals a function doing two things: split it. | tool |
| F4 | Dead Function | A function never called gets deleted. | tool |

### General (G)

| Code | Name | Prescription | Verdict |
|---|---|---|---|
| G1 | Multiple Languages in One Source File | One language per file; minimize the extent of the others. | signal |
| G2 | Obvious Behavior Is Unimplemented | The behavior any reader expects exists (least surprise). | guideline |
| G3 | Incorrect Behavior at the Boundaries | Every boundary condition gets hunted down and tested. | signal |
| G4 | Overridden Safeties | Silenced warnings and disabled tests: immediate debt, to refuse. | tool |
| G5 | Duplication | Every duplication is a missed abstraction: method, polymorphism, Template Method or Strategy. | tool (textual), signal (structural) |
| G6 | Code at Wrong Level of Abstraction | Details stay in the lower levels; a generic base ignores the details of its uses. | guideline |
| G7 | Base Classes Depending on Their Derivatives | A base class never mentions its derivatives. | tool |
| G8 | Too Much Information | Small, tight interfaces: few methods, little exposed. | signal |
| G9 | Dead Code | Code that never runs (impossible branch, catch without throw) gets buried. | tool |
| G10 | Vertical Separation | Variables declared close to their use; private functions below their first caller. | tool |
| G11 | Inconsistency | The same thing is done the same way everywhere (names, parallel shapes). | signal |
| G12 | Clutter | Empty constructors, unused variables, empty comments: out. | tool |
| G13 | Artificial Coupling | Every declaration lives in the right place; a general enum does not get locked inside a specific class. | signal |
| G14 | Feature Envy | A method that mostly handles another object's data moves there (exceptions admitted). | signal |
| G15 | Selector Arguments | An argument that selects the behavior becomes several functions. | signal |
| G16 | Obscured Intent | Dense expressions and cryptic names unfold into visible intent. | signal |
| G17 | Misplaced Responsibility | Code sits where the reader expects to find it. | guideline |
| G18 | Inappropriate Static | Instance method by default; static only with no chance of polymorphism. | signal |
| G19 | Use Explanatory Variables | Computations break into named intermediates. | guideline |
| G20 | Function Names Should Say What They Do | The name suffices, without reading the implementation. | guideline |
| G21 | Understand the Algorithm | Know the solution is right, not only that the tests pass. | guideline |
| G22 | Make Logical Dependencies Physical | Ask the owning module for the information instead of assuming it. | guideline |
| G23 | Prefer Polymorphism to If/Else or Switch/Case | At most one switch per selection type, and it builds polymorphic objects. | signal |
| G24 | Follow Standard Conventions | A team standard based on industry norms, tooled; the code serves as the document. | tool |
| G25 | Replace Magic Numbers with Named Constants | Named constants; tolerance for the self-evident inside a readable formula. | tool |
| G26 | Be Precise | Decide precisely: null handled, concurrency locked, money out of floats, wide types declared. | guideline |
| G27 | Structure over Convention | Enforce through structure (abstract method) what a convention cannot force. | guideline |
| G28 | Encapsulate Conditionals | Compound booleans become intent-revealing functions. | signal |
| G29 | Avoid Negative Conditionals | Conditions read in the positive. | tool |
| G30 | Functions Should Do One Thing | A function with sections becomes several functions. | signal |
| G31 | Hidden Temporal Couplings | A mandatory call order becomes visible: each step produces the next step's input. | guideline |
| G32 | Don't Be Arbitrary | Every structure has a reason, communicated by the structure. | guideline |
| G33 | Encapsulate Boundary Conditions | The +1/-1 get computed once under a name (nextLevel). | signal |
| G34 | Functions Should Descend Only One Level of Abstraction | Every statement in a function sits one level below its name. | signal |
| G35 | Keep Configurable Data at High Levels | Configuration lives at the top and travels down as arguments. | signal |
| G36 | Avoid Transitive Navigation | Talk to immediate neighbors: a.getB().getC() forbidden on objects. | tool |

### Java (J), to transpose per stack

| Code | Name | Transposition | Verdict |
|---|---|---|---|
| J1 | Avoid Long Import Lists by Using Wildcards | Dated; the core: the import list says who the module collaborates with, tooling manages it. | tool |
| J2 | Don't Inherit Constants | Constants get imported, never inherited. | tool |
| J3 | Constants versus Enums | Sum types, enums, unions rather than bare integers. | tool |

### Names (N)

| Code | Name | Prescription | Verdict |
|---|---|---|---|
| N1 | Choose Descriptive Names | Names are 90% of readability; reconsidered at every reading. | guideline |
| N2 | Choose Names at the Appropriate Level of Abstraction | Name the what, not the how (connect rather than dial). | guideline |
| N3 | Use Standard Nomenclature Where Possible | Patterns and domain language in the names. | guideline |
| N4 | Unambiguous Names | A long exact name beats a short vague one. | guideline |
| N5 | Use Long Names for Long Scopes | Name length follows scope: i over five lines, a real name beyond. | signal |
| N6 | Avoid Encodings | Neither type nor scope in the name (m_, I, Impl, Hungarian notation). | tool |
| N7 | Names Should Describe Side-Effects | The name says everything the function does (createOrReturnOos). | guideline |

### Tests (T)

| Code | Name | Prescription | Verdict |
|---|---|---|---|
| T1 | Insufficient Tests | Everything that could break gets tested; "seems like enough" is worth nothing. | signal |
| T2 | Use a Coverage Tool! | Coverage reveals the holes in the test strategy. | tool |
| T3 | Don't Skip Trivial Tests | Their documentary value exceeds their cost. | guideline |
| T4 | An Ignored Test Is a Question about an Ambiguity | An ignored test expresses a fuzzy requirement, to resolve. | signal |
| T5 | Test Boundary Conditions | Boundaries get tested with particular care. | signal |
| T6 | Exhaustively Test Near Bugs | One bug found: retest the whole function, bugs travel in groups. | guideline |
| T7 | Patterns of Failure Are Revealing | The pattern of failures diagnoses the cause. | guideline |
| T8 | Test Coverage Patterns Can Be Revealing | What the green tests execute explains the red ones. | guideline |
| T9 | Tests Should Be Fast | A slow test ends up removed under pressure. | tool |

## Chapter rules outside the catalog

**Naming (ch. 2)**: pronounceable, searchable; one word per concept across the codebase (fetch or get, not both) and
one concept per word; classes = nouns, methods = verbs; the names l and O forbidden; context through classes, not
prefixes. Verdict: signal, except l/O and case conventions: tool.

**Functions (ch. 3)**: a function does one thing, all its steps one level below its name (the stepdown rule: reading
top to bottom); command/query separation (CQS): do or answer, never both; no hidden side effect, and the unavoidable
one goes into the name; exceptions rather than error codes; a try is the first word of its function; DRY. Verdict:
signal, except detecting error-code enums and mixed try blocks: tool.

**Comments (ch. 4)**: acceptable: license, intent, clarification of an external API, warning of consequences,
referenced TODO, amplification, public API docs. Everything else gets replaced by code: a good name, a function, a
variable. Verdict: tool for unreferenced TODOs and commented-out code, signal for the rest.

**Formatting (ch. 5)**: one team rule, applied by an automatic formatter; the file reads like a newspaper (high level
at the top); caller above callee; related lines stay together. Verdict: tool (the formatter), signal for vertical
order.

**Objects and data structures (ch. 6)**: objects hide their data and expose behavior; data structures expose their
data with no behavior; hybrids combine the flaws of both; Law of Demeter: a method only calls its class, its
creations, its arguments, its fields; DTOs legitimate; an Active Record carries no business rules. Verdict: signal
(the mechanical part of call chains: tool, G36).

**Errors (ch. 7)**: unchecked exceptions (transposed: typed errors Result/Either where that is the idiom); every
error carries its context; error classes are defined by the caller's needs; third-party APIs get wrapped; Special
Case so the normal flow stays flat; never return null, never pass null (transposed: enable the language's
null-safety, empty collections rather than null). Verdict: tool for null-safety and return null, signal for the rest.

**Boundaries (ch. 8)**: a third-party type (Map, SDK client) stays confined to the class that uses it, never in a
public API; learning tests that exercise the third-party API the way production does, re-run at every version bump;
code against the interface you wish you had, then an Adapter. Verdict: tool (third-party types in public signatures),
guideline for the rest.

**Tests (ch. 9)**: the three laws of TDD (a red test before the code; just enough test to fail; just enough code to
pass); F.I.R.S.T.: Fast, Independent (any order), Repeatable (any environment), Self-Validating (boolean verdict),
Timely (just before the code); test code as clean as production, allowed to be less optimized; one concept per test.
Verdict: tool for Fast/Independent/Repeatable (random-order runs, no network), guideline for the rest.

**Classes (ch. 10)**: small, measured in responsibilities: one single reason to change (SRP); cohesion: when subsets
of methods share subsets of fields, a class wants out; describable in 25 words without "if", "and", "or"; open for
extension, closed for modification (OCP); depends on abstractions (DIP). Verdict: signal (measurable proxies: public
method count, LCOM), guideline for the reason to change.

**Systems (ch. 11)**: constructing and wiring objects is separated from using them; everything gets built in main or
its modules, and nothing depends on main; dependency injection; the business core in plain language objects,
cross-cutting concerns (logs, transactions, security) as decorators or middleware; defer decisions. Verdict: see the
architecture rules (this chapter leads there).

**Simple design (ch. 12)**, four rules in priority order: passes all the tests; no duplication; expresses intent;
minimizes the number of entities (the guard against the dogma of the first three). Verdict: guideline, except tests
and duplication: tool.

**Concurrency (ch. 13)**: concurrent code is isolated from the rest (it is a reason to change on its own); the scope
of shared data is severely restricted; copies and immutability rather than sharing; minimal critical sections; know
your library (thread-safe collections, executors, atomics); an intermittent failure is never ignored; test under
load, on every platform, with more threads than cores. Transposed: async/await, goroutines, actors, immutability by
default, race detectors (Go, TSan). Verdict: signal, except repeated runs under load in CI: tool.

## Transpositions beyond Java

| The book (Java 2008) | Today, any stack |
|---|---|
| Unchecked exceptions | The core: happy path separated from error handling; typed errors (Result, Either, Go error, Rust ?) where that is the idiom |
| Don't return/pass null | Language null-safety enabled (strict TypeScript, Optional, Option/Maybe); Special Case; empty collections |
| Enums (J3) | Sum types, discriminated unions, enums |
| Javabean getters/setters | Properties, records, data classes; the core intact: an object is not a bag of accessors |
| POJO + aspects (EJB2, Spring XML) | Business core in plain objects; middleware, decorators, interceptors at the edge |
| synchronized, ConTest | Immutability by default, async, channels, race detectors; same defense principles |
| Wildcard imports (J1) | Tooling manages imports; the import list remains the map of collaborations |
| Hungarian notation, m_ | Won; the core remains: neither type nor scope in names (Impl, I prefix) |
