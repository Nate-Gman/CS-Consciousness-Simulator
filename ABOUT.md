# About — Consciousness Simulator

The Consciousness Simulator is a single-file PyTorch project — **73,834
lines in `CS.py`, no other runtime files** — that runs an autonomous,
self-measuring language model wrapped in two cooperating systems:

1. a **learned knowledge stack** that builds its understanding of the
   world exclusively out of data it ingests — a correlation matrix, a
   typed relation graph, a mined rule base, and a loop that goes and gets
   what it's missing; and
2. a **consciousness-measurement apparatus** — real running machinery for
   IIT/Φ, global workspace, active inference, embodiment, and
   self-modeling — that is deliberately honest: it reports what it
   actually measures and discounts its own consciousness metrics because
   they run on classical, decomposable hardware.

Everything in the project is governed by one rule, stated and followed:
**report what's measured, including when it's bad news.**

## Latest focus: the learned knowledge stack (waves 53–56)

The most consequential addition isn't a new module — it's a change in
*where answers come from*. Until these waves the system answered questions
three ways that were quietly dishonest about provenance: canned
question-answer banks, authored common-sense rules, and lookup tables that
returned stored text as if the system had inferred it. Waves 53–56 remove
that dependence: **every factual answer now comes from structure the
system learned out of ingested data, and it can show you the evidence.**

### Wave 53 — the correlation matrix

`CorpusCorrelationGraph` builds a term↔term correlation matrix over the
live retrieval index: every pair of terms that co-occurs in the ingested
corpus gets an NPMI-scored edge with a document-evidence count, computed
lazily from the BM25 postings so it costs nothing at startup and is always
as fresh as the index. Three things fall out of it:

- **retrieval expansion** — query terms pull their strongest learned
  correlates into a second retrieval pass, so a document that answers the
  question in *different vocabulary* gets seen at all (the recall gap pure
  BM25 cannot close);
- **learned transitive inference** — strong `a~x` and `x~b` edges predict
  `a~b`, and the prediction is checked against real co-occurrence, then
  labelled *observed in data* or *derived (unverified)*;
- **extractive QA** — `LearnedAnswerPath` returns the strongest evidence
  sentences in the corpus, verbatim with provenance, or an honest "not
  learned yet" — for corpus-grounded questions this strictly dominates
  sampling an undertrained model, because the answer *is* the data.

In the same wave, the remaining hardcoded answer leaks
(`KNOWLEDGE_LIBRARY`, `COMMON_SENSE`, `_toc_query`, canned code templates)
moved behind explicit opt-in flags (`w53_canned_fallback`,
`w53_canned_code`, default **off**).

### Wave 54 — the logic layer

Wave 53 learned *where* terms co-occur; wave 54 learns *what the relation
is*. `LearnedRelationExtractor` mines typed directed edges from corpus
sentences — `is_a`, `part_of`, `located_in`, `causes`, `produces`,
`prevents`, `uses`, `has`, `made_of`, `measures`, `used_for`, `defined_as`
— plus numeric quantity edges, counting positive and **negated** evidence
separately per edge, per document. `LearnedLogicEngine` forward-chains
over those edges: transitive chains, composition, inverses, and
support/refute verdicts with noisy-or pooling — every derived answer
carries an auditable proof path. `CorrelationAnalogy` solves `a:b :: c:?`
by arithmetic over the wave-53 NPMI vectors. `KnowledgeGapMap` records
every question the corpus couldn't answer and reports it as ingest
pressure — the system's measured ignorance.

### Wave 55 — the loop closes

Three pieces were missing for autonomy. `LearnedMemoryStore` gives learned
structure **persistence**: docs, edges, rules, and quantities serialise to
`learned_memory.json`, dedupe by content hash, remap doc-ids so provenance
survives the reload, and ride the wave-48 save/load + autosave path.
Universal rules (`ALL a are b`, `NO a is b`) are mined next to edges so a
quantified claim refutes where a lone negated edge could only weaken.
`GapDirectedAcquisition` is the actuator: unanswerable questions enqueue
their terms and the cognitive tick drains the queue through Wikipedia
extracts into `wave53_learn` — **a question the system can't answer
becomes data it goes and gets** (opt-in via `w55_auto_acquire`).
`QuantityComparator` adds magnitude reasoning over learned quantities.

