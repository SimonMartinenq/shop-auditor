# Roadmap — shop-auditor

Six étapes testables, environ 3 semaines à temps partiel. Une étape ne commence que lorsque la précédente passe ses tests.

## Étape 1 — Socle et fixtures
- [x] Repo initialisé (git, pyproject, arborescence, CI)
- [x] `uv sync` + `uv.lock` committé
- [x] Modèles Pydantic : `SiteSnapshot`, `PageSnapshot`, `Finding`, `AuditReport` (`models.py`)
- [x] 4 mini-boutiques statiques dans `fixtures/sites/`, chacune avec un `expected.yaml` ; une boutique « propre » de contrôle
- [x] Défauts plantés en priorité hors Lighthouse : JSON-LD Product sans prix/dispo, bouton panier hors écran sur mobile, frais de port invisibles avant le panier, fausse « app d'avis » présente dans `signatures.yaml` sur toutes les pages, même défaut répété sur 3 pages
- [x] Serveur local des fixtures pour pytest (`tests/fixture_server.py`)
- [x] CI verte sur GitHub

**Fini quand** la CI sert les fixtures et passe.

## Étape 2 — Collecteurs
- [ ] `crawler.py` : robots.txt, choix des pages types, parcours jusqu'au panier
- [ ] `platform.py` : détection Shopify / WooCommerce (tests sur extraits HTML enregistrés)
- [ ] `lighthouse.py` : sous-processus Node, parsing JSON
- [ ] `accessibility.py` : axe-core
- [ ] `ecommerce.py` : Product JSON-LD, réassurance, CTA mobile, ajout au panier, frais de port
- [ ] `third_parties.py` + `data/signatures.yaml` (~20 apps Shopify / plugins WooCommerce)
- [ ] `seo.py` : canonical, variantes dupliquées, sitemap, liens cassés
- [ ] `eco.py` : EcoIndex + Green Web (licence vérifiée → `docs/decisions.md`)
- [ ] `screenshots.py`, `aggregate.py` (déduplication multi-pages)
- [ ] `shop-auditor collect <url>` écrit `runs/<domaine>/<horodatage>/`

**Fini quand** chaque défaut planté est détecté par les tests et que `collect` produit un snapshot complet sur une vraie boutique publique.

## Étape 3 — Scores et outils agent
- [ ] Scores par axe : fonctions pures
- [ ] Outils de lecture : `get_overview`, `get_performance`, `get_third_parties`, `get_ecommerce`, `get_accessibility`, `get_seo`, `get_eco`, `view_screenshot`

**Fini quand** tout est testé sur un snapshot figé.

## Étape 4 — Agent
- [ ] Framework choisi et justifié (README + `decisions.md`)
- [ ] Prompt système, vision, `submit_report`
- [ ] `checks.py` : evidence_ref existants, quick_wins valides, pas de doublon, violations axe « critical » couvertes ; 2 essais max
- [ ] `render.py` (Jinja2), commandes `analyze` et `audit`

**Fini quand** un rapport valide est produit pour chaque fixture.

## Étape 5 — Évals et observabilité
- [ ] Rejeu sur snapshots figés : rappel (≥ 90 %), précision, faux positifs sur la boutique propre, critiques dans le top 5
- [ ] Valeur ajoutée vs Lighthouse brut
- [ ] Comparaison de deux modèles (coût, latence)
- [ ] Traces : un span par page collectée et par appel LLM/outil ; pied de page HTML (durée, coût, modèle)

**Fini quand** rappel, précision et coût sont publiés dans le README.

## Étape 6 — Livraison
- [ ] FastAPI : tâche asynchrone + statut, page de démo
- [ ] Docker (image Playwright officielle + Node), déploiement Fly.io ou Railway
- [ ] Protections : limite de requêtes, domaines bloqués, budget LLM journalier, timeout global
- [ ] README final : « Pourquoi pas juste Lighthouse ? », GIF, exemple de rapport

**Fini quand** la démo est en ligne.

## V2 (hors périmètre)
Audits planifiés et historique.
