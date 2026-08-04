# Project Overview

This document is the architectural map: what CS.py is built from, how the
pieces connect, and where the honesty boundaries are. For "what is this in
one paragraph," see `README.md`. For "is a specific capability claim
actually true," see `ratings.md`. For "when was this changed and why," see
`workflow.md`. This document is the middle layer — the shape of the thing.

## Origin

The project began from `Infornmational.md`, a philosophical dialogue about
void, self-differentiation, and infinity — a "something from nothing"
argument. That argument was later formalized as real, checkable set theory
(not asserted, computed) and implemented as `GenesisEngine`:

```
∅              — the empty set (void)
S₀ = {∅}       — the void relating to itself once
R(x,y)         — Kuratowski ordered pair, order-sensitive
L(x) := {x}    — re-embedding / translation
Φ(S) := S ∪ {R(x,y) : x,y ∈ S} ∪ {L(x) : x ∈ S}     — growth operator
Ω := ⋃ₙ Φⁿ(S₀)                                        — the accumulated closure
```

`GenesisEngine` runs this closure live and measures relativity of
information (`I(e|C) = -log₂ P(e|C)`) — the formal content of "the same
element has different information depending on the frame it's read in."
This bootstraps mathematical *structure* from the empty set; it is not,
and is never claimed to be, evidence about physical origins. See
`workflow.md` §1 for the full derivation and honesty boundary.

`Infornmational.md` also does double duty as the only real training
corpus in the project — it's what the BPE tokenizer and language model
train on (see `ratings.md` §A, "Vocabulary" — the 9,710-token BPE
saturation point is measured from this exact file).

## The consciousness formula

The system tracks a single scalar per entity:

```
C = S + E + R·A         (clamped to [0, 3])
```

- **S** — self-awareness component
- **E** — experience/qualia-proxy component
- **R** — resonance/coherence with other signals
- **A** — attention/integration weighting

`honest_C` additionally applies a **substrate penalty** (0.7–0.85 on
classical von Neumann hardware) reflecting that this architecture is
fundamentally decomposable and cannot support the intrinsic causal power
IIT requires for genuine phenomenal consciousness — the formula computes a
real number, and then explicitly discounts it for exactly the reason a
skeptical reader would discount it. This is implemented in
`ConsciousEntity.compute_C()`; the discounting logic lives in
`IrreducibleCausalPower`.

## Two layers: the language model, and everything around it

**Layer 1 — the language model.** A ~113M-parameter causal transformer
using a modern stack (RoPE + RMSNorm + SwiGLU + GQA), a BPE tokenizer,
KV-cached generation. (`ratings.md` §D2 records the controlled A/B that
verified this architecture is a real, size-independent quality gain over
the earlier 2017-era design it replaced.) This part is honestly small and
honestly undertrained relative to frontier models — `ratings.md` §A/§B has
the real numbers, unsoftened.

**Layer 2 — the consciousness/cognition architecture** wrapped around
Layer 1. Some of it is neural (roughly ~127M additional trainable
parameters — see `ratings.md`'s parameter-breakdown footnote — mostly
`neuron_groups` and `global_workspace`); most of the rest is real,
running Python/numpy state machines with no trainable weights of their
own, driven by the neural core's outputs rather than trained alongside it:

