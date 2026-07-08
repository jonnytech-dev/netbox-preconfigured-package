# NetBox Docker — Pre-configured with Plugins

A ready-to-go NetBox v4.6.1 Docker setup with plugins pre-installed. Clone it, build, and run — no manual plugin installation needed.

## Included Plugins

| Plugin | Version | Description |
|--------|---------|-------------|
| netbox-secrets | 3.1.0 | Securely store and categorize secrets like device passwords |
| netbox-floorplan-plugin | 0.9.2 | Graphical floor plan mapping for sites and locations |
| netbox-topology-views | latest | Auto-generated topology maps from devices and cables |
| slurpit-netbox | latest | Automated network device discovery via SNMP/SSH |
| netbox-documents | latest | Attach files and documents to any NetBox object |
| netbox-plugin-dhcp | latest | DHCP management within NetBox |

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2+)

## Quick Start

1. **Clone the repo:**

   ```bash
   git clone https://github.com/jonnytech-dev/netbox-preconfigured-package.git
   cd netbox-docker
   ```

2. **Review the env files** in the `env/` folder. They contain default template values that work out of the box for local development. For production use, replace the default passwords and keys with your own:

   | File | What to change |
   |------|----------------|
   | `env/netbox.env` | `SECRET_KEY`, `API_TOKEN_PEPPER_1`, `DB_PASSWORD`, `REDIS_PASSWORD`, `REDIS_CACHE_PASSWORD` |
   | `env/postgres.env` | `POSTGRES_PASSWORD` (must match `DB_PASSWORD` in netbox.env) |
   | `env/redis.env` | `REDIS_PASSWORD` (must match `REDIS_PASSWORD` in netbox.env) |
   | `env/redis-cache.env` | `REDIS_PASSWORD` (must match `REDIS_CACHE_PASSWORD` in netbox.env) |

   > **Important:** If you deploy this to production, change all default passwords and generate unique keys. The passwords in `env/postgres.env`, `env/redis.env`, and `env/redis-cache.env` must match their corresponding values in `env/netbox.env` or NetBox will fail to connect. The included values are for local development and testing only.

   **Generating a secure key:**

   Use one of the following to generate a cryptographically secure key for `SECRET_KEY`, passwords, or API tokens:

   *Bash / macOS / Linux:*
   ```bash
   openssl rand -base64 50
   ```

   *PowerShell (Windows):*
   ```powershell
   -join ((1..50) | ForEach-Object { [char](Get-Random -Minimum 33 -Maximum 127) })
   ```

   *Python (any OS):*
   ```python
   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```

3. **Build and start:**

   ```bash
   docker compose build --no-cache
   docker compose up -d
   ```

4. **Create your admin account.** Superuser auto-creation is disabled (`SKIP_SUPERUSER=true`) so that no default admin credentials ship with the repo. Create your own:

   ```bash
   docker compose exec netbox python /opt/netbox/netbox/manage.py createsuperuser
   ```

   You will be prompted for a username, email, and password.

5. **Access NetBox** at `http://localhost:8000` and log in with the account you just created.

## File Structure

```
netbox-docker/
├── docker-compose.yml        # Container orchestration
├── docker-compose.override.yml # Build config and port mapping
├── Dockerfile-Plugins        # Builds NetBox image with plugins pre-installed
├── plugin_requirements.txt   # Plugin packages and versions
├── configuration/
│   ├── configuration.py      # NetBox core configuration
│   └── plugins.py            # Plugin enablement and settings
└── env/
    ├── netbox.env            # NetBox app settings (secret key, DB/Redis passwords, etc.)
    ├── postgres.env          # PostgreSQL credentials
    ├── redis.env             # Redis password
    └── redis-cache.env       # Redis cache password
```

## Customization

### Adding a Plugin

Three steps: add the package, enable it in the config, and rebuild.

**Step 1 — Add to `plugin_requirements.txt`:**

```
netbox-my-new-plugin
```

**Step 2 — Enable in `configuration/plugins.py`:**

```python
PLUGINS = [
    "netbox_secrets",
    "netbox_floorplan",
    "netbox_topology_views",
    "slurpit_netbox",
    "netbox_documents",
    "netbox_dhcp",
    "netbox_my_new_plugin",  # <-- add your new plugin here
]

PLUGINS_CONFIG = {
    # for some plugins, this part is OPTIONAL
    # add any plugin-specific settings here
    "netbox_my_new_plugin": {
        "some_setting": True,
    },
}
```

**Step 3 — Rebuild and restart:**

```bash
docker compose build --no-cache
docker compose up -d
```

> **Note:** The Docker build process handles `pip install` automatically from `plugin_requirements.txt`. You do not need to run pip manually. If you are developing outside of Docker or need to install packages manually inside the container, the individual install commands are:
>
> ```bash
> pip install netbox-secrets
> pip install netbox-floorplan-plugin
> pip install netbox-topology-views
> pip install --no-cache-dir slurpit_netbox
> pip install netbox-documents
> pip install netbox-plugin-dhcp
> ```

### Removing a Plugin

1. Remove the package from `plugin_requirements.txt`
2. Remove the entry from `PLUGINS` and `PLUGINS_CONFIG` in `configuration/plugins.py`
3. Rebuild: `docker compose build --no-cache && docker compose up -d`

### Changing the Superuser

**Create a new superuser:**

```bash
docker compose exec netbox python /opt/netbox/netbox/manage.py createsuperuser
```

**Change an existing user's password:**

```bash
docker compose exec netbox python /opt/netbox/netbox/manage.py changepassword yourusername
```

You can also manage users, passwords, and API tokens through the NetBox web UI under **Admin → Users**.

<!-- **Enable automatic superuser creation on startup** (optional — for personal/dev setups only):

In `env/netbox.env`, change `SKIP_SUPERUSER=true` to `SKIP_SUPERUSER=false` and add:

```
SUPERUSER_NAME=admin
SUPERUSER_EMAIL=admin@example.com
SUPERUSER_PASSWORD=your-secure-password
SUPERUSER_API_TOKEN=your-api-token
```

NetBox will create this account automatically on first startup. Do not use this in a public or shared repo with real credentials. -->

## Built With

- [NetBox Community Docker](https://github.com/netbox-community/netbox-docker) v4.6.1
- Plugins listed above

## Notes

- This setup is based on the [netbox-community/netbox-docker](https://github.com/netbox-community/netbox-docker) project.
- All plugin static files and database migrations are handled automatically on build and startup.
- Topology views require devices and cables to be created in NetBox before a map will render.
- The env files contain default template values. They are safe for local development but should be changed before any production deployment.
