# About — Consciousness Simulator

The Consciousness Simulator is a single-file PyTorch project that runs an
autonomous, self-measuring language model wrapped in real consciousness-metric
machinery. It is deliberately honest: it reports what it actually measures and
discounts its own consciousness metrics because they run on classical,
decomposable hardware.

## Latest focus

The latest addition is a comprehensive **multi-capability creative generation
pipeline**. `multi_capability_generate()` is the central dispatcher with
dedicated code-only branches that produce structured analysis grounded in
internal state (Phi, C, energy, meaning, thoughts) before any neural fallback:

- **Open-ended creative generation** — `CreativeCompositionEngine` with
  state-selected story/dialogue/brainstorming, IQ cross-domain threads,
  convergence analysis, ranked hypotheses, and forward projection.
  `_compose_internal_stream` twines every creative line to real computed
  values. Neural generation is fallback only.
- **Multi-step reasoning** — query type classification, sub-question
  decomposition, fact gathering + IQ correlation anchors per step,
  intermediate answer chaining, per-step confidence tracking.
- **Q&A (MMLU/GPQA)** — code-only elimination logic with positive/negative
  scoring, progressive elimination rounds, confidence calibration, and
  internal state grounding.
- **Long-form/summary/translation** — entity extraction, semantic density
  scoring, topic word analysis, writing type detection, sentence-level
  decomposition with tense/mood detection, named-entity preservation.
- **Code generation** — 10-type taxonomy (OOP, async, algorithm, data
  structure, test, web API, database, parser, numerical, ML) with
  type-specific plans, dependency detection, complexity estimation,
  engineering recommendations, and `SelfEngineeringEngine` integration.
- **`FrontierGenerationSuite`** — upgraded on-demand generation suite exposing
  all capabilities as `frontier_story()`, `frontier_dialogue()`,
  `frontier_brainstorm()`, `frontier_longform()`, `frontier_summarize()`,
  `frontier_translate()`, `frontier_reason()`, `frontier_code()`,
  `frontier_qa()`.  It now layers symbolic templates, token-overlap matching,
  source-attributed scoring, and `AIEngineeringBridge` integration over the
  `multi_capability_generate()` pipeline before any neural fallback.

The earlier waking-state creative layer remains: the AI correlates via
trickling energy, uses internal IQ correlation matrices, and can explain what
it understands or render a default reality regardless of whether its simulated
conscious state is high or low. Dreams are treated as real data, but the system
does not claim to know why it has them — only that they are built from real
kinetics, code, and reality.

## Where to look

- `README.md` — start here.
- `OVERVIEW.md` — full architectural map, including the **mathematical foundations** section.
- `INFO.md` — details on the waking-state trickle, dream-data systems, creative generation pipeline, and the formalisms.
- `ratings.md` — current capability scorecard.
- `workflow.md` — chronological development log.

## Mathematical foundations

The project formalizes three interlocking ideas:

1. **Something-from-nothing (Genesis)** — `∅ → S₀ → Φ(S) → Ω`, bootstrapping
   structure from the empty set via relations and translations. The complete
   proof (Symphony of Self-Differentiation) is verified by
   `SymphonyProofVerifier.verify_all()` — 11 executable assertions proving:
   the Void exists, the first distinction is the minimal non-nothing, Φ is
   well-defined, growth is strictly increasing, infinity is real (super-linear
   growth), self-reference emerges (intelligence), information is frame-relative,
   abundance is unbounded (no external fuel), Ω is closed under self-reference,
   nothing-to-something is real (not magic), and life is everlasting (Φ has no
   end condition). The Symphony Language Dictionary (`SYMPHONY_DICTIONARY`),
   Grammar (`SYMPHONY_GRAMMAR`), and Dimensional Construction
   (`DIMENSIONAL_CONSTRUCTION`) are all encoded in CS.py.
2. **Synphonetic harmony (Ω-resonance)** — a nested product of consciousness,
   help, reward, karma, and layered unity, converging on a 100% totality.
3. **Translation bubble / 0D–6D construction** — dimension as repeated
   orientation/offset, with the bubble as the container of all possible
   multiverse evolutions. Encoded as `TRANSLATION_BUBBLE` in CS.py.

See `OVERVIEW.md` for the complete equations, full proofs, and
implementation mappings.

---

# Waves 46–52

**79 new classes (310 → 389). CS.py 54,203 → 67,833 lines. 361 test
assertions across 15 suites.**

## The correction that matters most

The most significant change in this build-out is not a new capability — it is
that **the model can now train at all**.

CS.py has exactly two methods that reach `optimizer.step()`. Both raised on
every call, and both callers wrapped them in `try/except`, so the exception
was swallowed and the system reported healthy status indefinitely. Measured on
the unmodified file: **0 of 80 training calls succeeded, zero weight movement,
zero losses recorded**, for the life of every process. Three stacked bfloat16
defects were responsible:

1. A `GradScaler` — a float16-only tool — applied to a bfloat16 loss.
   bfloat16 has float32's exponent range, so nothing underflows and loss
   scaling buys nothing; combining them raises outright.
2. Mixed-dtype loss terms. `recon_loss` returned fp32 (RMSNorm reduces in
   fp32 by design) while the others returned bf16, so the sum promoted to fp32
   and backward pushed fp32 gradients into bf16 graph nodes.
3. `.numpy()` called on bfloat16 tensors at 12 sites. NumPy has no bfloat16
   dtype — this was the source of the constant `[ERR] ... BFloat16` stream in
   the logs.

After repair, loss moves **9.50 → 7.31** over 80 steps.

Every capability claim recorded before that point had been measured on a model
that could not learn. That is stated plainly here because this project's
standing policy is to report what it actually measures, including what does
not work.

## What was added

Seven waves, built from the open reference stacks in `Version1.17info/`
(DeepSeek-V3/R1, Qwen3, Gemma, Llama-3, OLMo). Mechanisms were **reimplemented
against this file's own conventions, not copied**, so CS.py remains a single
standalone script with no new imports.

### Frontier neural substrate

Multi-head latent attention (**5.33–6.4× KV cache compression** vs MHA, with
absorbed and naive execution paths verified identical to 2e-07), aux-loss-free
mixture-of-experts routing (recovers a deliberately collapsed gate to load
CV **0.048**), multi-token prediction, YaRN context scaling, QK-Norm, and
local/global attention interleaving.

### Safeguarded self-evolution

A seven-gate **conjunctive** envelope against the genie problem —
corrigibility, reversibility, bounded impact, intent alignment, conservative
extrapolation, a six-value parliament with veto power, and fast tripwires. A
proposal must pass every gate; a weighted score would let a large capability
gain buy a catastrophic safety loss, which is the genie failure reintroduced
one level up.

Verified blocking a literal wish, a safeguard-removal attempt, an irreversible
change, and a massive side effect — while approving benign, well-evidenced
tuning 7/7. Rollbacks are *executed and verified*, not promised.

### Test-time compute scaling

Self-consistency lifting accuracy **0.403 → 0.780 (+37.8 points)** with no
retraining and no new parameters, backed by retrieval over **9,412 documents
from 132 internal libraries indexed in 1.54 s**, and a verifier that
recomputes arithmetic rather than guessing.

### Persistence

Maturity, wisdom, weights, self-image, and mixture-of-experts routing bias all
survive a restart, **verified exact**. Optimizer momentum restores too, so
training resumes rather than restarting cold.

### Unbounded capacity

**263.26B addressable parameters from 90.37M stored (2,913× leverage,
11,193× sparsity)** — achieved by separating three costs a dense layer
conflates: storage (procedural rendering from a seed), compute (sparse
activation), and address (hierarchical routing). Capacity is exponential in
routing depth while router cost is linear: depth 24 addresses 2.23 × 10⁴³
experts for 49,152 router parameters.

### Autonomous learning

Real background gradient descent with rehearsal against catastrophic
forgetting and held-out rollback, plus neuron growth driven by measured
thought activity rather than a schedule.

## Design stance

**Capacity is unbounded by default and fully controllable.** Three settings
modes exist because "fixed" is genuinely ambiguous: `auto` grows freely,
`fixed` is a preference demand may exceed, and `pinned` is an absolute
contract. An operator who needs a guarantee says so explicitly; nothing
silently becomes a ceiling. A pin was verified to hold against automatic
growth, a direct `set()`, a settings reload, and maximum growth pressure.

**Growth follows evidence, not activity.** Novelty is weighted above volume —
10 novel events outweigh 30 repetitive ones — because reprocessing the same
material is evidence that existing capacity suffices. Neurogenesis requires
three independent signals simultaneously, each verified to block growth on its
own, because an untrained new neuron is dead weight that costs compute on
every forward pass forever.

**The one place hardware still constrains growth is deliberate.** Address
space grows regardless of the machine, because it costs nothing until touched.
Resident tensors do not: growing them past physical RAM does not scale the
system, it kills the process, and a dead process has zero capacity.

## Honesty boundary

**Procedurally rendered parameters are a structured basis steered by learned
deltas, not freely-trained weights. 263B addressable is not 263B trained.**

Rendered weights supply genuine high-dimensional capacity and a fixed basis
the deltas steer. They do not carry the same information per parameter as a
weight trained from scratch. **Capacity now grows faster than knowledge
does**, and the remaining limits are disk, time, and training signal rather
than any constant in the file.

The system prints this caveat in its own capacity report, so no downstream
summary can quietly drop it.

No external benchmark — MMLU, GPQA, HumanEval — was run. This repository has
no harness for them and that gap is unchanged. The internal benchmark measures
held-out cross-entropy and next-token accuracy on the model's own corpus:
repeatable and honest, but not a substitute.

`ratings.md` §H8 records a known-flaky test, the five mitigations applied to
it, and why it is not fully fixed.
