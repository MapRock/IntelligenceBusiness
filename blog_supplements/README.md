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

## Eliciting Creative Questions from AI

These experiments extend [Abductive Calculation](https://eugeneasahara.com/2026/11/04/abductive-calculation/) by exploring whether an LLM can be prompted to discover creative questions rather than simply answer questions presented to it. The premise is that creativity often arises through analogy—recognizing relationships from other experiences and applying them to a new problem. Given the enormous breadth of knowledge represented in LLMs, they potentially have an extraordinary pool of inspiration from which to draw.

The experiments follow three steps:

1. **First iteration — Simple prompting:** Ask Grok to generate 30 questions, including creative ones, to estimate the number of books in my home office. The results were largely conventional.
2. **Developing a structured prompt:** Work with ChatGPT to design instructions encouraging exploration of alternative explanations, non-obvious relationships, and competing hypotheses.
3. **Second iteration — Structured prompting:** Give Grok the same problem using the improved prompt. The resulting questions explored a broader range of relationships, including ones that could have exposed errors in its earlier estimates.

The objective is not simply to generate more questions, but to discover **questions that open new investigative paths**. The comparison illustrates how prompting can influence exploratory reasoning, while leaving open whether those questions ultimately improve the accuracy of the resulting estimates.

### [Grok — Asking 30 Questions, First Iteration](https://github.com/MapRock/IntelligenceBusiness/blob/main/blog_supplements/grok_ask_30_questions_1.md)

The first experiment asked Grok 4.7 to generate 30 questions that would help estimate the number of physical books in my home office. The instruction was deliberately simple: ask 30 questions, including some creative ones, before attempting an estimate. Grok produced a reasonable questionnaire, but most questions focused on obvious measurements and direct proxies, such as shelf dimensions, bookcase counts, storage capacity, and purchasing habits. Although some questions explored less direct indicators, the result largely demonstrated conventional information gathering rather than the discovery of unexpected relationships.

### [Creative Question Generation — The Structured Prompt](https://github.com/MapRock/IntelligenceBusiness/commit/b6a67d66240d8089ee0b49bed4cb672269e7e6f1)

Following the first experiment, I worked with ChatGPT to develop a more deliberate prompt for eliciting creative questions from an LLM. Rather than merely requesting creativity, the prompt instructs the model to explore multiple possible explanations, investigate less obvious relationships, challenge assumptions, and identify questions capable of separating competing hypotheses. It also requires an explanation of why each question was selected and how different answers might affect the eventual estimate. The objective is to encourage broader exploration before committing to a calculational approach.

### [Grok — Asking 30 Creative Questions, Second Iteration](https://github.com/MapRock/IntelligenceBusiness/blob/main/blog_supplements/grok_ask_30_creative_questions.md)

The second experiment presented Grok 4.7 with the same home-office book-count problem, this time using the structured creative-question prompt. The result was substantially more exploratory. In addition to physical capacity, Grok investigated historical accumulation, book retention, digital substitution, professional needs, household influences, and other indirect relationships. Importantly, it raised questions about whether current digital reading habits accurately reflect a physical collection accumulated over decades—the very assumption that had misled its earlier estimation attempts. Not every question was particularly creative, and no subsequent estimate was tested, but the comparison illustrates how more deliberate prompting can elicit a broader and potentially more revealing investigation. The two iterations provide a concrete starting point for studying creative question generation as a component of Abductive Calculation.

## About the material

The transcripts and model responses are presented as records of exploratory tests. Numerical estimates, inferred relationships, and claims made by the AI systems should be treated as provisional unless independently verified. The broader research question is whether **preserving how a problem was approached—including unsuccessful hypotheses and missed questions—can improve reasoning on future problems**.