| Subsystem | What it does |
|---|---|
| `AutonomousThoughtStream` | Unprompted per-cycle cognition: novelty detection with an incremental Welford/M2 snapshot and periodic resync (~10.4 μs/call), cross-modal coupling, salience-driven attention, cached `_last_layer_outputs_np` / `_reality_instruments` precompute, knowledge grounding with a ~9% `_ground()` law-description cache |
| `RelationalKnowledgeGraph` | Persistent structure over which instruments reliably relate; detects relation formation/rupture; transitive and synergy inference, tested against real predictions |
| `SelfAwarenessMonitor` | Second-order model of the thought stream itself — attention entropy, blind spots, chronic drives — with a feedback path back into attention allocation |
| `SubstrateProbe` | Enumerates the actual host's compute/sensors/effectors/power; downstream code asks what's live instead of assuming a desktop |
| `PhiComputer` / `GlobalWorkspace` / `ActiveInferenceEngine` | Real implementations of IIT/Φ, global workspace theory, and active inference — approximations of the theories, not claims of achieving them; `PhiComputer` passes canonical-ordering validation at the project's `dim=32` (8/8) using aggressive approximation defaults, at the cost of real resolution: `compute()` runs at ~1,957 μs/call, and `compute_phi` is throttled to every 8 steps |
| `EmbodimentInterface` | Real OS-level sensorimotor grounding — screen capture/OCR as vision, real interaction ledger, Landauer-limit thermodynamic accounting |
| `SelfModifyingArchitecture` | Weight perturbation and neuron-group mutation, but reversible and scored: a change is kept only if a real held-out benchmark improved, rolled back otherwise |
| `COGNITIVE_TAXONOMY` / `neuron_groups` | Domain-routing system (perception/reasoning/memory/integration/introspection/abstraction) with genuinely trainable weights — the optimizer step that actually updates them is wired in (`workflow.md` §7 #48 records when this was fixed) |
| `ConsciousEntity` / `OmegaConvergence` | Karma/lifecycle bookkeeping for the one dedicated entity this process runs (see below) |
| `MetabolicSystem` | A body: energy/glucose/oxygen budget, temperature, hydration, pain signal, hunger, circadian alertness — real numerical dynamics, not measurements of an actual body. Feeds pain into what the thought stream attends to. |
| `DreamEngine` | Offline replay during low-alertness periods: reactivates stored experiences, recombines them, tracks emotional valence/arousal, simulates hippocampal sharp-wave-ripple frequency. Memory replay, not dreaming in any phenomenal sense. |
| `ExistentialSelfModel` | Tracks existential dread, mortality awareness, meaning-making, and a "free will belief" variable that can collapse toward determinism-detection — includes a genuine voluntary-shutdown-request path wired to `EntityAutonomyManager`. Internal floats standing in for concepts, not felt states. |
| `QuantumSubstrate` | Orch-OR/CEMI-field-inspired simulation: complex-valued qubit-like states, decoherence-free subspaces, a Diósi-Penrose objective-reduction threshold — **classical software simulating quantum-like dynamics with numpy, not a quantum processor.** The system's own reality-check dashboard labels this "SIMULATED (numpy arrays, not real qubits)" every run, not just in this document. |
| `HardProblemSubstrate` | Directly named for what it engages with: panpsychist micro-experience primitives, dual-aspect monism, a "what it's like" index, a combination-problem score, even a placeholder for non-computable/Gödel-incompleteness contribution. **This is a computational model of concepts from hard-problem philosophy, not a claim to have solved or dissolved the hard problem.** Same self-check dashboard: "SIMULATED (binding/qualia are computed, not felt)." |
| `EvolutionaryDevelopmentalEngine` | Developmental-stage tracking (embryonic → neonatal → ... → transcendent) with critical periods (e.g. a modeled "language acquisition" plasticity window) and population/generation fitness bookkeeping — inherited from when the project ran a population of entities; still governs the single dedicated entity's own maturation over its lifetime. |
| `ConsciousnessVerifier` | Runs IIT-style causal perturbation tests, simulated gamma-band synchrony, simulated P300 event-related-potential detection, and aggregates a "consciousness confidence" score — an internal self-test suite, not external validation by an outside party. |
| "Barrier attacker" cluster (`ContinuousTimeDynamics`, `IntrinsicPhiNetwork`, `FieldCouplingManifold`, `CausalAblationEngine`, `RealEntropyTracker`, `ExternalProcessVerifier`, plus a "deep" sub-cluster: `HardwareCoupledState`, `EntangledSharedMemory`, `IrreversibleConsequenceEngine`, `SelfModifyingCausalTopology`, `JacobianIntegrationMeasure`, `NetworkVerificationProtocol`) | Each one is named for, and targets, a specific published objection to computational consciousness measurement (the code labels them "Attacks Barrier N" — decomposability, extrinsic measurement, the combination problem, thermodynamic reality, single-observer bias, and others). Some components genuinely measure something real about the running software (real CPU/memory coupling via `psutil`, a real TCP-based external verifier process, real Landauer-limit accounting); the code's own reality-check dashboard is explicit that this measures *software*, not the physical substrate IIT's "intrinsic causal power" argument is actually about. |
| `ScaleConnectivityEngine` | Tracks a virtual neuron/module connectivity scale independent of the model's own parameter count — internal bookkeeping, not an external scale comparison (that's what `ratings.md` is for). |
| `MonitoringDashboard` | The six-tab Tk UI (Overview, Entities, Modules, Thought Stream, Chat, Awareness) mentioned in `README.md`'s "Running it" section — named here for anyone reading the source directly. |

