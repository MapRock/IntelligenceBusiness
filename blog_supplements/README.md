# Blog Supplements — Enterprise Intelligence

This directory contains supplementary material for articles on [eugeneasahara.com](https://eugeneasahara.com/) concerning **Enterprise Intelligence**, the integration of business intelligence, knowledge graphs, AI, and other reasoning methods. The broader foundation is described in my book, [*Enterprise Intelligence: Bridging the Gaps between Wisdom, Business Intelligence, Knowledge Graphs, and Artificial Intelligence*](https://technicspub.com/enterprise-intelligence/), published by Technics Publications.

The supplements preserve experiments, AI-generated responses, and prompts that would be cumbersome to reproduce in full within a blog article. They make it possible to examine the reasoning paths, assumptions, and limitations behind the examples rather than relying only on a summary of the results.

## Abductive Calculation: Reasoning with Imperfect Information

The files currently documented here accompany my article **“Abductive Calculation: Reasoning with Imperfect Information.”** The article considers how an intelligence system can estimate a quantity that is not directly known and for which no predefined calculation may exist. It examines Fermi estimation, reasoning by analogy, provisional relationships, multiple estimation paths, and the importance of keeping hypotheses separate from established facts.

These examples are **reasoning experiments, not verified measurements**. Their purpose is to expose how an AI approaches an unfamiliar question, including where its assumptions succeed, fail, or change as additional information becomes available.

### [Gemini — Fermi Estimation of Inari Makers in Greater Boise](https://github.com/MapRock/IntelligenceBusiness/blob/main/blog_supplements/gemini_fermi.md)

Google Gemini's response to a deliberately obscure question: how many people in the greater Boise area might make inari on a particular day? The transcript shows its Fermi-style decomposition into population, likely participation, cooking frequency, and ingredient availability, with a proposed estimate and supporting assumptions.

### [Grok — Fermi Estimation of Inari Makers in Greater Boise](https://github.com/MapRock/IntelligenceBusiness/blob/main/blog_supplements/grok_fermi.md)

Grok's response to the same inari question. It explains why the problem calls for a Fermi estimate and builds a rough answer from population, demographics, food preparation habits, and possible restaurant activity. The two inari files allow readers to compare how different models construct estimates from an answer that is not available for direct lookup.

### [Grok — Estimating the Books in My Home Office](https://github.com/MapRock/IntelligenceBusiness/blob/main/blog_supplements/grok_books_in_my_home_office.md)

An extended experiment in which Grok was asked to estimate the number of physical books on my home-office shelves using limited information. It initially declined to estimate because no direct public answer was available. Once prompted to use Fermi estimation, it produced a reasonable first approximation, but later clues about digital reading habits and book retention shifted its estimates away from the actual count of 300. The preserved exchange illustrates the dangers of over-weighting plausible clues, neglecting alternative explanations, and confusing current acquisition habits with an accumulated collection.

### [Abductive Calculation — A Reasoning Prompt](https://github.com/MapRock/IntelligenceBusiness/blob/main/blog_supplements/abductive_calculation_prompt.md)

I asked ChatGPT to write this prompt because I wanted it to tell me **what instructions would help it perform this kind of reasoning**. The request arose from the experiments: rather than expecting a model to discover a suitable approach spontaneously, what guidance would help it brainstorm relevant factors, construct multiple possible explanations and calculational paths, examine shared assumptions, incorporate new clues without overreacting, and identify what additional information would reduce uncertainty? The file captures the model's proposed working instructions, not a claim that the prompt has been proven to improve every LLM or every estimation problem.

### [Grok — Home-Office Books Estimate Using the Abductive Calculation Prompt](https://github.com/MapRock/IntelligenceBusiness/blob/main/blog_supplements/grok_books_with_abductive_calculation_prompt.md)

A follow-up test of the **same home-office book-count question** with Grok 4.7 in a **fresh private browsing session**, this time supplying the Abductive Calculation prompt at the outset. Rather than stopping when no direct answer was available, Grok generated alternative stories and four calculational paths: room-and-shelving capacity, historical acquisition and retention, demographic proxies, and analogy to other knowledge workers. It explicitly considered shared assumptions and proposed additional observations that could reduce uncertainty.

Its central estimate was **100–150 books**, with a wider plausible range of **40–300**; the actual count was **300**. This is evidence of what the structured instructions elicited in this instance, not proof of improved accuracy or a controlled comparison: the supplied context and instructions differed from the earlier exchange.

**No prior reasoning episodes were provided to Grok**, so this tests prompting, not whether retrieving stored reasoning histories improves an LLM's estimates.

### [Grok — Initial 30 Questions for Estimating a Home-Office Book Collection](https://github.com/MapRock/IntelligenceBusiness/blob/main/blog_supplements/grok_ask_30_questions_1.md)

An initial experiment asking Grok 4.7 to generate 30 questions that could help estimate the number of physical books in my home office. The request encouraged creativity but provided no structured methodology. Grok produced a comprehensive set of questions, many focused on shelving dimensions, book density, storage arrangements, acquisition rates, and direct or indirect counting. Although reasonable, several questions approached the same underlying factors from slightly different directions. The experiment established a baseline for examining the difference between generating many questions and discovering genuinely different relationships that could influence an estimate.

### [Creative Question Generation — A Generalized 30-Question Prompt](https://github.com/MapRock/IntelligenceBusiness/blob/main/blog_supplements/abductive_calculation_30_creative_questions_prompt.md)

Following the initial experiment, I asked ChatGPT to formulate a domain-independent prompt designed to encourage broader exploration before selecting 30 questions. The prompt asks the model to consider alternative explanations, explore conceptual relationships, challenge assumptions, and identify questions that could expose important missing information. It deliberately avoids supplying domain-specific clues such as Kindle, historical book accumulation, or alternative storage. The objective is to investigate whether general instructions can elicit more imaginative and consequential questions without telling the model which factors to discover.

### [Grok — 30 Questions Using the Generalized Creative Prompt](https://github.com/MapRock/IntelligenceBusiness/blob/main/blog_supplements/grok_ask_30_creative_questions.md)

A follow-up experiment conducted in a fresh private Grok 4.7 session using the generalized prompt. The only problem-specific input was **“number of physical books in my home office.”** Grok again generated 30 questions, but this time explored a broader range of possible influences, including digital substitution, retention preferences, inherited collections, competing physical media, household circumstances, environmental constraints, and changes in ownership over time.

Of particular interest was Grok's identification of digital reading without being explicitly prompted to consider it, and its recognition that adopting digital formats does not necessarily imply disposing of existing physical books. The experiment suggests that generalized prompting can broaden the relationships an LLM considers without explicitly supplying the relevant factors. However, it does not establish that the questions improve the resulting numerical estimate or that the model has discovered fundamentally new relationships.

These experiments lead toward a larger question: how might an intelligence creatively discover relevant relationships, and how could insights from previous human or AI problem-solving experiences be generalized and reused when investigating entirely different problems?

## About the material

The transcripts and model responses are presented as records of exploratory tests. Numerical estimates, inferred relationships, and claims made by the AI systems should be treated as provisional unless independently verified. The broader research question is whether **preserving how a problem was approached—including unsuccessful hypotheses and missed questions—can improve reasoning on future problems**.
