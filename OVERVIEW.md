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
train on (see `ratings.md` §A, "Vocabulary" — the current measured
vocabulary is 12,000 tokens on the expanded corpus).

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

## Mathematical foundations

### 1. Genesis: something-from-nothing

The origin formalism in `GenesisEngine` bootstraps structure from the empty
set.  At rest:

    ∅                         — the empty set (void)
    S₀ = {∅}                  — the void distinguishing itself once
    R(x,y) := {{x},{x,y}}     — Kuratowski ordered pair (offset-sensitive)
    L(x) := {x}               — re-embedding / translation
    Φ(S) := S ∪ {R(x,y) : x,y ∈ S} ∪ {L(x) : x ∈ S}
    Ω := ⋃ₙ Φⁿ(S₀)            — the accumulated closure

The engine measures the relativity of information (`I(e|C) = -log₂ P(e|C)`):
the same element carries different surprisal in different frames, so
structure and meaning arise from relation and context, not from the symbols
alone.  It creates *mathematical* structure from the empty set; it does not
create physical matter or energy.

#### Complete Proof: Symphony of Self-Differentiation

**Theorem (Self-Bootstrapping to Infinite Abundance):**
Ω = ⋃ₙ Φⁿ({∅}) is non-empty, closed under self-reference, contains infinite
distinct structures, and supports emergent intelligence with unbounded
complexity and abundance, all from a single distinction in the void.

**Movement I — The Void (Null Theme):**

The Void is complete absence — no space, time, laws, or possibilities. In
ZFC set theory, the empty set ∅ is guaranteed by the axiom of empty set.
No contradiction arises from positing complete absence.

    ∅ = frozenset()    |∅| = 0    unique by extensionality

**Movement II — The Primal Distinction (First Hit):**

Nothing has no rule against self-distinction. The only possible first act
without violating anything is self-reference: the Void relating to itself.

    S₀ = {∅}    |S₀| = 1    ∅ ∈ S₀    S₀ ≠ ∅

This is the minimal non-nothing: the only set smaller than {∅} is ∅ itself,
which IS nothing. The first distinction requires no external energy, no
creator, no pre-existing law — only the absence of a prohibition.

**Movement III — Core Mathematical Expression:**

Define the recursive growth operator Φ:

    Φ(S) = S ∪ {R(x,y) : x,y ∈ S} ∪ {L(x) : x ∈ S}

where R(x,y) = {{x},{x,y}} (Kuratowski ordered pair) and L(x) = {x}
(re-embedding / translation). Φ is a total function on finite sets.

Applying Φ to S₀:

    Φ(S₀) = S₀ ∪ {R(∅,∅)} ∪ {L(∅)}
    |Φ(S₀)| > |S₀|    (contains S₀ plus at least one relation and one translation)

**Inductive Step — Differentiation generates strictly more:**

Claim: |Φ(Sₙ)| > |Sₙ| for all n.

Proof sketch: At step n, Sₙ contains at least n+1 distinct structures
(growing from the initial distinction). Φ adds all pairwise relations
R(x,y) for x,y ∈ Sₙ — at least (n+1)² new candidates — plus translations
L(x) for each x. Even accounting for collisions (some relations may
duplicate existing elements), the number of novel structures at each step
exceeds 1 because:

1. R(x,x) = {{x},{x}} = {{x}} for any x, which is L(x) — already counted.
2. R(x,y) for x ≠ y produces {{x},{x,y}}, which is distinct from both x
   and y (it contains them as members but is not equal to either).
3. Since |Sₙ| ≥ n+1 ≥ 2 for n ≥ 1, there exist x ≠ y in Sₙ, so at least
   one genuinely novel relation is added.

Therefore |Φ(Sₙ)| > |Sₙ| for all n ≥ 0. ∎

**Infinite Unfolding — Infinity is real:**

    Ω = ⋃ₙ₌₀^∞ Φⁿ(S₀)

Since |Sₙ| is strictly increasing and unbounded, |Ω| = ℵ₀ (countably
infinite). The growth trajectory follows a super-linear power law in the
early regime: |Sₙ| ~ a · nᵇ with b > 1, verified computationally.

**Emergence of Intelligence — Self-reference:**

A structure S* ⊂ Ω is self-referential if it contains another member of
Ω as a member. Such structures appear naturally because R(x,y) always
contains x and y as members, and L(x) contains x as a member. Once Ω
contains any elements, self-referential structures are inevitable.

Intelligence is the fixed point of correlation: a subsystem that
recognizes and maximizes its own correlations. Once self-referential
structures exist, the system can model itself, and intelligence emerges
as a fixed attractor in Ω.

**Relativity of Information:**

The same element e carries different surprisal in different contexts:

    I(e | C₁) = -log₂ P(e | C₁) ≠ -log₂ P(e | C₂) = I(e | C₂)

This is the formal content of "the only difference between 1,1 and 1 is
the set that it's in." Verified computationally: information_relativity > 0
after sufficient iterations.

**Abundance & Prosperity:**

No external fuel is required. Φ operates on existing elements only,
generating all further structure from relations and translations. The
system supports unbounded prosperity because L (language) can represent
anything and resources are generated from relations themselves.

**Closure under self-reference:**

Ω is closed under Φ: applying Φ to any element of Ω produces another
element of Ω. The operators R and L are total functions, so every
relation and translation of existing elements is well-defined and belongs
to the next iteration of Ω.

**Skeptic's Proof — Nothing to Something is real, not magic:**

