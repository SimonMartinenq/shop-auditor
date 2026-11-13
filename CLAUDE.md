# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projet

shop-auditor audite une boutique e-commerce publique (Shopify / WooCommerce) et produit un plan d'action priorisé. Le contexte est dans `docs/CONTEXT.md`, l'avancement dans `docs/ROADMAP.md` (cocher les cases au fil de l'eau), les décisions dans `docs/decisions.md`. `docs/brief.txt` est le brief d'origine et fait foi.

## Commandes

```sh
uv sync                                  # installer (Python 3.12+)
uv run pytest                            # tous les tests
uv run pytest tests/test_cli.py::test_x  # un seul test
uv run ruff check . && uv run ruff format .
uv run mypy                              # strict, sur src/ et tests/
uv run shop-auditor collect|analyze|audit <url|run_dir>
```

Lighthouse est une dépendance Node épinglée dans `package.json` (`npm ci`), lancée en sous-processus.

## Architecture

Deux phases séparées, reliées par un snapshot sur disque :

1. **Collecte déterministe** (`collect/`) : robots.txt → détection de plateforme → choix des pages types (accueil, collection, produit, panier via ajout au panier, contenu ; max 10 URLs) → pour chaque page × viewport (mobile, desktop) : Lighthouse JSON, axe-core, requêtes réseau attribuées via `data/signatures.yaml`, contrôles e-commerce, SEO complémentaire, EcoIndex, capture. `aggregate.py` fusionne un même problème présent sur plusieurs pages en une seule entrée. Sortie : `SiteSnapshot` JSON + PNG dans `runs/<domaine>/<horodatage>/`.
2. **Analyse** (`agent/`) : l'agent ne lit **que** le snapshot, via des outils en lecture seule (`get_overview`, `get_performance`, `get_third_parties`, `get_ecommerce`, `get_accessibility`, `get_seo`, `get_eco`, `view_screenshot`) puis `submit_report(AuditReport)`. Il ne navigue jamais. Il reçoit un résumé compact, pas le JSON entier.
3. **Contrôles post-génération** (`agent/checks.py`) : chaque `evidence_ref` existe dans le snapshot, `quick_wins` (5 max) référencent des constats existants, pas de doublon, toute violation axe « critical » est couverte. En cas d'échec, erreurs renvoyées à l'agent, 2 essais max.
4. **Rendu** HTML (Jinja2). Pied de page : durée, coût, version du modèle.

Rejouer `analyze` sur un snapshot existant ne recrawle pas : c'est ce qui rend les évals reproductibles et bon marché.

Les **scores par axe** (0–100) sont calculés en code par des fonctions pures, jamais par le LLM. Les contrats entre phases sont dans `models.py` (Pydantic v2).

## Règles

**Règle n°1 : ne jamais réimplémenter une mesure que Lighthouse ou axe-core fournit déjà.** L'effort va aux contrôles e-commerce, à l'attribution des scripts, à l'agrégation et à l'analyse.

- Avancer étape par étape (`docs/ROADMAP.md`) ; une étape commence quand la précédente passe ses tests.
- Vérifier la version installée de Playwright, du framework d'agent et du SDK anthropic, et suivre leur API actuelle, pas des exemples de mémoire.
- Vérifier la licence et l'API de la bibliothèque EcoIndex avant de l'intégrer ; consigner la décision dans `docs/decisions.md`.
- Aucun appel réseau externe ni LLM dans la CI : fixtures locales (`fixtures/sites/`, défauts attendus dans `expected.yaml`) et mocks uniquement. Les évals avec LLM réel vivent dans `evals/`, hors CI.
- Collecte : timeout par page et global, fermeture propre du navigateur, une page à la fois, respect de robots.txt, User-Agent identifiable.
- Jamais de soumission de formulaire de paiement ni de création de compte sur le site audité.
- Typage complet, mypy strict ; fonctions de scoring pures.
- Code en anglais ; rapport, README et docs en français.
- Simplicité : pas de base de données serveur ni de file de tâches externe en V1 (asyncio + SQLite).
- Commits petits et explicites (Conventional Commits).
- Variables d'environnement : `ANTHROPIC_API_KEY`, `PAGESPEED_API_KEY` (optionnelle), `SHOP_AUDITOR_MODEL`.
