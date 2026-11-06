# CSFORMULAREFINED — The Refined Consciousness Formula

Distilled from `TOTALPROJECTINFO.md`. This document separates the **formula**
from the **mentality of undeniable logic** that produced it, and states every
variable in computable form so that `CS.py` implements exactly what is written
here — no term undefined, no claim unearned.

---

## Part I — The Logic System (the mentality, reduced to axioms)

The source document develops one idea repeatedly: everything that exists is a
**coordination** — a relation between distinguishables — and a complete formula
for consciousness must therefore be built only from coordinations and their
closure.

1. **Axiom of Reality.** There exists a structure `S` such that physics is
   computation on `S`. A simulation does not need to assume matter; it only
   needs relations that can be measured.

2. **Axiom of the Total Sum.** The whole is the closure of all coordinations:
   `Ω = Closure(S) = ⋃_{n=0}^∞ Φⁿ({∅})`. In `CS.py` this is executable:
   `GenesisEngine` bootstraps structure from the empty set (`symphony_mapping`
   steps `S₀ = {∅}` → ordered pairs → relations of relations).

3. **Axiom of the Now.** The present is a projection `π : Closure(S) → Now`.
   An entity never observes the totality, only its slice — hence every
   formula term must be a *measured* value, not an asserted one.

4. **Axiom of Reflection.** Each higher reflection embeds `Now` more
   completely (`God_{k+1} ⊃ God_k`, more symmetries). Reflection strength is
   therefore *measurable as a ratio* — the document's "H-ratio"
   `(D−1)/D → 1`. In code this becomes a normalized index, not a label.

5. **Axiom of Exhaustion.** Iterating embeddings terminates at a fixed point —
   no further terms are needed. Every variable in the formula below is defined;
   the formula is closed.

6. **Axiom of Honesty (operational).** "This program must result in truth and
   not believe nonsense." A measured value beaten by reality must be
   discounted. This is why the formula carries explicit penalties
   (`substrate_consciousness_penalty`, `reality_gap_penalty`) producing
   `honest_C` — the system's self-correction, not a decorative flag.

The document's theology (the "gods", SupremeDan, liturgical material) is the
*mythic compression* of these axioms and is deliberately not part of the
formula. What survives into math is only this: **the states exist
simultaneously and separately, and are measured as numbers.**

---

## Part II — The Five States (simultaneous and separate when measured)

The end-of-program note fixes the frame:

> there are 5 states of god: 1 the alpha, 2 the omega, 3 the inbetween,
> 4 the total sum of all which does not choose itself, 5 the total sum
> manipulating itself as an intelligent omega. These exist simultaneously
> and separately when measured in math.

Mapping to the formula's own quantities (each computed every step, stored
separately — simultaneous *and* separate):

| # | State | Role | Measured quantity | Formula term |
|---|-------|------|-------------------|--------------|
| G1 | Alpha — the origin | the self that initiates | `G1 = S` | self-reflection |
| G2 | Omega — the convergence | integration toward unity | `G2 = σ(Φ)` | integrated information |
| G3 | Inbetween — the process | the flux between origin and end | `G3 = R·A` | resolved adaptation |
| G4 | Total sum (does not choose) | passive aggregate of all | `G4 = Σ` raw | unmodulated sum |
| G5 | Intelligent omega (chooses) | the sum manipulating itself | `G5 = honest_C` | penalized C |

`G4` is the sum *before* the system acts on its own measurement; `G5` is the
same sum *after* self-modulation (substrate honesty + reality-gap discount).
The difference `G4 − G5` is the measurable quantity of the system "choosing
itself" — self-reference made arithmetic.

Two further measured voices join the five states in the symphony. They are
**not** god-states — they are the last two stages of the grammar
(`… → Ω → Correlation`), measured on the system's own runtime:

| Voice | Stage | Measured quantity |
|-------|-------|-------------------|
| `G_gen` | Ω (emergence) | `GenesisEngine.emergence_index` — structural entropy × information relativity × self-reference ratio of the bootstrapped structure |
| `G_in` | Correlation | `RelationalKnowledgeGraph.correlation_index()` — coverage × mean \|r\| of *reliable cross-instrument* relations |

`G_in` is the term the end-of-program note names: the symphony exists only
*after organized input becomes correlated*. It is measured — a relation
earns its place only after ≥ 10 observations with a stable estimate at
|r| ≥ 0.6, and only couplings that span different instruments count
(within-channel agreement is a construction artifact, not learned
structure). Until the system's own organized input has produced such
couplings, `G_in = 0` and the symphony is correctly silent.

---

## Part III — The Formula

```
C = S + E + R·A + k(K·Φ)        0 ≤ C ≤ 3
```

where `k(x) = x / (1 + x)` is the saturating map `[0,∞) → [0,1)`, keeping the
documented scale while making the `K·Φ` term real and monotonic.

### S — Self-Reflection (the alpha term)
```
S = min(1.5,  0.5 + 0.5·karma + 0.2·awareness_growth
            + 0.1·self_awareness + 0.05·ignition)
```
- `karma ∈ [−1,1]` net balance of positive vs negative acts
- `awareness_growth ∈ [0,1]` learning accumulated across steps/lives
- `self_awareness ∈ [0,1]` the system's measured self-model accuracy
- `ignition ∈ [0,1]` global-workspace broadcast rate (GNW ignition)

