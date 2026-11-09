---
number: 5
title: HumeBot: Experimental Evaluation, Frontier Models and Efficiency
subtitle: What the project's experiments have established about the reliability, interpretive quality and practical costs of its evidence-based approach
short: Experimental Evaluation, Frontier Models and Efficiency
audience: Philosophers, educators and AI researchers
version: 0.2 — Review draft
date: 8 November 2026
status: Research findings on development and held-out material; no configuration is qualified for student use; no learning outcome has been studied.
pdf: HumeBot_Report_5_Experimental_Evaluation_Frontier_Models_and_Efficiency_v0_2_review_draft.pdf
draft: false
---

<div class="box" markdown="1">
<p class="label">About this report</p>
<dl>
<div><dt>Central question</dt><dd>What has HumeBot's evaluation established about the reliability, interpretive quality and practical costs of its evidence-based approach to philosophical AI?</dd></div>
<div><dt>Audience</dt><dd>Philosophers, educators and AI researchers who have not followed the project's development. This is the collection's principal quantitative report; Reports 2 and 4 draw on it, and Report 1 describes the system evaluated.</dd></div>
<div><dt>Evidence and scope</dt><dd>The project's evaluation studies from September to November 2026: the harness comparisons and held-out study with an open-weight model, the model comparisons, the development diagnostics on the University's research computing, the formal qualification attempt, the frontier-model comparisons, the synthesis and instructor-guidance experiments, and the cost and efficiency analyses. Every figure is taken from the study's own closure or results record and was checked against the repository on 8 November 2026.</dd></div>
<div><dt>Status</dt><dd>All results come from development or held-out material, with small samples, mostly judged by AI reviewers. No configuration is qualified or accepted for student use; no student has used the system; no learning outcome has been studied.</dd></div>
</dl>
</div>

## The questions the experiments address

HumeBot's design involves three things that the evidence treats differently. The first is a textual guarantee that has been mechanically established: that a software harness around a language model makes the model's explanations of Hume *accountable to the text*, with every quotation exact, every citation real and located, every interpretive sentence tied to displayed evidence, and nothing shown that fails those checks. The second is an interpretive benefit that has been investigated but not proven: that explanations produced this way are also good, faithful to Hume's arguments and alert to his qualifications. The third is an educational benefit that has not yet been tested with students at all. The project's evaluations have therefore had to keep three dimensions apart.

**Textual reliability** concerns facts about the text: whether displayed quotations are exact, whether citations resolve to real locations, whether every claim can be traced to supplied evidence, and whether the system withholds rather than delivers when a check fails. These properties can be measured mechanically and, where the architecture guarantees them, they hold by construction.

**Interpretive quality** concerns whether an explanation represents Hume's argument faithfully: whether it preserves his distinctions and qualifications, states his conclusions with the modality he gave them, relates passages correctly and omits nothing important. No mechanical check can establish this; it is a matter of philosophical judgment, and the question of *whose* judgment runs through every result below.

**Practical performance** concerns whether the system delivers an answer at all under its strict contract, at what cost and speed, and whether it could be useful in a course.

Success in one dimension does not establish success in another. A system can cite the right words and misunderstand them; it can be interpretively excellent and deliver nothing because a single quoted phrase failed verification; it can be reliable, faithful and far too slow or costly to use. The state of the evidence differs across the three. The first dimension has been **mechanically established**: the harness's textual guarantees hold in every case checked, by construction. The second has been **investigated without demonstrating improvement**: repeated comparisons have measured interpretive quality, found the harness no better than direct prompting, and found no tested change that reliably improved it. The third is **untested with students**: costs and speeds have been measured for particular configurations, and nothing has been measured in a classroom.

<div class="box" markdown="1">
<p class="label">Mechanically established, investigated, untested</p>
<p><strong>Mechanically established.</strong> Inside the harness, constructed citations were exact and located in every case checked, across more than a thousand citations, two open-weight models and one frontier model. The open-weight models prompted directly, with the same text, produced faulty citations that nothing in their responses revealed; the frontier model's direct citations were exact in the sample reported. Fail-closed verification withholds answers rather than delivering faults, at a measured cost in delivery that rises steeply for less reliable models. The citation guarantee holds by construction and does not depend on the model.</p>
<p><strong>Investigated, not demonstrated.</strong> Whether the harness improves interpretive quality: in the comparisons made it did not, and with a frontier model a blinded AI reviewer more often preferred the direct form of explanation on pedagogical grounds. Whether any tested change improves faithfulness to Hume's qualifications and provisional conclusions: none did reliably. Whether any configuration meets the project's standard for students: the one formal qualification attempt stopped before scholarly review.</p>
<p><strong>Untested.</strong> Whether students learn better, find the answers useful, or tolerate the cost and the wait: no student has used the system, and nothing has been measured under classroom conditions.</p>
</div>

