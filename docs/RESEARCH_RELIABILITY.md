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

The ordinary online chat path follows the same evidence boundary: it extracts the linked page before giving the local model any evidence. Search snippets are discovery leads only. Current office-holder questions in English and Bengali trigger live retrieval, require a dated official/primary page plus independent reporting from a separate publisher group, and remain unverified when either page is missing or undated. A page's explicit update date can establish freshness for a maintained government directory; otherwise its publication date is used.

Discovery is not restricted to a small domain allowlist. Search can return public pages across countries and subject areas; source tiers describe how much weight a page can carry, and low-tier or user-generated pages can remain useful leads without qualifying as verified evidence. Research plans should cover primary records, independent reporting, technical documentation, academic work, criticism, and other relevant perspectives for the topic. The same workflow applies to book projects and cybersecurity research, with the source-quality and safe-use boundaries appropriate to the request.

NIMO is local-first: greetings, ordinary conversation, and stable explanations stay with the local model. A request that clearly asks for current facts, a lookup, verification, research, or a book can enable public-web retrieval for that task. `/offline` is a hard override that blocks network retrieval until `/online` is used; `/network auto` restores automatic behavior. Search is broad rather than limited to a hard-coded list of sites, but no provider indexes the entire Internet, so results are never exhaustive by default.

Only directly extracted page text can support a research claim. Failed, empty, blocked, or entity-mismatched pages remain traceable as leads where possible and cannot contribute snippets to claim status, rankings, or direct answers. An unmarked legacy record is not automatically treated as verified page extraction.

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
