# Cross-Domain Knowledge: Four Complementary Paths to Creative Questions

*Supplement to [Eliciting Creative Questions from AI for Abductive Calculation](https://eugeneasahara.com/).*

The accompanying four illustrations examine **how knowledge from different domains becomes connected**. Cross-domain thinking is one source of creative questions: a relationship familiar in one setting may suggest a question, explanation, or calculational pathway in another. But the four approaches do not acquire, organize, or connect knowledge in the same way. Their differences help explain why combining them may expose possibilities that any one approach overlooks.

The four images are collected in the [images](https://github.com/MapRock/IntelligenceBusiness/tree/main/blog_supplements/images) folder. 

## 1. Large Language Models: Diverse Sources, One Learned Model

[**View the LLM illustration**](images/cross_domain_llm.png)

LLMs learn from documented knowledge spanning many domains and forms of expression: books, papers, articles, blogs, code, forums, and, for multimodal models, visual and other media. Rather than independently consulting every original document for each question, the model draws on an integrated learned representation. Its breadth and flexibility make it possible to propose unexpected analogies and intermediate relationships between subjects that appear unrelated.

The trade-off is that those learned relationships are mostly implicit, difficult to inspect directly, and potentially outdated or mistaken. An LLM can creatively propose a connection without establishing that the connection actually holds.

## 2. People: Distributed Expertise, Shared Culture, and Conversation

[**View the human-knowledge illustration**](images/cross_domain_peoplepng)

Human knowledge is not concentrated in a single model. It is distributed among people with different combinations of expertise and lived experience. Teams bring disciplines together; generalists and polymaths connect some domains within one mind. Shared culture, language, and communication make knowledge exchange possible, even though what one person communicates is never perfectly assimilated by another. That imperfect exchange—including tangents and half-formed ideas—can generate unexpected questions.

A relatively small portion of human knowledge is deliberately published in the books, articles, research, and online material used to train models. Much operational, contextual, and tacit knowledge remains in people's experience. The trade-off is that bringing people together, communicating, and preserving their knowledge can be slow and costly.

## 3. ISG and TCW: Connections Emerging from Enterprise Activity

[**View the ISG/TCW illustration**](images/cross_domain_isg_tcw.png)

Enterprises are organized around domains and processes. Some processes cross departmental boundaries; others interact through defined interfaces. Master data, common semantics, and especially time offer ways to relate observations across those boundaries. A high-performance semantic layer makes governed measures and dimensions available for repeated analytical investigations.

The **Insight Function Array (IFA)** observes patterns in the dataframes produced by analysts' and knowledge workers' BI activity. The **Insight Space Graph (ISG)** preserves noteworthy observations **whether the worker noticed them, noticed but did not care, or never consciously considered them**. The **Tuple Correlation Web (TCW)** connects qualified metrics through measured relationships, including correlations and time-lagged associations. Both are inspectable graphs; LLMs can propose possible intermediate relationships for further investigation.

Their advantage is grounding in enterprise activity and data. Their limitations include dependence on semantic quality, available observations, computational effort to discover relationships, and the fact that correlation is not proof of causation.

## 4. Knowledge Graphs: Explicit Links Across Domains

[**View the knowledge-graph / Wikidata illustration**](images/cross_domain_kg_wikidata.png)

Knowledge graphs represent entities and relationships explicitly. **Wikidata** demonstrates how crowdsourced knowledge from many domains can share persistent identifiers—such as Wikidata item IDs and corresponding IRIs—so that a person, publication, organization, place, or event can be linked across subject boundaries. These links are inspectable and traversable: a graph query can follow an explicit path rather than asking an LLM to reconstruct the relationship from its learned representations.

Enterprise knowledge graphs apply the same principle within a usually narrower organizational scope. Their strengths are explicit semantics, traceability, and relatively efficient targeted traversal. Their limitation is coverage: they can expose only relationships that have been entered, derived, or otherwise made available in the graph. They do not automatically possess the flexible associative breadth of an LLM.

## 5. Time Molecules: A Shared Event Grammar Across Domains

[**View the Time Molecules illustration**](images/cross_domain_time_molecules.png)

[**Time Molecules**](https://github.com/MapRock/TimeMolecules/blob/main/README.md) takes a different route to cross-domain knowledge: it abstracts heterogeneous real-world activity into events with a common core—**DateTime, Event Type, CaseID**, and categorized **event and case properties**. An order, shipment, support ticket, hospital treatment, equipment alarm, or AI-agent tool call can contribute to the same general event representation, without pretending that these events have the same business meaning. Events related to a case become a time-ordered story; cases can also be linked across systems when their identities or relationships can be established.

Across many such stories, **Time Molecules** summarizes recurring event sequences into compact, inspectable probabilistic models, including Markov transition models. The models can be sliced and compared by event type, case type, time period, location, or other properties supported by the semantic context. This is where cross-domain questions emerge: *Does a change in one process tend to precede an event in another? Which transitions are different from last year? Do cases with certain properties follow unexpected paths?* The system makes the **temporal and process structure** of experience available for investigation, complementing the ISG's detected observations and the TCW's measured associations among qualified metrics.

The trade-offs are real. Cross-system event normalization, case linking, event coverage, and appropriate property definitions require work. Transition probabilities are descriptions of observed sequences under modeling assumptions, **not proof of causal mechanisms**; missing events or incompatible case boundaries can produce misleading patterns. Time Molecules is strongest when temporal relationships are interpreted alongside enterprise semantics, human context, and other evidence. For more detail, see the [2026 Time Molecules refresh](https://eugeneasahara.com/2026/05/15/time-molecules-2026-refresh/).

## Putting the Four Together

The purpose is not to choose one winner. **LLMs integrate broad documented patterns; people contribute diverse and often undocumented experience; ISG/TCW make enterprise observations and measured relationships available across domains; and knowledge graphs supply explicit, traversable connections.** Together, they enlarge the space of relationships an intelligence can consider.

For **Abductive Calculation**, the next step is to turn a promising connection into a *question*: Could this relationship provide another way to estimate the unknown quantity? Which observation or calculation would test it? And is obtaining that evidence worth the effort? The creative connection is an investigative starting point, not an established answer.
