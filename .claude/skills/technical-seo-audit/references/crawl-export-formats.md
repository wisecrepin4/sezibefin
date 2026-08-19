# Crawl export formats

Load this when you need to map columns from a specific crawl tool, or when you need the method for tracing a redirect chain from a flat export.

## Screaming Frog (primary format)

### internal_all export (the main crawl export)

Export from the **Internal** tab, filter **All**, as CSV or XLSX. Typical columns:

| Column | What it is | Use it for |
|---|---|---|
| Address | The URL | Everything |
| Status Code | HTTP status (200, 301, 404, etc.) | Redirects, broken links |
| Status | Text version (OK, Moved Permanently, Not Found) | Confirming status |
| Indexability | Indexable / Non-Indexable | Indexing checks |
| Indexability Status | Reason (noindex, Canonicalised, Blocked by robots.txt, Redirected) | Indexing checks |
| Title 1 | The page title tag | Duplicate titles |
| Meta Description 1 | The meta description | Duplicate metas |
| H1-1 | The first H1 | Duplicate H1s |
| Canonical Link Element 1 | The canonical URL the page declares | Canonical mismatches |
| Word Count | Body word count | Thin page detection |
| Crawl Depth | Clicks from the start URL | Orphan and depth checks |
| Inlinks | Count of internal links pointing at this URL | Orphan detection (0 = orphan) |
| Outlinks | Count of links out of this URL | Context |
| Redirect URL | Where a redirecting URL points next | Tracing redirect chains |
| Redirect Type | 301, 302, etc. | Redirect severity |
| Sessions / Clicks | Joined from GA4 or Search Console, if connected | Spotting high-traffic pages stuck in chains |

### redirect_chains export (dedicated redirect report)

Export from **Reports > Redirects > Redirect Chains**. This report has already traced the chains for you. Typical columns:

| Column | What it is |
|---|---|
| Address | The starting URL |
| Final Address | Where the chain ends |
| Number of Redirects | Hop count |
| Redirect Loop | TRUE if it loops |
| Final Status Code | Status at the end of the chain |
| Address 1 / Status Code 1 / Address 2 / Status Code 2 ... | Each hop in order |

If you are given this report, the chains are pre-traced. Just read, sort by Number of Redirects, and flag loops and any Final Status Code that is not 200.

## Sitebulb

Export a **URL List** or an **Audit** export as CSV or XLSX. Column names differ but the concepts map cleanly:

| Sitebulb column | Maps to |
|---|---|
| URL | Address |
| HTTP Status Code | Status Code |
| Indexable | Indexability |
| Indexability / No Index Reason | Indexability Status |
| Page Title | Title 1 |
| Meta Description | Meta Description 1 |
| Canonical URL | Canonical Link Element 1 |
| Redirect URL / Redirect Location | Redirect URL |
| No. of Internal Links In / Internal Inlinks | Inlinks |
| Crawl Depth | Crawl Depth |
| Word Count | Word Count |

## Ahrefs Site Audit

Export the **Page Explorer** or **All issues** data as CSV:

| Ahrefs column | Maps to |
|---|---|
| URL / Page URL | Address |
| HTTP code / Status code | Status Code |
| Indexability | Indexability |
| Title | Title 1 |
| Meta description | Meta Description 1 |
| Canonical URL | Canonical Link Element 1 |
| Redirect URL / Final URL | Redirect URL |
| Internal links to URL / Inlinks | Inlinks |
| Depth | Crawl Depth |
| Word count | Word Count |
| Organic traffic | Sessions / traffic signal |

Ahrefs sometimes splits issues across multiple export files (one per issue type). If the user gives you several files, read them all and join on the URL column.

## How to trace a redirect chain from a flat export

If you have an `internal_all` style export (one row per URL with a Redirect URL column) and not a pre-traced chain report, build the chains yourself:

1. Take every row with a 3xx status code. Each one is the start of a hop: `Address` redirects to `Redirect URL`.
2. For each redirecting URL, look up its `Redirect URL` in the dataset. Find that row. Read its status.
3. If that row also redirects, follow it again. Keep going.
4. Stop when you reach a row with a 200 (a real page), a 404 or 5xx (a dead end), or a URL already seen in this chain (a loop).
5. Count the hops. Record the full path with the status at every step.
6. A redirect that points to a URL not in the crawl: note it as "destination not crawled" and report the chain up to that point.

Watch for loops: if you revisit a URL already in the current chain, stop immediately and flag it as a loop. Do not follow it forever.

## When traffic data is present

Any column joined from Google Analytics 4 (Sessions, Users) or Search Console (Clicks, Impressions) is gold. A redirect chain or a 404 on a page with real historical traffic is far more urgent than the same issue on a page nobody visits. Always surface those first. If no traffic column exists, say so and suggest the user connect GA4 or Search Console in their crawler and re-run the crawl for a sharper priority order.
