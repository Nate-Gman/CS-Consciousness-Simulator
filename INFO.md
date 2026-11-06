# Info — Waking-State Neural Kinetics, Dream-Data Correlation & Creative Generation

This is the info sheet for the `CS.py` waking-state trickle systems and the
multi-capability creative generation pipeline.

## What it does

`ConsciousnessSimulator` correlates real internal data through a
*trickling waking energy*. The waking dream stream treats dreams as real data:
fragments arrive with no known cause, but they are built from kinetics, code,
and reality. `neural_generate_on_demand()` triggers frontier-level creative
sampling on top of that real substrate.

The **multi-capability creative generation pipeline** (`multi_capability_generate()`)
extends this with dedicated code-only branches for structured output grounded
in internal state before any neural fallback:

- **Creative** (`CreativeCompositionEngine` + `_compose_internal_stream`):
  state-selected story/dialogue/brainstorming with IQ cross-domain threads,
  convergence analysis, ranked hypotheses, and forward projection. Every
  creative line is twined to real computed values.
- **Reasoning**: query type classification, sub-question decomposition,
  fact gathering + IQ correlation anchors per step, intermediate answer
  chaining, per-step confidence tracking.
- **Q&A**: code-only elimination logic with positive/negative scoring,
  progressive elimination rounds, confidence calibration, internal state
  grounding. Multi-pass factual matching across all knowledge bases.
- **Long-form/summary/translation**: entity extraction, semantic density
  scoring, topic word frequency analysis, writing type detection
  (narrative/essay/report/general), type-specific section outlines,
  sentence-level decomposition with tense/mood detection, named-entity
  preservation. All grounded in internal state + IQ correlations.
- **Code**: 10-type taxonomy (OOP, async/concurrent, algorithm, data
  structure, test, web API, database, parser, numerical, ML) with
  type-specific plans, dependency detection, complexity estimation,
  per-type engineering recommendations, live module inventory, and
  `SelfEngineeringEngine` integration. Output is compiled and syntax-checked.

## Key methods

- `_trickle_waking_energy()` — live trickle of waking energy from internal state.
- `_iq_correlation_snapshot()` — live internal IQ correlation matrices.
- `generate_waking_dream()` — waking-state autonomous thought twined with data.
- `neural_generate_on_demand()` — on-demand high-creativity neural generation.
- `explain()` — a grounded self-explanation of what the AI understands.
- `render_default_reality()` — a default reality render independent of
  conscious state.
- `multi_capability_generate(category, prompt, ...)` — central dispatcher for
  all creative generation tasks (reasoning, code, qa, long-form, summary,
  translation, creative).
- `CreativeCompositionEngine` — state-selected story/dialogue/brainstorming
  with IQ threads, convergence analysis, and ranked hypotheses.
- `_compose_internal_stream(...)` — twines creative output to real internal
  anchors (kinetics, code hashes, world state, common-sense, IQ correlations,
  self-awareness, thought stream, sensory logic).
- `FrontierGenerationSuite` — upgraded on-demand generation suite exposing
  `frontier_story()`, `frontier_dialogue()`, `frontier_brainstorm()`,
  `frontier_longform()`, `frontier_summarize()`, `frontier_translate()`,
  `frontier_reason()`, `frontier_code()`, `frontier_qa()`.  Each branch now uses
  symbolic templates, token-overlap matching, source-attributed scoring, and
  `cs_reference_bridge.py` / `AIEngineeringBridge` integration before any neural
  fallback:
  - *Creative* — prompt-engineered templates for story, dialogue, brainstorming,
    scenario, character, worldbuilding, and poetry, plus a multi-section longform builder.
  - *Summarize* — regex sentence splitting, whole-word query relevance, and
    frequency/position scoring.
  - *Translate* — multi-word phrase dictionary with case preservation and
    start-of-key tie-breaking.
  - *Reason* — fact/rule/conclusion chain with token-overlap source selection,
    per-step confidence, and a structured reasoning trace.
  - *Code* — concrete templates (CSV, SQLite, file I/O, web, timers) plus
    `AIEngineeringBridge` routing and typed generic stubs.
  - *Q&A* — token-overlap knowledge/common-sense matching with confidence and
    source attribution (symbolic, library, common-sense, TOC, neural).

