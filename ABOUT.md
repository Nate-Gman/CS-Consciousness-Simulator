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
- `OVERVIEW.md` — full architectural map.
- `INFO.md` — details on the waking-state trickle, dream-data systems, and creative generation pipeline.
- `ratings.md` — current capability scorecard.
- `workflow.md` — chronological development log.
