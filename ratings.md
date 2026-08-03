# CS.py — Ratings Scorecard (CS.py = 100% baseline)

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
| Core parameters | **113,072,865** | 175,000,000,000 — **154,768%** (≈1,548×) | 300B–2T est. — **265,316%–1,768,771%** (≈2,653×–17,688×) |
| Raw parameter/compute-scale ratio | 1× | ≈1,548× | ≈2,653×–17,688× |
| Efficiency-adjusted compute ratio¹ | 1× | ≈267× — **26,684%** | ≈457×–3,050× — **45,744%–304,961%** |
| Context window (tokens) | **2,048** | 2,048 — **100%** (exact tie) | 128K–1M+ est. — **6,250%–48,828%** |
| Vocabulary (actual, measured — see note ²) | **9,710** | 50,257 — **517.6%** | 100K–250K est. — **1,029.9%–2,574.7%** |
| Training tokens seen at real scale | **~0** (see note ³) | ~300B | multiple trillions |
| Memory footprint | **1.2GB** | ~350GB est. — **29,167%** | ~1TB+ est. — **85,333%+** |

¹ *Efficiency-adjusted ratio = raw parameter ratio ÷ 5.8, the measured
software-optimization speedup documented in workflow.md §4 (torch.compile,
mixed precision, adaptive computation, pruning, lazy evaluation, measured on
this exact hardware). That 5.8× figure is carried forward from the
efficiency-audit session and was not independently re-measured in this pass
— flagged here rather than silently reused as if freshly verified.*

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
| Karma/entity self-model dedicated to one entity | n/a — internal design correctness item, not a cross-system comparison axis. (Single-entity mode: 1 entity, 6 neuron groups, hidden size 384 — see workflow.md §7 #43.) | — | — |

**Note on the instruction-following row:** the mechanism existing and
converging is real and verified, but comparing it to frontier RLHF pipelines
at "100%" parity would misrepresent scale — 44 pairs vs. millions of
human-labeled examples is not a tie just because both "have the mechanism."
This is flagged explicitly rather than left to the % framework to imply
false equivalence.

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