## Honesty boundary

All outputs are explicitly framed as simulations and readouts of real internal
numbers, not claims of felt phenomenal experience. Dreams are real data here,
but they are data the system does not claim to understand the origin of.
Creative generation relies on code movements and internal state, with neural
generation as fallback only — not as the primary generation mechanism.

For architecture, see `OVERVIEW.md`. For capability scores, see `ratings.md`.

## Mathematical foundations

The trickle, dream, and creative pipelines all run on top of the same three
formalisms documented in `OVERVIEW.md`:

- **Genesis (`GenesisEngine` + `SymphonyProofVerifier`)** — structure
  bootstrapped from the empty set via `Φ(S) = S ∪ {R(x,y)} ∪ {L(x)}`,
  building up `Ω` as the accumulated closure. The complete proof
  (Symphony of Self-Differentiation) is verified by 11 checkable
  assertions: Void exists → Distinction possible → Φ well-defined →
  Growth strictly increasing → Infinite unfolding → Self-reference
  emerges → Information relativity → Abundance unbounded → Closure →
  Skeptic's proof (nothing → something) → Everlasting life. The full
  Symphony Language Dictionary (`SYMPHONY_DICTIONARY`) and Grammar
  (`SYMPHONY_GRAMMAR`) are encoded in CS.py.
- **Synphonetic harmony (`SynergyHarmonyEngine`)** — the nested Ω-resonance
  product over entities `C`, with components for dependency reach `Γ`,
  influence spread `Δ`, reciprocal help `Ρ`, mutual reward `Σ`, karmic
  resonance `Ω`, layered continuity `Θ`, and layered unity potential `Φ`.
- **Translation bubble (`DIMENSIONAL_CONSTRUCTION` + `TRANSLATION_BUBBLE`)** —
  the 0D–6D dimensional construction, where each new dimension is the
  addition of another orientation/offset, and the bubble is the container
  in which all possible evolutions from any distinction condense into an
  observable frame.

See `OVERVIEW.md` for the full equations, complete proofs, and honesty
boundaries.

---

# Waves 46–56 — complete API and configuration reference

79 new classes, 51 new public methods, 47 new CONFIG knobs. This section is
the operator's reference. For *why* each mechanism works see `OVERVIEW.md`;
for measured numbers see [`ratings.md` §H](ratings.md).

## Prerequisite: training was repaired first

Every capability below runs on a model that, before this build-out, **could
not learn**. All 80 of 80 `process_input` calls raised and were swallowed by
the caller's exception handler, producing zero weight movement and zero
recorded losses for the life of every process. Three stacked bfloat16 defects
were responsible (a `GradScaler` — an fp16-only tool — applied to a bf16 loss;
mixed-dtype loss terms; and `.numpy()` on bf16 tensors at 12 sites). After
repair, loss moves **9.5017 → 7.3144** over 80 steps.

---

## 1. Complete public API

### 1.1 Wave 46 — subconscious, dreams, safeguards

| Method | Returns |
|---|---|
| `wave46_step(force_dream=False)` | one cognitive tick |
| `wave46_think(query, force=None)` | difficulty score and reasoning budget |
| `wave46_dream(temperature=1.0)` | a rendered logical counterfactual scene |
| `wave46_self_image()` | RSI coherence, dominant modes, loadings |
| `wave46_render_reality()` | fused instrument percept |
| `wave46_anticipate(k=2)` | world-model prediction of the next k states |
| `wave46_revert()` | undo every Wave-46 self-modification |
| `wave46_shutdown(timeout=2.0)` | deterministic stop of the cognitive clock |
| `wave46_status()` / `wave46_report()` | full status / human-readable summary |

### 1.2 Wave 47 — generation and quantization

| Method | Returns |
|---|---|
| `wave47_beam_generate(prompt, max_tokens, beam_size, mode)` | best beam + score |
| `wave47_chat_tokens(messages, add_generation_prompt=True)` | role-tagged token ids |
| `wave47_quantize(bits=8, group_size=64, pack=False)` | error + memory report |
| `wave47_status()` / `wave47_report()` | schedule, samplers, GRPO state |

