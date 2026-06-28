# meteo-agent

> Projet éducatif Claude Code — assistant météo Python avec MCP et skills.
> Utilisé dans le cadre du TP2 du parcours débutant développeur.

## Commandes essentielles

```bash
pip install mcp httpx          # installer les dépendances MCP
python support/scripts/mcp_meteo.py   # lancer le serveur MCP manuellement (test)
pytest tests/ -v               # lancer les tests
```

## Conventions

- Langage : Python 3.11, types obligatoires sur toutes les fonctions publiques
- Formatage : black, longueur max 88 caractères
- Tests : pytest, fixtures dans `tests/conftest.py`
- Nommage : snake_case pour tout, sauf les classes (PascalCase)

## Structure

```
meteo-agent/
├── support/
│   ├── scripts/mcp_meteo.py   ← serveur MCP météo
│   └── skills/                ← skills Claude Code
├── tests/                     ← golden files et tests de régression
└── .claude/
    └── commands/              ← skills actives
```

## Règles absolues — NE JAMAIS

- Modifier un fichier sans confirmation explicite de l'utilisateur
- Écrire des clés API ou tokens en dur dans le code
- Appeler des APIs tierces autres que wttr.in sans validation préalable
