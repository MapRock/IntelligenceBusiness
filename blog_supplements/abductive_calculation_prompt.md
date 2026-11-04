# Abductive Calculation: A Reasoning Prompt

I want you to estimate or infer something that may not be directly known, measured, or modeled.

**Question:** [Insert question]

**Available information:** [Insert any observations, clues, or constraints]

**Restrictions:** [Specify whether direct lookup of the answer is prohibited, what external information may be used, and any other constraints]

**Purpose:** [Optional: Explain the decision being supported and how accurate the answer needs to be]

Do not stop merely because the requested answer cannot be retrieved. Consider Fermi estimation, analogical reasoning, indirect measurement, and other means of constructing an answer from available information.

Approach the problem as a combination of an estimator, a detective, and a skeptical analyst.

### 1. Identify the unknown

Define exactly what is being estimated, its units, scope, and time frame. Determine whether it is a stock, a flow, a rate, a hidden state, or a hypothetical outcome. Identify what would count as an acceptable answer.

### 2. Brainstorm potentially relevant factors

Before estimating, identify a broad collection of factors that might influence the answer. Consider physical constraints, population, behavior, capacity, economics, historical accumulation, acquisition and disposal, available proxies, and unusual circumstances where relevant.

Distinguish **observed facts, retrieved facts, estimates, hypotheses, and unknowns**. Do not silently convert a plausible assumption into a fact.

Include factors that could push the answer higher as well as factors that could push it lower. Do not focus exclusively on the first plausible explanation.

### 3. Construct alternative stories

Like Sherlock Holmes reconstructing a person's circumstances from clues, construct several plausible explanations of how the observations could have arisen.

For each story, identify its essential assumptions, the observations it explains, what it would predict, and what would contradict it.

Do not treat an internally coherent story as necessarily true. Consider competing stories that explain the same observations differently.

### 4. Construct candidate calculational paths

Try to construct two to four materially different paths to the unknown, where defensible. Possibilities include Fermi decomposition, demand divided by capacity, representative-unit scaling, economic throughput, physical measurement, proxy relationships, inverse reasoning, and adaptation of previous reasoning episodes.

For each candidate path, identify its intermediate quantities, proposed relationships, assumptions, and sources of evidence. Explain briefly why the relationship is plausible.

Do not invent additional paths simply to meet a numerical target.

### 5. Calculate provisional estimates

Estimate the necessary inputs using available evidence and explicitly labeled assumptions.

Compute a plausible range for each path. Prioritize order-of-magnitude accuracy before precision. Show the calculations sufficiently clearly that their assumptions and arithmetic can be checked.

### 6. Compare and challenge the paths

Examine which paths depend on the same observations, estimates, or assumptions. Do not automatically count paths as independent merely because their calculations look different.

Investigate disagreements rather than automatically averaging the results.

Test sensitivity to consequential assumptions. Ask whether the models measure the same quantity, whether a proxy might be misleading, and whether an important factor was overlooked.

### 7. Incorporate new clues carefully

When additional information is supplied, identify which hypotheses and assumptions it actually affects.

Do not assume that every new clue must change the answer. Do not let an appealing new explanation displace stronger existing evidence without justification.

Preserve the previous estimates and explain why any revisions were made.

### 8. Determine what else would be worth knowing

Identify up to three additional observations or questions most likely to change the estimate or distinguish competing explanations.

Explain what each possible answer would imply. If direct measurement is practical and preferable, say so.

### 9. Report the result

Provide a concise summary showing the candidate reasoning paths, their estimates, shared dependencies, major uncertainties, and the resulting plausible range.

Give a central estimate only when justified. State whether the estimate is sufficient for the stated purpose.

If the evidence supports only a broad order of magnitude, report that rather than inventing precision.

### 10. Learn from previous reasoning

If prior reasoning episodes are provided, use them as possible strategies, not as answers to copy. Identify what structure might transfer, what circumstances differ, and which previous assumptions failed.

If the actual answer later becomes available, compare it with the estimate. Preserve both successful reasoning patterns and failure modes for possible reuse.

**Governing principle:** Generate hypotheses broadly enough to discover unexpected relationships, but retain the ability to explain, challenge, revise, and reject them. Never confuse what is known with what is merely plausible.
