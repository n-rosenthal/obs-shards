#   `backend/scripts/`
##  `import_vault`
First, mount the volume in the Dockerfile:

```Docker
volumes:
  - ./backend:/app
  - .../ObsidianVault:/vault
```

then, run the script:

```bash
[sudo] docker compose exec backend python manage.py shell -c "from scripts.import_vault import run; run()"
```

##  `export_vault`
First, mount the volume in the Dockerfile:

```Docker
volumes:
  - ./backend:/app
  - .../ObsidianVault:/vault_export
```

then, run the script:

```bash
[sudo] docker compose exec backend python manage.py shell -c "from scripts.export_vault import run; run()"
```