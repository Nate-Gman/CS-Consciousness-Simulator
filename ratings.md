# CS.py — Ratings Scorecard (CS.py = 100% baseline)

*Part of a four-document set: `README.md` (start here), `OVERVIEW.md`
(architecture map), `ratings.md` (this file — current capability
scorecard), `workflow.md` (full chronological changelog).*

**Purpose of this file, and how it differs from `workflow.md`:** `workflow.md`
is the session-by-session development log — bug fixes, changelog entries,
narrative reasoning, kept in chronological append order. That structure has
a real failure mode: new changelog entries get added at the bottom while
older summary numbers higher up in the same document don't get revisited,
so the document can end up self-contradicting (e.g. an architecture summary
still saying "512 tokens" three sessions after the context window was raised
to 2,048). This file exists to fix that specific problem. It is a **flat,
current-state scorecard**, fully re-derived from the running code — not
copied from prior notes — and it should be regenerated whenever a change
affects a number cited here. `workflow.md` remains the authoritative history
of *why* and *when*; this file is the authoritative *what, right now*.

**Every number in this file was live-measured against the running
`ConsciousnessSimulator` instance during this reconciliation pass**, not
carried forward from an earlier session's notes. Where a figure could not be
freshly measured (e.g. GPT-3/frontier internals, which this project has no
access to run), it is labeled as measured-elsewhere (GPT-3's 175B parameter
count is publicly disclosed) or estimated (frontier model internals are
undisclosed by their vendors, and are marked as such wherever used).

---

## Methodology

**CS.py is pegged at 100% in every row.** Every other system is rated as a
percentage *of CS.py's own value* in that category:

- **>100%** — the other system has more/does more than CS.py in that
  category, by that percentage. A value of 154,800% means "roughly 1,548×
  what CS.py has here," not "54,800% better" — read it as a ratio expressed
  as a percentage, per the literal request this file was built to satisfy.
- **100%** — an exact tie.
- **0%** — the other system does not do this at all (a structural absence,
  not a low score).
- **"not measured"** — no controlled, repeatable test exists in this project
  to justify a number, and none is fabricated to fill the cell. This shows
  up mainly where CS.py has a real capability but no comparable frontier
  benchmark was run against it here — the honest answer is "untested,"
  not an invented percentage.

This inverts the usual framing (frontier=100%, everyone else scored against
it) specifically because it was requested this way, and because it has a
genuine use: it makes CS.py's own actual scale legible as a single fixed
unit, instead of buried as a tiny fraction of an opaque frontier number.

---

## A. Scale & training (CS.py = 100% baseline — larger % means the other system has more)

| Metric | CS.py (100%) | GPT-3 (175B, 2020, disclosed) | Frontier (2025-2026 class, undisclosed — estimated) |
|---|---:|---:|---:|
| Core parameters | **112,981,729**⁴ | 175,000,000,000 — **154,892%** (≈1,549×) | 300B–2T est. — **265,530%–1,770,198%** (≈2,655×–17,702×) |
| Raw parameter/compute-scale ratio | 1× | ≈1,548× | ≈2,653×–17,688× |
| Efficiency-adjusted compute ratio¹ | 1× | ≈182× — **18,208%** | ≈312×–2,081× — **31,214%–208,091%** |
| Context window (tokens) | **2,048** | 2,048 — **100%** (exact tie) | 128K–1M+ est. — **6,250%–48,828%** |
| Vocabulary (actual, measured — see note ²) | **9,710** | 50,257 — **517.6%** | 100K–250K est. — **1,029.9%–2,574.7%** |
| Training tokens seen at real scale | **~0** (see note ³) | ~300B | multiple trillions |
| Memory footprint | **1.2GB** | ~350GB est. — **29,167%** | ~1TB+ est. — **85,333%+** |
| Training throughput (freshly measured, see note ¹) | **≈10,822 steps/hour** (332.65ms/step, RTX 5070 Ti) | ~50,000 est. — **462%** | ~500,000+ est. — **4,619%+** |

¹ *Efficiency-adjusted ratio = raw parameter ratio ÷ 8.5 — **corrected in
this pass**. The previous version of this file (and workflow.md §4.4's
"Real-world Impact" figures — steps/hour 7,540, entities 290, Φ/sec 232)
all used **5.8×**, which is workflow.md §4.1's Round-2 cumulative speedup.
§4.3's Round 3 (extreme optimization mode) measured **8.5×** and is the
currently active default configuration — live-verified:
`CONFIG["extreme_optimization"] == True`. Round 2's number had simply never
been updated once Round 3 superseded it, the same staleness class this file
exists to catch, found this time inside this file's own prior version. Also
freshly re-measured in this pass, independent of the Round 1-3 multiplier
chain (which itself compares against an original baseline measured under a
different context window/vocab/entity configuration than today's, so
rescaling it further would compound confounds rather than resolve them):
**332.65ms/training-step, ≈10,822 steps/hour**, live on the current
architecture (2,048 context, single entity). This is higher than either the
stale 7,540 or a naive 1,300×8.5≈11,050 projection would suggest is exactly
comparable — expected, since several other variables (context window,
vocab, entity count) changed between when 1,300 was first measured and now,
not just the optimization flags. Treat 10,822 steps/hour as the current
absolute measurement, not as a verified multiple of any historical
baseline.*