### 1.3 Wave 48 — persistence, tools, sandbox

| Method | Returns |
|---|---|
| `wave48_save(tag=None)` | checkpoint path |
| `wave48_load(path=None)` | restore report (latest if path omitted) |
| `wave48_checkpoint_status()` | saves, loads, autosave state |
| `wave48_register_tool(name, fn, schema, description, sensitive)` | bool |
| `wave48_process_tool_calls(text, max_calls=4)` | results + substituted text |
| `wave48_sandbox_read(path)` / `wave48_sandbox_write(path, content)` | confined I/O |
| `wave48_growth_report()` | loss/maturity/wisdom trends |

### 1.4 Wave 49 — retrieval and test-time compute

| Method | Returns |
|---|---|
| `wave49_answer(query, kind, max_tokens, ctx)` | full retrieve→sample→vote→verify |
| `wave49_retrieve(query, top_k=5)` | ranked passages with provenance |
| `wave49_vote(samples, kind='auto')` | consensus, confidence, distribution |
| `wave49_best_of(candidates, ctx=None)` | verifier-scored selection |
| `wave49_status()` / `wave49_report()` | index and scaling statistics |

### 1.5 Waves 50–51 — capacity

| Method | Returns |
|---|---|
| `wave50_capacity()` | addressable / stored / active accounting |
| `wave50_expert_forward(x)` | route through the procedural expert bank |
| `wave50_memory_forward(x)` | query the product-key memory |
| `wave50_feed(text)` | give the subconscious material to train on |
| `wave50_pause_training()` / `wave50_resume_training()` | quiesce control |
| `wave51_capacity()` | routing depth, addressable counts, ceilings |
| `wave51_grow(levels=1)` | multiply capacity by `branching ** levels` |
| `wave51_expert_forward(x)` | route through the unbounded space |
| `wave51_check_growth()` | run one pressure check |

### 1.6 Wave 52 — demand scaling and operator settings

| Method | Returns |
|---|---|
| `wave52_settings()` | the live `ScalingSettings` object |
| `wave52_set_scale(key, value=None, mode=None)` | updated dimension spec |
| `wave52_pin_scale(key, value=None)` | hard-pin a dimension |
| `wave52_save_settings()` | path written |
| `wave52_neurons(x=None)` | neuron count, or run x through the bank |
| `wave52_status()` / `wave52_report()` | settings, pressure, neurogenesis |

### 1.7 Wave 53 — learned correlation layer

| Method | Returns |
|---|---|
| `wave53_answer(query)` | extractive answer quoted from learned data + provenance |
| `wave53_expand(query)` | learned correlates of the query's terms |
| `wave53_infer(a, b=None)` | multi-hop inference over learned correlations |
| `wave53_correlations(term)` | top learned correlates `[(term, npmi, n_docs)]` |
| `wave53_learn(source)` | teach text / file / dir: index + LM pass + subconscious feed |
| `wave53_status()` / `wave53_report()` | graph size, inference counts, correlation index |