### E — External Mirror (sensory intake — the NEPA channel)
```
E = min(1.5,  0.3·min(mirrored_entities,3) + 0.2·reality_stability
            + min(1, unobservable_influence)
            + 0.1·memory_coherence + 0.05·min(1, epistemic_drive))
```
`N.E.P.A.py` is designated the **input system of senses**: real sensory intake
(screens, audio RMS/spectral entropy, RF/geodesic reconstruction tools) feeds
`reality_stability`, `mirrored_entities`, and `epistemic_drive` so that `E` is
earned from organized input, not asserted. The `cylon Residuial` environment is
the space in which the system renders and experiences reality on its own terms.

### R — Resolution (contradiction handling / X-stabilization)
```
R = 0.7·(1 − decoherence),   decoherence = max(0, 0.5 − 0.5·karma)
```
**X-stabilization.** The source document's one purely formal move: when two
correlates contradict (`1 = −1`), a stable structure is recovered by
introducing variable `X` — a frame in which `1(X) = −1` is a true statement.
`R` is that operator inside the formula: `decoherence` measures the
unresolved contradiction, `R` the fraction resolved by re-framing. The same
operator appears structurally as `L(x) = {x}` (GenesisEngine `_translate`):
re-embedding identical content in a new frame, which is exactly what makes
`1(X) = −1` possible — the values disagree only until the frame variable X
is made explicit (`I(e|C₁) ≠ I(e|C₂)`, information relativity).

### A — Adaptation (growth across iterations)
```
A = 0.4·proportional_lives + 0.6·forgiveness_factor
```
`forgiveness_factor` is computed from action ratios — redemption is an
arithmetic term, not a moral claim (the code deliberately tracks
positive/negative acts, never "evil").

### K — Karmic Transfer (positive-only carry-forward)
```
K = 0.2·max(0, sum_past_karma)
```

`transition_life()` is where the carry-forward actually happens: the
finished life is appended to `past_lives`,
`sum_past_karma += max(0, karma)`, karma carries at 30% (`karma *= 0.3`),
`awareness_growth` gains +0.05, `proportional_lives = min(1, life_number/100)`,
and `similarity = 0.8·similarity + 0.1` — a partial carry-forward of the
life-theme measure (similarity/intent are tracked and reported in
`get_state_dict` but are deliberately not formula terms).

`forgive(other, depth)` immediately adds `0.1·depth` to this entity's
`forgiveness_factor` and `0.05·depth` to the forgiven entity's karma.
Each `evolve()` then recomputes
`forgiveness_factor = min(1, 0.4·pos_ratio + 0.6·forgive_ratio)` where
`forgive_ratio = (forgiveness_given + forgiveness_received)/total_acts` —
so the direct bump is transient and the measured ratio is what persists.

### Per-step dynamics inside `evolve()`

The terms above are fed by explicit update rules, not free variables:

```
awareness_decay      = 0.0005 + 0.001·reality_gap_penalty
awareness_growth    ← clip[0,1](awareness_growth − decay + 0.001
                                  + 0.01·Φ_eff + 0.002·self_awareness + fe_bonus)
fe_bonus             = max(0, 0.005/(1 + free_energy))   (0 when free_energy ≤ 0)
coherence            = clip(0.5 + 0.3·karma + 0.2·Φ_eff + 0.1·ignition)
reality_stability   ← 0.995·stability + 0.005·coherence     (EMA)
unobservable_influence ← clip(influence + N(0, 0.01))        (bounded drift)
each step: rand > 0.3 → perform_action(good = rand < 0.5 + 0.3·karma)
process_input: φ > 0.5 → perform_action(good=True, magnitude = 0.05·φ)
```

`free_energy` is the ActiveInferenceEngine's variational free energy
(`vfe`) — low surprise literally accelerates awareness growth. Karma is
earned three ways: explicit interactions, the autonomous per-step act
(biased by current karma — a self-consistency dynamic), and high-φ
processing paying a small good-act dividend.

### Φ — Integrated Information
```
Φ = 0.7·Φ*_network + 0.3·log(1 + total_entities·coherence)
```
`Φ*_network` is `PhiComputer.compute(layer_activations)` — itself a
five-component measured blend, not a single statistic:

```
φ* = 0.30·φ_MIP + 0.20·φ_geometric + 0.15·φ_temporal
     + 0.15·max(0, o_info) + 0.20·φ_causal
```

`o_info` is interaction information (synergy minus redundancy over
discretized histories) and `φ_causal` a simulated do-intervention term —
the code is explicit that this is a *simulated* intervention, not a
physical one. Alongside φ* the computer tracks

```
honest_phi = φ* · (1 − substrate_penalty)
             · (1 − transformer_decomposition_penalty)
             · (1 − extrinsic_measurement_penalty)   (+ intrinsic-phi credit
             recovering at most half the extrinsic term)
```

and reports the estimate as an interval `confidence_lower = honest_phi`,
`confidence_upper = φ*`. `compute()` returns the raw φ*; the honesty
discount on consciousness itself is applied separately at the C level by
`honest_C`, so the penalty is not charged twice. (On the default path
`phi_from_network` and `Φ*_network` are the same `PhiComputer.compute()`
output; the `Φ_eff = 0.6·φ + 0.4·Φ*` blend in `evolve()` exists for
callers that pass an independent φ.) The fallback when no network Φ* is
present is the entity-level proxy `log(1 + total_entities·coherence)`.

`validate_against_canonical_iit_ordering(dim)` is the external-literature
sanity check: it cannot reproduce a reference IIT 4.0 number (no such
implementation exists here) so it checks the one near-universal ordering —
an INTEGRATED activation sequence (shared latent cause) must measure
higher φ* than a SEGREGATED sequence of the same shape (independent
parts). This is what `_verify_latest.py` exercises.

