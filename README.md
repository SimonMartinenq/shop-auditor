# shop-auditor

Audit de boutique e-commerce (Shopify / WooCommerce) : Lighthouse et axe-core sur le parcours d'achat complet, contrôles e-commerce, attribution des scripts tiers aux apps et plugins, puis un agent qui produit un plan d'action priorisé par impact sur les ventes.

> En construction. Voir [docs/CONTEXT.md](docs/CONTEXT.md) et [docs/ROADMAP.md](docs/ROADMAP.md).

## Pourquoi pas juste Lighthouse ?

shop-auditor utilise Lighthouse et ne cherche pas à le remplacer : il ajoute ce que Lighthouse ne fait pas.

| Lighthouse seul | shop-auditor |
|---|---|
| Audite une page isolée | Audite le parcours accueil → collection → produit → panier, et regroupe un même problème présent sur plusieurs pages en un seul constat |
| Générique, ignore le e-commerce | Vérifie les données structurées Product complètes, la réassurance (livraison, retours, avis), la visibilité du bouton panier sur mobile, le comportement du panier |
| « Reduce unused JavaScript », 1,2 s de JS tiers | « L'app d'avis X coûte 1,2 s sur la fiche produit » : attribution des scripts aux apps Shopify / plugins WooCommerce, avec réglage ou alternative |
| Rapport pour développeur | Top 5 priorisé par impact business pour le gérant, détails techniques en annexe |
| Ne regarde pas la page | Analyse visuelle du parcours (hiérarchie, CTA, friction) sur captures mobile et desktop |

**Limites assumées** : des SaaS d'audit e-commerce existent et Shopify fournit son propre rapport de vitesse. Le projet ne prétend pas les battre ; il démontre la construction d'une couche d'analyse spécialisée et vérifiable au-dessus d'outils de référence.

## Développement

```sh
uv sync
uv run pytest
```
