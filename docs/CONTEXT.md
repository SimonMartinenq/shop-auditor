# Contexte du projet — shop-auditor

> Version condensée de [brief.txt](brief.txt), qui fait foi.

## En une phrase

Une couche d'interprétation métier e-commerce au-dessus des outils standard : on donne l'URL d'une boutique, le collecteur lance Lighthouse + axe-core sur le parcours d'achat, ajoute des contrôles e-commerce et attribue chaque script tiers à l'app/plugin qui le charge ; un agent agrège, analyse les captures et produit un plan d'action priorisé par impact sur les ventes.

## Pour qui

- Le gérant d'une boutique Shopify / WooCommerce (lecteur non technique : top 5 en clair).
- Le développeur freelance qui veut un diagnostic rapide avant un devis (annexe technique).

## Ce que le projet démontre (portfolio)

1. Automatisation navigateur et collecte fiable en Python async (Playwright).
2. Un agent sur framework reconnu (Claude Agent SDK **ou** PydanticAI) : outils, sortie structurée, vision.
3. **Les mesures viennent des outils, l'agent interprète et priorise.** Chaque constat cite une preuve du snapshot.
4. Tests, évals reproductibles sur fixtures, observabilité, démo en ligne.

Contraste voulu avec le projet « empreinte carbone » (boucle agent maison) : ici, framework.

## Valeur ajoutée vs Lighthouse seul

| Lighthouse seul | shop-auditor |
|---|---|
| Une page isolée | Parcours accueil → collection → produit → panier, problèmes dédupliqués entre pages |
| Générique | Product JSON-LD, réassurance, bouton panier visible sur mobile, ajout au panier |
| « Reduce unused JavaScript » | « L'app d'avis X coûte 1,2 s sur la fiche produit » (attribution app/plugin) |
| Rapport développeur | Top 5 par impact business + annexe technique |
| Ne regarde pas la page | Analyse visuelle (vision) mobile/desktop |

Piège à éviter : « Lighthouse + un LLM qui reformule ». La valeur vient des contrôles e-commerce, de l'attribution et de l'agrégation, et elle est mesurée par les évals.

## Périmètre V1

- 4 à 6 pages types (accueil, collection, produit, panier, contenu), max 10 URLs, mobile + desktop.
- Six axes : performance, accessibilité, SEO technique, e-commerce, scripts tiers, visuel + éco.
- Sortie : `AuditReport` JSON + HTML, score par axe (calculé en code), constats, top 5 « cette semaine ».
- Détection de plateforme : Shopify / WooCommerce / autre.

**Hors périmètre** : pages connectées, paiement, crawl complet, audit RGAA certifiant, historique (V2).

**Règles d'usage** : robots.txt respecté, une seule session lente, User-Agent identifiable, sites publics uniquement.

## Stack

Python 3.12+ / uv · Playwright async · Lighthouse CLI (Node, sous-processus, `--port` sur le Chromium de Playwright) · axe-playwright-python · extruct + selectolax · EcoIndex + Green Web Foundation · Pydantic v2 · Claude Agent SDK ou PydanticAI · FastAPI + HTMX · asyncio + SQLite · Logfire ou Langfuse · Ruff, mypy strict, pytest · Docker, Fly.io / Railway.

Variables d'environnement : `ANTHROPIC_API_KEY`, `PAGESPEED_API_KEY` (optionnelle), `SHOP_AUDITOR_MODEL`.

## Décisions ouvertes

Voir [decisions.md](decisions.md) : choix du framework d'agent, licence EcoIndex.