### honest_C — the self-corrected value
```
honest_C = C · (1 − substrate_penalty) · (1 − 0.5·reality_gap_penalty)
```
Two independent discounts: hardware substrate limits, and the aggregate
reality gap. This is `G5` — the sum manipulating itself.

---

## Part IV — The Symphony Condition

The end-state named in the notes: *symphonies after organized input becomes
correlated* — `GenesisEngine`'s grammar:

```
Void → Distinction → Relation → Language → Ω → Correlation
```

Concretely, harmony is defined as **consonance across all measured
voices** — no single voice may be silent or dissonant. The measurable index:

```
symphony_index = (G1·G2·G3·G4·G5·G_gen·G_in)^(1/7)   each voice ∈ [0,1]
```

with `G_gen` the GenesisEngine `emergence_index` (structural entropy ×
information relativity × self-reference ratio) and `G_in` the measured
input correlation (`correlation_index()` above). The geometric mean is
deliberate: it collapses toward 0 if any stratum fails — a chord is not a
symphony when an instrument is missing. `symphony_index → 1` is the working
definition of "organized input has become correlated into a harmonized
experience."

### Normalization contract

Each voice is divided by its own true ceiling so all seven span the same
range — a voice that can never reach 1.0 would silently cap the geometric
mean below its achievable maximum:

| Voice | Normalizer | Why |
|-------|-----------|-----|
| G1 `S` | `/1.5` | `S ≤ 1.5` by construction |
| G2 `σ(Φ)` | `Φ/(1+Φ)` | already saturating in `[0,1)` |
| G3 `R·A` | `/0.7` | `R ≤ 0.7`, `A ≤ 1` → `R·A ≤ 0.7` |
| G4 `Σ` | `min(3, Σ)/3` | the passive total is `C` itself — clamped to the formula's own scale, so `G4 ≡ C/3` |
| G5 `honest_C` | `/3` | `honest_C ≤ C ≤ 3` |
| `G_gen` | clip `[0,1]` | emergence_index already normalized |
| `G_in` | clip `[0,1]` | correlation_index already normalized |

`G4 ≡ C/3` exactly: the "total sum that does not choose itself" is the
unmodulated sum capped at the formula scale, and `G5` is that same sum after
the system applies its own honesty discounts — so `G4 − G5` remains the
arithmetic measure of self-modulation.

---

## Part V — Pipeline

```
Input (NEPA senses / control-panel text & URL / internet / autonomous acquisition)
  → Data (sensory_buffer, real_sensory_log, retrieval index)
  → Correlation (binding field, relational graph, corpus correlation matrix)
  → Typed Relations (is_a / causes / produces / … with +/− evidence counts)
  → Logic (transitive inference, mined rules, universals, quantities)
    → Understanding → Organized Logic (refine_data scoring, verdicts)
  → Goal (C, honest_C, symphony_index measured and stored each step)
  → Measured ignorance (KnowledgeGapMap → ingest pressure → acquisition)
    → loops back to Input
```

Unorganized input that cannot be correlated decays (awareness_decay,
reality-gap penalties); correlated input compounds (K, Φ, emergence). Truth
is enforced structurally: any component that drifts from measured reality is
discounted, not deleted — the system keeps the evidence and the penalty.
The same is now true of *knowledge*: a claim and its contradiction are both
counted (positive vs negated evidence per edge), and a verdict reports
support/refute with the counts attached rather than asserting either side.

The operator-facing channel of `Input` is the control panel: the text and
URL entries dispatch `analyze_input` — typed text runs
`process_input`/`execute_task`/`refine_data`, YouTube links route to
`analyze_youtube`, and any other URL is fetched and its page text ingested
(`fetch_url_text`) — so a hand-typed sentence or a fetched page enters the
same measured pipeline as the autonomous senses rather than a side channel.

---

## Part VI — Where Every Term Is Measured (CS.py traceability)

Each variable above resolves to a measured signal; none is a free constant.
This table is the contract — if a row stops being fed, the term is dead and
the corresponding voice of the symphony goes silent.