## How HumeBot was evaluated

The project's experiments share a small set of methods, and a reader needs four distinctions to weigh them.

**Development material versus held-out material.** Most studies used *development* questions: questions the project had seen, used to find and fix failures. Results on development material are diagnostic, not estimates of performance. Two studies used *held-out* questions, written in isolation and sealed until use: a 60-question generalization study in September 2026 and the 170-question set of the formal qualification attempt in October, which was spent without reaching review. A held-out question, once used, is used; this is why the project's qualification sets are treated as a scarce resource.

**Controlled comparison.** The central design throughout was the same model, the same questions and the same frozen protocol, with one thing varied: the harness against direct prompting; one model against another; one prompt, context or evidence route against another. Protocols, question sets and prompts were frozen and hashed before the first call, and where reviewers judged outputs the arm labels were hidden from them until every judgment was recorded.

**Who judged.** Textual reliability was measured by software. Interpretive quality was judged, in nearly every study, by AI reviewers: Claude models in the September studies, ChatGPT in the frontier comparisons and the November experiments, with reviewer identities recorded in each study. The faculty lead adjudicated escalated cases, audited a sample of nine answer pairs in the held-out study, adjudicated the disputed grades of the development diagnostics, and served as sole adjudicator of the early evidence-use study. No study was reviewed by an independent philosopher, and the project's own calibration found AI review less stable than its confident tone suggests (section 5). **Where this report says a result "was preferred" or "showed no winner," it reports an AI reviewer's judgment, not a scholarly finding.**

**Development research versus formal qualification.** Every study below except one is development research: exploratory, small, and never intended to qualify anything. The exception is the Instructional Qualification attempt of October 2026, designed in advance with frozen thresholds and a scholarly review, which stopped at its evidence gate (section 7). Throughout, proportions from samples of 24 or 60 questions are reported as what they are, counts in a sample, not population error rates, and most figures come from a single run.

<p class="caption"><strong>Table 1.</strong> The principal studies. AI = AI reviewer; PI = faculty lead. Development questions unless marked held-out.</p>

| Study (date) | Design and size | Judged by | What it established |
|---|---|---|---|
| Epistemic-harness pilot (Sept 2026) | 8 held-out questions × 4 arms, open-weight model | AI; PI partial | Direct prompting misquoted 29 of 86 quoted strings; constructed-citation arms none; length confounded ratings |
| Native harness comparison (Sept 2026) | 24 questions, harness vs direct prompting, Gemma 4 31B | 2 AI, blinded; PI on escalations | Direct: 12 faulty citations of 51, undetected; harness: 0 of 89, 22 of 24 delivered; no interpretive winner |
| Locator ablation and repeatability (Sept 2026) | 24 questions × 2 prompts; 3 repetitions × 24 × 3 arms | software | Revised prompt removed invented locators; direct exactness 86–92%; harness 250 citations, 0 faults, 21–22 of 24 delivered |
| Held-out generalization (Sept 2026) | 60 new questions (48 answerable, 12 boundary), harness vs revised direct prompt | 2 AI, blinded; PI audit of 9 pairs | Harness 238 citations, 0 faults, 50 of 60 delivered; direct 12 faulty of 107; false abstention 2 of 48 |
| Model comparison (Sept 2026) | Same 24 questions, Gemma vs gpt-oss-120b, both arms | 2 AI, blinded | Richer when direct but 83% of citations faulty; in the harness delivered 12 of 24 |
| MSI development diagnostics (Oct 2026) | 36 development questions; selector, prompt and writer variants | development grader; PI adjudicated disputes | Serious errors concern scope and qualification; selector information and a larger writer reduced omissions, not those errors |
| Instructional Qualification 0.1 (Oct 2026) | 170 held-out questions, frozen thresholds, 230 conditions | gate; review never reached | Not eligible at the evidence gate; neither pass nor fail; set spent |
| Frontier pilot and comparison (Oct 2026) | 5 hard questions; then 20 questions, 40 pairs; Opus 5.5 in and out of the harness | 1–2 AI (ChatGPT), blinded | Citations exact in and out; no fidelity gain; direct form preferred on pedagogy; length confounded |
| Three-arm evidence routes (Nov 2026) | 7 questions × 2, three evidence routes, Opus | 1 AI, advisory; PI decision | No route better overall; baseline retained |
| Synthesis and instructor-guidance experiments (Oct–Nov 2026) | 1–12 questions each, Opus; format, context, inference, length, course guidance | 1 AI, advisory; PI rulings | No advance from any tested change; one recurring omission persisted; guided answers more often withheld |