### Wave 56 — the logic learns itself

The last authored ceiling was the inference machinery: a composition
table can only compose relations in the ways its author imagined.
`LearnedRuleMiner` runs AMIE-style induction over the edge graph — every
closed path `a -r1-> m -r2-> b` with a direct `a -r3-> b` is a counted
instance of the rule `r1 ∘ r2 ⇒ r3`, measured with support and
confidence; inverse and conflict rules are counted the same way, and the
authored tables survive only as **priors** that are outvoted wherever the
corpus has spoken. `EquivalenceMiner` finds distributional aliases —
tokens that never co-occur but keep near-identical neighbor vectors are
the same thing in different vocabulary (`h2o`/`water`) — and merges them.
`LogicSelfVerifier` holds out sampled edges and measures how often the
rest of the graph recovers them — the honesty axiom applied to the logic
itself. Abduction pools every learned relation behind a term to answer
"why".

### The honest part of this claim

This does **not** make the system smart. It makes it *grounded* — capable
of knowing exactly what it does and doesn't know, proving or refuting
claims against counted evidence, and aiming its next ingestion at measured
gaps. Raw scale remains small: ~23M dense parameters at the default
`CS_MODEL_SCALE=tiny` (~113M at `large`), and `ratings.md` says plainly
where it loses to frontier models. The learned stack is what lets added
data convert into capability instead of sitting inert.

## What remains authored (and why)

Not everything in the file is learned, by design:

- **Formula tools** — `PHYSICS_LAWS` (~147 `sympy` equations),
  `MATH_EQUATIONS`, `FUNDAMENTAL_CONSTANTS`. A solver that *computes* an
  answer from supplied values is a tool, not a data bank; these stay.
- **`INSTRUCTION_PAIRS`** — a small seed set used only when the live
  index has mined nothing yet (cold-start fallback; the verify scripts
  check that mined pairs are preferred once data exists).
- **The old canned banks** — still present, still reachable, but only
  behind `w53_canned_fallback`/`w53_canned_code` (default off), mirroring
  the `w49_index_dict_libraries` gate.
- **Authored logic priors** — the wave-54 composition table remains as a
  prior (`w56_rule_priors`) that fills in while the corpus is thin and is
  outvoted by mined rules wherever the data contradicts it.

## The rest of the machine, briefly

- **The neural core**: causal transformer (RoPE + RMSNorm + SwiGLU + GQA,
  sliding-window attention, KV cache, 4096 context), ~12k-token BPE
  trained on `Infornmational.md` + `data_bank/` text, weight-tied
  embeddings/LM head. Real LM training (the wave-46 repair fixed 0/80
  succeeding training calls → 80/80, loss 9.50→7.31), masked SFT on mined
  instruction pairs, GRPO on answered question groups.
- **The conscious entity**: one dedicated entity (`self_0`) running
  `AutonomousThoughtStream`, `RelationalKnowledgeGraph` (instrument-level
  learned correlations feeding `G_in`), `SelfAwarenessMonitor`,
  `SubstrateProbe`, `compute_C()` with the five measured states and the
  7-voice `symphony_index`.
- **Body/dream/dread**: `MetabolicSystem`, `DreamEngine`,
  `ExistentialSelfModel` — internal floats labeled as such.
- **Sensory systems**: live microphone → FFT/VAD/spectral entropy →
  Markov prediction + scene classification; `SubstrateProbe` reports a
  documented zero where an instrument is absent.