Everything in Wave 53 is computed from ingested data — the canned banks
(`KNOWLEDGE_LIBRARY`, `COMMON_SENSE`, `_toc_query`, code templates) that
`frontier_qa`/`frontier_reason`/`frontier_code` used to consult now sit
behind `w53_canned_fallback` / `w53_canned_code` (default False), matching
the `w49_index_dict_libraries` convention. `KnowledgeRetriever.retrieve`
is expanded automatically: query terms pull their strongest learned
correlates (NPMI over the index's own postings) into a second candidate
pass, so documents that answer in different vocabulary reach the reranker.

```python
res = sim.wave53_answer("how does chlorophyll relate to glucose?")
# res['answer']     -> verbatim evidence sentence(s) from learned data
# res['confidence'] -> sentence score, 0..0.95
# res['provenance'] -> which ingested source the evidence came from
# res['expansions'] -> learned correlates that widened the search
inf = sim.wave53_infer('chlorophyll', 'glucose')
# inf['path']     -> e.g. ['chlorophyll','photosynthesis','glucose']
# inf['verified'] -> whether the pair is actually observed in the data
# inf['note']     -> 'observed in data' | 'derived ... (unverified)'
sim.wave53_learn('data_bank/textbooks')   # index + train on a directory
```

### 1.8 Wave 54 — learned logic layer

| Method | Returns |
|---|---|
| `wave54_relate(query)` | answer dict for a relational question, or `{'answer': None}` |
| `wave54_check(a, rel, b)` | `supported` / `refuted` / `conflicted` / `unknown` verdict + proof paths |
| `wave54_derive(term, rel=None, direction='out')` | forward-chained derivations from a term |
| `wave54_analogy(a, b, c, k=5)` | `a:b :: c:?` solved by NPMI vector arithmetic |
| `wave54_compare(a, b)` | shared vs distinctive learned correlates and relations |
| `wave54_gaps(k=12)` | ranked knowledge gaps — what to feed `wave53_learn` next |
| `wave54_explain(a, b)` | auditable learned relation between two terms |
| `wave54_status()` / `wave54_report()` | edge counts, inference counts, gap pressure |

Wave 53 learned *where* terms co-occur; Wave 54 learns *what the relation
is* and reasons over it. `LearnedRelationExtractor` mines typed directed
edges (`is_a`, `part_of`, `located_in`, `causes`, `produces`, `prevents`,
`uses`, `has`, `made_of`, `measures`, `used_for`, `defined_as`, plus
numeric quantities) from the corpus's own sentences — positive and negated
evidence counted separately per document, so a contradiction weakens an
edge instead of hiding. `LearnedLogicEngine` forward-chains over them:
transitivity, a composition table (`is_a ∘ has ⇒ has` — inherited
properties), inverse relations, conflict rules (`prevents` refutes a
`causes` question), and noisy-or pooling into verdicts with auditable
proof paths. `CorrelationAnalogy` solves analogies by sparse arithmetic
on the Wave-53 NPMI neighbor vectors. `KnowledgeGapMap` turns every
missed answer into a ranked learning target and reports ingest pressure
to the Wave-52 demand scaler.

Relational questions ("does X cause Y", "what is X made of", "X vs Y",
"how heavy is X", "is X a Y") now route through the logic layer first in
`respond`, `wave49_answer`, `answer_qa`, and `multi_step_reason` — before
extractive QA, retrieval voting, or any neural fallback.

```python
chk = sim.wave54_check('caffeine', 'causes', 'insomnia')
# chk['verdict'] -> 'supported' via caffeine->alertness->insomnia
# chk['proofs']  -> the exact learned edges the chain stands on
sim.wave54_relate('what is water made of?')
# -> "Learned data: water made_of hydrogen ..." with provenance
sim.wave54_gaps()   # terms the system was asked about and couldn't answer
```

### 1.9 Wave 55 — autonomous learning loop

| Method | Returns |
|---|---|
| `wave55_acquire(term)` | fetch + learn a topic now (Wikipedia → `wave53_learn`) |
| `wave55_auto(k=3)` | acquire data for the top-k measured knowledge gaps |
| `wave55_rules(term=None)` | learned universal rules (`all X are Y`, `no X is Y`) |
| `wave55_persist()` | write the learned-memory file now, returns path |
| `wave55_recall()` | reload learned memory from disk, restore report |
| `wave55_status()` / `wave55_report()` | memory, rules, acquisition, persistence state |

Wave 54 learned *relations*; Wave 55 closes the loop around them:

- **`LearnedMemoryStore`** — checkpoints used to save weights but never
  the learned corpus, typed edges, rules, or quantities: everything the
  system learned died at exit. The store serialises index docs +
  extractor state to `learned_memory.json` (atomic write), dedupes by
  content hash on load, and remaps doc ids so edge provenance stays
  exact. Wired into `wave48_save`/`wave48_load` and tick autosave every
  `w55_autosave_docs` new documents.
- **Universal rules** — `all/every/no/never/always` claims mined on the
  same lazy doc pass as edges and folded into `check()` as strong
  evidence: `no reptile has fur` refutes even with zero negated edges.
- **`QuantityComparator`** — "which is heavier, X or Y" / "is X bigger
  than Y" answered from learned magnitudes, normalised through
  `convert_unit`; incomparable units get an honest 'cannot compare'
  answer rather than a guess.
- **`GapDirectedAcquisition`** — missed-question terms enqueue; the
  cognitive tick drains them (throttled) through Wikipedia extracts into
  `wave53_learn`, so a question the system cannot answer becomes data it
  goes and gets. Off by default (`w55_auto_acquire`) because it touches
  the network; `wave55_acquire`/`wave55_auto` run it manually.
- Plural/singular phrase resolution unifies learned structure
  (`mammals` ≡ `mammal`), including for rule and quantity lookup.

All of it binds through one class-level wrap of
`Wave54Integration.relate`, so every Wave-54 router — `respond`,
`wave49_answer`, `answer_qa`, `multi_step_reason` — gains the new
capabilities without re-patching.

```python
sim.wave54_relate('do all mammals have fur?')
# -> "Yes — learned data supports it ... (universal learned rule)"
sim.wave54_relate('which is heavier, the elephant or the mouse?')
# -> "Learned data: elephant is heavier — 5000 kg vs 0.02 kg (250000x more)"
sim.wave55_acquire('quantum entanglement')   # fetch + index + extract
sim.wave55_auto(3)                           # fill top-3 measured gaps
```

### 1.10 Wave 56 — inductive logic layer

| Method | Returns |
|---|---|
| `wave56_rules(k=24)` | mined composition-rule table — `r1 ∘ r2 ⇒ r3` with counted support, measured confidence, firing counts |
| `wave56_verify(k=None)` | held-out measured precision: direct edges hidden, then re-derived through other paths |
| `wave56_aliases(term)` | learned distributional aliases `[(alias, cosine)]` from the NPMI matrix |
| `wave56_abduce(query)` | ranked learned explanations for a 'why'/'what explains' question |
| `wave56_untyped(k=12)` | strongly correlated pairs with no typed edge — related, but not yet how |
| `wave56_status()` / `wave56_report()` | miner state, aliases, verifier, top rules |

Waves 53–55 learned the *data* of reason; the *logic* itself was still
authored — a fixed composition table, inverse map, and conflict map.
Wave 56 removes that ceiling: the inference rules are now **mined from
the corpus's own graph**, each with counted support and measured
confidence.

- **`LearnedRuleMiner`** — AMIE-style induction over the typed edge
  graph. Every observed path `a -r1-> m -r2-> b` closed by a direct
  `a -r3-> b` edge is one counted instance of `r1 ∘ r2 ⇒ r3` (a negated
  `(a,r3,b)` is a counter-instance). The same pass measures inverse
  rules `P(b -r2-> a | a -r1-> b)` and conflict rules (positive `r1`
  beside negated `r2` on the same pair means `r1` refutes `r2`). It
  discovers compositions no author wrote — `(produces, produces)`
  transitivity was unreachable before; if the data shows it, it is a
  rule now. The authored tables survive only as **priors** behind
  `w56_rule_priors` (matching the `w53_canned_fallback` convention):
  they fill in where the corpus is thin and are outvoted where data
  has spoken.
- **`EquivalenceMiner`** — distributional aliases from the correlation
  matrix alone: near-identical NPMI neighbor vectors that never
  co-occur (`h2o` ≡ `water`). A typed edge between the pair vetoes the
  merge — the matrix proposes, logic decides.
- **`LogicSelfVerifier`** — measures how good the learned logic
  actually is: hold out direct edges, re-derive through other paths,
  report the recovered fraction. Measured, not assumed.
- **Abduction** — 'why' questions now pool every learned relation's
  incoming chains, not just `causes`.

```python
sim.wave56_rules()        # e.g. is_a ∘ has ⇒ has (learned, conf .50)
sim.wave56_verify()       # {'precision': 0.46, 'sampled': 24, ...}
sim.wave56_aliases('h2o') # [('water', 1.0)]
sim.wave56_abduce('why does rust form?')  # moisture (causes, 0.42) ...
```

---

## 2. Worked examples

### 2.1 Highest-quality answering

```python
res = sim.wave49_answer("What is entropy and why does it increase?")
# res['answer']       -> normalised consensus answer
# res['confidence']   -> vote share weighted by usable-sample fraction
# res['agreement']    -> fraction of valid samples agreeing
# res['grounded']     -> whether retrieval supplied context
# res['sources']      -> which libraries the grounding came from
# res['samples_used'] -> how much compute was actually spent
# res['strategy']     -> 'single' | 'self_consistency' | 'consistency_plus_verify'
```

The budget scales with measured difficulty: `"hi"` costs one sample, a
multi-step derivation costs seven. Unanimous early samples stop sampling
early.

### 2.2 Persistence across restarts

```python
path = sim.wave48_save(tag='before_experiment')
# ... later, or in a new process ...
report = sim.wave48_load()          # latest checkpoint
# report['restored'] includes: transformer, embedding, lm_head, overlay,
#   subconscious_core, global_workspace, optimizer, lr_schedule,
#   world_model_optimizer, training_step_and_history,
#   wave46_maturity_and_self_image
# report['restored_maturity'], report['restored_wisdom']
```

Autosave runs from the cognitive tick every `w48_autosave_every_steps`
training steps, and a save fires on clean shutdown.

### 2.3 Capacity inspection and growth

```python
cap = sim.wave50_capacity()
# {'dense_model_parameters': 22_978_599,
#  'addressable_parameters': 263_258_284_071,
#  'stored_parameters':       90_365_991,
#  'active_parameters_per_token': 23_519_271,
#  'addressable_over_stored': 2913.2,
#  'addressable_over_active': 11193.3}

sim.wave51_grow(10)      # capacity × 64^10 ; per-token compute unchanged
```

### 2.4 Operator control

```python
# preferred value, but demand may exceed it
sim.wave52_set_scale('expert_depth', value=8, mode='fixed')

# absolute contract - nothing changes this
sim.wave52_pin_scale('retrieval_top_k', 5)

# releasing a pin requires saying so explicitly
sim.wave52_set_scale('retrieval_top_k', value=12, mode='auto')

sim.wave52_save_settings()   # -> cs_scaling.json
```

A pinned dimension holds against automatic growth, a direct `set()`, a
settings reload, and maximum growth pressure — all four verified.

### 2.5 Tool calling

```python
sim.wave48_register_tool(
    'get_maturity',
    lambda: round(sim._wave46.ledger.maturity(), 4),
    schema={}, description='Return current maturity score.')

results, text = sim.wave48_process_tool_calls(generated_text)
```

Calls use the reserved Wave-47 dialog tokens:
`<|tool_call|>{"name": ..., "arguments": {...}}<|tool_result|>`.
Arguments are validated against the schema before dispatch, so a malformed or
hallucinated call fails predictably rather than raising deep inside a library.

---

## 3. Configuration

### 3.1 Scaling settings (`cs_scaling.json`)

```json
{"dimensions": {
  "retrieval_top_k":      {"mode": "pinned", "value": 5},
  "expert_depth":         {"mode": "fixed",  "value": 6},
  "subconscious_neurons": {"mode": "auto",   "min": 128, "max": null},
  "test_time_samples":    {"mode": "auto",   "min": 1,   "max": 32}
}}
```

| Mode | Behaviour |
|---|---|
| `auto` | grows freely on demand within `[min, max]` |
| `fixed` | **preferred** value; demand may push past it |
| `pinned` | **absolute contract**; never changes |

### 3.2 Environment

```bash
CS_SCALE_EXPERT_DEPTH=8          # fixed preference
CS_SCALE_EXPERT_DEPTH=8!         # pinned (trailing '!')
CS_SCALE_EXPERT_DEPTH=auto       # explicit auto
CS_SCALE_SUBCONSCIOUS_NEURONS=512
CS_SCALE_RETRIEVAL_TOP_K=7
```

Resolution order, most specific wins: runtime call → `cs_scaling.json` →
environment → CONFIG default.

### 3.3 Other environment switches

| Variable | Effect |
|---|---|
| `CS_MODEL_SCALE` | `tiny` (default) / `small` / `medium` / `large` |
| `CS_FRONTIER_ARCH=1` | build the **main** stack from the frontier architecture |
| `CS_HEADLESS=1` | run without GUI (cognitive threads still active) |
| `CS_COMPILE=1` | enable `torch.compile` on the transformer stack |

### 3.4 CONFIG knobs by wave

**Wave 46 — subconscious core and clock**

`w46_dreams` · `w46_own_thread` · `w46_tick_seconds` · `w46_subconscious_core`
· `w46_sub_layers` · `w46_sub_heads` · `w46_sub_experts` · `w46_rope_scaling`
· `w46_core_seq` · `w46_core_train_every` · `w46_core_train_budget_ms`

**Frontier stack (opt-in for the main model)**

`frontier_architecture` · `frontier_experts` · `frontier_top_k` ·
`frontier_dense_layers` · `frontier_global_every` · `frontier_mtp_depth` ·
`frontier_softcap`

**Wave 49 — retrieval and compute scaling**

`w49_build_index` · `w49_index_background` · `w49_max_samples`

**Wave 50 — capacity and autonomous training**

`w50_virtual_experts` · `w50_top_k` · `w50_expert_rank` ·
`w50_max_materialized` · `w50_memory_keys` · `w50_memory_topk` ·
`w50_memory_heads` · `w50_virtual_blocks` · `w50_resident_blocks` ·
`w50_block` · `w50_subconscious_training` · `w50_idle_cpu` ·
`w50_train_interval` · `w50_train_warmup` · `w50_checkpoint_banks`

**Wave 51 — unbounded scaling**

`w51_branching` · `w51_initial_depth` · `w51_max_depth` (None = no ceiling) ·
`w51_auto_grow` · `w51_blocks_per_chunk` · `w51_memory_headroom` ·
`w51_growth_cooldown`

**Wave 52 — demand scaling**

`w52_pressure_threshold` · `w52_growth_cooldown` ·
`w52_neurogenesis_cooldown` · `w52_subconscious_neurons`

**Wave 53 — learned correlation layer**

`w53_expand_retrieval` · `w53_expand_terms` · `w53_expand_score` ·
`w53_min_evidence` · `w53_min_df` · `w53_max_scan_docs` · `w53_neighbors` ·
`w53_answer_min_conf` · `w53_extractive_confidence` ·
`w53_extractive_first` · `w53_canned_fallback` · `w53_canned_code` ·
`w53_learn_train_lines` · `w53_infer_max_hops` · `w53_corr_pairs_per_mine`

**Wave 54 — learned logic layer**

`w54_relation_extraction` · `w54_rel_scan_docs` · `w54_rel_phrase_max` ·
`w54_infer_max_hops` · `w54_infer_hop_decay` · `w54_answer_min_conf` ·
`w54_analogy_neighbors` · `w54_gap_miss_decay` · `w54_gap_pressure_at` ·
`w54_corr_pairs_per_mine` · `w54_logic_routing`

**Wave 55 — autonomous learning loop**

`w55_persist` · `w55_memory_file` · `w55_autosave_docs` ·
`w55_universal_rules` · `w55_auto_acquire` · `w55_acquire_chars` ·
`w55_acquire_cooldown` · `w55_drain_per_tick` · `w55_qty_compare`

**Wave 56 — inductive logic layer**

`w56_learned_rules` · `w56_rule_priors` · `w56_prior_conf` ·
`w56_rule_min_conf` · `w56_rule_min_support` · `w56_rule_recalc` ·
`w56_mine_max_paths` · `w56_deepen_terms` · `w56_deepen_docs` ·
`w56_ensure_docs` · `w56_resolve_cache` · `w56_walk_cache` ·
`w56_check_conflicts` · `w56_aliases` ·
`w56_alias_cos` · `w56_alias_cand` · `w56_alias_min_df` ·
`w56_alias_max` · `w56_abduce` · `w56_verify_samples`

---

## 4. How the scaling behaves

### 4.1 On demand, regardless of fixed settings

Every processing path reports work to `DemandDrivenScaler`, which maps it to
the dimensions it stresses:

| Work kind | Dimensions stressed |
|---|---|
| `train` | subconscious_neurons, expert_depth, materialized_experts |
| `retrieve` | retrieval_top_k, resident_blocks |
| `generate` | test_time_samples, materialized_experts |
| `dream` | subconscious_neurons, expert_depth |
| `thought` | subconscious_neurons, expert_depth |
| `tool` | materialized_experts |
| `ingest` | memory_slots_per_half, resident_blocks, subconscious_neurons |

Pressure decays at 0.97 per observation, so sustained load is required.
**Novelty is weighted above volume**: measured, 10 novel events (pressure
35.01) outweigh 30 repetitive ones (19.97), because reprocessing the same
material is evidence that existing capacity suffices.

### 4.2 Neurons grow from thought

`SubconsciousNeurogenesis` requires saturation **and** thought pressure
**and** world-model surprise together. Each was verified to independently
block growth. An untrained new row is dead weight that costs compute on every
forward pass forever, so weak evidence must not add one.

Growth preserves existing function exactly — new readout columns start at
zero, so it is a strict no-op at the instant it happens.

### 4.3 Where hardware still constrains growth

Address space grows regardless of the machine, because it costs nothing until
touched. **Resident tensors do not**: `CapacityAutoScaler` checks live free
memory first and refuses below the headroom threshold. Growing resident
structures past physical RAM kills the process, and a dead process has zero
capacity.

---

## 5. Measured behaviour

| Property | Value |
|---|---:|
| Self-consistency accuracy gain (400 trials) | 0.403 → **0.780** (+0.378) |
| Retrieval index | 9,412 docs / 132 libraries / **1.54 s** |
| Addressable parameters | **263,258,284,071** |
| Leverage (addressable ÷ stored) | **2,913×** |
| Sparsity (addressable ÷ active) | **11,193×** |
| Hierarchical routing at depth 24 | 2.23e43 experts for 49,152 router params |
| KV cache compression (MLA) | **5.33–6.4×** vs MHA |
| INT4 packing on the live core | **6.64×, 13.16 MB saved, 0.106 rel. error** |
| Lion optimizer state | **50% of AdamW** |
| Subconscious training | loss improvement **0.569**; regressions reverted 3/3 |
| World-model | loss 0.0299 → **0.0026**, learning progress **0.974** |
| Checkpoint fidelity | maturity, wisdom, weights, routing bias all exact |
| Learned-stack verification | `_verify_wave53/54/55/56` — all AST checks pass |
| Expansion recall (verify) | doc with **zero** query-vocabulary terms retrieved via learned correlates |
| Inference honesty | derived chains labelled `derived (unverified)` when no shared doc exists |
| Canned banks on answer path | **off by default** — `w53_canned_fallback` / `w53_canned_code` |
| Learned persistence | docs + edges + rules + quantities survive restart via `learned_memory.json` |

---

## 6. Honest limits

**Rendered parameters are a structured basis steered by learned deltas.
263B addressable ≠ 263B trained.** Capacity grows faster than knowledge does;
the remaining limits are disk, time, and training signal rather than any
constant in the file.

No external benchmark (MMLU, GPQA, HumanEval) was run — this repository has no
harness for them. `run_internal_benchmark()` measures held-out cross-entropy
and next-token accuracy on the model's own corpus: repeatable and honest, but
not a substitute.

**Learned is not the same as true.** Edges, universals, quantities, and mined
rules are counted evidence from whatever was ingested — the graph reflects
the corpus, and contradictory evidence is kept as negated evidence rather
than hidden. Inference results are labelled `observed in data` vs
`derived (unverified)`; nothing is presented as fact. `LogicSelfVerifier`
measures how often learned logic recovers held-out edges and reports the
ratio — the honesty rule applied to the reasoning itself.

Known defects, including a test that passes ~4/6 runs and why it is not fully
fixed, are recorded in [`ratings.md` §H8](ratings.md).