## What the open-weight experiments established

### The difference between asking for accuracy and enforcing it

The project's first controlled study, in September 2026, ran four frozen arms over eight held-out questions with an open-weight model. The conventional arm, a capable model asked to answer and quote, misquoted 29 of its 86 quoted strings, one in three; the three arms that declared or constructed their citations misquoted none. The pilot also found what would complicate every later interpretive comparison: answer length varied five- to sevenfold across arms, and the AI judge's ratings tracked length. The planned human rating of every response was abandoned as too burdensome for a diagnostic pilot.

The **native comparison** that followed is the project's cleanest result. Twenty-four development questions were answered twice by the same open-weight model, Gemma 4 31B, at the same settings: once by a carefully structured prompt holding the whole 216-unit corpus and asked to quote and cite exactly, and once through the harness. The direct arm produced 51 citations, of which 12 were faulty, 8 quotations absent from the passage cited and 4 references to locations in an identifier scheme the corpus does not use, spread across 11 of the 24 questions; none was detected, and all would have reached a reader as quotations of Hume. The harness produced 89 citations with no fault. The difference is not that the model behaved better inside the harness. Twice the model made the same kind of error inside it, a support phrase with no exact occurrence in the unit it named, and twice the answer was withheld: 22 of 24 delivered. **The harness makes misquotation detectable and fail-closed; direct prompting makes it invisible.** On interpretive quality the two blinded AI reviewers found no winner, and the project recorded that the comparison "establishes nothing" on that dimension: the harness's two withheld answers drew the lowest ratings, a residual length difference ran the other way from the pilot's, and 24 questions were never powered to separate the arms.

Two follow-up studies tested the comparator and the stability of the result. A revised direct prompt removed the invented locators entirely (3 of 48 under the original prompt, 0 of 37 under the revision) without changing quotation exactness (85.4 against 86.5 percent). Three fresh repetitions of the whole design, 216 answer conditions, found the direct prompt's exactness between 85.7 and 91.7 percent across runs and no invalid locators in 107 citations, while the harness produced 250 citations with no fault and delivered 21 or 22 of 24 in each run. The failure types were stable across runs; the particular questions that failed were not, which is why the project tracks failure types rather than question lists.

### Does it hold on new questions?

The **held-out generalization study** asked whether these properties survived on 60 questions the project had never seen, 48 answerable and 12 testing the system's limits, with the revised direct prompt as comparator. The harness constructed 238 citations, every one exact, valid and drawn from the evidence supplied for its answer, and delivered 50 of the 60; of the 48 answerable questions it wrongly abstained on 2, both of which it nonetheless answered in part. The direct comparator delivered 59 of 60 and quoted exactly 96 times in 107, inside the band the repeatability study had measured.

The comparator's faulty citations deserve a precise statement, because the study's closeout summed two overlapping categories (11 quotations absent from the corpus and 12 not found in the cited unit) to a total of 23. The study's per-citation measures resolve the overlap: of the comparator's 107 citations, **12 were faulty, across 9 of 60 questions**. Eleven contained quotations absent from the corpus; one quoted Hume accurately but cited the wrong unit. Every one would have reached a reader as a quotation of Hume at a location. The harness produced none.

### A less reliable model