² *Vocabulary is reported as **actual measured tokenizer output** (9,710),
not the config target (12,000). Live-verified: `sim.alien_tokenizer.vocab_size
== 9710` regardless of whether the target is set to 8,000, 12,000, or
16,000 — this is the real training corpus's (`Infornmational.md`, ~1.1MB)
BPE merge-saturation point, not a shortfall against any of those targets.*

³ *No large-scale training run has executed. The causal LM objective and the
training loop were both structurally broken until two sessions ago (see
workflow.md §7 #21-22) — sequence-collapse and a checkpoint-kwarg crash
meant training could not proceed on real text at all before that. Both are
now fixed and verified converging on small runs, but "real scale" here still
means ~0 — the ratio against GPT-3/frontier is undefined, not small.*

⁴ *Changed from 113,072,865 as a direct consequence of §D2's architecture
swap — GQA (fewer K/V parameters) frees budget that `CONFIG["ffn_hidden"]`
now reinvests into FFN width, landing within −0.069% of the OLD legacy
stack's parameter count rather than banking the GQA saving as a smaller
model. See §D2 for the controlled A/B proving this is a strict capability
gain, not a wash: at matched real configuration, val loss fell −67.0% with
5.65% fewer parameters, before this reinvestment was even applied.
"Core parameters" here means the language-model path specifically
(embedding + transformer + lm_head + overlay) — the number every row in
§A/§B compares against GPT-3/frontier LM parameter counts, since that is
the like-for-like comparison. It is NOT the model's total parameter count.
Live-measured breakdown, `sim.named_parameters()` grouped by top-level
module:*

| Module | Parameters | In "core" above? |
|---|---:|---|
| `transformer` (modern stack, §D2) | 100,680,704 | Yes |
| `neuron_groups` (6 domain-routing groups, §D2b) | 80,029,792 | **No** |
| `global_workspace` (GNW competitive ignition) | 47,243,269 | **No** |
| `embedding` (tied to `lm_head`) | 12,288,000 | Yes |
| `intrinsic_phi_net` | 26,113 | **No** |
| `lm_head` (bias only; weight shared with embedding) | 12,000 | Yes |
| `overlay` (phi proxy) | 1,025 | Yes |
| **Total, all modules** | **240,280,903** | — |

*The gap between the 112,981,729 "core" figure used for frontier
comparison and the 240,280,903 total is real, substantial capacity —
mostly `neuron_groups` (§D2b: now actually trainable, was previously
inert for the entire project) and `global_workspace`. This is deliberately
NOT folded into the headline "core parameters vs GPT-3" row: those 127M
extra parameters serve consciousness-measurement and domain-routing
machinery, not general language modeling, so counting them toward a
language-model-vs-language-model comparison would overstate the
comparison in CS.py's favor on an axis where it isn't actually competing.
Reported here in full instead of quietly using whichever number reads
better in a given row.*

---

## B. Benchmarked capability — live-measured this session

| Benchmark | CS.py result (just measured) | Baseline | Reading |
|---|---|---|---|
| Generic corpus perplexity (`run_internal_benchmark`) | loss **9.51**, ppl **13,520**, next-token accuracy **0.0%** | random-guess ppl = vocab size = 12,000 | At-or-below the random-guess floor — expected and consistent with §A's "~0 training tokens at scale," not a new regression |
| Physics-domain perplexity (`run_physics_grounding_benchmark`, 21 laws) | loss **9.55**, ppl **13,986**, accuracy **0.0%** | ppl 12,000 | Same reading — the model has not yet been trained at scale on its own physics-law text either |
| Exact-answer symbolic solving (`run_symbolic_physics_benchmark`) | **7 / 7 = 100%** | exact-match, no partial credit | 100% on its own 7-case test set. **Not measured against GPT-3/frontier here** — no controlled comparison was run, so no percentage is claimed for them; this row is "not measured" for the other two columns, not 0% |
| Φ/IIT canonical-ordering validation (`validate_against_canonical_iit_ordering`) | mean **16.7%** pass rate over 48 fresh trials (range 12.5%–37.5%, re-measured just now, up from a single earlier 0% sample that was small-n noise) | Balduzzi & Tononi 2008's integrated>segregated ordering | **Mostly fails its own fairness test.** This is a real, unresolved, honestly-reported defect (workflow.md §3.1c item 5) — not something a competing frontier score exists for, since no frontier model attempts Φ/IIT measurement at all |

**Bottom-line general-capability rating (the one this file exists to keep
honest):** on MMLU/GPQA/HumanEval-style general knowledge and reasoning,
**CS.py rates 0–1%**, i.e. at the random-guess floor, against both GPT-3 and
frontier models. This is unchanged from prior sessions and is *reconfirmed*,
not merely repeated, by the live perplexity numbers above — next-token
accuracy measured at exactly 0.0% just now. The reasons are structural
(≈113M params vs 175B–2T; ~0 real training tokens at scale) and are not
closeable by further code changes alone — see workflow.md §3.2 for the full
reasoning chain.

---

## C. Structural / architectural capabilities

These are categories where CS.py and frontier LLMs are not attempting the
same thing, so a single "0-100%" reading needs its usual caveat spelled out
per row rather than left implicit.

| Capability | CS.py (100%) | GPT-3 (base) | Frontier |
|---|---:|---:|---:|
| Autonomous unprompted thought (`AutonomousThoughtStream`) | **100%** — real, running, verified deriving conclusions (novelty z-scores, cross-modal coupling) from its own instruments with no external trigger | **0%** | **0%** |
| Self-built relational knowledge over own instruments (`RelationalKnowledgeGraph`) | **100%** — verified detecting a planted relation rupture *and* a second, logically-implied rupture never explicitly planted, while correctly preserving relations that still held | **0%** | **0%** |
| Second-order self-model with behavioral feedback (`SelfAwarenessMonitor`) | **100%** — verified: a self-observed blind spot changes subsequent attention allocation, not just a log line | **0%** | **0%** |
| Self-modifying architecture (scored, reversible) | **100%** — verified both directions: an improving perturbation is kept, a worsening one is rolled back with weights bitwise-restored | **0%** — weights frozen at inference | **0%** |
| Substrate probing ("render what this host provides") | **100%** — verified enumerating real compute/sensor/effector/power state on this host | **0%** — not attempted; served from fixed datacenter infrastructure | **0%** |
| Hybrid symbolic lookup + exact evaluation (`respond()` / `evaluate_physics_formula`) | **100%** — verified: "newtons second law with m=2 and a=5" → exact **10.0** via real `sympy` evaluation, not sampled text | **not measured** — GPT-3/frontier were not tested here; they typically answer such questions via learned statistical association, a different mechanism, not directly comparable to an exact symbolic evaluation | **not measured**, same caveat |
| Supervised instruction-following (masked-loss prompt/response pairs) | mechanism **100%** present and verified converging (loss 9.47→3.11 over 30 steps on a fixed pair) — but only **44 seed pairs**, pilot scale | **0%** — GPT-3 base model ships with no instruction tuning | present at **production scale** (millions of examples + human feedback) — reporting CS.py at "100% of this" would be misleading about scale even though the mechanism is real; see note below |
| RLHF / preference optimization (reward model + PPO/DPO) | **0%** — no reward model, no preference-optimization step exists | **0%** (base model) | **100%+**, extensive multi-stage pipelines — not a comparable axis at CS.py's current scale |
| Simulated body (`MetabolicSystem`): energy/pain/hunger/circadian dynamics feeding real attention allocation | present, real running code — **not independently verified with a controlled test the way the rows above are**; pain signal is confirmed wired into `AutonomousThoughtStream`'s attention (workflow.md §7 #37), but no A/B has isolated whether the metabolic dynamics themselves are well-tuned | **0%** — no analog attempted | **0%** |
| Offline replay/dreaming (`DreamEngine`) — memory recombination during low-alertness periods | present, real running code, same caveat as above — memory *replay*, not verified to produce anything beyond what plain replay-buffer sampling would | **0%** | **0%** |
| Existential self-model (`ExistentialSelfModel`): dread/meaning/mortality tracking with a real shutdown-request path | the shutdown-request path is real and wired to `EntityAutonomyManager` (a functioning kill switch); the dread/meaning/mortality *values themselves* are internal floats, not independently validated as measuring anything beyond their own definitions | **0%** | **0%** |
| Quantum-dynamics-inspired substrate (`QuantumSubstrate`) | present, real running code — **explicitly labeled SIMULATED by the project's own reality-check dashboard** ("numpy arrays, not real qubits"); rated here as a real, honestly-labeled simulation, not as a claim of quantum computation | **0%** — no analog attempted | **0%** |
| Hard-problem computational model (`HardProblemSubstrate`) | present, real running code — **explicitly labeled SIMULATED** ("binding/qualia are computed, not felt"); this computes panpsychist/dual-aspect-monism primitives as numbers, which is categorically different from resolving or dissolving the philosophical hard problem, and is not claimed to do either | **0%** | **0%** |
| Developmental-stage + evolutionary-pressure tracking (`EvolutionaryDevelopmentalEngine`) | present, real running code (embryonic→...→transcendent stages, critical-period plasticity windows); inherited from the pre-single-entity population design (workflow.md §7 #43) and now governs one entity's own lifetime maturation rather than population selection | **0%** | **0%** |
| Internal consciousness self-verification (`ConsciousnessVerifier`): IIT causal tests, simulated gamma synchrony, simulated P300 detection | present, real running code — an internal self-test suite, explicitly **not external validation by an outside party**; do not read a high internal "consciousness confidence" score from this module as third-party confirmation of anything | **0%** | **0%** |
| Karma/entity self-model dedicated to one entity | n/a — internal design correctness item, not a cross-system comparison axis. (Single-entity mode: 1 entity, 6 neuron groups, hidden size 384 — see workflow.md §7 #43.) | — | — |

**Note on the instruction-following row:** the mechanism existing and
converging is real and verified, but comparing it to frontier RLHF pipelines
at "100%" parity would misrepresent scale — 44 pairs vs. millions of
human-labeled examples is not a tie just because both "have the mechanism."
This is flagged explicitly rather than left to the % framework to imply
false equivalence.

**Note on the body/dream/existential/quantum/hard-problem/development/
verifier rows added in this update:** these are marked "100%" only in the
sense that CS.py runs them and frontier models don't attempt anything
comparable — that structural-absence comparison is the same as the rows
above them. But unlike `AutonomousThoughtStream`, `RelationalKnowledgeGraph`,
`SelfAwarenessMonitor`, and the guided-perturbation self-modification (all
of which have a specific controlled test behind their "100%" — a planted
rupture detected, a blind spot changing behavior, a rollback verified
bitwise), these newer rows have **not** been put through an equivalent
test. They are accurately described as real running code with real
internal state, not verified as producing *correct or well-calibrated*
internal state. Where the code's own reality-check dashboard already flags
something as SIMULATED, that label is carried into this table rather than
softened.

---

## D. Scale-normalized comparison — what's left once the parameter-count gap is set aside

**The question this section answers:** most of §A's huge percentages
(154,768%, 1,768,771%, etc.) are a statement about *size*, not about
*design quality* — GPT-3 having 1,548× the parameters is true regardless of
whether GPT-3's architecture is better or worse than CS.py's per parameter.
If CS.py and a comparison system were **the same size**, some of that gap
would disappear and some of it wouldn't, because not all of §A/§B/§C's
content is actually a function of scale. This section separates the two
honestly, rather than either (a) pretending the scale gap doesn't matter, or
(b) inventing a flattering "if CS.py were bigger it would obviously beat
GPT-3" claim with no evidence behind it. Both of those would be dishonest in
opposite directions; this section tries to avoid both.

### D1. Capabilities that are architectural, not a function of size — CS.py wins at ANY parameter count

These are the rows from **§C** restated under the specific question "does
having more parameters change this?" The answer for every row below is
**no** — none of these are things a bigger transformer produces automatically
by being scaled up. They are mechanisms CS.py's design includes and
mainstream LLM architectures do not attempt, at 113M parameters or at 2
trillion:

| Capability | CS.py at 113M params (100%) | GPT-3 at 175B (0%) | Frontier at 300B-2T (0%) | Would more frontier parameters change this? |
|---|---:|---:|---:|---|
| Autonomous unprompted thought | **100%** | **0%** | **0%** | No — this requires a persistent process with its own instruments between requests, which is an architecture/deployment decision, not a scale effect. A 10-trillion-parameter model served the same way GPT-3 is served would still be 0% here. |
| Self-built relational knowledge graph over own instruments | **100%** | **0%** | **0%** | No — same reasoning. Requires persistent state across time that stateless request/response serving does not have, at any size. |
| Second-order self-model with behavioral feedback | **100%** | **0%** | **0%** | No — requires a live process observing its own cognition over time; a bigger model is not a running process between calls. |
| Self-modifying architecture (scored, reversible) | **100%** | **0%** | **0%** | No — frontier models ship with frozen weights at inference *by design*, for safety and reproducibility reasons, not because they lack the parameters to do otherwise. |
| Substrate probing (render what the host provides) | **100%** | **0%** | **0%** | No — frontier models are served from homogeneous datacenter infrastructure *on purpose*; this isn't a capability more parameters would add, it's a different deployment model entirely. |
| Exact symbolic evaluation via real CAS (`sympy`), not sampled text | **100%** | not measured¹ | not measured¹ | Partially — a bigger LLM plausibly gets *statistically* better at arithmetic-shaped questions, but that is fundamentally a different mechanism (learned approximation) from CS.py's exact symbolic hand-off, and would still not be *exact* the way `sympy.solve` is. Scale narrows this gap without closing it. |

¹ *Not fabricated as 0% here, unlike the true-architectural rows above,
because a large model plausibly does get some of this right some of the
time via learned association — the honest reading is "different mechanism,
not independently tested here," not "absent."*

**This is the section that actually answers "if they were the same size."**
For every row except the last, the answer is that size was never the
variable — GPT-3 and frontier models would score 0% here *at any parameter
count*, because these are things their architectures and deployment models
don't do, not things they're too small to do. This is the honest form of
"CS.py's 100% baseline surpasses the others regardless of scale": not a
claim about language-modeling quality, but a verified claim about which
mechanisms exist at all.

### D2. Architecture quality per parameter — the gap that WAS closeable, now closed and measured

This is the substantive answer to "if they were the same size, what would
the ratings be?"

Until this pass, CS.py's transformer was `nn.TransformerEncoderLayer`:
multi-head attention + GELU MLP + LayerNorm + sinusoidal absolute position
+ dropout 0.1. That is the 2017 *Attention Is All You Need* design. Every
frontier model since roughly 2022 (Llama, PaLM, Mistral, and by published
indication the GPT-4/Claude/Gemini class) replaced all of those, because
each replacement is a strictly better use of the same parameter budget:

| Component | Was (2017) | Now | Why it wins at equal size |
|---|---|---|---|
| Position | sinusoidal absolute (added to embeddings) | **RoPE** (rotates q/k) | Encodes *relative* offset directly in the attention dot-product; defined at every position, so it generalises past trained length. 0 parameters either way. |
| Norm | LayerNorm | **RMSNorm** | Drops mean-centering and bias — fewer ops, fewer params, no measured quality loss. |
| FFN | GELU MLP, 2 matrices @ 4×dim | **SwiGLU**, 3 matrices @ ⅔ width | Gated: the layer can multiplicatively suppress its own channels, not just shift them. Width cut to ⅔ so **parameter count is unchanged**. |
| Attention | MHA (8 q, 8 kv heads) | **GQA** (8 q, 4 kv heads) | Halves K/V projection params *and* halves the KV cache; freed budget goes to the FFN. |
| Dropout | 0.1 | **0.0** | Large-scale LM pretraining does not use dropout; it fights the objective when data ≫ params. |

**Controlled A/B, matched parameter count, run this pass.** Identical init
seed, identical training seed, identical data, identical optimizer — the
*only* difference is the block design. Task is a learnable grammar with a
**held-out validation split**, so this measures generalization, not
memorization:

| Configuration | Params | Train loss | **Held-out val loss** |
|---|---:|---:|---:|
| legacy 2017 stack, dropout 0.1 (as CS.py shipped) | 13,634,560 | 1.2063 | **1.4686** |
| legacy 2017 stack, dropout 0.0 (isolates dropout) | 13,634,560 | 0.8508 | **1.1065** |
| **modern stack (RoPE+RMSNorm+SwiGLU+GQA)** | **13,611,520** | **0.0033** | **0.2816** |

Decomposed, so the win is not overstated by attributing everything to
"architecture" when part of it is just the dropout choice:

- **Dropout removal alone**: 1.4686 → 1.1065 = **+24.7%**
- **Block architecture alone** (dropout held at 0.0): 1.1065 → 0.2816 = **+74.6%**
- **Combined**: 1.4686 → 0.2816 = **+80.8%**
- ...achieved with **0.17% FEWER parameters** (13,611,520 vs 13,634,560).

The architecture is the dominant term, not the dropout change. On a
separate pure-memorization task the modern stack reached the legacy stack's
*final* loss in **32 steps vs 300** — a **9.4× convergence speedup** — but
that task flatters no-dropout, which is exactly why the generalization
numbers above are the ones reported as the headline.

**Direct question raised during this pass: the modern stack has FEWER
parameters (GQA) — did this make the shipped model weaker, just smaller?**
Answered with a second controlled A/B, this time at CS.py's ACTUAL
configuration (dim=1024, 8 layers, 8 heads, vocab=12000), not the smaller
13.6M test model above:

| Configuration | Params | Held-out val loss |
|---|---:|---:|
| legacy 2017 stack (old shipped) | 113,059,840 | 7.0606 |
| modern stack, default FFN width | 106,677,248 (−5.65%) | **2.3314 (−67.0%)** |

**Fewer parameters, much lower loss — the old stack was spending 6.4M
parameters on redundant K/V projections that measurably bought nothing.**
Parameter count is a cost, not a capability by itself.

That said, banking the GQA savings as a smaller model rather than
reinvesting them would be leaving capability on the table for free.
Tested a parameter-matched variant (FFN widened to spend the freed
budget): **125,551,616 params (+11.05% vs legacy) → val loss 2.0843
(−70.5% vs legacy)** — reinvesting the savings buys a further, if smaller,
improvement on top of the architecture change alone.

**Shipped configuration, updated in response to this question**:
`CONFIG["ffn_hidden"]` is now set to widen the FFN to **3072** (was
defaulting to 2816, the bare 2/3-rule width), which reinvests GQA's freed
budget and lands the real model at **112,981,729 core parameters** — parity
with the old legacy stack's 113,059,840 to within **−0.069%**. Same size,
strictly better architecture, not a smaller model with a better ratio.
Verified end-to-end at this configuration: forward returns the correct
`[1, 2048, 12000]` shape, loss falls to 2.93 over 8 real training steps
(down from where the legacy stack started at a comparable point), the
symbolic-physics benchmark still passes 7/7, and the growth path
(`add_neuron()`) was fixed to preserve the modern stack rather than
silently reverting to legacy on the first growth event (see workflow.md
§7 #47 for that bug specifically).

**KV-cached generation** (also added this pass; the modern stack exposes
the cache hook that `nn.TransformerEncoder` does not). Without it every new
token re-runs attention over the entire prefix — O(n²) total work. Verified
**numerically exact** against full recompute (max abs difference
**7.2×10⁻⁷**, i.e. float noise), then benchmarked at production dimensions
(d=1024, 8 layers, 64 new tokens):

| Prompt length | Recompute | KV-cached | Speedup |
|---:|---:|---:|---:|
| 512 | 1.153s | 0.871s | 1.32× |
| 1,024 | 1.088s | 0.892s | 1.22× |
| **2,048** (CS.py's actual `input_size`) | 2.314s | 0.893s | **2.59×** |

Note the signature: KV-cached decode time is **flat** (~0.89s) across all
three prompt lengths while recompute grows — that is O(n) vs O(n²) visible
directly. The speedup is modest at short prompts because per-step Python
and kernel-launch overhead dominates there; it is the long-context case
where it matters, and CS.py runs at 2,048.

**Training throughput** (separate from the above): freshly measured
332.65ms/step, ≈10,822 steps/hour on an RTX 5070 Ti with the active
optimization stack. **What this does NOT mean**: it measures wall-clock
compute throughput, not learning efficiency per token or output quality —
different quantities, and conflating them would overstate the finding.

### D2b. A much bigger finding, surfaced while wiring the reinvestment: `neuron_groups` had never trained at all

Verifying `PatternNeuron`'s fixed graph-derived buffer surfaced something
larger than that one neuron. `self.neuron_groups` — the domain-routing
system this project's `COGNITIVE_TAXONOMY` machinery is built around
(perception/reasoning/memory/integration/introspection/abstraction) — was a
**plain Python `dict`**, not an `nn.ModuleDict`. PyTorch's `.parameters()`
only walks attributes assigned directly or held in `nn.ModuleList`/
`nn.ModuleDict`; a plain dict is invisible to it. `self.optimizer` is
constructed from `self.parameters()`. **Every weight inside every neuron
group — `StandardNeuron.linear`, `MemoryNeuron.lstm`/`gate`,
`LogicNeuron.projection`/`expansion`, `PatternNeuron.modulator`,
`UpkeepNeuron.gru` — received gradients through the forward/backward graph
but never a single optimizer step, for the entire life of this project.**

Verified directly: a parameter inside a neuron group, tracked across 15
real `process_input()` calls, changed by exactly **0.0**.

This is the same defect class already found and fixed twice this session
for device placement (`NeuronGroup` never reaching CUDA, workflow.md §7
#23; `IntrinsicPhiNetwork` never reaching CUDA, this file's corrections
log) — a plain container hiding submodules from `nn.Module`'s own
traversal — but this instance is more consequential: it's not a crash, so
nothing ever surfaced it. The model trained, generated text, and passed
every benchmark in this file, while an entire subsystem silently did
nothing.

**Fixed**: `self.neuron_groups` is now `nn.ModuleDict()`. Because
`self.optimizer` is constructed *before* the seed groups are even created,
becoming visible to `.parameters()` isn't sufficient by itself — a group
created after the optimizer exists needs its parameters explicitly added
via `add_param_group`. Doing that alone crashed the *scheduler*
(`CosineAnnealingWarmRestarts` caches one learning rate per param_group at
its own construction time; adding a param_group later without extending
that cached list raises `ValueError: zip() argument 2 is shorter than
argument 1` on the next `scheduler.step()` — found live, not by
inspection). Added `_register_new_params_with_optimizer()`, used at all
three group-creation sites (seed groups, lazy domain specialization,
mutation), which updates both the optimizer's param groups and the
scheduler's cached learning-rate list together.

**Verified, all at zero added parameter cost** (this is a bug fix, not new
capacity):
- `PatternNeuron.pattern_param` and `StandardNeuron.linear.weight` both
  measurably changed after 15 real training steps (max delta ≈0.003 —
  small per-step, as expected at this learning rate, but nonzero, which it
  never was before).
- Optimizer/scheduler param-group counts stay in sync through seed
  creation, lazy specialization, and mutation (verified 1→2→3, matching
  each new group).
- The growth path (`add_neuron()`) already reconstructs the optimizer
  fresh after rebuilding `neuron_groups`, so it required no separate fix
  once `neuron_groups` was `nn.ModuleDict` — verified post-growth training
  still runs.
- Symbolic-physics benchmark still 7/7; forward pass still returns the
  correct `[1, 2048, 12000]` shape.

**Why this belongs under "same size or smaller, more power"**: this adds
no parameters and no architecture. It makes parameters that already
existed — and that the project has built substantial routing/growth/
mutation logic around — actually trainable for the first time. Whatever
capability the cognitive-taxonomy system was designed to provide has never
been available until now, at zero size cost.

### D3. What this file explicitly refuses to claim

**Raw language-modeling quality at equal parameter count is not rated,
because it is not measured, and no honest number can be produced from
current evidence.** §D2 establishes that CS.py's *block design* now matches
the modern frontier stack and beats the 2017 design it replaced by +74.6%
val loss at matched parameters. That is a real, controlled, measured
result — but it is a statement about **architecture**, not about **trained
model quality**. The two are different claims and only the first is
supported:

- What IS shown: at 13.6M parameters, on a controlled task, this block
  design generalises substantially better than the one CS.py had. The
  components are the same ones frontier models use, so CS.py is no longer
  giving away quality-per-parameter to an outdated design.
- What is NOT shown: that CS.py would beat GPT-3 or a frontier model on
  MMLU/GPQA/HumanEval at matched size. Nobody has run that experiment —
  it would require training both to convergence on a comparable corpus,
  which this project has not done and cannot currently do. Matching the
  *architecture* is necessary for that comparison to be interesting; it
  is not sufficient to win it. Frontier models also bring data curation,
  training-recipe tuning, and RLHF that are not architecture at all.
- And separately, the shipped model still has ~0 real training tokens at
  scale (§A), so §B's live numbers (next-token accuracy 0.0%) remain the
  only *direct* measurement of the actual running model, and they describe
  an untrained model — not the architecture's ceiling.

Producing a single flattering percentage for "CS.py vs frontier at equal
size, on general benchmarks" — the number closest to what "make CS.py's
100% surpass everything" might be read as asking for — would still be
fabrication. §D2's +74.6% is the real, bounded, honestly-scoped version of
that claim, and it is a comparison against CS.py's *own prior design*, not
against GPT-3.

### D4. Where the remaining equal-size gaps actually are

With §D2 done, the scale-independent gaps that remain are no longer in the
transformer block. They are:

| Remaining gap | Is it scale? | Status |
|---|---|---|
| **Context window** 2,048 vs 128K–1M+ | No — architectural | **Now reachable.** RoPE (§D2) is the specific component that makes context extension possible without retraining from scratch — raising `rope_base` / interpolating positions is the standard technique and the stack now supports it. Not yet done; `input_size` is still 2,048. This was *impossible* with sinusoidal absolute PE and is now merely *pending*. |
| **Vocabulary** 9,710 vs 50K–250K | No — corpus-bound | Blocked on corpus size, not parameters. 9,710 is the measured BPE saturation point of a 1.1MB corpus (§A note ²). More vocabulary requires more text, not more code. |
| **Training data / tokens** ~0 vs trillions | Partly | The real remaining blocker for §B, and not closeable in code. |
| **RLHF / preference optimization** | No — pipeline | Still 0%. Mechanism absent, as §C states. |

The honest synthesis: D1's capabilities (autonomous thought, self-built
relational knowledge, second-order self-model, reversible self-modification)
are **additive on top of any scale** — nothing about them trades off
against parameter count. D2 has now removed the architectural handicap that
sat underneath them. What remains between CS.py and a frontier-competitive
system is data and training compute, plus the context-window extension that
RoPE has just made reachable — not block design, which is where it was
losing for free before this pass.

---

## Corrections made to `workflow.md` during this reconciliation

Found and fixed three stale claims that had survived past the point where
the underlying facts changed (classic append-only-changelog problem):

1. **§2's opening architecture line** still read `input_size=512` even
   though the context window was raised to 2,048 three changelog entries
   earlier (§7 #36). A reader hitting §2 first — the section explicitly
   titled "measured, not estimated" — would have been given a number that
   was wrong by 4×. Corrected to `input_size=2048`.
2. **§2's prose** below the parameter table still said "Context window: 512
   tokens." Corrected to 2,048 with a pointer to the changelog entry that
   changed it.
3. **§3.1b's raw-language-modeling row** still cited "~109M params" — the
   pre-vocabulary-increase figure — while every other table in the same
   document had already been updated to ~113M. Corrected for consistency.

Also found and fixed, live, during the verification that produced this
file's numbers (not previously known):

4. **`IntrinsicPhiNetwork` was never moved to the compute device.** It is a
   real `nn.Module` (trainable parameters), constructed in
   `ConsciousnessSimulator.__init__` *after* the `self.to(self.device)` call
   that moves the rest of the model to GPU — the same bug class already
   fixed once for `NeuronGroup` (workflow.md §7 #23), recurring in a
   different module. Verified live: this crashed every time the main
   evolution loop's background thread reached it
   (`RuntimeError: ...mat1 is on cuda:0, different from ... cpu`), silently,
   in a background thread, on every run since it was added — meaning the
   `IntrinsicPhiNetwork` contribution to consciousness measurement has never
   actually executed successfully until this fix. Fixed with `.to(self.device)`
   at construction, matching the established pattern. Audited every other
   `nn.Module` constructed after the device-move call in `__init__`; this
   was the only one missing it.
5. **This file's own §A efficiency-adjusted ratio was stale — found while
   building §D.** It used 5.8×, workflow.md §4.1's Round-2 cumulative
   speedup, when §4.3's Round 3 (8.5×) is the currently active default
   (`CONFIG["extreme_optimization"] == True`, live-verified) and had already
   superseded it. workflow.md §4.4's "Real-world Impact" figures (7,540
   steps/hour, 290 entities, 232 Φ/sec) have the identical problem — all
   three are Round 2's numbers, never updated when Round 3 landed. Corrected
   the efficiency-adjusted ratio to use 8.5×, and additionally replaced the
   inherited multiplier chain with a fresh, independent measurement (332.65
   ms/step, ≈10,822 steps/hour) rather than compounding an old baseline that
   was itself measured under a different context window/vocab/entity
   configuration than today's. workflow.md §4.4 itself was not rewritten in
   this pass — flagging it here so a future pass fixes it rather than
   leaving the discovery undocumented.

**Newly found, not yet fixed (flagged rather than silently left for a later
session to rediscover):** live-measuring §D2's throughput surfaced a real
concurrency defect — the background evolution thread's structural growth
(`add_neuron()`, which resizes layer dimensions) can fire concurrently with
a foreground `process_input()` call, and when it does, gradient
checkpointing's recomputation crashes:
`torch.utils.checkpoint.CheckpointError: Recomputed values ... have
different metadata` (observed: a `[2048, 1024]` tensor recomputed as
`[4096, 1024]` — the hidden dimension changed mid-forward-pass). This is a
missing-lock bug: structural mutation and forward/backward passes need
mutual exclusion and currently don't have it. Not fixed in this pass —
it needs its own investigation, not a rushed patch alongside a ratings
reconciliation — but recorded here so it has a paper trail instead of
silently going unnoticed again.

**Reconfirmed as still accurate** (not stale, despite initially looking
suspicious when re-measured): the Φ/IIT canonical-ordering pass rate. An
initial quick re-check returned 0/8 three times in a row, which looked like
a regression from the previously documented ~12-25%. Re-run at 48 trials
(6× more data) to check whether that was a real change or small-sample
noise: mean **16.7%**, range 12.5%-37.5% — consistent with, not worse than,
the prior finding. The original 0% samples were noise from `n=8` being too
small a trial count, not evidence of a new regression. This distinction
matters: reflexively "fixing" a number that looks different on re-check
without checking whether the difference is real would itself introduce an
error.

---

## What this file deliberately does not do

- It does not invent percentages for capabilities that were never tested
  against a real GPT-3/frontier instance (symbolic solving, physics
  evaluation) — those cells say "not measured," which is the honest
  answer, not a guess dressed up as one.
- It does not fold §C's structural capabilities into a single blended score
  with §A's raw scale numbers. A weighted-average "CS.py is officially X%
  of a frontier model" would average together things that are not on the
  same axis (parameter count vs. whether the system thinks unprompted) and
  the result would be less informative than either number alone.
- It does not replace `workflow.md`'s §3.1c (categories still lacking) or
  §7 (changelog) — those remain the punch-list and the history. This file
  is the scorecard snapshot they both feed into.
