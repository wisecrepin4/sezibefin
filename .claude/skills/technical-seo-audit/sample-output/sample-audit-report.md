# Technical SEO Audit: brightwaterplumbing.com.au

**Pages analysed:** 60  |  **Crawl source:** Screaming Frog (internal_all export)  |  **Date:** 20 May 2026

This is the report the Technical SEO Audit skill produces when you run it on `sample-input/sample-crawl-screamingfrog.csv`. It shows you what a finished audit looks like.

---

## Health snapshot

| Check | Result |
|---|---|
| Redirect chains | 6 |
| Redirect loops | 1 |
| Chains ending in an error | 2 |
| Duplicate title tags | 1 group (4 pages) |
| Duplicate meta descriptions | 1 group (3 pages) |
| Indexing and crawl blocks | 7 pages |
| Broken internal links | 3 dead pages still linked |
| Orphan pages | 2 |
| **Overall verdict** | **Needs work. One critical issue is actively losing traffic.** |

The site basics are sound. The problem is a layer of old redirects and broken links nobody has cleared out, and one of them is draining what used to be a strong traffic page straight into a dead end.

---

## Redirect chains and loops

A redirect chain is when one web address sends a visitor to a second address, which sends them to a third, and so on. Each extra hop slows the page down, wastes the time Google spends crawling your site, and leaks a little ranking strength. A chain that ends at a dead page (a 404) wastes all of it.

**The worst one, fix this first.**

`/emergency-plumbing-melbourne` redirects five times and lands on a dead page. The starting address used to pull around **2,980 visits a month**. Today anyone who clicks an old link, an old ad, or an old search result gets bounced five times and ends on a "page not found". That traffic and its ranking strength are being thrown away.

`/emergency-plumbing-melbourne (301) → /services/emergency-plumbing (301) → /services/emergency-plumber (301) → /services/24-hour-plumber (301) → /melbourne/emergency-plumber (301) → /emergency-plumber (404)`

The fix: decide which live page should own emergency plumbing (likely a new or restored `/services/emergency-plumbing` page), then point `/emergency-plumbing-melbourne` straight at it in one hop. Do not point it at the next URL in the chain. Point it at the final live destination.

### Every chain found

| # | Chain (status at each hop) | Hops | Ends in | Severity | Fix |
|---|---|---|---|---|---|
| 1 | /emergency-plumbing-melbourne → /services/emergency-plumbing → /services/emergency-plumber → /services/24-hour-plumber → /melbourne/emergency-plumber → /emergency-plumber | 5 | 404 | Critical | Point the start URL at one live emergency plumbing page in a single hop |
| 2 | /about → /about-us → /about (loop) | Loop | Loop | Critical | Point both `/about` and `/about-us` straight at the real page, `/about-brightwater` |
| 3 | /hot-water-repairs → /services/hot-water → /services/hot-water-systems → /services/hot-water-repair | 3 | 200 | High | Point `/hot-water-repairs` straight at `/services/hot-water-repair` |
| 4 | /old-pricing → /pricing-2023 → /pricing-old | 2 | 404 | Critical | Point `/old-pricing` straight at the live `/pricing` page |
| 5 | /blocked-drains → /blog/blocked-drain-tips → /blog/how-to-clear-a-blocked-drain | 2 | 200 | Medium | Point `/blocked-drains` straight at the final blog post |
| 6 | /gas-fitting → /services/gas → /services/gas-fitting | 2 | 200 | Medium | Point `/gas-fitting` straight at `/services/gas-fitting` |
| 7 | /contact-us-page → /contact-us → /contact | 2 | 200 | Medium | Point `/contact-us-page` straight at `/contact`. Note hop 1 is a 302 (temporary) and should be a 301 (permanent) |

**The loop (chain 2)** is its own problem. `/about` and `/about-us` redirect to each other forever, so nobody, human or Google, ever reaches a real page. Nine internal links still point at `/about` and five point at `/about-us`, while the real page, `/about-brightwater`, has only three. Repoint both redirects at `/about-brightwater` and update the internal links to point there directly.

---

## Duplicate title tags

The title tag is the clickable headline that shows in Google. When several pages share one title, Google cannot tell them apart and may show none of them well.

**"Plumber Melbourne | Brightwater Plumbing"** is used on 4 pages:

- /plumber-richmond
- /plumber-hawthorn
- /plumber-camberwell
- /plumber-kew

These are suburb pages, so they are also competing with each other for the same search (this is called keyword cannibalisation). Give each a title that names its suburb, for example "Richmond Plumber | Fast Local Service | Brightwater Plumbing". The H1 on each page is already suburb-specific, so the page content is fine. Only the titles need fixing.

---

## Duplicate meta descriptions

The meta description is the grey summary text under the title in Google. It will not make or break rankings, but unique text earns more clicks.

**"Expert plumbing tips and advice from the team at Brightwater Plumbing in Melbourne."** is used on 3 pages:

- /blog/tag/tips
- /blog/tag/drains
- /blog/tag/hot-water

