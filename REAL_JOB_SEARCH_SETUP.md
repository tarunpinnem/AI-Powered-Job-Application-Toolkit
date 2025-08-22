# AI Career Success Platform - Real Job Search Setup

## Overview
This platform now includes **real job search integration** using the LinkedIn Job Search API (via RapidAPI), which provides access to live job listings directly from LinkedIn's professional network.

## Quick Setup (2 minutes)

### 1. Get Your Free API Key
1. Visit [RapidAPI LinkedIn Job Search](https://rapidapi.com/linkedin-job-search-api/api/linkedin-job-search-api)
2. Sign up for a free account (if you don't have one)
3. Subscribe to the **LinkedIn Job Search API** (has a generous free tier)
4. Copy your RapidAPI key from the dashboard

### 2. Configure Environment Variables
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your keys:
   ```bash
   # Required for real job search from LinkedIn
   RAPIDAPI_KEY=your_rapidapi_key_here
   
   # Required for AI features
   OPENAI_API_KEY=your_openai_key_here
   ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

## How It Works

### Real Job Search Features
- **Live LinkedIn Data**: Pulls real jobs directly from LinkedIn's professional network
- **Fresh Listings**: Jobs posted within the last hour for maximum relevance
- **Smart Filtering**: Matches jobs based on your skills, industry, and location preferences
- **AI Enhancement**: GPT-4 powered job matching and personalized insights
- **Fallback System**: Graceful degradation when APIs are unavailable

### Job Search Flow
1. **Extract Skills**: Analyzes your resume to identify key skills and experience
2. **Fetch Fresh Jobs**: Gets the latest job postings from LinkedIn (last hour)
3. **Smart Filtering**: Filters jobs by industry, location, and skill relevance
4. **AI Matching**: Uses GPT-4 to calculate personalized match scores
5. **Enhanced Results**: Returns top matches with AI insights and career advice

### API Integration Details
- **Primary**: LinkedIn Job Search API (RapidAPI) - Direct access to LinkedIn jobs
- **Backup**: Curated job listings for immediate functionality
- **Fallback**: Graceful degradation if external APIs fail

## Configuration Options

### Environment Variables
```bash
# Job Search Configuration
RAPIDAPI_KEY=your_key              # Required for real job search
JSEARCH_API_KEY=your_key          # Alternative key name

# AI Configuration  
OPENAI_API_KEY=your_key           # Required for AI features

# Optional Features
ENABLE_RATE_LIMITING=false        # Enable API rate limiting
ENABLE_DEBUG_MODE=true            # Show detailed logs
```

### Job Search Parameters
- **Industries**: Technology, Marketing, Finance, and more
- **Locations**: City, state, or "Remote" for remote positions
- **Experience**: Automatically matches based on resume content
- **Job Types**: Full-time, part-time, contractor positions

## API Status Indicators

The platform shows real-time status:
- ✅ **Real Jobs**: Connected to live job boards
- 📝 **Curated Jobs**: High-quality backup listings  
- ⚠️ **Fallback Mode**: Basic functionality only

## Free Tier Limits

### LinkedIn Job Search API (RapidAPI)
- **Free Tier**: 500 requests/month
- **Usage**: ~1 request per job search
- **Capacity**: ~500 job searches per month
- **Upgrade**: Paid plans available for higher volume
- **Fresh Data**: Jobs posted within the last hour

### OpenAI API
- **Pay-per-use**: ~$0.01-0.03 per job search
- **Monthly Cost**: Typically under $5/month for regular use

## Troubleshooting

### No Jobs Found
1. Check internet connection
2. Verify API keys in `.env` file
3. Try different search terms (industry/location)
4. Check API quotas on RapidAPI dashboard

### API Errors
- Platform automatically falls back to curated jobs
- Check logs for specific error messages
- Verify API key permissions

### Performance Issues
- Real job search may take 2-3 seconds
- Results are cached for better performance
- AI processing is optimized for speed

## Portfolio-Grade Features

This implementation demonstrates:
- **Real API Integration**: Production-ready external API usage
- **Error Handling**: Graceful degradation and fallback systems
- **Performance Optimization**: Caching and efficient data processing
- **User Experience**: Seamless real-time job search
- **Scalability**: Ready for production deployment

## Support

For issues or questions:
1. Check the console logs for error details
2. Verify API keys and quotas
3. Test with different search parameters
4. Review the `.env.example` for configuration help