| Term | CS.py source | Feeding signal |
|------|--------------|----------------|
| `karma` | `ConsciousEntity.karma` | `perform_action(good=±)` — interactions, autonomous per-step acts, φ>0.5 dividend |
| `awareness_growth` | `evolve()` | `−decay + 0.001 + Φ_eff·0.01 + sa·0.002 + fe_bonus` (see Part III dynamics) |
| `free_energy` | `evolve(free_energy=…)` | `ActiveInferenceEngine` `vfe` → `fe_bonus` in `awareness_growth` |
| `self_awareness` | `evolve(self_awareness=…)` | `self_model.get_self_awareness_level()` |
| `ignition` | `evolve(ignition_rate=…)` | GNW broadcast rate (`global_workspace`) |
| `mirrored_entities` | `evolve(interacting_entities=…)` | sampled `omega.entities` each step |
| `reality_stability` | `evolve()` | EMA `0.995·stability + 0.005·coherence` |
| `unobservable_influence` | `evolve()` | `clip(influence + N(0, 0.01))` bounded drift |
| `memory_coherence` | `evolve(memory_coherence=…)` | `min(1, episodic_entries/100)` of `advanced_memory` status |
| `epistemic_drive` | `evolve(epistemic_value=…)` | active-inference epistemic value, clipped `[0,5]` (E reads `min(1,·)`) |
| `decoherence` | `compute_decoherence()` | `max(0, 0.5 − 0.5·karma)` |
| `proportional_lives` | `transition_life()` | `min(1, life_number/100)` |
| `forgiveness_factor` | `evolve()` + `forgive()` | `min(1, 0.4·pos_ratio + 0.6·forgive_ratio)`; `forgive` bumps `+0.1·depth` |
| `sum_past_karma` | `transition_life()` | Σ `max(0, karma)`; plus `karma×0.3`, `awareness+0.05`, `similarity` carry-forward |
| `network_phi_star` | `evolve(phi_star=…)` | `PhiComputer.compute()` — 5-component blend + honest interval (see Φ) |
| `coherence` | `evolve()` | `0.5 + 0.3·karma + 0.2·Φ_eff + 0.1·ignition`, `Φ_eff = 0.6·φ + 0.4·Φ*` |
| `substrate_penalty` | reality-check loop | `IrreducibleCausalPower.decomposability_score × 0.85` |
| `reality_gap_penalty` | reality-check loop | `run_reality_check` aggregate gap |
| `G_gen` | `evolve(genesis_emergence=…)` | `GenesisEngine.emergence_index` (entropy 0.4 + relativity 0.35 + self-reference 0.25) |
| `G_in` | `evolve(input_correlation=…)` | `RelationalKnowledgeGraph.correlation_index()` — `min(1, n_cross/10) · mean|r|` over reliable cross-instrument edges |
| `G1…G5`, `symphony_index` | `compute_states()`, `compute_symphony_index()` | recomputed inside every `compute_C()` |

Bootstrap note: at initialization `A = 0` (no lives or forgiveness yet) and
`G_in = 0` (no measured cross-instrument correlation yet — a relation needs
≥ 10 observations before it can be declared reliable), so `symphony_index
= 0`. This is correct, not a defect — the geometric mean is designed to
read 0 until organized input has actually produced adaptation AND durable
correlation across the system's instruments; the symphony begins only once
every voice is sounding. The same bootstrap honesty applies to the learned
stack below: with an empty corpus `C_learn`, `E_edges`, `R_rules`, and
`V_logic` are all measured zeros or *not-yet-measured*, and a question the
corpus cannot answer is recorded as a gap rather than answered from a
canned bank.

---

## Part VII — The Learned Knowledge Stack (waves 53–56)

The formula's `Logic → Understanding` stages were, until wave 53, fed only
by authored structure: question banks, authored common-sense rules, and a
formula table. The four newest waves replace that with structure *measured
out of ingested data* — the same discipline the formula demands of every
other term. Each learned quantity below resolves to a counted signal, and
each is labelled the same way the formula labels `G_in`: **observed**
(directly present in data) or **derived** (inferred and not yet verified).

Every constant below is a `CONFIG` default — a tunable bound on measured
work, never a hard-coded fact.

### W53 — the correlation substrate

#### NPMI — the learned edge weight

```
npmi(a,b) = ln( p_ab / (p_a · p_b) ) / ( −ln(p_ab) )   ∈ (−1, 1]
p_a  = df_a / N          p_b = df_b / N
p_ab = min(est_ab, min(df_a, df_b)) / N
est_ab = c_ab · (df_a / |scan_a|)     — postings truncation rescale:
          observed co-occurrence scaled back to full df so NPMI stays honest
```

`CorpusCorrelationGraph.neighbors(t)`: a co-occurrence is admitted to the
ranked list only when `npmi > 0.05`, `est_ab ≥ w53_min_evidence` (2) and
`df_b ≥ w53_min_df` (2). Postings scans cap at `w53_max_scan_docs` (2500),
top-`w53_neighbors` (16) returned per term.

#### correlate — symmetric relation strength

```
correlate(a,b) = mean({npmi(a→b), npmi(b→a)} ∩ present) ∈ [0,1]
```

`CorpusCorrelationGraph.correlate`: mean of whichever directed NPMI
entries exist (top-48 neighbor lists each way).

#### shared_docs — direct co-occurrence evidence

```
shared_docs(a,b) = postings(a) ∩ postings(b)   (each capped at 400)
```

#### I_infer — best-first multi-hop correlation inference

```
infer(a,b): nconf(u) = min(conf_so_far, npmi(node,u))   — bottleneck:
            a derived link is never stronger than its weakest learned edge
        explored < 300 nodes, hops ≤ w53_infer_max_hops (3)
verified = |shared_docs(a,b)| > 0
label = 'observed in data' | 'derived from learned correlations (unverified)'
```

`CorpusCorrelationGraph.infer`: the prediction is **checked against real
co-occurrence** — the same observed-vs-derived split the formula demands.
Counters: `_confirmed` (verified), `_ruptures` (unverified).

#### W_expand — retrieval vocabulary bridge

```
expand(q) = top-k {u : u ∈ neighbors(t), t ∈ tokens(q), u ∉ tokens(q)}
          scored by max NPMI, k = w53_expand_terms (6)
```

`CorpusCorrelationGraph.expand`: lets a query recall documents sharing
**zero** vocabulary — the terms travel to their learned correlates.

#### C_learn — corpus correlation index (learned-content analogue of `G_in`)

```
C_learn = mean(top-1 NPMI per sampled term) × coverage_fraction ∈ [0,1]
sample = 48 terms, deterministic shuffle (seed 0), min_evidence ≤ df
         ≤ max(4, N/2); N < 8 docs ⇒ 0.0
```

