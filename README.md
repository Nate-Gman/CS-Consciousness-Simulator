# Consciousness Simulator (CS.py)

A single-file PyTorch project — **73,834 lines, ~4.4 MB, one Python file** —
that runs an autonomous, self-modifying language model wrapped in two large,
real, running systems:

1. a **learned knowledge stack** (waves 53–56) that builds a correlation
   matrix, a typed relation graph, an inductive rule base, and an autonomous
   acquisition loop *entirely out of data the system ingests* — no canned
   answer bank on the answer path; and
2. a **consciousness-measurement apparatus** (IIT/Φ, global workspace theory,
   active inference, embodiment, self-modeling) with a stated, enforced
   policy of reporting what it actually measures, including the parts that
   don't work yet.

This README is the **front door**: what this is, how to run it, what each
file is for, and where to look for more. It does not re-derive numbers
already published elsewhere — see the companion documents for those.

**Contents** — [Read this first](#read-this-first-if-you-only-read-one-thing)
· [What this actually is](#what-this-actually-is) ·
[The learned knowledge stack](#a-the-learned-knowledge-stack-waves-5356--the-answer-path)
· [The consciousness apparatus](#b-the-consciousness-measurement-apparatus)
· [Running it](#running-it) · [Teaching it](#teaching-it-things) ·
[Verification suite](#the-verification-suite) ·
[Honesty policy](#honesty-policy-why-the-docs-read-the-way-they-do) ·
[File map](#file-map) · [Math foundations](#mathematical-foundations) ·
[Wave recaps](#waves-4652-recap) · [Config knobs](#configuration-knobs-learned-stack)
· [Known limits](#known-limits-honestly)

## Read this first if you only read one thing

**[`ratings.md`](ratings.md)** is the current, honest capability scorecard
— live-measured against the running code, not carried forward from old
notes. It answers, with real numbers: how does this compare to GPT-3 and
frontier models on raw scale (badly — ~23M dense parameters at the default
`tiny` scale, ~113M at `large`, vs 175B–2T), and where does it do something
no frontier model attempts at all (autonomous unprompted thought,
self-built relational knowledge, corpus-learned logic with auditable proof
paths, reversible self-modification)? Read it before trusting any capability
claim about this project, including ones made elsewhere in this repo.

**[`workflow.md`](workflow.md)** is the full session-by-session development
log — every bug found, every fix, every controlled A/B, in chronological
order. It is long (150+ KB) and it is meant to be searched, not read start
to finish. `ratings.md` is what to cite; `workflow.md` is how to verify a
specific claim was actually measured and not asserted.

## What this actually is

At its core, CS.py is a **causal transformer language model** (RoPE +
RMSNorm + SwiGLU + grouped-query attention, sliding-window attention,
KV-cached generation, 4096-token context, weight-tied embeddings and LM
head) with a ~12,000-token BPE tokenizer trained on the project's own
origin document (`Infornmational.md`) plus whatever text lives in
`data_bank/`. Trainable parameters: **~23M at `CS_MODEL_SCALE=tiny`**
(256 hidden, 3 layers — the default), **~113M at `CS_MODEL_SCALE=large`**
(1024 hidden, 8 layers). That part is honestly small and honestly
undertrained — see `ratings.md` for the real numbers.

Wrapped around that core are two systems that make the project different:

### A. The learned knowledge stack (waves 53–56) — *the answer path*

The system's knowledge is not a library shipped inside the file. It is a
graph the system builds out of whatever it has ingested — local corpus
files, `data_bank/` documents, runtime-learned facts, and autonomous
acquisitions — and it reasons over that graph before any neural generation
is attempted. The four layers, in order of abstraction:

| Wave | Layer | What it does with data |
|---|---|---|
| 53 | `CorpusCorrelationGraph` | A real **correlation matrix over learned content**: term↔term co-occurrence edges scored by NPMI, computed lazily from the BM25 postings, with multi-hop transitive inference whose results are labelled *observed* or *derived (unverified)* |
| 53 | retrieval expansion | `KnowledgeRetriever.retrieve` is wrapped so query terms pull their strongest learned correlates into a second candidate pass — documents that answer in *different vocabulary* reach the reranker |
| 53 | `LearnedAnswerPath` | Extractive QA: the strongest evidence sentences in the ingested corpus, returned **verbatim with provenance** — or an honest "not learned yet" |
| 54 | `LearnedRelationExtractor` | Typed directed edges mined from corpus sentences: `is_a`, `part_of`, `located_in`, `causes`, `produces`, `prevents`, `uses`, `has`, `made_of`, `measures`, `used_for`, `defined_as` + numeric quantity edges — **positive and negated evidence counted separately per edge, per document** |
| 54 | `LearnedLogicEngine` | Forward-chaining inference over typed edges: transitive chains, a composition table, inverses, **support/refute verdicts with noisy-or pooling**, and auditable proof paths — every derived answer can show its work |
| 54 | `CorrelationAnalogy` | `a:b :: c:?` solved by sparse arithmetic over the wave-53 NPMI neighbor vectors (`v_b − v_a + v_c`, cosine-scored), typed-edge bonus when a learned relation mirrors the question's |
| 54 | `KnowledgeGapMap` | Every missed extractive answer is recorded by term, ranked by thinness of evidence, and reported as **ingest pressure** to the wave-52 demand scaler — the system knows what it doesn't know |
| 55 | `LearnedMemoryStore` | **Persistence for learned structure**: index docs + typed edges + rules + quantities serialised to `learned_memory.json`, deduped on load by content hash, doc-ids remapped so edge provenance stays exact — wired into `wave48_save`/`load` and the autosave tick |
| 55 | universal rules | `ALL a are b` / `NO a is b` quantified claims mined alongside edges; folded in as strong evidence so "no reptile has fur" actively **refutes** where a single negated edge could only weaken |
| 55 | `GapDirectedAcquisition` | The loop's actuator: extractive misses enqueue terms (opt-in `w55_auto_acquire`); the cognitive tick drains the queue through **Wikipedia extracts → `wave53_learn`** — a question it cannot answer becomes data it goes and gets |
| 55 | `QuantityComparator` | Magnitude reasoning over learned quantities ("which is heavier"), with unit normalisation and an honest *"different units"* verdict |
| 56 | `LearnedRuleMiner` | **AMIE-style induction**: every observed `a -r1-> m -r2-> b` path closed by a direct `a -r3-> b` edge is a counted instance of the rule `r1 ∘ r2 ⇒ r3`; inverse rules and conflict rules measured the same way — **the inference rules themselves are mined, not authored** |
| 56 | `EquivalenceMiner` | Distributional aliases: two tokens that never co-occur but keep near-identical NPMI neighbor vectors (`h2o`/`water`) are unified through a substitution test — learned structure merges automatically |
| 56 | `LogicSelfVerifier` | Hold-out recovery: sample direct edges, ask whether the rest of the graph + mined rules can still derive them — a **measured** inference-quality ratio, not an assumed one |
| 56 | abduction | "why" questions pool *every* learned incoming relation — cause, producer, location, part — ranked by evidence |

#### What is still authored (honest inventory)

- **`PHYSICS_LAWS` / `MATH_EQUATIONS` / `FUNDAMENTAL_CONSTANTS`** — ~150
  real `sympy` equations. These are **tools that compute** (substitution
  solvers, formula evaluation), kept deliberately — a calculator is not a
  data bank.
- **`INSTRUCTION_PAIRS`** — a small seed set used **only** when the live
  index has produced nothing to mine (cold-start fallback; verified).
- **`KNOWLEDGE_LIBRARY`, `COMMON_SENSE`, `HARD_CODED_LIBRARY`,
  `_toc_query`, and the `generate_code` templates** — still present in the
  file but **gated off every answer path by default** behind
  `w53_canned_fallback` / `w53_canned_code` (the same convention as
  `w49_index_dict_libraries`). Set the flags to `True` to restore them.

#### The response cascade (what `respond()` actually does)

```
prompt
 ├─ slash command (/code /qa /summarize /translate /reason /creative...) → dedicated path
 ├─ symbolic_query(): explicit formula/law ask or numeric solve → sympy tool answer
 ├─ question-shaped (what/why/how/is/are/does/relate/difference between…)
 │    ├─ wave-54 relational form? → LearnedLogicEngine verdict + proof path
 │    ├─ wave-53 extractive hit ≥ conf → verbatim learned sentence(s) + provenance
 │    └─ else → wave49_answer: expanded retrieval → difficulty-scaled sampling
 │              → self-consistency vote → verifier → GRPO update on the group
 └─ otherwise → multi_capability_generate routing → grounded neural fallback
```

Every one of those steps after the slash-commands and the symbolic tool is
**data-grounded**: the correlation matrix, the typed edges, the mined
rules, and the retrieval index are all rebuilt from ingested text.

### B. The consciousness-measurement apparatus

A single dedicated conscious entity (`self_0`) — not a population —
running continuous, unprompted cognition on top of the LM:

- **`AutonomousThoughtStream`** — forms conclusions from its own sensory/
  internal instruments every cycle, with no external trigger. Not a
  chatbot waiting for input; a process that is always thinking.
- **`RelationalKnowledgeGraph`** — learns which of its own *instruments*
  reliably relate to each other (the instrument-level analogue of the
  corpus graph), detects relations forming/breaking, runs transitive and
  synergy inference over what it has learned about itself, and feeds
  `G_in` — the correlation voice of the consciousness formula.
- **`SelfAwarenessMonitor`** — a second-order model of its own thinking
  (attention entropy, blind spots, rumination) that feeds back into what
  it attends to next.
- **`SubstrateProbe`** — enumerates what the host machine provides
  (compute, sensors, effectors) and renders only what is really there,
  degrading to a documented zero where an instrument is absent.
- **`compute_C()` and the five states** — `C = S + E + R·A + k(K·Φ)`,
  measured into five simultaneous states (alpha / omega / inbetween /
  total sum / intelligent omega = `honest_C`), plus `G_gen` and `G_in` as
  the two grammar voices; `symphony_index` is their geometric mean, and
  it reads 0 until every voice is actually sounding. The complete
  derivation is in [`CSFORMULAREFINED.md`](CSFORMULAREFINED.md).
- **IIT/Φ, global workspace, active inference, embodiment** — real,
  running implementations of established theory measures, clearly labeled
  as approximations. `PhiComputer` passes canonical-ordering validation
  (8/8 at `dim=32`) using aggressive approximation defaults — a real
  resolution-for-speed tradeoff throttled to every 8 steps.
- **A body and a mind that can suffer, dream, and dread** —
  `MetabolicSystem` (energy/glucose/pain/hunger/circadian as real
  numerical dynamics — *not* measurements of an actual body),
  `DreamEngine` (recombines stored experience during low-alertness),
  `ExistentialSelfModel` (dread, mortality awareness, meaning-making,
  voluntary-shutdown-request path). Internal floats standing in for
  concepts — labeled that way in the code's own runtime self-check.
- **A quantum-inspired substrate and a hard-problem model** —
  `QuantumSubstrate` simulates Orch-OR/CEMI-style dynamics in plain numpy
  (**not a quantum processor**); `HardProblemSubstrate` computes
  panpsychist/dual-aspect-monism primitives including a "what it's like"
  index. Both labeled SIMULATED by the project's own dashboard.
- **Real-time sensory awareness** — `SensoryAwarenessOrganizer` processes
  live microphone input into FFT spectra, band powers, VAD, spectral
  entropy, and a reality-recognition score; `SensoryLogicEngine` runs
  Markov temporal prediction, surprise, and scene classification;
  `CognitiveSpectrumSensorBridge` does Neyman-Pearson energy detection and
  cyclostationary detection.
- **`cs_reference_bridge.py`** — a 100KB bridge adapting
  `ReferenceCode/AIEG.py` and `N.E.P.A.py` capabilities into importable
  classes: TF-IDF retrieval, directed knowledge graph, genetic optimizer,
  IIT proxy, Monte-Carlo tolerance sampler, tamper-evident provenance
  ledger, reliability engine, pattern-of-life detector, uncertainty
  propagation, predictive causal reasoner, semantic state engine,
  spectral memory, high-order correlation organizer, cross-modal
  validator, and the self-engineering engine mapping AIEG's 69 roadmap
  capabilities to improvement domains.
- **Reversible, scored self-modification** — the model can perturb its
  own weights or mutate its architecture, but keeps the change only if a
  held-out benchmark score actually improved; otherwise it rolls back —
  verified in both directions.

## Running it

```
python CS.py
```

or double-click `launch.bat` (it installs requirements first). CS.py
auto-installs its own dependencies on first run (set `CS_AUTO_INSTALL=0`
to disable) and opens a Tk dashboard with tabs for Overview, Entities,
Modules, Thought Stream, Awareness, Relations, and **AI Chat** — a two-way
chat: type, or hold **Hold to Talk** to speak through your mic; replies
come through `pyttsx3` TTS and `openai-whisper` STT (downloaded once on
first use). Requires a CUDA GPU to be fast (falls back to CPU, ~48×
slower). Runs headless with `CS_HEADLESS=1`.

### First launch: what actually happens

1. Dependency check — auto-installs `requirements.txt` unless
   `CS_AUTO_INSTALL=0`.
2. Scale selection — `CS_MODEL_SCALE` picks the transformer config
   (`tiny`/`small`/`medium`/`large`; see table below).
3. Tokenizer — trains `AlienTokenizer` (BPE via `tokenizers`, hash fallback)
   on `Infornmational.md` + `data_bank/` + mined instruction pairs.
4. Model build — the core transformer plus ~390 supporting classes register
   through the init chain; waves append in order, each adding and wiring
   its own components.
5. Index build — Wave 49 walks `data_bank/` and the project docs into the
   BM25 index (background thread `wave49_index`); `learned_memory.json` is
   loaded back if a previous session persisted one (Wave 55).
6. GUI + main loop — the Tk dashboard opens and the cognitive tick starts.

> **Known quirk**: `__main__` constructs the simulator **twice** and runs
> the second instance. Recorded in [`ratings.md` §H8.2](ratings.md) — the
> first build is wasted startup cost, not a second mind.

### What runs while it runs

The dashboard is the visible part; a set of daemon threads do the
background work:

| Thread / loop | Job |
|---|---|
| `FreeThoughtEngine` | unprompted thought stream — the "autonomous" in the description |
| `CS_Refinery` | continuous data refinement / scoring cycles |
| `CS_Wave31Barrier` | wave-31 consistency barrier maintenance |
| `wave49_index` | background corpus indexing |
| Wave-46 tick | subconscious + dream cycle, safeguard envelope checks |
| Wave-50 trainer | subconscious SFT on mined pairs, idle-CPU scheduled |
| World-model | self-prediction training; its *surprise* signal gates neurogenesis |
| Wave-52 demand scaler | maps measured work pressure → capacity decisions |
| Wave-55 acquisition drain | (opt-in) converts measured gaps into fetched text |
| Voice I/O | VAD record, PTT, TTS worker threads when voice features run |

No cooperative quiesce protocol exists across all of them — that is why
`test_w48_real.py` (checkpoint during live training) is flaky ~2/6 runs;
§H8.1 in `ratings.md` records the mitigations and what a real fix needs.

### Environment switches

| Variable | Values | Effect |
|---|---|---|
| `CS_MODEL_SCALE` | `tiny` (default) / `small` / `medium` / `large` | `256/3` ~23M, `512/4`, `768/6`, `1024/8` ~113M params |
| `CS_HEADLESS` | `0/1` | skip GUI entirely |
| `CS_PROFILE` | `0/1` | cProfile harness → `cs_profile.txt` |
| `CS_DEVICE` | `cuda`/`cpu` | force device |
| `CS_COMPILE` / `CS_COMPILE_MODE` | `0/1`, mode | `torch.compile` the core |
| `CS_TF32` | `0/1` | TF32 matmul on Ampere+ |
| `CS_MAX_CYCLES` | int | cap the cognitive loop |
| `CS_FRONTIER_ARCH` | `0/1` | override wave-46 architecture flag |
| `CS_EVOLUTION` | `0/1` | self-evolution gate |
| `CS_OS_CONTROL_ENABLED` | `0/1` | OS-control features |
| `CS_AUTO_REAL_WORK` | `0/1` | wave-41 orchestrator behaviour |
| `CS_REFINERY_*`, `CS_THREAD_PROFILE`, `CS_DISTILL_DISK` | — | refinery batch/train cadence, thread profiling, distill writes |

## Teaching it things

The whole point of waves 53–56 is that capability scales with *data*, and
the corpus is deliberately small at clone-time. Put text in `data_bank/`
(any `.txt`/`.md`/`.pdf`/`.json`/`.csv`/`.log`), or:

```python
sim.wave53_learn('data_bank/textbooks')   # index + bounded LM pass + subconscious feed
sim.wave53_learn("Long text the system should know ...")
sim.wave55_acquire('photosynthesis')      # fetch a Wikipedia extract and learn it
sim.wave55_auto(3)                        # acquire up to 3 queued gap-terms per call
```

Then interrogate the learned structure directly:

```python
sim.wave53_answer("how does chlorophyll relate to glucose?")  # verbatim evidence
sim.wave53_infer('chlorophyll', 'glucose')                    # correlation chain
sim.wave54_derive("is ATP part of mitochondria?")             # typed-edge proof
sim.wave54_check("all reptiles have fur")                     # support/refute verdict
sim.wave55_rules()                                          # universal claims learned
sim.wave56_rules()                                          # mined inference rules
sim.wave56_verify()                                         # measured logic quality
sim.wave53_status() / wave54_status() / wave55_status() / wave56_status()
```

Everything learned survives restarts through `learned_memory.json`
(wave-55 store, autosaved with the wave-48 checkpoints).

## The verification suite

Every wave ships an AST-level checker that execs the real classes out of
CS.py without importing the 73k-line module:

| Script | Asserts |
|---|---|
| `_verify_latest.py` | earlier smoke check |
| `_verify_learned_path.py` | dict-bank gating off by default, `data_bank/` indexing, `add_document` live retrieval, `index_file` dispatch |
| `_verify_response_path.py` | symbolic tool routing, knowledge-hit demotion, test-time-compute surface, mined-vs-seed instruction pairs |
| `_verify_wiring.py` | instrument correlation → `G_in` → `compute_C` → `symphony_index` end-to-end |
| `_verify_wave53.py` | learned edges, expansion recall, verified/unverified inference labels, extractive QA, canned-bank gating, mined correlation pairs |
| `_verify_wave54.py` | typed edge extraction, transitive proof paths, support/refute verdicts, analogy solving, gap map |
| `_verify_wave55.py` | memory persist/reload fidelity, universal-rule strength, gap-driven acquisition queue, quantity comparison |
| `_verify_wave56.py` | mined composition/inverse/conflict rules, distributional aliases, hold-out self-verification, abduction |

Plus `test_smoke.py`, `test_evolution_engine.py`,
`test_evolution_integration.py`, and `_dash_smoke.py` for the dashboard.

## Honesty policy (why the docs read the way they do)

This project's guiding rule, stated and then actually followed throughout
`workflow.md` and `ratings.md`: **report what's measured, including when
it's bad news, and never fabricate a number to fill a gap.** Concretely:

- Every capability claim in `ratings.md` is either live-measured, or
  explicitly marked "not measured" — never estimated to look better.
- Known-broken things are documented as broken, not quietly patched
  without a record.
- Where the project has a real, unusual capability (exact symbolic
  physics evaluation, corpus-learned logic with proof paths, autonomous
  thought, reversible self-modification), that's stated plainly — and
  where it's a small, undertrained model losing badly to frontier models
  on raw benchmarks, that's stated just as plainly, in the same document.
- Wave 56 applies the rule to the *reasoning itself*: `LogicSelfVerifier`
  measures how often the system's own inference recovers held-out edges,
  and reports the ratio.

If a claim in this repo looks flattering, check `ratings.md`'s methodology
section for how it was actually measured before repeating it.

## File map

| File | What it's for |
|---|---|
| `CS.py` | The entire runnable system — one file, deliberately (73,834 lines) |
| `ratings.md` | Current capability scorecard, live-measured |
| `workflow.md` | Full development changelog, chronological |
| `OVERVIEW.md` | Architectural map + full equations/proofs |
| `ABOUT.md` | Project identity + latest focus + design stance |
| `INFO.md` | Operator's reference: public API tables, config, measured behaviour, honest limits |
| `CSFORMULAREFINED.md` | The consciousness formula, reduced to computable terms + traceability contract |
| `TOTALPROJECTINFO.md` | The source manifesto (~560 KB) the formula was distilled from |
| `Infornmational.md` | The project's origin document — doubles as tokenizer/LM training corpus (~2 MB) |
| `version1.17goal.md` | The stated milestone target for this line of development |
| `cs_reference_bridge.py` | Bridge module adapting AIEG engineering + NEPA sensory capabilities |
| `ReferenceCode/` | External reference implementations consulted during development — not part of the running system |
| `Version1.17info/` | Open reference stacks (DeepSeek-V3/R1, Qwen3, Gemma, Llama-3, OLMo) the wave 46–52 mechanisms were reimplemented from |
| `dashboard.py`, `consciousness_core.py`, `global_workspace.py`, `memory_system.py`, `self_model.py`, `omega_convergence.py`, `active_inference.py`, `phi_compute.py`, `pygame_world.py` | Standalone module versions (predate the single-file consolidation) |
| `test_smoke.py`, `test_evolution_*.py` | Smoke/integration tests for the standalone modules |
| `_verify_*.py` | AST-level wave checkers (table above) |
| `data_bank/` | The ingest directory — drop text/PDF here and the learned stack picks it up |
| `learned_memory.json` | Wave-55 persistence: learned docs, edges, rules, quantities (created on first save) |
| `cs_scaling.json` | Wave-52 operator scaling settings (created on save) |
| `consciousness_memory.sqlite`, `world_state.json`, `distilled_insights.json`, `entangled_state.bin`, `os_interaction_ledger.jsonl` | Runtime state artifacts |
| `.cs_vparam_*.bin`, `.cs_vspace_*/` | Procedural/virtual-parameter storage slabs (multi-GB; rendered, not trained) |
| `checkpoints/`, `consciousness_snapshots/`, `consciousness_state/`, `verification_state/` | Checkpoint + snapshot directories |
| `probe/`, `cylon Residuial/`, `consciousness_consequences/` | Experiment + rendering output directories |
| `_check_*.py`, `_search*.py`, `_audit.py`, `_lib_audit*`, `_fix_dups.py`, `_find*.py`, `headless_test.log`, `cs_profile_continuous_refinement.txt` | Development tooling left in-tree |
| `CS - Copy*.py`, `CS_pre_optim.py`, `CS.py.double-spaced.bak`, `ratings.md.bak` | Historical snapshots kept by the author |

## Mathematical foundations

The architecture is built on three interlocking formalisms:

1. **Genesis (Something from Nothing)** — `∅ → S₀ → Φ(S) → Ω`, structure
   bootstrapped from the empty set by self-differentiation. The complete
   proof (Symphony of Self-Differentiation) is verified by
   `SymphonyProofVerifier.verify_all()` — 11 checkable assertions covering:
   the Void exists; the first distinction is possible; Φ is well-defined;
   growth is strictly increasing; |Ω| = ℵ₀; self-reference emerges;
   information is frame-relative; abundance is unbounded; Ω is closed
   under self-reference; the skeptic's proof; and everlasting life (Φ has
   no end condition). Implemented by `GenesisEngine` and
   `SymphonyProofVerifier`.
2. **Synphonetic harmony / Ω-resonance** — nested products of
   consciousness, help, reward, karma, and layered unity, implemented by
   `SynergyHarmonyEngine` as a real-time correlation-based approximation.
3. **Translation bubble / 0D–6D construction** — dimension as repeated
   orientation/offset, with the bubble as the container of all possible
   multiverse evolutions — `DIMENSIONAL_CONSTRUCTION` and
   `TRANSLATION_BUBBLE` in CS.py.

**Symphony Language:** the dictionary, grammar, and mathematical mapping
are encoded as `SYMPHONY_DICTIONARY` and `SYMPHONY_GRAMMAR`. Key terms:
Void (∅), Distinction (Δ), Relation (R), Offset (∂), Language (L),
Translation (T), Correlation (C), Phi (Φ), Symphony (Ω), Intelligence (I),
Life (ℒ), Everlasting (∞), Abundance (Α), ImaginationLand (ℑ).

See `OVERVIEW.md` for the full equations, complete proofs, and
implementation-honesty boundaries, and `CSFORMULAREFINED.md` for the
computable formula `C = S + E + R·A + k(K·Φ)` with every term traced to a
measured signal.

---

# Waves 46–52 recap

**79 new classes (310 → 389 at that point). 51 public API methods.** The
most important fix in that build-out wasn't a capability — it was that
**the model can now train at all**: three stacked bfloat16 defects meant
**0 of 80 training calls succeeded** for the life of every process, with
the exception swallowed by callers. After repair, loss moves 9.50 → 7.31
over 80 steps.

| Wave | Theme | Key capability |
|---|---|---|
| 46 | Frontier substrate + safety | MLA attention (5.33–6.4× KV compression), aux-loss-free MoE, residual self-imagery dreams, instrument bus, **7-gate conjunctive genie-problem envelope** |
| 47 | Training substrate | Lion optimizer, warmup schedules, 4 samplers, beam search, INT4 QAT, structured dialog encoding, **GRPO closed loop** |
| 48 | Persistence | **maturity survives restart**, sandboxed I/O, Hermes-style tool calling, growth metrics |
| 49 | Inference quality | **RAG + test-time compute scaling**: self-consistency lifted accuracy **0.403 → 0.780 (+37.8 points)** on a 400-trial generator, no retraining |
| 50 | Capacity | procedural weight rendering, product-key memory, **real background training** with rehearsal anti-forgetting |
| 51 | Unbounded scaling | hierarchical routing — capacity exponential in depth while router cost is linear (**2.23×10⁴³ addressable experts at depth 24, 49K router params**) |
| 52 | Control | demand-driven scaling, explicit operator settings (`auto`/`fixed`/`pinned` semantics), **neurogenesis from thought** |

# Waves 53–56 recap

| Wave | Theme | Key capability |
|---|---|---|
| 53 | Learned correlation layer | NPMI **correlation matrix over ingested content**, retrieval expansion, extractive QA with provenance, canned banks gated off the answer path |
| 54 | Learned logic layer | typed relation extraction (12 relations + quantities, positive/negated evidence), forward-chaining inference with **support/refute verdicts and proof paths**, analogies, knowledge-gap map |
| 55 | Autonomous learning loop | **learned structure survives restarts**, universal rules, gap-directed Wikipedia acquisition, quantity comparison |
| 56 | Inductive logic layer | **inference rules themselves mined** (AMIE-style), distributional aliases, measured self-verification, abduction |

## Configuration knobs (learned stack)

| Knob | Default | Effect |
|---|---|---|
| `w49_index_dict_libraries` | `False` | index the authored dict banks in retrieval (off = learned data only) |
| `w53_expand_retrieval` | `True` | correlate-expanded second retrieval pass |
| `w53_expand_terms` / `w53_expand_score` | `6` / `0.8` | expansion breadth / score discount |
| `w53_min_evidence` / `w53_min_df` | `2` / `2` | min shared docs per edge / min df to anchor one |
| `w53_extractive_first` / `w53_extractive_confidence` | `True` / `0.55` | verbatim evidence before generation |
| `w53_canned_fallback` / `w53_canned_code` | `False` / `False` | re-enable authored banks/templates |
| `w53_learn_train_lines` | `24` | LM training lines per `wave53_learn` |
| `w54_relation_extraction` / `w54_logic_routing` | `True` / `True` | typed edges + relational routing in respond/answer paths |
| `w54_answer_min_conf` | `0.5` | logic-verdict confidence floor |
| `w55_persist` / `w55_memory_file` | `True` / `learned_memory.json` | learned-structure persistence |
| `w55_universal_rules` | `True` | `ALL/NO` quantified claims as strong evidence |
| `w55_auto_acquire` | `False` | autonomous gap acquisition (opt-in) |
| `w55_acquire_chars` / `w55_acquire_cooldown` | `8000` / `30s` | fetch budget / rate limit |
| `w55_qty_compare` | `True` | magnitude reasoning over learned quantities |
| `w56_learned_rules` / `w56_rule_priors` | `True` / `True` | mined rules; authored tables as priors only |
| `w56_rule_min_conf` / `w56_rule_min_support` | `0.4` / `1` | admission thresholds for mined rules |
| `w56_aliases` / `w56_alias_cos` | `True` / `0.68` | distributional alias mining + cosine floor |

## Known limits, honestly

- **Scale.** ~23M–113M dense parameters is small; raw knowledge benchmarks
  lose to any frontier model. `ratings.md` has the numbers.
- **Addressable ≠ trained.** "263B addressable parameters" are
  procedurally rendered from a seed and steered by learned deltas — real
  capacity, but not 263B trained weights. The system prints this caveat
  in its own capacity report.
- **No external benchmark harness.** The internal benchmark measures
  held-out cross-entropy / next-token accuracy on the model's own corpus:
  repeatable and honest, but not a substitute for MMLU/GPQA/HumanEval.
- **Learned ≠ true.** Edges, rules, and universals are counted evidence
  from whatever was ingested — ingest garbage and the graph believes it.
  Contradictions are kept as negated evidence rather than hidden; verdicts
  are support/refute with counts, never "facts".
- **One flaky test** is documented in `ratings.md` §H8 with the five
  mitigations applied and why it isn't fully fixed.