A larger open-weight model, `gpt-oss-120b`, run on the same 24 questions and protocol, showed the other face of fail-closed verification. Prompted directly it had, in the blinded AI reviewers' judgment, the richest interpretive profile of any configuration, and it overclaimed more; 83 percent of its declared citations were faulty. Inside the harness it delivered 12 of 24 answers. The harness contained the model's unreliability completely, and the price was half the questions. **Fail-closed verification trades delivery for reliability**, and the exchange rate depends on the model: two answers in 24 and ten in 60 for Gemma; twelve in 24 for a model that cannot quote.

<p class="caption"><strong>Table 2.</strong> Citation reliability inside and outside the harness. Counts in the samples studied, not population rates.</p>

| Study | Configuration | Citations checked | Faulty | Delivered |
|---|---|---|---|---|
| Native comparison | Gemma, direct prompt | 51 | 12 (undetected) | 24 of 24 |
| Native comparison | Gemma, harness | 89 | 0 | 22 of 24 |
| Repeatability (3 runs) | Gemma, revised direct prompt | 107 locators; quotations 85.7–91.7% exact | 0 invalid locators | 24 of 24 |
| Repeatability (3 runs) | Gemma, harness | 250 | 0 | 21–22 of 24 per run |
| Held-out generalization | Gemma, revised direct prompt | 107 | 12 (11 not in the corpus; 1 in the wrong unit) | 59 of 60 |
| Held-out generalization | Gemma, harness | 238 | 0 | 50 of 60 |
| Model comparison | gpt-oss-120b, direct prompt | 118 declared | 98 (83%) | 24 of 24 |
| Model comparison | gpt-oss-120b, harness | — | 0 | 12 of 24 |
| Frontier comparison | Claude Opus 5.5, harness | 442 | 0 | 20 of 20 |
| Frontier comparison | Claude Opus 5.5, direct prompt | 214 | 0 | 15 of 20 usable |

## What the frontier-model experiments established

In late October 2026 the project ran its unchanged prompts on a frontier model, Claude Opus 5.5, through its provider's service, in two studies judged by blinded ChatGPT sessions. The settings differed from the frozen candidate's (no fixed temperature, no JSON mode, a much larger output budget, a high reasoning-effort setting), so the project records every result as a *frontier experimental configuration*, not a run of the candidate.

The **frontier pilot** used five questions chosen because Gemma had struggled with them. Every usable frontier answer, in or out of the harness, reached the reviewer's top tier; none of Gemma's did; and the frontier model's 236 checked quotations contained no fault. The sample was chosen to probe weaknesses, so it shows where the open-weight model falls short, not by how much, and the ratings sat at a ceiling.

The **frontier comparison** used 20 previously used questions and three arms: the full harness (F-H), the same model writing directly from the harness's own evidence packet (F-P), and the model prompted directly with the whole corpus (F-D), compared in 40 pairs by two blinded sessions. Three results matter.

**Evidence integrity held everywhere.** The harness's 442 citations were exact, as the architecture guarantees. But so were the direct arms' 278 and 214: in this sample the frontier model quoted exactly without any harness. The harness's most clearly demonstrated benefit with the open-weight model, catching misquotation, had nothing to catch.

**No fidelity gain.** On fidelity to Hume's text the reviewers preferred the harness in none of the five non-tied pairs against direct prompting, a difference short of significance (*p* = 0.063), and found no difference against the packet arm (*p* = 1.00); the project records the hoped-for fidelity gain as "not supported." Direct prompting also failed to produce a usable answer on 5 of the 20 questions, a reminder that the harness's structured path delivers more consistently than an unconstrained prompt even when both quote exactly.

**The reviewers preferred the direct form on pedagogy.** On pedagogical quality the reviewers preferred the harness's answers in 0 of 13 decided pairs against direct prompting (*p* = 0.0002) and in 3 of 19 against the packet arm (*p* = 0.004): the frozen synthesis format, a numbered sequence of short anchored sentences, was judged less helpful to a student than connected prose written from the same evidence. The result comes with three cautions the project states itself. Arm and answer length were perfectly confounded, since the harness's format is shorter by construction, and length is known to drive AI ratings. The judgments were one AI reviewer's family, in two sessions, and the two disagreed on one serious-error flag. And twenty questions, already used in development, support a direction, not a measurement.

