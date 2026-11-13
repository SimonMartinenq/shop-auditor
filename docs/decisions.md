# Journal des décisions

Format : date — décision — raison. Les décisions ouvertes restent en haut tant qu'elles ne sont pas tranchées.

## Ouvertes

- **Framework d'agent** : Claude Agent SDK (outils en serveur MCP in-process) ou PydanticAI (sortie typée native). À trancher avant l'étape 4, à justifier aussi dans le README.
- **EcoIndex** : vérifier la licence et l'API de `ecoindex_python` (CNUMR). Les valeurs d'ACV (GES/eau) ne sont pas sous licence libre (© Frédéric Bordage) : sans autorisation claire, n'afficher que la note EcoIndex. À trancher à l'étape 2.

## Prises

- 2026-11-13 — Valeurs des enums en anglais (`critical`, `low`…), conformément à « code en anglais » ; la traduction française se fait au rendu HTML.
- 2026-11-13 — Les contrôles internes au rapport (quick_wins existants, ids uniques, pages connues, résumé ≤ 5 lignes) sont des validateurs Pydantic dans `models.py` ; `checks.py` ne fera que ce qui exige le snapshot.
- 2026-11-13 — Une boutique de test = un port fixe (8701–8704) : `robots.txt` et `sitemap.xml` à la racine, URLs absolues possibles dans les canonical et le sitemap.
- 2026-11-13 — Packaging avec uv + hatchling, `uv.lock` committé pour des installations reproductibles (CI identique au poste local).