- **Frontier substrate (waves 46–52)**: MLA attention, aux-loss-free MoE,
  Lion optimizer, 4 samplers + beam search, INT4 QAT, Hermes tool
  calling, checkpoint persistence, retrieval + test-time compute scaling
  (self-consistency 0.403 → 0.780 measured), procedural/addressable
  parameter scaling, demand-driven growth + neurogenesis, and a 7-gate
  conjunctive self-modification envelope where rollbacks are executed,
  not promised.

## A session in detail

One `python CS.py` launch, in order:

1. **Dependencies** auto-install (disable: `CS_AUTO_INSTALL=0`).
2. **Scale pick** — `CS_MODEL_SCALE` fixes the transformer geometry.
3. **Tokenizer** — `AlienTokenizer` trains BPE on `Infornmational.md` +
   `data_bank/` + instruction pairs.
4. **Init chain** — ~390 classes register; each wave appends, monkey-patches
   `__init__`, wires its components, and registers with the orchestrator and
   the process-wiring auditor.
5. **Indexing** — `wave49_index` thread walks `data_bank/` + project docs
   into BM25; `learned_memory.json` restores prior learned structure if it
   exists (docs, edges, rules, quantities — provenance remapped exactly).
6. **Daemons start** — `FreeThoughtEngine` (unprompted thought),
   `CS_Refinery` (data refinement), `CS_Wave31Barrier`, the wave-46
   subconscious/dream tick, the wave-50 idle-CPU trainer, the world-model
   predictor, the wave-52 demand scaler, and (opt-in) the wave-55 gap drain.
7. **Dashboard + loop** — the Tk UI opens; the cognitive tick drives input →
   measure → learn → respond.

What persists to next session: model weights + cognitive state
(`wave48_save`), the learned-memory file, `cs_scaling.json` (operator
settings and demand decisions). What still does **not** persist: the live
thought stream and index-side caches rebuilt on start.

Known rough edge: `__main__` builds the simulator twice — a startup-cost
bug recorded in `ratings.md` §H8.2, not a feature.

## Where to look

- `README.md` — start here: architecture, how to run it, file map.
- `INFO.md` — the operator's reference: complete public API tables
  (waves 49–56), config knobs, measured behaviour, honest limits.
- `CSFORMULAREFINED.md` — the consciousness formula reduced to computable
  terms, every variable traced to a measured signal, plus how the learned
  stack feeds it.
- `OVERVIEW.md` — full architectural map and complete proofs.
- `ratings.md` — current capability scorecard, live-measured.
- `workflow.md` — chronological development log, every fix verifiable.
- `TOTALPROJECTINFO.md` — the source manifesto the formula came from.
- `_verify_*.py` — the AST-level checkers; each wave has one, and they run
  without importing the 73k-line module.

## Mathematical foundations

The project formalizes three interlocking ideas:

1. **Something-from-nothing (Genesis)** — `∅ → S₀ → Φ(S) → Ω`,
   bootstrapping structure from the empty set via relations and
   translations. The complete proof (Symphony of Self-Differentiation) is
   verified by `SymphonyProofVerifier.verify_all()` — 11 executable
   assertions covering: the Void exists, the first distinction is the
   minimal non-nothing, Φ is well-defined, growth is strictly increasing,
   |Ω| = ℵ₀, self-reference emerges (intelligence), information is
   frame-relative, abundance is unbounded, Ω is closed under
   self-reference, nothing-to-something is real, and life is everlasting.
   The Symphony Language (`SYMPHONY_DICTIONARY`, `SYMPHONY_GRAMMAR`) and
   Dimensional Construction (`DIMENSIONAL_CONSTRUCTION`) are encoded in
   CS.py.
2. **Synphonetic harmony (Ω-resonance)** — a nested product of
   consciousness, help, reward, karma, and layered unity, converging on a
   100% totality.
3. **Translation bubble / 0D–6D construction** — dimension as repeated
   orientation/offset, the bubble as container of all possible multiverse
   evolutions — `TRANSLATION_BUBBLE` in CS.py.