What the project learned is best put as a shift in what the harness is for. With a model that misquotes, the harness earns its keep by catching faults. With a model that does not, its value lies in what it still provides that a direct answer cannot: a system-built text the student reads whole, sentence-level anchors the student can open, a typed separation of text from interpretation, an instructor's view of what was supplied and selected, and the refusal to deliver anything unverified. Those are properties of accountability, not of quality, and the comparison made the distinction impossible to blur. It also left the project with a cost: the harness's synthesis format, required for anchoring, was the arm the reviewer liked least, and the project's rule is that a normatively required component that costs quality stays, with the cost reported. The November synthesis experiments (section 5) were the attempt to reduce that cost within the requirement.

## Interpretation, omissions and philosophical fidelity

A model can cite the right words and still misunderstand their argumentative significance. This is the problem the project's evaluation kept returning to, and the one no intervention has yet solved.

**What the September studies found.** In the native comparison, the blinded reviewers' interpretive ratings separated nothing. In the held-out study the faculty lead audited nine answer pairs, blind to arm: both answers were acceptable in five; in two cases the harness's answer fell short on substance, omitting something important, and in one the direct answer failed to deliver. The AI reviewer had not noticed either omission. A random re-review of 24 cases found that about 27 percent of the individual fields the AI reviewers had rated changed on a second pass, and that 2 of the 24 cases differed materially. The project drew the consequence: AI review is triage, not validation, and human scholarly sampling stays in every design.

**Where the open-weight system fails.** The October development diagnostics on the University's research computing graded a 36-question development set answer by answer. Of 35 delivered answers, 16 had no material problem, 15 had a material problem, and 4 contained a serious scholarly error. The serious errors were of one kind: overstating the scope or finality of a claim Hume made conditionally or provisionally. Two changes reduced the material problems, showing the evidence selector the student's question (21 adequate, 13 material, 1 serious) and replacing the writer with a far larger open-weight model on the same evidence (25, 9 and 1); neither removed the remaining serious error, and the record's conclusion is exact: capacity "repaired evidence-use omissions, not the scope errors around conditional or interim claims." Report 4 gives the detail. The grades were a single development grader's, not blind to condition, with the faculty lead adjudicating the disputed cases; they are diagnostic, not a measurement.

**Relations between passages.** A second recurring limit appeared first in the native comparison and has not gone away. Asked something that turns on the *relation* between two passages, the harness may select exactly the right two and still mark the requirement unresolved, because no single passage states the relation; on the principal example the pipeline chose the same two passages a scholar later chose, and then abstained. The selector found evidence for 61 of 63 requirements in that study; the two it did not were of this kind. Deterministic verification can confirm that each passage is cited exactly. It has no way to confirm that two passages, read together, establish what an explanation says they do.

**The November synthesis experiments.** With the frontier model, the project tried to improve the harness's explanations within its invariants, one change at a time, on development questions, each judged by a single advisory AI reader (ChatGPT, GPT-6) with the faculty lead ruling on disputed items. A connected-prose format against the frozen sentence format: no format winner (7 questions, two replicates, 26 valid answers). Expanded context for the writer, revised synthesis instructions, and both together: neither showed a consistent advantage (35 cells, 33 valid), and one omission of an argumentative step, in a question about the problem of induction, appeared in every one of the five conditions. An explicit instruction to make inferential connections intelligible: the missing step did not appear in either condition (0 of 4 and 0 of 4), a result the project records as unresolved pending the faculty lead's ruling on the underlying finding. Relaxing the ceiling on the number of sentences, with length controlled: no advance for any of three variants across 12 questions (60 calls, 57 delivered), with the project cautioning that "no advance" is not evidence that the constraint has no effect. A three-way comparison of evidence routes, the frozen three-stage baseline against a single read-and-write call over the whole corpus and against run-level evidence selection: 40 of 42 answers delivered, no route better overall, the baseline retained and one route preserved for possible refinement. In every case the AI reader rated most answers at or near the ceiling, so that the experiments could detect only large effects; none appeared.

**Instructor guidance.** Three small experiments, run under a bounded exception to the rule that the writer sees only selected evidence, supplied the faculty lead's own course guidance or objectives to the model. Guidance changed the framing, attribution and form of the explanations and how the first stage decomposed the question; it did not produce a reliable improvement, and in one experiment the longer guided answers were more often withheld at the length limits (2 of 4 complete against 4 of 4). The faculty lead closed the line with a decision that instructor materials are, for now, to be displayed beside HumeBot's readings, not supplied to generation (Report 2). A further pilot in which two AI readers challenged each other's assessments with exact textual evidence found the challenges useful but the revisions they prompted not reliably better; the exchange is retained as an optional research instrument.

