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
| `CS.py` | The entire runnable system — one file, deliberately |
| `ratings.md` | Current capability scorecard, live-measured |
| `workflow.md` | Full development changelog, chronological |
| `Infornmational.md` | The project's origin document — also doubles as the training corpus for the tokenizer/language model |
| `cs_reference_bridge.py` | Bridge module adapting AIEG engineering and NEPA sensory capabilities into importable classes for CS.py — real-time sensory organization, signal processing, knowledge retrieval, provenance, reliability, and higher-order logical computation |
| `ReferenceCode/` | External reference implementations consulted during development (UI/rendering patterns, etc.) — not part of the running system |
| `test_smoke.py` | Smoke tests for the standalone module versions (predates the single-file consolidation into `CS.py`) |