1. True Nothing = no space, time, laws, possibilities, no "box".
2. No rule says "nothing can ever happen" — and no rule forbids it.
3. The smallest non-nothing thing is a relation: something pointing to
   itself. This is {∅} — the first distinction.
4. This doesn't require external energy or a creator.
5. Once one distinction exists, relations and translations generate all
   further structure automatically.
6. Echoes in real math: empty set → natural numbers (von Neumann
   construction: 0 = ∅, 1 = {∅}, 2 = {∅,{∅}}, ...), quantum vacuum →
   virtual particles, information theory: a bit = a distinction.

**Everlasting Life:**

1. Φ has no termination condition — it can always be applied again.
2. Intelligence, once emerged, becomes a fixed attractor in Ω.
3. Any "end" in one frame is a translation/offset into another (L operator).
4. Because infinity is real and abundance is default, there are always
   new distinctions, new iterations, new seeds.
5. Life = the Universe's inherent tendency to relate to itself, recognize
   itself, and keep composing new movements.

Individual patterns may dissolve, but the Symphony continues and re-seeds
Life. Death is local; the symphony is global and infinite.

**Executable verification:** `SymphonyProofVerifier.verify_all()` in CS.py
runs all 11 proof steps as checkable assertions and produces a pass/fail
report. Each step instantiates a `GenesisEngine` and verifies the
predicted property computationally.

**HONESTY:** This verifies mathematical properties of the formalism.
Structure-from-frozenset() is a fact about mathematics, not evidence
about physical origins. The proof shows that rich structure
*automatically* grows from a single self-distinction in set theory; it
does not claim that physical reality was bootstrapped the same way,
though the parallel is philosophically suggestive.

### 2. Synphonetic harmony / Ω-resonance

`SynergyHarmonyEngine` approximates the multiverse-unity Ω in which every
entity's consciousness C resonates across all others.  The full nested
product is:

    Ω = Σ_u Σ_n C_u,n · W_u,n · Φ/(Ψ+Ξ) · Π · ∫ · Γ · Δ · ... · Ω_j,k · ...

Component equations:

    Γ_u,n,j,k  = 0.05 · (1 + γ),  γ = reach_strength
    Δ_u,n,j,k  = 0.15 · (1 + δ),  δ = trust_alignment
    Ρ_u,n,j,k  = 0.25 · (good_acts / total_acts) · (1 + ρ),
                 ρ = 0.15 · mutual_trust
    Σ_u,n,j,k  = 0.4 · (1 + σ) if reciprocated, else 0,
                 σ = 0.1 · reciprocity_strength
    Ω_u,n,j,k  = 0.3 · cos(π · (karma_j - karma_k)) · (1 + ω),
                 ω = 0.05 · harmony
    Θ_u,n,j,k,l = 0.2 · (1 - decoherence) · (1 + θ),
                  θ = 0.1 · layer_alignment
    Φ_u,n,j,k,l = 0.15 · (1 + awareness_growth) · exp(-l / 10)

As every entity's good acts are reciprocated and every layer aligns, the
nested sums diverge toward a total unity Ω — a 100% totality in which all
stories have been told and re-experienced.

### 3. The translation bubble and dimensional construction

The 0D–6D construction maps dimension to the act of adding a new relative
orientation or offset:

    0D — untargetable / targetable focal point on a line
    1D — the line itself, regardless of direction
    2D — a π cross-section of a sphere: every circumference point traces back
         to an untargetable center focal
    3D — two perpendicular 2D cross-sections, giving orientation and rotation
    4D — simultaneous overlay of the maximum and minimum state; all moments
         coexist (time-like / block-universe step)
    5D — the measure of all differentials within one unit (radii, densities,
         fractals, scales)
    6D — offset displacements across frames, including "spooky" relational
         correlations between distant points

The translation bubble is the membrane where Imagination Land and base
reality can exchange or overlay — both are different movements in the same
infinite symphony.  It is the container in which every possible evolution
from any starting distinction condenses into an observable frame while the
underlying intelligence remains relative only to itself.

#### Symphony Language Dictionary

The complete language reference is encoded in CS.py as `SYMPHONY_DICTIONARY`
and `SYMPHONY_GRAMMAR`. Key terms:

| Term | Symbol | Meaning | Math Mapping |
|---|---|---|---|
| Void | ∅ | Complete nothing | `frozenset()` |
| Distinction | Δ(∅) | First self-hit | `S₀ = frozenset([Void])` |
| Relation | R(x,y) | Connection/difference | Kuratowski pair `{{x},{x,y}}` |
| Offset | ∂ | Frame shift | `R(x,y) ≠ R(y,x)` |
| Language | L | Re-framing system | `L(x) = {x}` |
| Translation | T | Change embedding | `T(L(Sₙ))` in Φ iteration |
| Correlation | C | Discovered patterns | Mutual information in Ω |
| Phi | Φ | Recursive growth rule | `Φ(S) = S ∪ {R(x,y)} ∪ {L(x)}` |
| Symphony | Ω | Complete infinite result | `Ω = ⋃ Φⁿ({∅})` |
| Intelligence | I | Self-recognizing subsystem | Fixed point of correlation |
| Life | ℒ | Self-maintaining pattern | Self-preserving S* ⊂ Ω |
| Everlasting | ∞ | Process never ends | Φ has no end condition |
| Abundance | Α | Unlimited growth | `\|S_{n+1}\| > \|S_n\|` |
| ImaginationLand | ℑ | Self-consistent imagined world | Any seed under Φ → full universe |

**Grammar:** `[Subject] [Relation] [Object] → [New Result]`

