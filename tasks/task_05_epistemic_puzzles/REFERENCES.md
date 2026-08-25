# References and Provenance

This bibliography separates three questions: where the semantics comes from, where each puzzle
comes from, and what this repository itself has checked. A citation supports the first two; only the
tests and Metamath run support the third.

## Semantic foundations

- **[FHMMV95]** Ronald Fagin, Joseph Y. Halpern, Yoram Moses, and Moshe Y. Vardi,
  *Reasoning About Knowledge*, MIT Press, 1995, ISBN 978-0-262-06162-9.
  [Publisher record](https://mitpress.mit.edu/9780262061629/reasoning-about-knowledge/).

  This is the general reference for possible-world models, information sets, multi-agent knowledge,
  and knowledge puzzles. Task 5 uses its ideal-agent reading of knowledge but implements only a
  small finite S5 fragment.

- **[P89]** Jan A. Plaza, “Logics of Public Communications,” in *Proceedings of the Fourth
  International Symposium on Methodologies for Intelligent Systems*, 1989, pp. 201–216; republished
  in *Synthese* 158 (2007), 165–179.
  [DOI: 10.1007/s11229-007-9168-7](https://doi.org/10.1007/s11229-007-9168-7).

  This is the source for the public-announcement idea used by `FiniteModel.announce`: keep precisely
  the worlds where the announced formula is true and restrict the relations to those worlds.

- **[VDK07]** Hans van Ditmarsch, Wiebe van der Hoek, and Barteld Kooi,
  *Dynamic Epistemic Logic*, Synthese Library 337, Springer, 2007/2008.
  [DOI: 10.1007/978-1-4020-5839-4](https://doi.org/10.1007/978-1-4020-5839-4).

  This supplies the broader dynamic-epistemic setting: knowledge is static uncertainty inside a
  model, while announcements are epistemic actions that change the model.

## Puzzle sources and analyses

- **[DHKWY17]** Hans van Ditmarsch, Michael Ian Hartley, Barteld Kooi, Jonathan Welton, and
  Joseph B. W. Yeo, “Cheryl's Birthday,” *Proceedings TARK 2017*, EPTCS 251, pp. 1–9.
  [DOI: 10.4204/EPTCS.251.1](https://doi.org/10.4204/EPTCS.251.1) ·
  [arXiv:1708.02654](https://arxiv.org/abs/1708.02654).

  Yeo, the designer of the SASMO version, is a coauthor. The paper records the ten dates, the 2015
  competition provenance, and the month/day indistinguishability graph reproduced by `cheryl.py`.

- **[FHMV98]** Ronald Fagin, Joseph Y. Halpern, Yoram Moses, and Moshe Y. Vardi,
  “Common Knowledge Revisited,” arXiv:cs/9809003, 1998; a previous version appeared at TARK 1996.
  [arXiv record](https://arxiv.org/abs/cs/9809003).

  The paper discusses the muddy-children example when analyzing the role and finite depth of common
  knowledge. Task 5 models the synchronized dialogue by repeated public restrictions and checks only
  bounded finite instances.

## Local evidentiary claim

These references do not certify this implementation. The repository's claim is narrower: its tests
exhaust the seven hat worlds, the ten Cheryl dates, and every nonempty muddy assignment for
`1 <= n <= 5`. The Python evaluator remains part of the disclosed computational trust base; it is
not silently counted as a Metamath proof.