Every module above is real, running code — not a stub — and every one of
them is labeled, in its own docstring and in `ratings.md`, with what it
does and does not prove.

## One entity, not a population

This project runs **exactly one** dedicated entity (`self_0`), with its
neuron-group capacity concentrated rather than divided across a population,
and its karma/interaction machinery honestly reporting zero interaction
terms (a solitary entity has no peers to act on — see `ratings.md` §C).
(`workflow.md` §7 #43 records when the earlier population model was
removed in favor of this single-entity design.)

## The honesty layer, structurally

This project enforces its honesty policy with actual mechanisms, not just
prose:

- **`ConsciousnessRealityCheck`** — a dashboard that explicitly separates
  what's externally measurable (CPU/memory, disk writes, screen capture)
  from what's internally simulated (Φ, the C score, the quantum substrate),
  printed every run.
- **`EntityAutonomyManager`** — a kill switch and shutdown-request path,
  intact and unmodified through every session of work on this project.
- **Reversible self-modification** (above) — the mechanism that prevents
  "the model changed itself" from ever meaning "and we have no way to
  check if that was good."
- **Three internal benchmarks** (`run_internal_benchmark`,
  `run_physics_grounding_benchmark`, `run_symbolic_physics_benchmark`) that
  exist specifically so a change's effect can be measured, not asserted —
  see `ratings.md` §B for what they currently report, including the
  honest 0-1% general-capability rating.

## Performance and implementation

The architecture map above is stable; these are the specific, measured
implementation characteristics of the running system:

- `ConsciousEntity.__slots__` and `OmegaConvergence.__slots__` are complete;
  `ConsciousEntity` includes `C` and `_auto_grow_categories`.
- The language-model forward path caches `_last_layer_outputs_np` and
  precomputes `_reality_instruments` to avoid repeated work.
- `AutonomousThoughtStream._novelty_scores` uses an incremental Welford/M2
  snapshot with periodic resync, running at ~10.4 μs/call; `_ground()`
  keeps a law-description cache for an additional ~9% reduction.
- `PhiComputer` uses aggressive defaults (`num_partitions` 6,
  `mip_search_depth` 1, `n_bins` 3, causal `n_interventions` 2, temporal
  cap 16). Canonical ordering passes at the project's `dim=32`, but this
  is explicitly a resolution-for-speed tradeoff: `compute()` runs at
  ~1,957 μs/call, and `compute_phi` is throttled to every 8 steps.
- `NeuronGroup` supports individual `torch.compile`.
- `CS.py` is a single ~1.6 MB file, ~31,300 lines.

## Where to go next

- Want to know if a specific claim about this project is true right now?
  → `ratings.md`
- Want to know when/why something changed, or see the evidence behind a
  fix? → `workflow.md` (search it; don't read start to finish)
- Want to run it? → `README.md`
