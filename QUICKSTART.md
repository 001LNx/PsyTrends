# PsyTrends - Quick Start Guide

## What is This?

PsyTrends is an intelligent social media trends analysis system that:
- Pulls trending keywords from Twitter, Reddit, TikTok, and Facebook
- Analyzes them with sentiment scoring
- Uses machine learning to forecast trend impacts on social behavior
- Generates detailed reports for G7 countries + China, Russia, Mexico

## Quick Start (5 Minutes)

### 1. Run Demo (No API Keys Needed)

```bash
cd /Users/ellenfrances/Documents/PsyTrends
python dashboard.py
```

This generates:
- `report.txt` - Human-readable trends report
- `report.json` - Machine-readable data
- `trends_data.csv` - Raw data

### 2. View Results

The report shows:
- **Top Rising Trends** - Keywords gaining influence
- **Top Falling Trends** - Keywords losing relevance  
- **Country Summaries** - Per-country trend analysis

### 3. Integrate Real APIs (Optional)

Edit `.env` and add your credentials:
```
TWITTER_API_KEY=your_key
REDDIT_CLIENT_ID=your_id
# ... etc
```

Then run again - system uses real data instead of synthetic.

## File Structure

```
PsyTrends/
├── intel.py          # Data collection & processing
├── dashboard.py      # Analysis & reporting
├── scheduler.py      # 24-hour automation
├── .env              # API credentials
├── requirements.txt  # Python dependencies
├── README.md         # Full documentation
├── report.txt        # Latest analysis report
├── report.json       # Machine-readable results
└── trends_data.csv   # Trend dataset
```

## Key Features

| Feature | Description |
|---------|-------------|
| **Multi-Source** | Aggregates from 4 social platforms |
| **ML Forecasting** | ARIMA time-series predictions |
| **Impact Scoring** | Sentiment × Volume = Impact |
| **24h Cycle** | Automate with scheduler.py |
| **Global Coverage** | 10 major countries |
| **Demo Ready** | Works without API keys |

## Common Tasks

### Run Single Analysis
```bash
python dashboard.py
```

### Run 24-Hour Automated Cycle
```bash
python scheduler.py
```

### Use Real API Data
1. Get API credentials from Twitter, Reddit, TikTok, Facebook
2. Add to `.env` file
3. Run `dashboard.py`

### Access Report Data
- **Text Report**: `report.txt` (human-readable)
- **JSON Data**: `report.json` (programmatic access)
- **Raw Data**: `trends_data.csv` (spreadsheet-compatible)

## Understanding Reports

### Impact Score Interpretation
- **High Positive** (+50000+): Rapidly rising, high influence potential
- **Positive** (+10000-50000): Growing trend
- **Neutral** (-10000 to +10000): Stable trend
- **Negative** (-50000+): Rapidly declining

### Sentiment Score
- **1.0**: Positive keywords (innovation, growth, success)
- **0.5**: Neutral keywords
- **0.0**: Negative keywords (crisis, risk, decline)

### Rising vs Falling
Shows whether a trend is gaining or losing momentum based on forecasted volume.

## Troubleshooting

**No forecasts showing?**
- First run generates synthetic data - this is normal
- Run again in a few minutes

**Want different countries?**
- Edit `intel.py` line: `self.countries = {...}`
- Add/remove country codes

**Memory issues?**
- Reduce historical days in `intel.py`
- Run on more powerful machine
- Use batch processing

## Next Steps

1. ✅ Run `python dashboard.py` to see it work
2. ✅ Check `report.txt` for results
3. ✅ Edit `.env` and add API keys (optional)
4. ✅ Setup `scheduler.py` for automation
5. ✅ Read `README.md` for advanced usage

## API Setup (Optional but Recommended)

### Twitter/X
- Go to https://developer.twitter.com/
- Create app, get API keys
- Add to `.env`

### Reddit  
- Go to https://www.reddit.com/prefs/apps
- Create app, get credentials
- Add to `.env`

### Facebook
- Go to https://developers.facebook.com/
- Create app, get credentials
- Add to `.env`

### TikTok
- Official API limited; uses mock data in demo

## Support

- Full docs: See `README.md`
- Issues: Check `.env` configuration
- Questions: Review code comments

---

**Ready? Run:** `python dashboard.py`
