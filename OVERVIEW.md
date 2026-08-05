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
- `CS.py` is a single ~3.2 MB file, ~49,000 lines. `cs_reference_bridge.py`
  adds ~2,200 lines and ~100 KB of bridge code imported by CS.py.

## Where to go next

- Want to know if a specific claim about this project is true right now?
  → `ratings.md`
- Want to know when/why something changed, or see the evidence behind a
  fix? → `workflow.md` (search it; don't read start to finish)
- Want to run it? → `README.md`