**The limit of deterministic verification.** Every one of these results points at the same boundary. Software can establish that a quotation is Hume's and where it stands. It cannot establish that a sentence reads the quotation rightly, that an argument has been reconstructed with its steps intact, that a conditional has stayed conditional, or that the passage a reading leaves out would have changed it. The project's design says this to every student in the two verdicts shown for each sentence, *source and location verified*, *interpretation not verified as correct*, and its experiments have borne the design out: the first verdict has never been wrong in any case checked, and the second names the dimension on which every tested improvement has so far failed to register.

## Cost, efficiency and practical viability

The project's cost figures are measurements of particular configurations, and the distinction between a measurement, a projection and an unexecuted plan is kept throughout.

**Measured.** In the frontier comparison, a harness answer with Claude Opus 5.5 cost about **$0.50** in API charges at list price and took **66 seconds** at the median (90 seconds at most) across 20 answers. The structure of that cost is the structure of the pipeline: evidence selection reads the entire corpus on every question, so the selector's prompt is 88 to 93 percent of all input tokens in every configuration measured, and with Opus the selector's input alone accounted for $0.31 of the $0.50; the writer's stage accounted for 19 percent, and output tokens, about half of them the model's reasoning, for 30 percent. The open-weight configurations carried no per-token charge; their median times on the research services ranged from about 18 to 34 seconds per harness answer and about 6 to 15 seconds for the direct prompt. In the three-arm comparison with Opus, a delivered answer cost $0.43 by the single-call route and $0.56 by run-level selection, against $0.11 for the baseline's writer stage alone.

**Analysed, not measured.** Because the selector's prompt is the corpus, it is almost identical from one question to the next: rebuilding the exact prompts from recorded runs showed 99.5 to 99.6 percent of the selector's characters unchanged. Providers price the reuse of an identical prompt prefix at a fraction of ordinary input, so caching is available without changing a prompt; the saving it would yield has not been measured, and no caching run has been made. An offline analysis of November 2026 asked what a hybrid evidence-selection strategy would save: supplying the selector with the relevant section plus a dozen retrieved passages, instead of the whole corpus, would cut its input by about three fifths on the frontier configuration, while recovering 90 percent of the passages the full-corpus selector had chosen and leaving 13 of 25 answers' evidence complete; the losses fell on passages that link one section's argument to another's. The analysis used a lexical stand-in for retrieval and made no model call; the project judged a live comparison not warranted now.

**Prepared, not executed.** A screen comparing the frontier model against a smaller model of the same family on 12 questions, with a spending cap and stop rules, is prepared and has made no paid call.

**What this means practically.** At the measured rates, a course in which students asked a thousand questions would incur about $500 in API charges and each student would wait about a minute for an answer; both figures belong to one configuration and one provider's list price, and neither has been measured under classroom load. Whether a minute is acceptable, whether the cost is, and whether students find the answers useful are questions no experiment has asked: the system has never been used by a student. Delivery rates are the one practical figure the evaluations do speak to, and they are the mirror of reliability: 22 of 24 and 50 of 60 for the open-weight model in the harness, 20 of 20 for the frontier model, 12 of 24 for a model that cannot quote.

## What the evaluations justify

### Established

The harness's textual guarantees hold, by construction and across models: every citation it constructed was exact and located, for an open-weight model, a frontier model, and a model so unreliable that it answered only half the questions. Fail-closed verification withholds rather than delivers faults, at a cost in delivery that is small for reliable models and large for unreliable ones. And the project's instruments, frozen protocols, blinded review, held-out sets and a qualification design with pre-set thresholds, work as designed, including by refusing to proceed.

### Observed limitations

Interpretive quality has not been shown to benefit from the harness, and the open-weight system's serious errors, which concern the scope and finality of Hume's claims, survived every tested change in the samples tried. The harness cannot resolve requirements that turn on the relation between passages, and the synthesis format that anchoring requires was judged less helpful than connected prose. The evidence about interpretation rests almost entirely on AI reviewers whose ratings proved unstable on re-review and who missed omissions a scholar caught.

### Exploratory findings