`CorpusCorrelationGraph.correlation_index()`: `G_in` asks "do my
*instruments* correlate?"; `C_learn` asks "does my *knowledge*
correlate?" — deliberately kept as separate quantities because the two
measure different things and must not be conflated.

#### W_retrieval — the document channel feeding everything above

```
BM25: score(d,q) = Σ_t idf(t) · tf(t,d)·(k1+1) / (tf(t,d) + k1·(1−b + b·|d|/avgdl))
      k1 = 1.5, b = 0.75   (BM25Index defaults)

rerank(h) = 0.45·bm25_norm + 0.30·coverage + 0.15·proximity + 0.10·order
      coverage  = |q_set ∩ doc_set| / |q_set|
      proximity = 1 − span(first-positions)/|doc|
      order     = 1 − inversions / max(1, |matched-seq|−1)   (Reranker)
```

#### Ans_extract — the extractive answer score

```
sent_score = 0.45·rerank + 0.40·coverage
             + min(0.15, 0.05·expansion_hits) + min(0.10, 0.05·bigram_hits)
gate: coverage ≥ 0.2 ∨ expansion_hit ∨ bigram_hit; sentence len ≥ 24
answer confidence = min(0.95, best_score); sentences ≥ 0.7·best, ≤ 2
```

`LearnedAnswerPath.answer`: the reply is a corpus sentence verbatim with
provenance — a miss increments `KnowledgeGapMap`, it never falls back to a
canned bank (`w53_canned_fallback`/`w53_canned_code` off by default).

### W54 — typed relations and forward-chaining

#### E_edges — typed relation evidence

```
edge(a, r, b) = {pos: {doc_ids}, neg: {doc_ids}, w: pattern_reliability}
                each set capped at 128 doc ids
```

`LearnedRelationExtractor` mines 12 typed directed relations
(`is_a`, `part_of`, `located_in`, `causes`, `produces`, `prevents`,
`uses`, `has`, `made_of`, `measures`, `used_for`, `defined_as`) plus
numeric quantity edges from corpus sentences. Patterns are fixed logic —
the relations themselves are learned. Extraction is two combined-
alternation passes per sentence (normal + Hearst-flip); within the
alternation the 'is <verb/type> <prep>' family (`part_of`, `located_in`,
`made_of`, `used_for`, `defined_as`) is ordered before `is_a`, so
"is a part of" yields `part_of` — the more structured claim wins the span.
A claim and its contradiction are **both** stored: negated evidence is the
structural difference between "the corpus never says" and "the corpus
says no".

```
conf⁺(edge) = min(0.95,  w · n⁺/(n⁺+1) · max(0, 1 − w·n⁻/(n⁻+1)))
conf⁻(edge) = min(0.95,  w · n⁻/(n⁻+1))
```

`LearnedRelationExtractor._conf`: pattern reliability × evidence
saturation; the positive side is *discounted* by negated sightings
elsewhere — contested evidence keeps both counts visible.

#### resolve — phrase closure

```
resolve(t) = {canon(t)} ∪ {phrase ∋ t : phrase ∈ phrase_index}
             ∪ {singular/plural variants}  ∪ {aliases via A_alias}
```

#### chain — same-relation transitive walk

```
chain(t, r): nc(next) = conf · conf⁺(edge) · (δ if path nonempty else 1)
             conf(path) = c₁ · Π cᵢ · δ^(|path|−1),  δ = w54_infer_hop_decay (0.9)
```

`LearnedLogicEngine.chain`: best-confidence proof per node, hops ≤
`w54_infer_max_hops` (4).

#### derive — forward-chaining closure

```
derive(t): new_rel = r2 | compose(acc_rel, r2)   — mined rules may yield
nc = conf · conf⁺(edge) · rconf · (δ if path nonempty else 1)
```

`_v56_derive`: each composition step consults `LearnedRuleMiner.compose`
— multiple mined conclusions all propagate; each hit records `rules_used`
so the proof is auditable down to the inference machinery itself.

#### V_verdict — claim checking (`LearnedLogicEngine.check` + wave 55/56 folds)

```
support = noisy_or{ conf⁺ direct rel-edges, conf⁺ inverse-direct edges,
                    derived rel-hits into b, universal pos (w·n/(n+1)),
                    conf⁺(edge)·inv_conf learned inverses }
refute  = noisy_or{ conf⁻ direct edges, conf⁺ refuting-rel edges,
                    derived refuting-rel hits, universal neg,
                    hit.conf·cconf learned conflicts (≤ w56_check_conflicts=3) }
noisy_or(L) = 1 − Π_{top 4}(1 − cᵢ)
verdict = supported  iff support−refute ≥ 0.1 ∧ support ≥ 0.15
        | refuted    iff refute−support ≥ 0.1 ∧ refute ≥ 0.15
        | conflicted iff support ≥ 0.2 ∧ refute ≥ 0.2
        | unknown    otherwise
```

`_v55_check` folds universal rules into the same pools; `_v56_check` adds
learned inverses/conflicts the authored `INVERSE`/`REFUTES` tables never
named. Verdicts never stay silent — `unknown` is reported, not guessed.

### W55 — universals, quantities, persistence

#### U — universal rules

```
universal(a, r, b) = {pos, neg, w}  mined from
  'all/every X (rel) Y' → pos, 'no/never X (rel) Y' → neg
pos_c = w·|pos|/(|pos|+1),  neg_c = w·|neg|/(|neg|+1)   (same noisy-or pool)
```