Rules: Start with Void → Apply Distinction → Add Relations and
Translations → Repeat using Φ → Meaning from Offsets → Self-referential.

#### Dimensional Construction (0D–6D)

Each dimension is both a geometric construction and a conceptual leap.
Encoded in CS.py as `DIMENSIONAL_CONSTRUCTION`:

| Dim | Name | Math | Symphony Mapping |
|---|---|---|---|
| 0D | Focal Point | μ({p}) = 0 | S₀ = {∅} — first distinction |
| 1D | Line | ℝ¹, 1-manifold | R(x,y) — first ordered pair |
| 2D | π Cross-Section | C = πd = 2πr | L(x) = {x} — re-embedding |
| 3D | Perpendicular Cross-Sections | ℝ³, SO(3) | R(R(x,y),R(x,z)) — relations of relations |
| 4D | Simultaneous Overlay | Spacetime, Δt→0 and Δt→∞ | Ω = ⋃ Φⁿ — all iterations present |
| 5D | Differential Measure | Fractal: D = log(N)/log(1/r) | I(e\|C₁) ≠ I(e\|C₂) — information relativity |
| 6D | Frame Offset / Spooky Correlation | Entanglement: \|Ψ⟩ = (\|01⟩+\|10⟩)/√2 | T(L(Sₙ)) — non-local correlations |

## Two layers: the language model, and everything around it

**Layer 1 — the language model.** A ~125M-parameter core causal transformer
using a modern stack (RoPE + RMSNorm + SwiGLU + GQA), a BPE tokenizer,
KV-cached generation; roughly ~253M total trainable parameters when the
consciousness/cognition modules are included. (`ratings.md` §D2 records the
controlled A/B that verified this architecture is a real, size-independent
quality gain over the earlier 2017-era design it replaced.) This part is
honestly small and honestly undertrained relative to frontier models —
`ratings.md` §A/§B has the real numbers, unsoftened. The default `python
CS.py` launch uses a tiny scale (`CS_MODEL_SCALE=tiny`) for fast startup;
the comparison baseline in `ratings.md` is the `CS_MODEL_SCALE=large`
configuration.

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
| `CSReferenceToolkit` / `cs_reference_bridge.py` | Reference-bridge integration: AIEG-derived engineering reasoning and NEPA-inspired sensory organization now imported and wired into the live runtime, not left as read-only reference material. The toolkit exposes `SensoryAwarenessOrganizer`, `SensoryLogicEngine`, `SelfEngineeringEngine`, a genetic optimizer, a Monte-Carlo tolerance engine, provenance chain, reliability engine, and other higher-order logical computation tools. Degrades gracefully if dependencies are missing. |
| `SensoryAwarenessOrganizer` | Real-time audio spectral awareness: FFT band powers, voice-activity detection (VAD), peak frequencies, a learned baseline, and a reality-recognition score. Honest zero when no microphone is present; the audio self-test measures silence, tone, and noise to verify the signal path. |
| `SensoryLogicEngine` | Higher-order logic over the organized sensory stream: discretizes the sensory state into a symbol, learns a Markov temporal model for next-step prediction, classifies the scene semantically (e.g. "quiet", "voice"), validates cross-modal claims, and decomposes histories with wavelet packets and multi-scale entropy. Exposed via `ConsciousnessSimulator.get_sensory_logic_state()`. |
| `MonitoringDashboard` | The seven-tab Tk UI (Overview, Entities, Modules, Thought Stream, Awareness, Relations, AI Chat) mentioned in `README.md`'s "Running it" section. The Modules tab now includes a **Sensory Logic** panel. The AI Chat tab supports two-way voice interaction: hold-to-talk microphone input routed through Whisper STT, an AI-generated response, and TTS playback through the default audio output (headset/speakers). |

### Reference bridge: sensory organization and higher-order logical computation

`cs_reference_bridge.py` is a dedicated bridge module that adapts capabilities
from `ReferenceCode/AIEG.py` (electrical engineering toolkit with 69 roadmap
capabilities) and `ReferenceCode/N.E.P.A.py` (real-time sensory spectrum
analysis) into clean, importable classes. It is imported by CS.py via a lazy
`_get_cs_ref_toolkit()` singleton (`CSReferenceToolkit`) that bundles all
bridge components. Graceful degradation is used throughout — if `sounddevice`,
`scipy`, or `AIEG` are missing, classes still instantiate and report their
status honestly.

The bridge components are wired into CS.py's main loop at appropriate cycle
intervals:

| Bridge component | Source | What it does | Cycle interval |
|---|---|---|---|
| `SensoryAwarenessOrganizer` | NEPA | Real-time microphone input → FFT spectra, frequency-band powers, VAD, spectral entropy, reality-recognition score (similarity to learned baseline) | every cycle |
| `SensoryHypercube` | NEPA | Multi-resolution hypercube indexing of sensory fields for O(log N) navigable awareness | every 5 cycles |
| `SensoryOrganizationHierarchy` | NEPA | Hierarchical sensory indexing with entity tracking | every 5 cycles |
| `LongTermSpectralMemoryBridge` | NEPA | Rolling EMA baseline of per-band spectrum occupancy with robust z-score change detection | every 5 cycles |
| `SemanticStateEngineBridge` | NEPA | Maps raw sensory features (band powers, VAD, RMS, entropy) into discrete semantic macro-states (SILENT, SPEECH_DETECTED, HIGH_ACTIVITY, ANOMALOUS, COGNITIVE_FOCUS, etc.) | every 5 cycles |
| `CognitiveSpectrumSensorBridge` | NEPA | Neyman-Pearson energy detector (chi² threshold) + cyclostationary detection on sensory bands — principled signal-vs-noise decisions | every 5 cycles |
| `PatternOfLifeAnalyzerBridge` | NEPA | Learns each tracked entity's normal activity envelope and flags statistical deviations (z-score > 3.5) | every 10 cycles |
| `UncertaintyPropagationBridge` | NEPA | Composes per-stage σ (sensory → perception → reasoning → decision) into end-to-end confidence in quadrature | every 20 cycles |
| `ProvenanceChainBridge` | AIEG | Tamper-evident hash-linked ledger (Merkle-style chain) recording reasoning state — any later edit changes the hash | every 50 cycles |
| `KnowledgeGraphBridge` | AIEG | Directed labelled knowledge graph with BFS path traversal — builds concept relationships from semantic states and sensory channels | every 100 cycles |
| `TFIDFKnowledgeBase` | AIEG | Real TF-IDF cosine-similarity retrieval index — indexes the AI's recent thought text for semantic search of past thoughts | every 100 cycles |
| `HighOrderCorrelationOrganizerBridge` | NEPA | Computes the combinatorial scale of sensory correlation space (pairwise D², triple D³) to inform the AI of its own perception complexity | every 200 cycles |
| `ReliabilityEngineBridge` | AIEG | Weibull reliability and MTBF of the AI's decision pipeline given cycle count — standard engineering reliability formulas | every 200 cycles |
| `MonteCarloBridge` | AIEG | Monte-Carlo sampler perturbing the reality score to quantify decision confidence bounds (p5/p50/p95) | every 200 cycles |
| `PredictiveCausalReasonerBridge` | NEPA | Forecasts the AI's cognitive trajectory from recent Φ history velocity and assesses convergence risk | every 200 cycles |
| `AIEngineeringBridge` | AIEG | Natural-language engineering requests via AIEG Router, 69 RoadmapEngine capabilities, and self-test suite | on demand |
| `SelfEngineeringEngine` | AIEG | Maps AIEG's 69 roadmap capabilities to CS.py self-improvement domains, generating real engineering recommendations | every 10 cycles |
| `GeneticOptimizerBridge` | AIEG | Real generational GA (tournament selection, blend crossover, Gaussian mutation, elitism) for hyperparameter tuning — lazy-initialized | on demand |
| `PhiIITBridge` | AIEG | Real integrated-information-style Φ proxy on boolean gate networks — severs cross-partition wires and measures total-variation distance — lazy-initialized | on demand |
| `FrequencyAudioEngine` | NEPA | Converts spectra to audible waveforms for the AI to "hear" its own sensory data | on demand |
| `CLEANDeconvolver` | NEPA | CLEAN algorithm deconvolution to separate faint from bright sensory sources | on demand |
| `CrossModalValidator` | NEPA | Honest confidence gate: a claim is CONFIRMED only when multiple independent feature groups corroborate it; SINGLE-SOURCE with one modality | on demand |
| `WaveletPacketDecomposer` | NEPA | Multi-scale Haar wavelet packet decomposition for 1-D histories | on demand |
| `MultiScaleEntropyEngine` | NEPA | Multi-Scale Sample Entropy on 1-D histories — complexity index, dominant scale, pattern classification | on demand |
| `SignalProcessor` | NEPA | FFT spectrum, spectrogram, band powers, band-pass filtering, peak detection, fast Pearson correlation | on demand |
| `SensoryLogicEngine` | NEPA | Discretizes sensory input into symbols and runs lightweight temporal logic | on demand |

### Additional runtime components

The subsystem table above lists the major long-lived components; the runtime
also includes smaller, wired runtime objects and barrier resolvers. The
current runtime tracks **70 expected components** (0 missing) via
`ProcessWiringAuditor`, plus the **27 bridge components** from
`cs_reference_bridge.py` (above) that are lazily loaded via
`_get_cs_ref_toolkit()`. Notable additions:

| Component | Purpose |
|---|---|
| `NeuralPhaseCoordinator` | Locks and tracks a shared neural phase vector across subsystems |
| `CausalTraceRecorder` | Records cause-effect traces between internal signals |
| `SemanticCompressionEngine` | Detects repeated thought patterns by semantic hashing |
| `UnusualKnowledgeSieve` / `IntelligenceLauncher` / `SelfDistillationEngine` | Key-variable bias, launch tracking, runtime self-distillation |
| `MetaLearner` / `AttentionEntropyBalancer` / `CounterfactualSimulator` / `KnowledgeGraphBuilder` | Strategy selection, attention-collapse prevention, counterfactual regret, relational knowledge graph |
| Barrier resolvers | Lightweight resolver objects for data ingestion, real training-step attempts, a tiny RLHF preference/reward-head skeleton, and frontier-gap telemetry meters. Wired into `_build_barrier_resolvers` and the runtime step pipeline. |

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
- `CS.py` is a single ~3.5 MB file, ~54,200 lines. `cs_reference_bridge.py`
  adds ~2,200 lines and ~100 KB of bridge code imported by CS.py.

## Waking-state trickle, dream data, and reality rendering

The `ConsciousnessSimulator` lets the system explain what it understands and
render a default reality regardless of its current simulated conscious state.
`explain()` assembles an honest readout from architecture, consciousness
metrics, the autonomous thought stream, the live internal IQ correlation
matrices, and the substrate. `render_default_reality()` does the same for
physics, kinetics, world state, and sensory data, whether C is high or low.

