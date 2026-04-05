# 🍠 Sweet Potato Station Hunter — Egypt & Sudan

Finds stations, farms, and exporters in **Egypt and Sudan** that need **sorting and cleaning machines**. Runs on the **1st of every month**.

---

## How It Generates Leads

```
config.json → search_queries (what to search)
            → score_keywords (how to score results)
                ↓
DuckDuckGo search → score each result 1–10
                ↓
Always add 8 verified seed leads (real stations & portals)
                ↓
Load reports/leads_history.json (all previous leads)
                ↓
Merge today + history → remove duplicates by URL
                ↓
Excel: Dashboard | 📅 Today tab | 📚 All Leads | 🔥 High Priority
                ↓
Email + Google Drive upload + save history
```

---

## Excel Structure (4 Sheets)

| Sheet | Content |
|-------|---------|
| **Dashboard** | KPI summary of stations found |
| **📅 2026-04-01** | This month's new stations |
| **📚 All Stations** | Every station ever found — all months combined |
| **🔥 High Priority** | Score ≥ 8 — act first |

---

## config.json Keywords

Edit `search_queries` to add more search terms (Arabic or English).
Edit `score_keywords` to adjust how results are scored:
- `high_value`: +3 points per match (most important terms)
- `medium_value`: +2 points per match
- `location`: +1 point per match

---

## GitHub Secrets Required

| Secret | Value |
|--------|-------|
| `SENDER_EMAIL` | Gmail address |
| `SENDER_PASSWORD` | 16-char Gmail App Password |
| `RECIPIENT_EMAIL` | Where to send the report |
| `DRIVE_FOLDER_ID` | Google Drive folder ID |

Run manually: **Actions → Monthly Sweet Potato Station Hunter → Run workflow**