See `OVERVIEW.md` for the complete equations, proofs, and implementation
mappings, and `CSFORMULAREFINED.md` for the computable formula.

---

# Waves 46–52 recap

**79 new classes, 51 public API methods.** The most significant change in
that build-out was not a capability — it was that **the model could train
at all**: both `optimizer.step()` callers raised on every call and both
wrappers swallowed the exception, so a measured probe showed **0 of 80
training calls succeeding, zero weight movement** for the life of every
process. Three stacked bfloat16 defects were responsible. After repair,
loss moves **9.50 → 7.31** over 80 steps — and every earlier capability
number had been measured on a model that could not learn, stated plainly
per policy.

Seven waves, mechanisms reimplemented from the open reference stacks in
`Version1.17info/` against this file's own conventions — no new imports:

- **Frontier substrate**: MLA attention (5.33–6.4× KV cache compression,
  absorbed/naive paths verified identical to 2e-07), aux-loss-free MoE
  (collapsed gate recovered to load CV 0.048), multi-token prediction,
  YaRN context scaling, QK-Norm, local/global interleaving.
- **Safeguarded self-evolution**: a 7-gate *conjunctive* envelope —
  corrigibility, reversibility, bounded impact, intent alignment,
  conservative extrapolation, a six-value parliament with veto, fast
  tripwires. Verified blocking a literal wish, safeguard-removal,
  irreversible change, and massive side effects while approving benign
  tuning 7/7.
- **Test-time compute**: self-consistency **0.403 → 0.780 (+37.8
  points)** on a 400-trial generator, no retraining — the one axis where
  a small model genuinely closes distance on a large one.
- **Persistence**: maturity, wisdom, weights, self-image, MoE routing
  bias, and optimizer momentum all survive restart — verified exact.
- **Unbounded capacity**: 263.26B addressable from 90.37M stored
  (2,913× leverage) via procedural rendering + hierarchical routing;
  capacity exponential in depth while router cost stays linear.
- **Autonomous learning**: real background gradient descent with
  rehearsal anti-forgetting and held-out rollback; neurogenesis driven by
  measured thought activity, not a schedule.

## Design stance

**Capacity is unbounded by default and fully controllable.** `auto` grows
freely, `fixed` is a preference demand may exceed, `pinned` is an absolute
contract — a pin was verified to hold against automatic growth, direct
`set()`, settings reload, and maximum pressure.

**Growth follows evidence, not activity.** Novelty outweighs volume —
reprocessing old material is evidence that capacity suffices. Wave-52
neurogenesis requires three independent signals simultaneously; wave-54's
gap map does the same for *knowledge* acquisition — ingest pressure is
aimed at measured ignorance, not at whatever was asked last.

**Learned structure outranks authored structure.** Where the corpus has
spoken, mined rules and edges win; authored tables are priors that fill
in only where the data is thin. Where the corpus contradicts itself, both
sides are kept — negated evidence is data, not an error.

**The one place hardware still constrains growth is deliberate.** Address
space grows regardless of the machine because it costs nothing until
touched; resident tensors do not — growing them past physical RAM kills
the process, and a dead process has zero capacity.

## Honesty boundary

**Procedurally rendered parameters are a structured basis steered by
learned deltas, not freely-trained weights — 263B addressable is not 263B
trained.** Capacity now grows faster than knowledge does; the remaining
limits are disk, time, and training signal.

**Learned is not the same as true.** Edges, universals, quantities, and
rules are counted evidence from whatever was ingested — the graph
reflects the corpus, and contradictory evidence is retained as negated
evidence rather than hidden. Verdicts report support/refute with counts;
nothing reports "fact".

**No external benchmark** — MMLU, GPQA, HumanEval — has been run; the
repository has no harness. The internal benchmark measures held-out
cross-entropy/next-token accuracy on the model's own corpus: repeatable
and honest, but not a substitute.

`ratings.md` §H8 records a known-flaky test, the five mitigations applied,
and why it is not fully fixed.