Showing the evidence selector the student's question reduced serious errors in the development set and is a candidate for a future successor through the full freeze-and-qualify discipline; a larger writer reduces omissions; cost is dominated by evidence selection and is largely cacheable; a hybrid retrieval strategy would trade evidence completeness for cost and is not yet worth a live test. The first two rest on development grades adjudicated by the faculty lead; the cost and caching observations are measurements of recorded usage; the hybrid analysis is offline, with no model call.

### The qualification attempt

The project's one formal attempt to qualify a configuration for students was designed before any question was written: 170 held-out questions, thresholds of at least 85 percent verified delivery, under 10 percent false abstention, under 5 percent serious scholarly error and under 10 percent material omission, each decided by a one-sided 95 percent confidence rule, and a blinded scholarly review. It was executed in full on the University's research computing in October 2026. Its post-run evidence gate returned *not eligible*: one condition had invoked an exception under a rule that had never been adopted, and the frozen procedure did not allow the review to proceed. The attempt was closed as terminal. No scholarly review was performed, no pass or fail exists, and the 170 questions are spent. A redesigned attempt exists only as a plan and would need a fresh set of about the same size. **No configuration of HumeBot is qualified for student use.**

### Questions that require further study

Whether faithfulness to Hume's qualifications can be improved by any means short of expert feedback, and whether such feedback can be collected at a useful scale under University governance. Whether comparative requirements can be met by a representation of evidence that admits relations between passages. How far AI review can be relied on, and for what, given its measured instability and the omissions it missed. Whether the harness's accountability properties, which the frontier comparison isolated from its fault-catching, are worth their cost to a student, which only a classroom study could show. What the system costs and how it performs under real load. And, before all of these for any classroom use, whether a fresh qualification set can be authored and a configuration can pass it.

<div class="keep" markdown="1">
## Conclusion {: .unnumbered }

HumeBot's evaluations have established one thing firmly and failed to establish another, and the project's credibility rests on saying both. The firm result is textual: inside the harness, every citation checked in every study was exact and located, while the open-weight models prompted directly produced faulty citations that nothing revealed and a frontier model, in the sample tested, did not need the harness to quote exactly; the guarantee holds by construction, transfers across models, and, in the configurations tested, withheld few answers from a reliable model and many from an unreliable one. The unestablished result is interpretive: no tested change in model, prompt, context, length, evidence route or instructor guidance reliably improved faithfulness to Hume's arguments and qualifications, the harness has not been shown to interpret Hume better than direct prompting, and with a frontier model a blinded AI reviewer preferred the direct form of explanation on pedagogical grounds. The one formal qualification attempt stopped before scholarly review; no configuration is qualified for students, and no student has used the system. What the evaluations justify is the design's central distinction, now measured rather than asserted: the text can be made reliable by software, and the reading cannot.
</div>

## Sources and document status {: .unnumbered }

<ul class="sources">
<li>September 2026: epistemic-harness pilot 0.1.2 closeout; native harness comparison (engineering conclusions, unblinding record); locator-schema ablation and Gemma repeatability findings; held-out generalization closeout, analysis, per-citation measures, reviewer-calibration analysis and the faculty lead's audit; model comparison 0.1 analysis.</li>
<li>October 2026: MSI development baseline, ablation, successor and capacity reports; Instructional Qualification 0.1 decision record and strategic directions §15.1; frontier pilot 0.1 and comparison 0.2 (protocols, freeze records, unblinded assessments) and strategic directions §15.4; cost and efficiency baseline; cost–quality Stage 1 preflight (not executed).</li>
<li>November 2026: three-arm comparison decision report and the faculty lead's decision; format pilot 0.3 closeout; context-synthesis pilot record; inference-aware synthesis comparison; sentence-ceiling results and closure; the instructor-guidance experiments and their closure; review-harness live pilot 1 closure; evidence-context comparison 0.1 (offline).</li>
<li>Constitutional document §2 and §4 (epistemic constraint is not evidence of interpretive benefit); Report 1 for the system evaluated.</li>
</ul>

<p class="small"><strong>Document status.</strong> Version 0.2, review draft of 8 November 2026, prepared for the faculty lead's review. A faculty-led project report of the University of Minnesota Morris; not an official University publication and not University policy. No configuration is qualified for student use; no learning outcome has been studied.</p>
