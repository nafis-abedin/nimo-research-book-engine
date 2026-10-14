# Research Reliability Contract

NIMO must not treat a search result, snippet, or model response as a fact by itself.

## Claim states

Every important claim should be one of: `verified`, `corroborated`, `contested`, `stale`, `lead-only`, or `unverified`. Only `verified` and appropriately labeled `corroborated` claims may be presented as established findings. `Contested`, `stale`, and `unverified` claims must remain visibly qualified.

## Current and high-impact questions

For questions about current office holders, elections, laws, public safety, prices, health, finance, or breaking events, NIMO must:

1. Convert relative language such as “now” or “latest” into an explicit UTC date window.
2. Retrieve an official or primary source when one exists.
3. Retrieve an independent corroborating source from a separate publisher group.
4. Verify that the source names the same entity and refers to the same jurisdiction and date.
5. Record disagreements and refuse to collapse them into a single answer when the evidence is unresolved.
6. State the retrieval timestamp and source limitations.

A model must answer “The retrieved sources do not establish that reliably” when these gates fail. It must never fill a missing fact from memory.

## Book workflow

Research comes before drafting. Each chapter should carry a source ledger, claim ledger, evidence gaps, dates, and limitations. A citation proves only what the cited page supports; citation presence alone is not proof of correctness.

## Evaluation set

Before public release, maintain human-reviewed cases for:

- current Bangladesh and international office holders;
- election and government changes;
- current product release and price;
- laws and regulatory status;
- health and safety claims;
- finance and market values;
- historical claims with conflicting sources;
- intentionally misleading snippets and prompt-injection text.

Score retrieval relevance, source diversity, freshness, entity match, citation coverage, groundedness, completeness, and abstention quality. Publish aggregate results, not private queries or personal data.