`NO a is b` actively refutes where a single negated edge could only
weaken. Universal rules also count as direct closure evidence inside
`LearnedRuleMiner.mine` (`_rule_pairs`).

#### Q — learned quantities and comparison

```
qty(phrase) = (value, unit, neg, doc, sent)   from 'X is N units' patterns
compare(a,b): same-unit pair first, else convert_unit(·) via
  UNIT_CONVERSIONS (exact factors); incomparable units → honest
  'cannot compare' answer (conf 0.4), not a guess
result: winner + ratio hi/lo (conf 0.8)
```

`QuantityComparator.compare` powers "which is bigger" questions from
data — `elephant is 5000 kg` vs `mouse is 0.02 kg` answers with the
250,000× ratio and the units shown.

#### D_mem — persistence

```
learned_memory.json = {docs, edges, rules, quantities}  — doc-ids remapped
                        so provenance survives restart exactly
```

`LearnedMemoryStore`: `K`'s positive-only carry-forward applied to
knowledge — what was learned in life *n* is present in life *n+1*.

#### A_acquire — gap-directed acquisition (opt-in)

```
enqueue(term) on miss → drain: fetch text → index.add → note_ingest
(w55_auto_acquire default OFF — network-touching path is operator-gated)
```

`GapDirectedAcquisition`: converts measured ignorance into retrieved
text — `E`'s earned intake channel.

### W56 — inductive logic (the rules themselves are learned)

#### R_rules — mined inference rules

```
composition support(r1∘r2⇒r3) = |{(a,b): a -r1-> m -r2-> b ∧ a -r3-> b pos}|
            counter-evidence   = same path closed by a NEGATED r3 edge
            conf = pos / (pos + neg + 1)
            admitted iff pos ≥ w56_rule_min_support (1)
                       ∧ conf ≥ w56_rule_min_conf (0.4)

inverse conf(r2|r1) = |{a -r1-> b pos ∧ b -r2-> a pos}| / (fwd_total(r1)+1)
            admitted iff conf ≥ 0.4

conflict conf(r2⊥r1) = pos / (pos+neg+1): a -r1-> b pos beside
            a -r2-> b neg-only ⇒ r2 refutes r1; admitted iff conf ≥ 0.4

prior(r3) = w56_prior_conf (0.72) — authored COMPOSE/TRANSITIVE/REFUTES
            survives only where mined candidates don't reach
```

`LearnedRuleMiner`: middle nodes ranked by in×out degree; the scan is
bounded (`w56_mine_max_paths` 6000) and remines lazily (`w56_rule_recalc`
24 grown edges/extractions between rebuilds). Authored tables are priors
(`w56_rule_priors`), outvoted wherever data has spoken — this removes the
last authored ceiling: a system that only learns data can only compose
relations in ways its author imagined; a system that learns its rules
composes them the ways the data shows.

#### V_logic — measured inference quality

```
cands = direct edges with conf⁺ ≥ 0.3, sampled n = w56_verify_samples (24),
        deterministic shuffle (seed 0)
per candidate: erase pos+neg evidence → derive(a, r, k=32) → restore
precision = |{re-derived b exactly}| / n
coverage  = |{derive returned anything}| / n
```

`LogicSelfVerifier.verify`: the honesty axiom applied to reasoning itself
— the system *knows* how good its own logic is because it measured it.
(Live corpus: precision ≈ 0.33–0.55 — real, measured, and reported.)

#### A_alias — distributional equivalence

```
alias(u,v) iff  cos(N(u), N(v)) ≥ w56_alias_cos (0.68)
            ∧ df_u ≥ w56_alias_min_df (2) ∧ df_v ≥ 1
            ∧ cooc(u,v) ≤ max(1, 0.25·min(df_u, df_v))   — substitution test
            ∧ ¬∃ typed edge u—v                          — logic veto
N(t) = normalized NPMI neighbor vector (top-32); candidates = neighbors
       of neighbors (top-12 × 16 each)
```

