# PsyTrends: Social Media Trends Impact Prediction System

PsyTrends is a Python-based system that pulls trending keywords from multiple social media platforms, analyzes them into structured datasets, and uses machine learning algorithms to forecast their projected impact on social decision-making patterns across major countries.

## Features

- **Multi-Platform Data Collection**: Fetches trending keywords from Twitter/X, Reddit, TikTok, and Facebook
- **Data Processing**: Cleans, normalizes, and analyzes keyword data with sentiment scoring
- **ML Forecasting**: Uses ARIMA time series forecasting to predict trend trajectories
- **Impact Projection**: Correlates trend changes with potential social behavior influence
- **Comprehensive Reporting**: Generates detailed 24-hour cycle reports with visualizations and JSON export
- **Global Coverage**: Analyzes trends across G7 countries plus China, Russia, and Mexico

## Installation

### Prerequisites
- Python 3.10+
- pip or conda

### Setup

1. Clone or download the project
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure API credentials:
   - Edit `.env` file with your API keys:
     - **Twitter/X**: Get keys from [Twitter Developer Portal](https://developer.twitter.com/)
     - **Reddit**: Get credentials from [Reddit App Registration](https://www.reddit.com/prefs/apps)
     - **TikTok**: API access (limited for trends)
     - **Facebook**: Get app credentials from [Facebook Developers](https://developers.facebook.com/)

   Without credentials, the system runs in **demo mode** using synthetic data.

## Usage

### Run Full Analysis Cycle

```bash
python dashboard.py
```

This will:
1. Collect trends from available social media platforms
2. Process and analyze the data
3. Generate ML forecasts for each trend
4. Create reports (text and JSON)
5. Display the report in console

### Output Files

After running, the following files are generated:
- `report.txt` - Formatted text report with trends and projections
- `report.json` - Machine-readable JSON with all forecast data
- `trends_data.csv` - Raw collected and processed trends data

## Report Format

The generated report includes:

1. **Top Rising Trends**: Keywords with highest positive projected impact
   - Current Volume
   - Forecasted Volume
   - Impact Score (volume change × sentiment)
   - Sentiment Score

2. **Top Falling Trends**: Keywords with highest negative projected impact

3. **Country Summaries**: 
   - Total trends analyzed per country
   - Rising vs. falling trend count
   - Average impact score

## Architecture

### Core Modules

**intel.py** - Data Collection & Processing
- `TwitterTrendsFetcher`: Fetches trends from Twitter API
- `RedditTrendsFetcher`: Extracts trending keywords from Reddit
- `DataCollector`: Unified data collection from all platforms
- `simple_sentiment_score()`: Sentiment analysis for keywords
- `generate_synthetic_history()`: Creates demo data for testing

**dashboard.py** - Analysis & Reporting
- `forecast_trends()`: Time series forecasting using ARIMA
- `generate_report()`: Formats and exports results
- `run_cycle()`: Orchestrates full analysis pipeline

## Data Flow

```
Social Media APIs
        ↓
   intel.py (collect_and_process)
        ↓
   Data Processing (clean, normalize, sentiment)
        ↓
   Synthetic History (for forecasting)
        ↓
   dashboard.py (forecast_trends)
        ↓
   Impact Projection & Reporting
        ↓
   Output (report.txt, report.json, trends_data.csv)
```

## Forecasting Algorithm

The system uses **ARIMA (AutoRegressive Integrated Moving Average)** for time series forecasting:

- **With 5+ data points**: Full ARIMA(1,1,1) model for complex patterns
- **With 2-4 data points**: Exponential trend extrapolation
- **Impact Score**: Calculated as `(forecasted_volume - current_volume) × sentiment_score`

## Impact Projection Logic

**Impact on Social Decision Making** is defined as influence on general social behavior patterns:

- **Sentiment Score**: Positive words increase impact, negative words decrease
- **Volume Change**: Larger trend increases indicate higher impact potential
- **Combined Impact**: Impact score reflects both trend magnitude and sentiment polarity

## Demo Mode

Without API credentials, the system generates synthetic data simulating:
- 10 countries across 14 days
- 5 major trending keywords
- Realistic volume fluctuations and trends
- Consistent sentiment patterns

This allows testing and demonstration without API access.

## Scheduling (24-Hour Cycle)

To run analysis automatically every 24 hours:

```python
import schedule
from dashboard import run_cycle

schedule.every(24).hours.do(run_cycle)

while True:
    schedule.run_pending()
    time.sleep(1)
```

Or use system cron/Task Scheduler:
```bash
# Cron example (Unix/Linux/Mac)
0 0 * * * /path/to/.venv/bin/python /path/to/dashboard.py >> /path/to/psytrends.log 2>&1
```

## Configuration

### Environment Variables (.env)

```
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_TOKEN_SECRET=your_token_secret

REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USER_AGENT=your_agent

TIKTOK_API_KEY=your_key

FACEBOOK_APP_ID=your_id
FACEBOOK_APP_SECRET=your_secret
```

### Customization

Edit `dashboard.py` to:
- Change forecast periods: `forecast_trends(df, periods=3)`
- Modify report format: Customize `generate_report()` function
- Adjust data retention: Change CSV storage logic

Edit `intel.py` to:
- Modify sentiment keywords in `simple_sentiment_score()`
- Change countries analyzed in `DataCollector.countries` dict
- Adjust synthetic data generation parameters

## Limitations

1. **API Rate Limits**: Twitter, Reddit, and Facebook have rate limits; implement backoff strategies for production
2. **Real-Time Accuracy**: Synthetic demo data provides illustration, real data accuracy depends on API coverage
3. **Prediction Uncertainty**: ARIMA forecasts best for stable, historical trends; unexpected events may invalidate predictions
4. **Data Privacy**: Focuses only on aggregated trends; no personal data collected

## Future Enhancements

1. **Advanced ML Models**: LSTM neural networks for complex patterns
2. **NLP Analysis**: Deeper semantic understanding of trending topics
3. **Web Dashboard**: Real-time visualization with Flask/FastAPI
4. **Database Storage**: PostgreSQL/MongoDB for scalable data retention
5. **Alert System**: Notify on significant trend changes
6. **Multi-Language Support**: Analyze trends across different languages
7. **Custom Weights**: Adjustable sentiment and volume weighting per country

## Troubleshooting

**No forecasts generated**
- Ensure data has at least 2 data points per group
- Check that `date` column exists in DataFrame
- Verify ARIMA model parameters are appropriate

**API connection errors**
- Verify credentials in `.env` file are correct
- Check internet connectivity
- Ensure API keys have necessary permissions

**Memory issues with large datasets**
- Reduce historical data retention period
- Implement batch processing
- Use streaming data architecture for production

## License

MIT License - Feel free to use and modify for your projects

## Support

For issues or questions, please refer to the project documentation or create an issue in the repository.

---

**Version**: 1.0  
**Last Updated**: April 2026  
**Author**: PsyTrends Development Team