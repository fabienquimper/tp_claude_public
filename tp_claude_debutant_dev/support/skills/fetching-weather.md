---
name: fetching-weather
description: >-
  Récupère et affiche les conditions météo actuelles d'une ville via le MCP météo.
  À utiliser quand l'utilisateur demande la météo, les conditions actuelles,
  "il fait quel temps", "quel temps fait-il", ou cite une ville avec météo/temps/température.
  Ne pas utiliser pour des prévisions sur plusieurs jours → utiliser fetching-forecast.
allowed-tools: mcp__meteo__get_weather
---

# Récupération météo — ville actuelle

## Quand utiliser cette skill
- Météo actuelle d'une ville nommée
- Température, humidité, vent d'un lieu précis
- Comparaison météo entre 2-3 villes (appeler l'outil plusieurs fois)

## Quand NE PAS utiliser
- Prévisions sur plusieurs jours → skill `fetching-forecast`
- Données historiques → pas de skill disponible, informer l'utilisateur
- Plus de 5 villes simultanément → risque de timeout

## Workflow

- [ ] 1. Identifier la ou les villes dans le prompt (orthographe anglaise si possible)
- [ ] 2. Appeler `mcp__meteo__get_weather` pour chaque ville
- [ ] 3. Si la ville est inconnue : signaler clairement et proposer une alternative orthographique
- [ ] 4. Présenter le résultat au format tableau (voir ci-dessous)
- [ ] 5. Ajouter une ligne de synthèse si plusieurs villes sont comparées

## Format de sortie

```
### Météo actuelle — [Ville]

| Indicateur    | Valeur            |
|---------------|-------------------|
| Température   | X°C (ressenti Y°C)|
| Conditions    | [Description]     |
| Humidité      | X%                |
| Vent          | X km/h [Direction]|
| Visibilité    | X km              |
```

## Règles

- ❌ Ne pas inventer des données si l'API échoue → signaler l'erreur clairement
- ❌ Ne pas convertir en Fahrenheit sauf si demandé explicitement
- ✅ Toujours indiquer la source : "Données : wttr.in"
- ✅ Si ville ambiguë (ex: "Lyon" peut être France ou USA) → demander confirmation

## Exemples

**Entrée :** "Quelle est la météo à Paris ?"
**Sortie attendue :**
```
### Météo actuelle — Paris

| Indicateur    | Valeur              |
|---------------|---------------------|
| Température   | 18°C (ressenti 16°C)|
| Conditions    | Partly Cloudy       |
| Humidité      | 62%                 |
| Vent          | 14 km/h SW          |
| Visibilité    | 10 km               |

*Données : wttr.in*
```

**Entrée :** "Météo à Xyzabc"
**Sortie attendue :**
```
La ville "Xyzabc" est inconnue de l'API météo. Vérifiez l'orthographe
ou utilisez le nom anglais de la ville.
```