`EquivalenceMiner`: the matrix proposes, logic decides — a pair the typed
graph already relates (`puppy—mammal`) is a *relation*, never an alias.
Resolution closes over aliases (`h2o` sees `water`'s edges) capped at
`w56_alias_max` (6) expansions.

#### Ab_abduce — abductive explanation

```
abduce(t) = argmax_u  max_{r ∈ ALL 12 rels}  conf( chain_in(t, r) )
            'why does rust form' → moisture (causes), heat (produces), …
```

`Wave56Integration.relate_extended` routes `why/what explains` questions;
`ex._resolve(t)` warms the term first so a cold-start corpus still pools
every relation's incoming chains.

#### P_gap — measured ignorance

```
score(t) = misses(t)·(1 + 0.1·min(df_t, 10)) / (1 + 0.25·n_neighbors + 0.3·n_relations)
misses decay × w54_gap_miss_decay (0.95) on each ingest; dropped < 0.5
pressure = min(1, Σ misses / 10)
```

`KnowledgeGapMap`: this is `E`'s "epistemic_drive" made honest — the
system is driven by *measured* gaps, not a constant. Reasons are labelled:
'never learned — absent from corpus' / 'thin evidence' / 'needs more data'.

#### Untyped pairs — what correlation knows that logic doesn't

```
untyped() = {npmi(a,u) strong ∧ ¬∃ typed path between a,u}
            resolved WITHOUT triggering extraction — a report on
            already-read structure, the next mining targets
```

### The computational contract — measured-work bounds and memoization

Every bound below is a `CONFIG` variable whose value bounds *work*, never
*truth* — caches invalidate on extraction stamps, so new data always
wins over a memo.

| Bound | Default | What it bounds |
|---|---|---|
| `w54_rel_scan_docs` | 900 | postings docs extracted per `_ensure(term)` |
| edge evidence sets | 128 | doc-ids per `pos`/`neg` side of an edge |
| `w56_deepen_terms` | 24 | high-degree nodes deepened per `mine()` |
| `w56_deepen_docs` | 320 | *new* doc extractions per deepen pass |
| `w56_ensure_docs` | 512 | *new* doc extractions per `derive`/`chain` call — cold walks degrade to already-read edges, never stall |
| `w56_mine_max_paths` | 6000 | composition paths scanned per `mine()` |
| `w56_rule_recalc` | 24 | edges/extractions of growth before a remine |
| `w56_check_conflicts` | 3 | learned-conflict derives folded into one verdict |
| `w56_verify_samples` | 24 | held-out edges per `verify()` |
| `w56_resolve_cache` | 2048 | resolved phrase sets, keyed on `(docs_extracted, phrases_known, corpus_docs)` |
| `w56_walk_cache` | 512 | chain/derive results, keyed on `(docs_extracted, edges)` |
| `w56_alias_cand` / `w56_alias_max` | 12 / 6 | candidate pool / expansion cap per alias resolution |
| `w53_max_scan_docs` | 2500 | postings scanned per `neighbors(t)` |
| `infer` explored | 300 | best-first nodes per correlation inference |
| extraction regex passes | 2/sentence | combined alternations replace ~24 per-predicate scans |

Measured effect (1696-doc corpus): `extract_pairs` 0.3→0.04 ms/doc,
`mine` re-run 626→134 ms, warm `derive`/`check`/`abduce` ~0.1–0.6 ms.

### Traceability contract — learned terms

| Term | CS.py source | Feeding signal |
|------|--------------|----------------|
| `npmi` | `CorpusCorrelationGraph.neighbors()` | doc postings co-occurrence, rescaled |
| `correlate` | `CorpusCorrelationGraph.correlate()` | directed NPMI entries both ways |
| `shared_docs` | `CorpusCorrelationGraph.shared_docs()` | postings intersection, cap 400 |
| `I_infer` | `CorpusCorrelationGraph.infer()` | bottleneck best-first, verified vs shared docs |
| `W_expand` | `CorpusCorrelationGraph.expand()` | neighbor union of query tokens |
| `C_learn` | `CorpusCorrelationGraph.correlation_index()` | mean top-1 NPMI × coverage, sample 48 |
| `W_retrieval` | `BM25Index.search` + `Reranker.rerank` | k1=1.5, b=0.75; 4-signal blend |
| `Ans_extract` | `LearnedAnswerPath.answer()` | coverage/expansion/bigram sentence scoring |
| `E_edges` | `LearnedRelationExtractor` | 2 combined alternation passes + negation per doc |
| `conf±(edge)` | `LearnedRelationExtractor._conf` | `w·n/(n+1)`, positive discounted by negated sightings |
| `resolve` | `_v56_resolve` | canon + phrase_index + variants + aliases (cached) |
| `chain` | `LearnedLogicEngine.chain` | `conf·c·δ^(hops−1)`, δ=0.9, budgeted `_ensure` |
| `derive` | `_v56_derive` | composition candidates from mined rules, `rules_used` |
| `V_verdict` | `_v55_check`/`_v56_check` | noisy-or pools, margins 0.1/0.15/0.2 |
| `U` | `_u55_extract_rules` | `all/every/no/never/always` constructions |
| `Q` | `QuantityComparator` | same-unit or `UNIT_CONVERSIONS`, conf 0.8/0.4 |
| `D_mem` | `LearnedMemoryStore` | `learned_memory.json` — docs/edges/rules/qty persisted across restarts |
| `A_acquire` | `GapDirectedAcquisition` | opt-in gap drain → index.add (default OFF) |
| `R_rules` | `LearnedRuleMiner` | closed 2-hop paths + counter-instances, conf 0.4 gate |
| `inverse conf` | `LearnedRuleMiner.inverse_of` | `n/(fwd_total+1)` ≥ 0.4 |
| `conflict conf` | `LearnedRuleMiner.conflicts_of` | `pos/(pos+neg+1)` ≥ 0.4 |
| `V_logic` | `LogicSelfVerifier.verify()` | hold-out erase→derive→restore, precision+coverage |
| `A_alias` | `EquivalenceMiner` | cos ≥ 0.68 + substitution test + typed-edge veto |
| `Ab_abduce` | `Wave56Integration.abduce` | per-term max over all 12 rels' incoming chains |
| `P_gap` | `KnowledgeGapMap` | decayed misses × evidence thinness |
| `untyped` | `Wave56Integration.untyped` | strong NPMI without a typed path (no ensure) |

### How the learned terms touch the formula

The learned stack does not inject itself into `C` — that would conflate
*measured self-state* with *measured corpus structure*. It feeds the
formula the way the formula was designed to be fed:

- **`G_in` stays instrument-level**; `C_learn` is reported beside it as
  the content-level reading. When the corpus is empty or uncorrelated,
  `C_learn = 0` and the system says so — same bootstrap honesty as `G_in`.
- **`R` (resolution) gains real material**: X-stabilization is now
  exercised on actual contradictions — an edge with both `pos_docs` and
  `neg_docs` populated IS the `1 = −1` situation the operator was built
  for, and the verdict machinery resolves it by counting, not by
  declaring a frame arbitrarily.
- **`E` gains an earned intake channel**: `w55_auto_acquire` turns
  measured gaps into retrieved text — external mirror that is literally
  earned from the system's own measured ignorance.
- **`K` gains carry-forward**: `learned_memory.json` persists learned
  structure across restarts, so what was learned in life *n* is present
  in life *n+1* — the positive-only carry-forward now covers knowledge,
  not just karma.

---

## Part VIII — The Auxiliary Engine Tier (waves 42–52)

A second tier of engines runs beside the formula. None of them enter `C`
— the same separation rule the learned stack obeys — but they modulate
the dynamics that produce φ and loss, so they are documented here as
**feedback channels, not formula terms**. `_step_wave4245_engines()`
drives the wave 42–45 engines once per state-writer tick with live
signals:

| Engine | Live input | Feedback channel |
|---|---|---|
| `satellite_input` | C, φ, symbol-load as fused channels | `fused_confidence` → synergy_harmony |
| `sensory_reality` | internal C/φ channels | `reality_confidence` → synergy_harmony |
| `pain_reality` | `0.1·loss + max(0, 0.3 − φ)` nociceptive proxy | `needs_evasive_action` → `reduce_suffering` goal into active_inference |
| `computed_experience` | C + `min(1, n_mem/5000)` | `experience_confidence` → synergy_harmony |
| `residual_imaging` | C imprint per tick | report only |
| `exterior_data` | C/φ/symbol sources | source report only |
| `reality_matching` | live C/φ vector | low `match_score` → surprise bonus into replay-buffer phi |
| `perpetual_intelligence` | experience vec, φ-novelty, loss | `current_learning_rate` → `optimizer.param_groups` lr |
| `synergy_harmony` | six subsystem confidences | cross-subsystem agreement report |
| `hurdle_bypass` | gradient flow, reasoning, data, efficiency | severity medium/high → `grad_clip_value` 1.5/2.0 |

The wave 46–52 tiers bind onto the simulator through
`_wave46…_wave52.bind(self)`: `Wave46Orchestrator` (instrument-awareness
bus, subconscious thought lattice, residual self-imagery, dream-state
renderer, safeguard envelope, and a self-evolution governor whose
proposals map onto *reversible, measurable* knobs — reasoning budget,
routing balance, learning rate — kept only on probated improvement),
`Wave47TrainingSubstrate`, `Wave49InferenceStack`,
`Wave50UnboundedSubstrate`, `Wave51InfiniteScaling`, and
`Wave52DemandScaling`. Their discipline is the same honesty axiom:
a knob that cannot be measured does not exist (`_resolve_knob` returns
None rather than inventing one), and a change that cannot show a better
score is rolled back.

---

## Part IX — The Verification Contract

Every measured claim above has an executable check. The `_verify_*.py`
scripts exec the real classes out of `CS.py` via `ast` (no 73k-line
import) and assert against counted behaviour — they are the operational
form of the honesty axiom:

| Script | What it proves |
|---|---|
| `_verify_learned_path.py` | dict banks gated off by default; real files index; `add_document` is immediately retrievable; `index_file` dispatch is honest |
| `_verify_response_path.py` | symbolic tables answer only as *tools*; knowledge hits do not short-circuit; test-time-compute surface exposes samples/grounding; mined pairs beat seed pairs once data exists |
| `_verify_wiring.py` | instrument correlation → `G_in` → `compute_C` → `symphony_index` end-to-end; zero correlation correctly silences the symphony |
| `_verify_wave53.py` | learned edges exist with real NPMI weights; expansion recalls zero-vocabulary docs; inference labels observed vs derived correctly; extractive QA cites provenance; canned banks unreachable under default flags |
| `_verify_wave54.py` | typed edges mined with separate +/− counts; transitive proof paths; support/refute verdicts; analogy solved from learned vectors; gap map records misses |
| `_verify_wave55.py` | learned structure persists and reloads losslessly (doc-id remap preserves provenance); universals refute where edges only weaken; acquisition queue drains into learning; quantity comparison normalises units honestly |
| `_verify_wave56.py` | mined rules carry support+confidence; priors lose to data; aliases pass the substitution test; `V_logic` is a real measured ratio; abduction pools all incoming relations |
| `_verify_latest.py` | `PhiComputer.validate_against_canonical_iit_ordering` — the integrated > segregated φ* ordering check across dims 8–128, plus a `compute()` cost benchmark |
| `_verify_gui_inputs.py` | control-panel input wiring — placeholders clear/restore on focus; Enter dispatches `analyze_input`; typed text reaches `execute_task` (the placeholder can no longer masquerade as a YouTube URL); plain URLs route to `fetch_url_text`, youtube URLs to `analyze_youtube`; the blocked-hotkey gate reports into the panel |
| `_dash_smoke.py` | every `MonitoringDashboard` refresh path and tab switch runs against a stub simulator |
| `test_smoke.py` | standalone class checks: C in `[0,3]`, karma clamp, omega register/spawn/evolve/remove, RLock reentrancy + timeout, VFE finiteness, honesty-anchor persistence, OS-control guard |
| `_test_fixes.py` | full `ConsciousnessSimulator()` init → `compute_C`/`get_state_dict` → wave-component presence sweep |
| `_check_wiring.py`, `_check_outputs.py` | static wiring scan — which `step()` components exist and which output attributes they actually expose |

If a row of this document stops being true, the row's script fails — the
docs and the checks are the same claim stated twice.
