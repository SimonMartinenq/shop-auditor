# Journal des décisions

Format : date — décision — raison. Les décisions ouvertes restent en haut tant qu'elles ne sont pas tranchées.

## Ouvertes

- **Framework d'agent** : Claude Agent SDK (outils en serveur MCP in-process) ou PydanticAI (sortie typée native). À trancher avant l'étape 4, à justifier aussi dans le README.
- **EcoIndex** : vérifier la licence et l'API de `ecoindex_python` (CNUMR). Les valeurs d'ACV (GES/eau) ne sont pas sous licence libre (© Frédéric Bordage) : sans autorisation claire, n'afficher que la note EcoIndex. À trancher à l'étape 2.

## Prises

- 2026-11-13 — Lockfile non committé à l'init, `uv` n'étant pas encore installé sur le poste ; à générer avec `uv sync`.
