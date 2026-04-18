import pandas as pd
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import seaborn as sns
import schedule
import time
import json
from intel import DataCollector

# Set up matplotlib for non-interactive mode
plt.switch_backend('Agg')
sns.set_theme()

def forecast_trends(df, periods=1):
    forecasts = []
    if len(df) == 0:
        print("DEBUG: Empty dataframe")
        return pd.DataFrame()
    
    # Group by country and keyword, ensure we have enough data
    for (country, keyword), group in df.groupby(['country', 'keyword']):
        # Sort by date to ensure time series is in order
        if 'date' in group.columns:
            group = group.sort_values('date')
        
        volume_data = group['volume'].values
        
        if len(volume_data) < 2:  # Need at least 2 data points
            continue
        
        try:
            # Try ARIMA for better forecasting
            if len(volume_data) >= 5:  # Use ARIMA only if we have enough data
                import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    model = ARIMA(volume_data, order=(1, 1, 1))
                    model_fit = model.fit()
                    forecast_result = model_fit.forecast(steps=periods)
                    # Extract forecast value - could be Series or ndarray
                    forecast_val = forecast_result[0] if hasattr(forecast_result, '__getitem__') else forecast_result.values[0]
            else:
                # Simple exponential smoothing for short time series
                # Use last value with simple trend
                recent_trend = (volume_data[-1] - volume_data[0]) / len(volume_data)
                forecast_val = volume_data[-1] + recent_trend * periods
            
            current_vol = float(volume_data[-1])
            sentiment = group['sentiment_score'].mean()
            
            # Impact is a measure of trend change weighted by sentiment
            impact = (forecast_val - current_vol) * sentiment
            
            forecasts.append({
                'country': country,
                'keyword': keyword,
                'current_volume': current_vol,
                'forecasted_volume': float(forecast_val),
                'impact_projection': float(impact),
                'trend_direction': 'rising' if forecast_val > current_vol else 'falling',
                'sentiment_score': float(sentiment),
                'data_points': len(volume_data)
            })
        except Exception as e:
            # Skip keywords that can't be forecasted
            continue
    
    return pd.DataFrame(forecasts)

def generate_report(forecast_df, output_prefix='report'):
    report = f"\n{'='*80}\n"
    report += f"PsyTrends Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"{'='*80}\n\n"
    
    if len(forecast_df) == 0:
        report += "No trends data available for forecasting.\n"
        report += "Please ensure API credentials are configured or run with synthetic data.\n\n"
    else:
        report += f"Total keywords analyzed: {len(forecast_df)}\n"
        report += f"Countries included: {forecast_df['country'].nunique()}\n\n"
        
        # Top rising trends
        report += "TOP RISING TRENDS:\n"
        report += "-" * 80 + "\n"
        top_rising = forecast_df.nlargest(10, 'impact_projection')
        for idx, row in top_rising.iterrows():
            report += f"  {row['keyword']} ({row['country']})\n"
            report += f"    Current Volume: {row['current_volume']:,.0f}\n"
            report += f"    Forecasted Volume: {row['forecasted_volume']:,.0f}\n"
            report += f"    Impact Score: {row['impact_projection']:.2f}\n"
            report += f"    Sentiment: {row['sentiment_score']:.2f}\n\n"
        
        # Top falling trends
        report += "\nTOP FALLING TRENDS:\n"
        report += "-" * 80 + "\n"
        top_falling = forecast_df.nsmallest(10, 'impact_projection')
        for idx, row in top_falling.iterrows():
            report += f"  {row['keyword']} ({row['country']})\n"
            report += f"    Current Volume: {row['current_volume']:,.0f}\n"
            report += f"    Forecasted Volume: {row['forecasted_volume']:,.0f}\n"
            report += f"    Impact Score: {row['impact_projection']:.2f}\n"
            report += f"    Sentiment: {row['sentiment_score']:.2f}\n\n"
        
        # By country summary
        report += "\nCOUNTRY SUMMARIES:\n"
        report += "-" * 80 + "\n"
        for country in sorted(forecast_df['country'].unique()):
            country_df = forecast_df[forecast_df['country'] == country]
            avg_impact = country_df['impact_projection'].mean()
            trending_up = len(country_df[country_df['trend_direction'] == 'rising'])
            trending_down = len(country_df[country_df['trend_direction'] == 'falling'])
            
            report += f"\n{country}:\n"
            report += f"  Total Trends: {len(country_df)}\n"
            report += f"  Rising Trends: {trending_up}\n"
            report += f"  Falling Trends: {trending_down}\n"
            report += f"  Average Impact: {avg_impact:.2f}\n"
    
    report += f"\n{'='*80}\n"
    
    # Save to text file
    with open(f'{output_prefix}.txt', 'w') as f:
        f.write(report)
    
    # Save to JSON
    if len(forecast_df) > 0:
        json_data = forecast_df.to_dict('records')
        with open(f'{output_prefix}.json', 'w') as f:
            json.dump(json_data, f, indent=2, default=str)
    
    print(report)
    print(f"Report saved to {output_prefix}.txt and {output_prefix}.json")

def run_cycle():
    collector = DataCollector()
    df = collector.collect_and_process()
    forecast_df = forecast_trends(df)
    generate_report(forecast_df)

if __name__ == "__main__":
    # Run once for demo
    run_cycle()
    # Schedule for every 24 hours
    # schedule.every(24).hours.do(run_cycle)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)