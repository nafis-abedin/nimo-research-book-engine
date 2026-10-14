# Book and Research Workflow

## Recommended workflow

1. Start with `/research deep <topic>`. NIMO uses the currently selected installed model and enables web retrieval for the explicit research task unless `/offline` is active.
2. Review the generated source ledger, claim ledger, dates, domains, and evidence gaps.
3. Ask follow-up questions against the saved research artifact.
4. Use `/book <topic>` only after the research scope is clear.
5. Review each chapter checkpoint before continuing.
6. Export or convert the final manuscript only after factual and citation review.

## Evidence rules

NIMO distinguishes retrieved evidence from model synthesis. Search snippets are discovery leads only and cannot support claims. Verify extracted primary sources, dates, scope, geography, definitions, and uncertainty. The system may report `evidence_insufficient`; do not treat that as a failure to be bypassed.

## Publisher review checklist

- Every material factual claim has a traceable source.
- Dates and version numbers are checked against the source.
- Conflicting sources are recorded rather than silently averaged.
- Quotes are verified against the original page or document.
- Copyright, licensing, privacy, and defamation risks are reviewed by a qualified human.
- AI-generated prose is edited and fact-checked before publication.

## Model independence

The book workflow supports any chat-capable model discovered through Ollama, including models imported from other sources. Choose the installed model with `/model`; the selection is saved with the book job and checked again when it runs or resumes. A smaller model may produce weaker synthesis; a larger model may require more RAM and time. Model choice affects quality, not the identity of the NIMO project.
