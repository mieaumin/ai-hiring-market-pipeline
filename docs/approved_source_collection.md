# Approved-Source-Only Collection

Phase 4 collection is intentionally narrow.

The collector runner reads `runtime/source_registry.csv`, filters only approved source rows, and skips everything else. It does not discover sources, approve sources, crawl search results, solve CAPTCHA, automate login, rotate IPs, or bypass access controls.

## Safe Runner

Command:

```bash
python scripts/run_approved_source_collection.py
```

Behavior:

- read `runtime/source_registry.csv`
- reject pending, rejected, suspended, expired, unknown, or missing approval status
- reject D/E/F grade sources
- reject sources with robots, Terms, login, CAPTCHA, anti-bot, or missing-field blockers
- select a collector by `allowed_method` or `ats_type`
- write raw rows to `data/raw/raw_jds.csv`
- write run logs to `runtime/runs.csv`
- write errors to `runtime/errors.csv`

If no approved source exists, the runner prints a clear skip message, writes a run log, and exits successfully.

## Collector Scope

Collectors are conservative skeletons:

- `public_json_collector.py`
- `rss_collector.py`
- `sitemap_collector.py`
- `greenhouse_collector.py`
- `lever_collector.py`
- `ashby_collector.py`

All collectors rely on `BaseCollector` guard checks before fetch.

## Why Broad Crawling Is Not Allowed

Broad crawling would collapse discovery, approval, and collection into one unsafe step. This project keeps them separate:

```text
discovery -> evidence review -> screening -> approved source -> collection
```

That separation follows Biz-Voyager-style quality gates while keeping the Korean AI hiring market pipeline conservative and auditable.
