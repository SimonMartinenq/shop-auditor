# Boutiques de test

Mini-boutiques statiques avec des défauts plantés volontairement. Chaque `expected.yaml` liste les défauts que shop-auditor doit trouver ; c'est la vérité terrain des tests (étape 2) et des évals (étape 5).

| Boutique | Port | Ce qu'elle teste |
|---|---|---|
| `clean` | 8701 | Contrôle : aucun défaut. Tout constat ici est un faux positif. |
| `slow` | 8702 | Performance et app tierce bloquante (FakeReviews) |
| `no-trust` | 8703 | E-commerce : JSON-LD incomplet, CTA hors écran mobile, panier cassé, frais de port cachés, pas de réassurance |
| `a11y-seo` | 8704 | Accessibilité et SEO, dont un défaut répété sur 3 pages (agrégation) |

Lancer les boutiques à la main : `uv run python tests/fixture_server.py`.

Chaque boutique a son propre port, donc sa propre origine : `robots.txt` et `sitemap.xml` sont à la racine, comme sur un vrai site. L'image hero de `slow` (~4 Mo) est générée au premier lancement et n'est pas versionnée.

À savoir pour les collecteurs : les boutiques sont servies en HTTP local, sans compression. Les audits Lighthouse liés à HTTPS, HTTP/2 ou à la compression texte sont à ignorer ; ce ne sont pas des défauts plantés.

`fixtures/signatures.yaml` contient la signature de la fausse app d'avis, séparée des vraies signatures (`data/signatures.yaml`, étape 2).