See the indexing section below. These tag pages have a bigger problem than their meta text.

---

## Indexing and crawl blocks

This section covers pages Google is told to ignore, or pages it is allowed to see that it would be better off ignoring.

**Set to "noindex" but should be indexed:**

- **/services/commercial-plumbing**: this is a full service page with around 960 words of real content, and it is set to noindex, which tells Google to leave it out of search results entirely. For a commercial plumbing company this is a money page being hidden. Remove the noindex tag. This is one of the highest-value fixes on the site and it is a five-minute change.

**Blocked by robots.txt but still linked internally:**

- **/quote**: this page is blocked in your robots.txt file, yet 14 internal links point at it. If this is your quote form, blocking it is usually fine, but the page should still load for customers. Confirm the form works, and if you want Google to index a quote landing page, unblock it.

**Indexable but probably should not be:**

- /blog/tag/tips, /blog/tag/drains, /blog/tag/hot-water: these blog tag pages have only 60 to 70 words each. Thin pages like these add little and can dilute the quality signal of the blog. Set them to noindex, or turn them off in your blog settings.

**Canonical mismatch:**

A canonical tag tells Google which page is the "main" version when content is similar. Here the tags form a chain:

- /services/drain-cleaning points its canonical at /services/drain-camera-inspection
- /services/drain-camera-inspection points its canonical at /services/blocked-drains-service

Google may ignore a canonical that points at another canonicalised page. Point both `/services/drain-cleaning` and `/services/drain-camera-inspection` straight at the one page you want to rank, `/services/blocked-drains-service`, or give each page its own distinct content and let each be its own canonical.

---

## Broken internal links

These pages are dead, but your own website still links to them. Every link is a dead end for a customer and a wasted crawl for Google.

| Dead page | Status | Internal links pointing at it | Fix |
|---|---|---|---|
| /emergency-plumber | 404 | 7 | This is also the end of the worst redirect chain. Once you build the live emergency plumbing page, update these 7 links to point at it |
| /booking | 503 | 11 | A 503 means the server is failing to load this page. If this is your online booking page, it is down and 11 pages link customers to it. Get your developer to check it urgently |
| /services/leak-detection | 404 | 5 | The page has been deleted. Either restore it or update the 5 links to point at `/services/leak-repairs`, which is live and covers the same topic |

`/booking` returning a 503 is a customer problem as much as an SEO problem. Treat it as urgent.

---

## Orphan pages

An orphan page is a page with zero internal links pointing at it. Google mainly finds pages by following links, so an orphan is hard to find and hard to rank.

- **/services/bathroom-plumbing**: a real service page with 740 words and no internal links at all. This is a service you sell, sitting invisible. Add links to it from `/services` and from related pages like `/services/tap-repairs`.
- **/blog/winter-plumbing-checklist**: a 560-word blog post with no internal links. Add a link from `/blog` and from related posts such as `/blog/burst-pipe-what-to-do`.

---

## Top 5 fixes to start with

1. **Fix the 5-hop chain on /emergency-plumbing-melbourne.** It used to pull around 2,980 visits a month and now ends on a dead page. Build or restore the emergency plumbing page and point the old URL straight at it. *Severity: Critical. Effort: Medium.*
2. **Get /booking working again.** A 503 error means your booking page is down, and 11 pages send customers to it. *Severity: Critical. Effort: Medium, needs your developer.*
3. **Remove the noindex tag from /services/commercial-plumbing.** A full commercial service page is hidden from Google for no reason. *Severity: Critical. Effort: Easy.*
4. **Repair the broken internal links** to /emergency-plumber and /services/leak-detection so customers and Google stop hitting dead ends. *Severity: High. Effort: Easy.*
5. **Give the 4 suburb pages unique titles.** Stop them competing with each other and help each rank for its own suburb. *Severity: High. Effort: Easy.*

---

## What this audit could not check

This audit reads your crawl data, which is code and numbers. It cannot see your website the way a customer does. It has **not** checked, and cannot check:

- Whether the layout is broken on a phone
- Whether a pop-up is covering the main content on mobile
- Whether images are loading properly
- Whether the page is slow to appear or jumps around as it loads
- Whether anything simply looks wrong

Those issues are real and they still cost you customers and rankings. Before you sign off, open your top 10 pages on an actual phone and look at them. A human still has to do that part.

---

## What is working well

- Your homepage and core service pages all return a healthy 200 status and are set to be indexed. The foundations are solid.
- Blog posts have genuine depth, most sitting between 800 and 1,200 words.
- Most service pages have a reasonable spread of internal links pointing at them, so Google can find them.
- The crawl shows no 5xx server errors beyond the single `/booking` page, which means your hosting is generally stable.

---

## Bottom line

Fix the 5-hop redirect chain on `/emergency-plumbing-melbourne` first. Restoring that one path reconnects a page that used to earn around 2,980 visits a month and stops Google pouring crawl budget and ranking strength into a dead end.
