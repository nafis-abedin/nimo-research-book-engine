# Book and Research Workflow

## Recommended workflow

1. Start with `/research deep <topic>`.
2. Review the generated source ledger, claim ledger, dates, domains, and evidence gaps.
3. Ask follow-up questions against the saved research artifact.
4. Use `/book <topic>` only after the research scope is clear.
5. Review each chapter checkpoint before continuing.
6. Export or convert the final manuscript only after factual and citation review.

## Evidence rules

NIMO distinguishes retrieved evidence from model synthesis. Headlines and snippets are not sufficient evidence for important claims. Verify primary sources, dates, scope, geography, definitions, and uncertainty. The system may report `evidence_insufficient`; do not treat that as a failure to be bypassed.

## Publisher review checklist

- Every material factual claim has a traceable source.
- Dates and version numbers are checked against the source.
- Conflicting sources are recorded rather than silently averaged.
- Quotes are verified against the original page or document.
- Copyright, licensing, privacy, and defamation risks are reviewed by a qualified human.
- AI-generated prose is edited and fact-checked before publication.

## Model independence

The book workflow is model-agnostic within Ollama. A smaller model may produce weaker synthesis; a larger model may require more RAM and time. Model choice affects quality, not the identity of the NIMO project.