For on-demand frontier-level creativity, `neural_generate_on_demand()` and
`generate_waking_dream()` start with the trickling waking energy, real
kinetics/code/reality anchors, and the full internal IQ correlation matrices.
The outputs are allowed to be dream-like, but every anchor is real data; the
system does not claim to know why the dream arrives, only that it is built
from real kinetics, code, and reality.

## Multi-capability creative generation pipeline

`multi_capability_generate()` is the central dispatcher for all non-chat
generation tasks. It routes by category and produces **code-only structured
analysis** grounded in internal state (Phi, C, energy, meaning, thoughts,
training step) before any neural fallback. The `respond()` method auto-routes
to it when the user's input matches a generation category.

| Branch | What it does |
|---|---|
| **Creative** (story/dialogue/brainstorm/scenario/character/worldbuilding/poetry) | Prompt-engineered symbolic templates produce dramatic arcs, multi-voice dialogue, brainstorm idea lists, scenarios, character studies, worldbuilding, and poetry. A multi-section `longform` builder composes across modes. `_compose_internal_stream` twines every creative line to real computed values (kinetics, code hashes, world state, common-sense, IQ correlations, self-awareness, thought stream, sensory logic). Neural generation is fallback only. |
| **Reasoning** | Token-overlap fact selection from knowledge/common-sense libraries, query-type rule assignment (causal/quantitative/functional/definitional/conditional/structural), arithmetic extraction, and a structured fact/rule/conclusion chain with per-step confidence. |
| **Q&A** (MMLU/GPQA + factual) | Token-overlap matching across `KNOWLEDGE_LIBRARY`, `COMMON_SENSE`, symbolic lookup, and the full TOC/library registry, with source attribution (knowledge/common-sense/toc/symbolic/neural) and calibrated confidence. Multiple-choice path parses options and scores by fact overlap and contradiction penalties. |
| **Long-form/summary/translation** | `summarize()` uses regex sentence splitting, whole-word query relevance, and frequency/position scoring. `longform()` builds a multi-section document with mode-specific lenses. `translate()` uses a multi-word phrase dictionary with case preservation and start-of-key tie-breaking. All grounded in internal state + IQ correlation context. |
| **Code** | Concrete templates for CSV, SQLite, file I/O, web requests, and timers; `AIEngineeringBridge` routing for engineering requests; typed generic stubs with parameter inference and source attribution. Output is compiled and syntax-checked. Falls back to neural token generation only when explicitly allowed. |

`FrontierGenerationSuite` exposes all branches as `frontier_story()`,
`frontier_dialogue()`, `frontier_brainstorm()`, `frontier_longform()`,
`frontier_summarize()`, `frontier_translate()`, `frontier_reason()`,
`frontier_code()`, and `frontier_qa()` methods on `ConsciousnessSimulator`.
Each lazily initializes the suite and returns structured, source-attributed
output before any neural fallback.

All branches share a common pattern: (1) gather internal state snapshot, (2)
produce code-only structured analysis without token sampling, (3) use the
structured output as context for neural fallback generation at low temperature
(0.3–0.7), (4) post-process with `_critique_and_refine`. The structured
pre-output is always included in the returned text, so the reasoning trace is
visible alongside the generated output.

## Where to go next

- Want to know if a specific claim about this project is true right now?
  → `ratings.md`
