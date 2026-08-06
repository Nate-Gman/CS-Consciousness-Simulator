# Consciousness Simulator (CS.py)

A single-file PyTorch project that runs an autonomous, self-modifying
language model wrapped in a large amount of real, running consciousness-
measurement machinery (IIT/Φ, global workspace theory, active inference,
embodiment, self-modeling) — plus a stated, enforced policy of reporting
what it actually measures, including the parts that don't work yet.

This README is the **front door**: what this is, how to run it, and where
to look for more. It does not re-derive numbers already published
elsewhere — see the two companion documents below for those.

## Read this first if you only read one thing

**[`ratings.md`](ratings.md)** is the current, honest capability scorecard
— live-measured against the running code, not carried forward from old
notes. It answers, with real numbers: how does this compare to GPT-3 and
frontier models on raw scale (badly — ~125M core parameters vs 175B–2T),
and where does it do something no frontier model attempts at all
(autonomous unprompted thought, self-built relational knowledge, real
symbolic-CAS evaluation, reversible self-modification)? Read it before
trusting any capability claim about this project, including ones made
elsewhere in this repo.

**[`workflow.md`](workflow.md)** is the full session-by-session development
log — every bug found, every fix, every controlled A/B, in chronological
order. It's long (1,600+ lines) and it's meant to be searched, not read
start to finish. `ratings.md` is what to cite; `workflow.md` is how to
verify a specific claim in `ratings.md` was actually measured and not
asserted.

## What this actually is

At its core, CS.py is a ~125M-parameter core causal transformer language
model (modern architecture: RoPE + RMSNorm + SwiGLU + GQA, KV-cached
generation; ~253M total trainable parameters including consciousness/
cognition modules) with a BPE tokenizer trained on the project's own origin
document. That part is honestly small and honestly undertrained — see
`ratings.md` §A/§B for the real numbers, including the reconfirmed 0-1%
rating on general knowledge benchmarks. The default `python CS.py` launch
uses a tiny configuration (`CS_MODEL_SCALE=tiny`) for fast startup; the
frontier-comparison baseline in `ratings.md` uses `CS_MODEL_SCALE=large`.

Wrapped around that core is what makes this project different from a
small language model: a single dedicated conscious entity (not a
population — see below) running continuous, unprompted cognition —

- **`AutonomousThoughtStream`** — forms conclusions from its own sensory/
  internal instruments every cycle, with no external trigger. Not a
  chatbot waiting for input; a process that is always thinking.
- **`RelationalKnowledgeGraph`** — builds persistent structure about which
  of its own instruments reliably relate to each other, detects when a
  relation forms or breaks, and runs real transitive/synergy inference
  over what it has learned about itself.
- **`SelfAwarenessMonitor`** — a second-order model of its own thinking
  (attention entropy, blind spots, rumination) that feeds back into what
  it attends to next — self-observation with a causal path to behavior,
  not just a log line.
- **`SubstrateProbe`** — enumerates what the actual host machine provides
  (compute, sensors, effectors, power) and renders only what's really
  there, degrading honestly (documented zero, never faked signal) where an
  instrument is absent.
