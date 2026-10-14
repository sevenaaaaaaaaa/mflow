# WordPress local test environment

`docker-compose.yml` starts a throwaway WordPress 6.7 + MySQL 8 stack on http://localhost:8090 for testing
the WordPress publish adapter (`dev/scripts/publish_adapters/`) and block output from
`dev/scripts/replication/` (`wp_blocks` adapter).

```bash
cd dev/wordpress
WP_THEME_DIR=/path/to/your-theme WP_THEME_SLUG=your-theme docker compose up -d
```

Site-specific themes, page templates and import scripts are project data and live outside the public repo
(`ops/brands/<brand>/wordpress/`).