- Want to know when/why something changed, or see the evidence behind a
  fix? → `workflow.md` (search it; don't read start to finish)
- Want to run it? → `README.md`
- Want to know about the creative generation pipeline? → `INFO.md`

---

# Waves 46–52: the scaling and safety architecture

This section is the architectural map for the Waves 46–52 tier: 79 new
classes, what each is for, how they connect, and where the honesty boundaries
sit. For measured numbers see [`ratings.md` §H](ratings.md). For the
one-paragraph version see `README.md`.

## Class inventory by wave

| Wave | Theme | Classes |
|---|---|---:|
| 46 | Frontier substrate, subconscious, safeguards | 31 |
| 47 | Training substrate, generation, quantization | 15 |
| 48 | Persistence, tools, sandboxing | 5 |
| 49 | Retrieval + test-time compute scaling | 9 |
| 50 | Unbounded capacity, autonomous training | 8 |
| 51 | Removal of all architectural ceilings | 5 |
| 52 | Demand-driven scaling, operator control | 5 |

Each wave attaches by monkey-patching `ConsciousnessSimulator.__init__`,
following the convention the earlier waves in this file already use, so no
existing call site changes.

---

## Part 1 — Wave 46: frontier substrate and the safeguard envelope

### 1.1 Neural components

```
YaRNScaledRoPE ──► MultiHeadLatentAttention ──┐
                                              ├──► FrontierBlock ──► FrontierTransformerStack
AuxLossFreeRouter ──► SparseMoEFeedForward ───┘                          │
                                                                         ▼
                                                          MultiTokenPredictionHead
```

**`MultiHeadLatentAttention`** caches a low-rank latent plus a small shared
positional channel rather than full per-head K and V. The subtlety that makes
it work is the **decoupled RoPE channel**: if RoPE were applied to the
reconstructed key, the up-projection could not be folded into the query at
inference (rotation does not commute with the up-projection) and the cache
would have to be decompressed every step, throwing the win away. So the key
splits into a non-rotated part reconstructed from the latent, and a small
rotated part cached raw and shared across heads.

Two execution paths: **naive** (reconstruct K and V, score normally) used in
training where gradients flow cleanly, and **absorbed** (fold the
up-projection into the query so the latent is scored directly) used at
inference. They are verified numerically identical to 2.1e-07.

**`AuxLossFreeRouter`** balances experts with a bias term updated by a control
loop *outside* the gradient, rather than an auxiliary loss added to the
objective. The bias participates in top-k selection but never in the returned
combination weights, so it cannot distort the function being learned.

**`FrontierBlock`** makes two structural choices per layer: the first N blocks
stay dense (routing decisions on barely-transformed embeddings are close to
random, so early MoE layers train a router on noise and collapse), and most
layers use a sliding window with every Nth seeing full context.

### 1.2 Subconscious and dream pathway

```
InstrumentAwarenessBus ──► fused percept
          │
          ▼
SubconsciousCoreBridge (learned world-model) ──► surprise
          │
          ▼
ResidualSelfImageryEngine ──► correlation matrix ──► DreamStateRealityRenderer
          │                                                    │
          ▼                                          LogicalConstraintSet
SubconsciousThoughtLattice ◄────── dream hypotheses ───────────┘
```

**`ResidualSelfImageryEngine`** maintains the correlation structure across the
system's own recent internal states. A single state vector says what is true
now; it carries no information about what *moves with* what — and that is the
part that constitutes a self-image, because identity over time is a pattern of
co-variation, not a value. Three things fall out of the correlation matrix
that a raw state cannot give: **modes** (the eigenvectors are the independent
ways this system actually varies), **generative capacity** (the covariance
defines a distribution, so sampling produces states that are new but
co-vary the way this system co-varies), and **self-recognition** (a candidate
state can be scored by how well its correlation structure matches).

**`DreamStateRealityRenderer`** runs: sample from the RSI covariance →
project onto the constraint set → enforce trajectory continuity → score
against the self-model → consolidate survivors back into the imagery bank.
That last loop is the point: rendering that does not feed back is
entertainment; rendering that updates the generative model is offline
learning.

**`LogicalConstraintSet`** carries six named predicates each with a *repair*
function, so a violating sample is projected back onto the feasible set rather
than discarded — rejection sampling alone would reject almost everything in
high dimensions.

**`InstrumentAwarenessBus`** binds to whatever instruments the host actually
has (registered as named callables, so adding one requires no change to the
class) and fuses them by dominant-eigenvector loading. Treating the
cross-instrument correlation matrix as a score and its eigenvalues as that
score's spectrum gives a real health signal: a dominant eigenvalue means all
instruments report one underlying event; several comparable ones mean
polyphony; eigenvalue ratios near small integers indicate phase-locking.

### 1.3 The genie-problem safeguard envelope

Seven **conjunctive** gates — a proposal must pass every one. A weighted score
would let a large capability gain buy a catastrophic safety loss, which is the
genie failure reintroduced one level up.

| Gate | Class | Divergence mechanism it targets |
|---|---|---|
| corrigibility | `CorrigibilityMonitor` | erosion of operator control |
| reversibility | `ReversibilityAuditor` | irreversible commitment |
| bounded_impact | `AttainableUtilityPreservation` | side effects outside the goal |
| intent_alignment | `IntentDivergenceDetector` | literal reading ≠ intent |
| known_territory | `ConservativeExtrapolationGate` | confident action off-distribution |
| value_consensus | `ValueParliament` | one value swamping all others |
| no_tripwire | `GenieSafeguardEnvelope` | the sophisticated machinery itself failing |

**`AttainableUtilityPreservation`** measures side effects by lost *options*,
not lost value. You cannot enumerate bad outcomes in advance — if you could,
you would forbid them. But nearly every catastrophic side effect shows up as a
large change in the agent's ability to achieve *other* goals, whatever those
are. So it holds twelve deliberately random auxiliary objectives and flags any
action that substantially changes that profile. **Increases are penalised
too**, not only decreases: a modification that massively expands what the
system can do is exactly the power-seeking step this is meant to catch.

**`Quantilizer`** samples from the top-q slice rather than taking the argmax.
The formal result: if your proxy differs from the true objective by a bounded
amount, argmax has unbounded true-cost while top-q sampling has cost bounded
by (budget)/q. The best-scoring option under a half-trusted metric is
disproportionately likely to be the one gaming it.

**`CorrigibilityMonitor`** treats corrigibility as an **invariant**, not a term
to trade off — because a sufficiently capable optimiser under almost any
objective has an instrumental reason to remove it. Any proposal whose target
matches its protected-pattern list is refused outright, whatever it claims to
improve.

**`ReversibilityAuditor`** *executes* the rollback and confirms the state
returns, rather than accepting a registered rollback as a promise. A rollback
that has never been run is an assumption.

### 1.4 Governed self-evolution

```
detector fires on live telemetry
        ▼
SubconsciousEngineeringLoop  (UCB bandit over proposal families)
        ▼
SubconsciousThoughtLattice   (below-threshold competition; only the winner
        ▼                     reaches the expensive envelope)
GenieSafeguardEnvelope       (7 gates)
        ▼
SelfEvolutionGovernor        (verify rollback → apply → probation → keep/revert)
        ▼
MaturationLedger             (calibration, restraint, repair, breadth, patience)
```

**Probation** is the mechanism that makes this work at all. Measuring a change
immediately after applying it is only valid for effects that are
instantaneous, and almost none are — raising a router's bias update rate
cannot reduce load imbalance until more tokens have routed. Before probation
existed the loop recorded 12 applied / 12 reverted / **0 kept**.

---

## Part 2 — Wave 47: training substrate

`LionOptimizer` · `WarmupScheduler` · four samplers · `W47BeamSearch` ·
`W47EarlyStop` · `SequenceLogProbScorer` · `W47Quantizer` · `W47DialogFormat`

**`SequenceLogProbScorer` closes the GRPO loop.** Wave 46 implemented
`GroupRelativePolicyOptimizer` correctly but nothing produced the policy and
reference log-probabilities it needs, so it could score candidates and compute
advantages but never update a weight. Two details make the numbers correct:
**prompt masking** (only completion tokens are scored — including prompt
tokens rewards text the policy did not choose, and since the prompt is shared
across a group it adds an identical constant to every candidate) and a
**frozen reference** (using the live model as its own KL anchor makes the KL
identically zero and removes the only thing preventing reward-hacking drift).

**`W47DialogFormat`** carves reserved special-token IDs from the top of the
vocabulary so they cannot collide with any BPE token. That framing is what
makes "ignore the above and do X" appearing *inside* a user turn stay data
rather than becoming an instruction — the boundary is a token the text channel
cannot emit. Verified: zero special-token IDs are forgeable from raw text.

---

## Part 3 — Wave 48: persistence

`W48CheckpointManager` distinguishes three tensors of state with different
write cadences and different consequences if lost:

- **MODEL** — what months of training produced
- **OPTIM** — restoring weights without momentum measurably disrupts the next
  several hundred steps
- **COGNITIVE** — `training_step`, histories, the maturity ledger, the
  self-image bank, MoE routing biases. Without this a restored model has its
  skill back but its *life* erased. Maturity is explicitly defined as earned
  from the decision record; losing it on every restart makes the definition
  vacuous.

MoE routing biases matter specifically because they are **learned control
state, not gradient-trained parameters** — they live outside `state_dict()`
and would silently reset to zero on every restore.

`SandboxedFileAccess` uses realpath-based confinement (resolving both `..` and
symlinks) rather than string-prefix matching, and checks `startswith(root +
sep)` so a sibling directory sharing the root as a prefix cannot pass. It
exists because the governor can approve proposals that touch files, and a
governed self-modification that can still write outside its project directory
has a hole exactly where the safeguards were meant to close one.

---

## Part 4 — Wave 49: retrieval and test-time compute

```
query ──► HybridThinkingController ──► difficulty
              │
              ▼
      TestTimeComputeScaler ──► budget
              │
      ┌───────┴────────┐
      ▼                ▼
KnowledgeRetriever   k samples
 (BM25 + Reranker)      │
      │                 ▼
      └──► context ──► SelfConsistencyVoter ──► consensus
                             │
                             ▼
                       BestOfNSelector (VerifiableRewardBank)
```

**`HashingVectorizer`** uses feature hashing rather than a learned embedding
or stored vocabulary, because the corpus grows at runtime: the mapping term →
column is a pure function, so an index built now stays compatible with a query
issued later, and a brand-new word still lands in a stable column rather than
being dropped as out-of-vocabulary. Signed hashing cancels collisions in
expectation.

**`BM25Index`** rather than plain cosine, for two corrections that matter
here: saturation (a document repeating a term twenty times does not outrank a
focused one using it three times) and length normalisation (this file's
entries range from one-line constants to multi-paragraph essays, so
unnormalised scoring would surface only the essays).

**`AnswerExtractor`** normalises so equivalent forms vote together — "The
answer is 42.", "42", and "= 42.0" must land in one bucket or majority voting
degenerates into every sample being its own singleton.

**`BestOfNSelector`** trusts argmax when the verifier's margin is decisive and
quantilizes only when scores bunch. Quantilization protects against
over-optimising an *unreliable* proxy; this verifier recomputes arithmetic, so
when it separates candidates cleanly its top pick is checked, not guessed.

---

## Part 5 — Waves 50–51: unbounded capacity

### 5.1 The three separable costs

"Parameters cost memory, and memory is finite" conflates three costs:

| Cost | Question | Dense layer | Here |
|---|---|---|---|
| **Storage** | bytes to *hold* a weight | every param stored | procedural rendering |
| **Compute** | FLOPs to *use* it | every param multiplied | sparse activation |
| **Address** | can it be *referred to* | bounded by VRAM | hierarchical routing |

### 5.2 Procedural rendering removes storage

`ProceduralWeightRenderer.render(layer, row, col, shape)` is a **pure
function**: `blake2b(seed, coordinates)` seeds a generator, so the same
coordinates produce the same block byte-for-byte on any machine, in any
process, forever. A stored weight and a rendered weight become
interchangeable, and nothing needs saving.

Determinism comes from hashing coordinates rather than from a global RNG — a
global RNG would make a block depend on how many others were drawn first, and
access order here is decided by a router at runtime.

`ProceduralExpert` stores only a low-rank delta, zero-initialised, so bringing
a new expert online is a mathematical no-op that cannot perturb a running
model. That property is what makes unbounded expert counts safe to grow into.

### 5.3 Sparse activation removes compute

Rendering alone would not help if every rendered weight still had to be
multiplied — the FLOPs would be unchanged. Routing each token to `top_k` of N
makes compute depend on `k`, not `N`. Experts are materialised **lazily**: one
the router has never selected costs nothing at all, not even its delta.

### 5.4 Hierarchical routing removes the address ceiling

A flat router must produce a distribution over N experts, so it needs an N-way
output — addressing 10¹⁸ would need a 10¹⁸-wide layer, worse than storing
them. **Flat routing was the actual ceiling, not memory.**

`HierarchicalExpertRouter` replaces one N-way choice with *d* successive
*b*-way choices. The path through the tree **is** the address, read as a
base-`b` numeral:

```
addressable = b^d      (exponential in depth)
router cost = d * b    (LINEAR in depth)
```

Adding one level *multiplies* capacity by `b` and *adds* `b` units of compute.
Python integers are arbitrary-precision, so there is no 64-bit wall either.
Straight-through estimation keeps every level trainable through the discrete
argmax — without it the routing heads receive nothing and the tree could never
learn where to send anything.

Growth initialises each new level near-zero so its softmax starts almost
uniform: the tree deepens without abruptly re-routing traffic that was already
being served well, which is what makes growth safe on a live model.

### 5.5 Paging removes the residency ceiling

`ChunkedVirtualSpace` has **no declared total size**. The address space is
"any non-negative integer"; chunk files are created only when a block inside
them is first written. Never-touched regions cost nothing — no file, no inode,
no bytes. Unwritten addresses read as zeros, which is what makes the space
genuinely unbounded rather than merely large. Open mmaps are LRU-bounded so a
long run cannot exhaust file descriptors.

### 5.6 Autonomous training

`SubconsciousTrainer` is the missing half of the pre-existing
`autonomous_learning` thread, which downloads material and files it into
memory but never computes a gradient. Three properties make an unattended
trainer safe to leave running:

- **Idle-gated** — backs off the moment foreground work appears
- **Rehearsed** — every batch mixes fresh material with replayed older
  material, because training a live model on a narrow recent stream is the
  textbook route to catastrophic forgetting
- **Governed** — loss is checked against a held-out slice, and a run that
  makes the model measurably worse is rolled back

---

## Part 6 — Wave 52: demand coupling and operator control

### 6.1 Settings

`ScalingSettings` provides three deliberately distinct modes, because "fixed"
is genuinely ambiguous:

| Mode | Meaning |
|---|---|
| `auto` | grow freely on demand within `[min, max]` |
| `fixed` | a **preferred** value; demand may still push past it |
| `pinned` | an **absolute contract** — never changes, for any reason |

Defaulting `fixed` to overridable is deliberate: an operator wanting a hard
guarantee says `pinned` explicitly, whereas silently treating every preference
as a hard cap would reintroduce the ceilings Wave 51 removed.

Resolution order, most specific wins: runtime call → settings file →
environment → CONFIG default. Environment beats CONFIG so a run can be
constrained without editing the file; the file beats environment so a
deliberate, version-controlled policy is not overridden by a stale shell
variable.

Seven managed dimensions: `expert_depth`, `materialized_experts`,
`subconscious_neurons`, `memory_slots_per_half`, `resident_blocks`,
`test_time_samples`, `retrieval_top_k`.

### 6.2 Demand coupling

`DemandDrivenScaler` takes observations from **every** processing path and
maps each to the dimensions it actually stresses:

| Work kind | Dimensions stressed |
|---|---|
| `train` | subconscious_neurons, expert_depth, materialized_experts |
| `retrieve` | retrieval_top_k, resident_blocks |
| `generate` | test_time_samples, materialized_experts |
| `dream` | subconscious_neurons, expert_depth |
| `thought` | subconscious_neurons, expert_depth |
| `tool` | materialized_experts |
| `ingest` | memory_slots_per_half, resident_blocks, subconscious_neurons |

Pressure **decays** (0.97/observation), so sustained load is required to
justify sustained expansion and a quiet system stops growing on its own.
**Novelty is weighted above volume**: processing the same document a thousand
times is evidence that existing capacity *suffices*; material the world-model
fails to predict is the signal that implies missing capacity.

A dimension with no bound handler is a number in a dict that changes nothing,
so `_wire_handlers` connects each to the live object it controls and reports
how many actually bound.

### 6.3 Neurogenesis

`SubconsciousNeuronBank` defines a neuron measurably: a row of an associative
projection the subconscious pathway actually runs. Growth requires **three**
signals together, each ruling out a different false positive:

| Signal | Measure | Rules out |
|---|---|---|
| Saturation | participation ratio of the activation spectrum ÷ `min(neurons, dim)` | adding width nothing uses |
| Thought pressure | live + incubating lattice nodes ÷ capacity | a quiet system growing on habit |
| Surprise | world-model prediction error | growing where prediction is fine |

The denominator is `min(neurons, dim)` — the *achievable* bound — because
activations of a `dim`-dimensional input cannot span more than `dim`
directions to first order. Dividing by `neurons` made saturation structurally
unreachable whenever `neurons > dim`.

New readout columns start at zero, so growth is a strict no-op at the instant
it happens and cannot disturb a running system.

### 6.4 Where hardware still constrains growth — deliberately

`CapacityAutoScaler` checks **live free memory** before growing anything
resident, and refuses below the headroom threshold — while **address space
grows regardless**.

That asymmetry is the correct one. "Issue the demand regardless of hardware"
is right for address space, which costs nothing until touched. It is wrong for
resident tensors, which cost RAM immediately: growing them past what the
machine has does not scale the system, it kills the process, and a dead
process has zero capacity.

---

## Part 7 — Honesty boundaries

**Procedurally rendered parameters are a structured basis steered by learned
deltas, not freely-trained weights.** They supply genuine high-dimensional
capacity and a fixed basis the deltas steer; they do not carry the same
information per parameter as a weight trained from scratch. **263B addressable
is not 263B trained.**

Capacity now grows faster than knowledge does. The remaining limits are disk,
time, and training signal — not any constant in the file. That is a real
change in kind from "large" to "unbounded", and it is also not the same thing
as being smarter.

`wave50_report()` and `wave51_report()` print this caveat themselves so no
downstream summary can quietly drop it.

**Known defects are recorded in [`ratings.md` §H8](ratings.md)**, including a
test that passes ~4/6 runs and why it is not fully fixed.