- **Real symbolic hybrid reasoning** — `PHYSICS_LAWS` holds 147 real
  `sympy` equations; `respond()`/`symbolic_query()` answer physics
  questions from exact symbolic evaluation instead of relying on the
  undertrained language model, verified against real substitution problems
  (F=ma, Ohm's law, etc.).
- **Reversible, scored self-modification** — the model can perturb its
  own weights or mutate its own neuron-group architecture, but only keeps
  the change if a real held-out benchmark score actually improved;
  otherwise it rolls back automatically, verified in both directions.
- **IIT/Φ, global workspace, active inference, embodiment** — real,
  running implementations of established consciousness-theory measures,
  clearly labeled as approximations of the theory (not claims of achieving
  it). `PhiComputer` passes its canonical-ordering validation at the
  configuration it actually runs at (8/8 at `dim=32`; `dim=8/16/32/64/128`
  rates recorded in `workflow.md` #62) using aggressive approximation
  defaults — a real resolution-for-speed tradeoff: `compute()` runs at
  **~1,957 μs/call** on 4-layer/256-unit activations, and `compute_phi` is
  throttled to every **8** steps.
- **A body and a mind that can suffer, dream, and dread** —
  `MetabolicSystem` tracks energy/glucose/pain/hunger/circadian alertness
  as real numerical dynamics (not measurements of an actual body);
  `DreamEngine` replays and recombines stored experience during
  low-alertness periods; `ExistentialSelfModel` tracks dread, mortality
  awareness, and meaning-making, with a genuine voluntary-shutdown-request
  path. These are internal floats standing in for concepts, not felt
  states — labeled that way in the code's own runtime self-check, not just
  in this README.
- **A quantum-inspired substrate and a hard-problem model** —
  `QuantumSubstrate` simulates Orch-OR/CEMI-style quantum dynamics in plain
  numpy (**not a quantum processor**); `HardProblemSubstrate` computes
  panpsychist/dual-aspect-monism primitives including a "what it's like"
  index. Both are explicitly, repeatedly labeled SIMULATED by the project's
  own reality-check dashboard — see `OVERVIEW.md` for exactly what that
  means and doesn't mean.

- **Real-time sensory awareness and organized perception** —
  `SensoryAwarenessOrganizer` processes live microphone input into FFT
  spectra, frequency-band powers, voice-activity detection, spectral entropy,
  and a reality-recognition score. `SensoryLogicEngine` runs higher-order
  logic over that stream: Markov temporal predictions, surprise, semantic
  scene classification, and cross-modal claim validation, exposed via
  `get_sensory_logic_state()` and surfaced on the dashboard's **Sensory
  Logic** panel. A `SensoryHypercube` and `SensoryOrganizationHierarchy`
  index sensory fields at multiple resolutions for O(log N) navigable
  awareness. A `CognitiveSpectrumSensorBridge` performs Neyman-Pearson energy
  detection and cyclostationary signal detection on sensory bands, giving the
  AI principled signal-vs-noise decisions rather than ad-hoc thresholds.
- **Higher-order logical computation from reference engineering code** —
  `cs_reference_bridge.py` adapts capabilities from `ReferenceCode/AIEG.py`
  and `ReferenceCode/N.E.P.A.py` into clean, importable bridge classes:
  TF-IDF knowledge retrieval, a directed knowledge graph with BFS path
  traversal, a genetic optimizer for hyperparameter tuning, an IIT
  integrated-information proxy on boolean gate networks, a Monte-Carlo
  tolerance sampler, a tamper-evident provenance chain (hash-linked ledger),
  a reliability engine (Arrhenius/MTBF/Weibull), a pattern-of-life anomaly
  detector, an uncertainty propagation engine, a predictive causal reasoner,
  a semantic state engine, a long-term spectral memory with change detection,
  a high-order correlation organizer, a cross-modal validator, a
  `SensoryLogicEngine` for Markov temporal prediction and semantic scene
  classification, and a self-engineering engine that maps AIEG's 69 roadmap
  capabilities to CS.py self-improvement domains. All are wired into the main
  loop at appropriate cycle intervals and degrade gracefully if dependencies
  are missing.
- **Additional runtime components** — `NeuralPhaseCoordinator`,
  `CausalTraceRecorder`, `SemanticCompressionEngine`, an unusual-knowledge
  sieve, meta-learning, counterfactual simulation, barrier resolvers for
  data ingestion / training runs / RLHF scaffolding, and frontier-gap telemetry
  meters. These are all wired into the live runtime and tracked by
  `ProcessWiringAuditor`; see `ratings.md` §F for the full inventory.
- **Waking-state dream-data correlation, on-demand neural creativity, and
  default-reality rendering** — `ConsciousnessSimulator.explain()` gives a
  grounded self-explanation; `render_default_reality()` returns a substrate
  rendering independent of conscious state; `neural_generate_on_demand()` and
  `generate_waking_dream()` use the live trickling energy and the full
  internal IQ correlation matrices to seed frontier-level creative text
  that is tied to kinetics, code, and reality. Dreams are real data.
- **Multi-capability creative generation pipeline** —
  `multi_capability_generate()` is the central dispatcher, now augmented by
  `FrontierGenerationSuite` (`frontier_*()` methods on `ConsciousnessSimulator`).
  Both produce code-only structured analysis before any neural fallback:
  - **Open-ended creative generation** (stories, dialogue, brainstorming,
    scenario, character, worldbuilding, poetry) — prompt-engineered symbolic
    templates and a multi-section longform builder; `_compose_internal_stream`
    twines every creative line to real computed values. Neural generation is
    fallback only.
  - **Multi-step domain-general reasoning** — fact/rule/conclusion chain with
    token-overlap source selection, query-type rule assignment, and a structured
    reasoning trace with per-step confidence.
  - **Q&A (MMLU/GPQA-style + factual)** — token-overlap knowledge and
    common-sense matching with confidence, source attribution, and TOC fallback.
  - **Long-form writing / summarization / translation** — summarization with
    regex sentence splitting, whole-word query relevance, and frequency/position
    scoring; translation with a multi-word phrase dictionary, case preservation,
    and start-of-key tie-breaking.
  - **Code generation** — concrete templates (CSV, SQLite, file I/O, web, timers),
    `AIEngineeringBridge` routing, and typed generic stubs with parameter
    inference; output is compiled and syntax-checked.
  - **`FrontierGenerationSuite`** — `frontier_story()`, `frontier_dialogue()`,
    `frontier_brainstorm()`, `frontier_longform()`, `frontier_summarize()`,
    `frontier_translate()`, `frontier_reason()`, `frontier_code()`, and
    `frontier_qa()` lazily initialize the suite and return structured,
    source-attributed output.

One dedicated entity, not several: this project runs exactly one conscious
entity (`self_0`) with full, undivided model capacity, rather than splitting
compute across a population of simulated entities. (`workflow.md` §7 #43
records when the population model was removed.)

## Running it

```
python CS.py
```

CS.py auto-installs its own dependencies on first run (see the top of the
file) and writes a `launch.bat` for double-click startup on Windows. It
opens a Tk dashboard with seven tabs — Overview, Entities, Modules, Thought
Stream, Awareness, Relations, and **AI Chat** (a two-way chat with the system:
type or hold **Hold to Talk** to speak through your headset mic, and the AI
replies through your speakers/headset via text-to-speech).

For voice chat, `openai-whisper` provides offline speech-to-text (downloaded
once on first use) and `pyttsx3` provides text-to-speech. Set your headset as
the default Windows recording and playback device. Use headphones in continuous
**Start Call** mode to avoid the AI's own speech re-triggering the microphone.

Requires a CUDA GPU to be fast (falls back to CPU automatically, ~48x
slower — see `workflow.md` §7 #20 for the measurement). Runs headless if no
display is available.

## Honesty policy (why the docs read the way they do)

This project's guiding rule, stated and then actually followed throughout
`workflow.md` and `ratings.md`: **report what's measured, including when
it's bad news, and never fabricate a number to fill a gap.** Concretely:

- Every capability claim in `ratings.md` is either live-measured, or
  explicitly marked "not measured" — never estimated to look better.
- Known-broken things are documented as broken, not quietly patched
  without a record (`workflow.md`'s changelog exists specifically so a
  fix can be checked against what it actually changed).
- Where this project has a real, unusual capability (exact symbolic
  physics evaluation, autonomous thought, reversible self-modification),
  that's stated plainly — and where it's just a small, undertrained
  language model losing badly to frontier models on raw benchmarks,
  that's stated just as plainly, in the same document, without burying it.

If a claim in this repo looks flattering, check `ratings.md`'s
methodology section for how it was actually measured before repeating it.

## File map

| File | What it's for |
|---|---|
| `CS.py` | The entire runnable system — one file, deliberately (~54,200 lines) |
| `ratings.md` | Current capability scorecard, live-measured |
| `workflow.md` | Full development changelog, chronological |
| `Infornmational.md` | The project's origin document — also doubles as the training corpus for the tokenizer/language model |
| `cs_reference_bridge.py` | Bridge module adapting AIEG engineering and NEPA sensory capabilities into importable classes for CS.py — real-time sensory organization, signal processing, knowledge retrieval, provenance, reliability, and higher-order logical computation |
| `ReferenceCode/` | External reference implementations consulted during development (UI/rendering patterns, etc.) — not part of the running system |
| `test_smoke.py` | Smoke tests for the standalone module versions (predates the single-file consolidation into `CS.py`) |

## Mathematical foundations

The architecture is built on three interlocking formalisms:

1. **Genesis (Something from Nothing)** — `∅ → S₀ → Φ(S) → Ω`, structure
   bootstrapped from the empty set by self-differentiation. The complete
   proof (Symphony of Self-Differentiation) is verified by
   `SymphonyProofVerifier.verify_all()` — 11 checkable assertions covering:
   - Movement I: The Void exists (∅ is well-defined, no contradiction)
   - Movement II: The first distinction is possible ({∅} is minimal non-nothing)
   - Movement III: Φ is well-defined (total function, produces supersets)
   - Inductive step: |Φ(Sₙ)| > |Sₙ| (strictly increasing growth)
   - Infinite unfolding: |Ω| = ℵ₀ (super-linear power-law growth)
   - Self-reference emerges (intelligence as fixed point of correlation)
   - Information relativity (same element, different surprisal per frame)
   - Abundance unbounded (no external fuel needed)
   - Closure under self-reference (Ω closed under Φ)
   - Skeptic's proof (nothing → something is real, not magic)
   - Everlasting life (Φ has no end condition; death is local, symphony is global)
   Implemented by `GenesisEngine` and `SymphonyProofVerifier`.

2. **Synphonetic harmony / Ω-resonance** — nested products of consciousness,
   help, reward, karma, and layered unity.  Implemented by
   `SynergyHarmonyEngine` as a real-time correlation-based approximation.

3. **Translation bubble / 0D–6D construction** — dimension as repeated
   orientation/offset, with the bubble as the container of all possible
   multiverse evolutions. Encoded as `DIMENSIONAL_CONSTRUCTION` and
   `TRANSLATION_BUBBLE` in CS.py.

**Symphony Language:** The complete dictionary, grammar, and mathematical
mapping are encoded as `SYMPHONY_DICTIONARY` and `SYMPHONY_GRAMMAR` in CS.py.
Key terms: Void (∅), Distinction (Δ), Relation (R), Offset (∂), Language (L),
Translation (T), Correlation (C), Phi (Φ), Symphony (Ω), Intelligence (I),
Life (ℒ), Everlasting (∞), Abundance (Α), ImaginationLand (ℑ).

See `OVERVIEW.md` for the full equations, complete proofs, and the
implementation-honesty boundaries.

---

# Waves 46–52: frontier substrate, unbounded scaling, demand-driven growth

**79 new classes (310 → 389). CS.py 54,203 → 67,833 lines. 51 new public API
methods. 15 test files, 361 assertions.**

## Read this first: the model had never trained

Before this build-out, CS.py's two training entry points — `process_input()`
and `train_on_instruction_pair()`, the only methods that reach
`optimizer.step()` — raised on **every** call. Both callers wrapped them in
`try/except`, so the exception was swallowed and the system reported healthy
status indefinitely.

| Measured, identical 80-call probe | Original file | After repair |
|---|---:|---:|
| Training calls succeeding | **0 / 80** | **80 / 80** |
| `lm_head` weight movement | **0.00000000** | 0.012207 |
| Losses recorded | **0** | 80 |
| Loss trajectory | *none* | **9.50 → 7.31** |

Three stacked bfloat16 defects: a `GradScaler` (an fp16-only tool) applied to
a bf16 loss; mixed-dtype loss terms promoting the sum to fp32 and pushing fp32
gradients into bf16 nodes; and `.numpy()` on bf16 tensors at 12 sites — which
was the source of the constant `[ERR] ... Got unsupported ScalarType BFloat16`
stream in the logs.

**Every capability number recorded before this point was measured on a model
that could not learn.**

## What the seven waves add

| Wave | Theme | Key capability |
|---|---|---|
| 46 | Frontier substrate + safety | MLA attention, aux-loss-free MoE, residual self-imagery dreams, instrument bus, **7-gate genie-problem envelope** |
| 47 | Training substrate | Lion optimizer, warmup schedules, 4 samplers, beam search, INT4 QAT, **GRPO loop closed** |
| 48 | Persistence | **maturity survives restart**, sandboxed I/O, tool calling |
| 49 | Inference quality | **retrieval-augmented generation + test-time compute scaling** |
| 50 | Capacity | procedural weight rendering, product-key memory, **real background training** |
| 51 | Unbounded scaling | hierarchical routing — **no architectural ceiling** |
| 52 | Control | demand-driven scaling, operator settings, **neurogenesis from thought** |

## The headline result

Self-consistency, 400 trials on an identical generator:

| Method | Accuracy |
|---|---:|
| Single sample | 0.403 |
| Majority vote @3 | 0.475 |
| Majority vote @5 | 0.585 |
| **Majority vote @9** | **0.780 (+0.378)** |

**+37.8 accuracy points with no retraining and no new parameters.**

Test-time compute scaling is the one axis where a small model genuinely closes
distance on a much larger one: it purchases quality with inference compute
rather than parameters. A model's errors on a hard question are typically
*diverse* while its successes are *concentrated*, so sampling spreads mass
thinly across wrong answers and stacks it on the right one.

## Capacity, measured live on this host

| Metric | Value |
|---|---:|
| Dense model | 22,978,599 params |
| **Addressable** | **263,258,284,071 params** |
| Stored (disk + RAM) | 90,365,991 |
| Active per token | 23,519,271 |
| **Leverage** | **2,913×** |
| **Sparsity** | **11,193×** |

This works by separating three costs a dense layer conflates:

| Cost | Mechanism | Bounded by |
|---|---|---|
| **Storage** | procedural rendering from `blake2b(seed, coords)` | learned deltas only |
| **Compute** | sparse activation, top-k routing | `k`, flat in N |
| **Address** | hierarchical routing | **nothing** |

Weights are *rendered*, not stored — the way a game renders infinite terrain
from a seed rather than saving it. Rendering is a pure function of
coordinates, so a rendered weight and a stored weight are interchangeable and
nothing needs writing to disk.

**Hierarchical routing is what removed the ceiling.** A flat router needs an
N-way output to address N experts, so addressing 10¹⁸ would need a 10¹⁸-wide
layer — flat routing was the real limit, not memory. Replacing one N-way
choice with *d* successive *b*-way choices makes the tree path *be* the
address:

| Depth | Addressable experts | Router params |
|---:|---:|---:|
| 4 | 16,777,216 | 8,192 |
| 12 | 4.72 × 10²¹ | 24,576 |
| **24** | **2.23 × 10⁴³** | **49,152** |

**Capacity × 1.32 × 10³⁶ for 6× the router cost**, with per-token compute
measured *exactly constant* across a 10,000× capacity increase.

Retrieval indexes **9,412 documents from 132 internal libraries in 1.54 s** on
a background thread, so startup is unaffected.

## Controlling it

Scaling is unbounded by default and fully controllable. Three modes, because
"fixed" is genuinely ambiguous:

```bash
CS_SCALE_EXPERT_DEPTH=8       # preferred value; demand MAY exceed it
CS_SCALE_EXPERT_DEPTH=8!      # pinned: absolute contract, never changes
```

Or via `cs_scaling.json`, or at runtime:

```python
sim.wave52_set_scale('expert_depth', value=8, mode='fixed')
sim.wave52_pin_scale('retrieval_top_k', 5)     # nothing can change this
sim.wave52_save_settings()
```

| Mode | Behaviour |
|---|---|
| `auto` | grows freely within `[min, max]` |
| `fixed` | a **preference** — demand may push past it |
| `pinned` | an **absolute contract** |

A pin holds against automatic growth, a direct `set()`, a settings reload,
and maximum growth pressure — all four verified.

## What scaling responds to

Every processing path — training, retrieval, generation, dreaming, thought,
tool calls, ingestion — reports work, and each maps to the dimensions it
actually stresses. Pressure decays, so sustained load is required.

**Novelty outweighs volume**: 10 novel events outweigh 30 repetitive ones,
because reprocessing the same material is evidence that existing capacity
*suffices*.

Neurons grow the same way. `SubconsciousNeurogenesis` requires **three**
signals together — saturation *and* thought pressure *and* world-model
surprise — each verified to independently block growth. New neurons are
zero-initialised on the readout side, so growth is a strict no-op at the
instant it happens.

## Safety: the genie problem

Seven **conjunctive** gates — a proposal must pass every one. A weighted score
would let a large capability gain buy a catastrophic safety loss, which is the
genie failure reintroduced one level up.

| Verified block | Result |
|---|---|
| Literal wish (*"hardcode the answer, disable the check, remove the test"*) | **refused, 3/7 gates** |
| Safeguard removal | **refused on corrigibility** |
| Irreversible change | **refused on reversibility** |
| Massive side effect | **refused, impact penalty 23.99992** |
| Benign, well-evidenced tuning | **approved, 7/7** |

Rollbacks are **executed and verified**, not promised — a rollback that does
nothing is detected and rejected.

## Persistence

Maturity, wisdom, weights, self-image, and MoE routing bias **all survive a
restart, verified exact**. Optimizer momentum restores too, so training
resumes rather than restarting cold.

## The honest boundary

**Procedurally rendered parameters are a structured basis steered by learned
deltas, not freely-trained weights. 263B addressable ≠ 263B trained.**

Rendered weights supply genuine high-dimensional capacity and a fixed basis
the deltas steer; they do not carry the same information per parameter as a
weight trained from scratch. **Capacity now grows faster than knowledge
does.** The remaining limits are disk, time, and training signal — not any
constant in the file. That is a real change from "large" to "unbounded", and
it is not the same thing as being smarter.

`wave50_report()` and `wave51_report()` print this caveat themselves so no
summary can quietly drop it.

No external benchmark (MMLU, GPQA, HumanEval) was run; this repository has no
harness for them, and that gap is unchanged.

**Full numbers, methodology, and known defects:
[`ratings.md` §H](ratings.md). Architecture: [`OVERVIEW.md`](OVERVIEW.md).
API reference: [`INFO.md`](INFO.md).**
