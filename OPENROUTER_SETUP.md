# OpenRouter Integration Guide

This guide explains how to configure GPT Researcher to use OpenRouter as your LLM provider.

## What is OpenRouter?

OpenRouter provides access to multiple AI models through a single API, including models from OpenAI, Anthropic, Google, and others. This allows you to:
- Access a variety of models without managing multiple API keys
- Compare different models for your research tasks
- Take advantage of competitive pricing
- Use models that might not be directly available in your region

## Setup Instructions

### 1. Get an OpenRouter API Key

1. Visit [OpenRouter](https://openrouter.ai)
2. Sign up for an account
3. Navigate to the API Keys section
4. Create a new API key
5. Copy your API key (starts with `sk-or-v1-`)

### 2. Configure Environment Variables

Update your `.env` file with the following configuration:

```env
# OpenRouter Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here

# LLM Configuration using OpenRouter
FAST_LLM=openrouter:anthropic/claude-3-haiku-20240307
SMART_LLM=openrouter:anthropic/claude-3-5-sonnet-20241022
STRATEGIC_LLM=openrouter:openai/o1-mini

# Optional: Rate limiting (requests per second, defaults to 1.0)
OPENROUTER_LIMIT_RPS=2.0

# Search API (still required)
TAVILY_API_KEY=your_tavily_api_key
```

### 3. Model Selection

OpenRouter supports many models. Here are some recommended configurations:

#### Budget-Conscious Setup
```env
FAST_LLM=openrouter:meta-llama/llama-3.1-8b-instruct:free
SMART_LLM=openrouter:microsoft/wizardlm-2-8x22b
STRATEGIC_LLM=openrouter:anthropic/claude-3-haiku-20240307
```

#### Balanced Performance
```env
FAST_LLM=openrouter:anthropic/claude-3-haiku-20240307
SMART_LLM=openrouter:anthropic/claude-3-5-sonnet-20241022
STRATEGIC_LLM=openrouter:openai/gpt-4o
```

#### High Performance
```env
FAST_LLM=openrouter:anthropic/claude-3-5-sonnet-20241022
SMART_LLM=openrouter:openai/gpt-4o
STRATEGIC_LLM=openrouter:openai/o1-preview
```

### 4. Test Your Configuration

Run the provided test script to verify everything is working:

```bash
python test_openrouter.py
```

This script will:
- Verify your API key is configured
- Test LLM provider initialization
- Make a test API call
- Optionally run a simple research task

## Model Usage Guidelines

### FAST_LLM
Used for: Quick summaries, source curation, simple tasks
Recommended models:
- `anthropic/claude-3-haiku-20240307` - Fast and cost-effective
- `meta-llama/llama-3.1-8b-instruct:free` - Free option
- `google/gemini-flash-1.5` - Good balance of speed and quality

### SMART_LLM
Used for: Research report writing, complex analysis, reasoning
Recommended models:
- `anthropic/claude-3-5-sonnet-20241022` - Excellent for research writing
- `openai/gpt-4o` - Strong general performance
- `google/gemini-pro-1.5` - Good alternative option

### STRATEGIC_LLM
Used for: Research planning, strategy, complex reasoning
Recommended models:
- `openai/o1-preview` - Best for complex reasoning (slower, more expensive)
- `openai/o1-mini` - Faster reasoning model
- `anthropic/claude-3-opus-20240229` - Excellent for strategic thinking

## Rate Limiting

OpenRouter enforces rate limits. Configure `OPENROUTER_LIMIT_RPS` to avoid hitting these limits:

```env
# Conservative setting (recommended for free tier)
OPENROUTER_LIMIT_RPS=0.5

# Standard setting
OPENROUTER_LIMIT_RPS=2.0

# Aggressive setting (only if you have high limits)
OPENROUTER_LIMIT_RPS=5.0
```

## Cost Management

Monitor your usage on the OpenRouter dashboard. Some tips:
- Use faster/cheaper models for FAST_LLM
- Reserve expensive models for SMART_LLM and STRATEGIC_LLM
- Set spending limits in your OpenRouter account
- Consider using free models for development/testing

## Troubleshooting

### Common Issues

1. **"OPENROUTER_API_KEY not found"**
   - Ensure your API key is in the `.env` file
   - Check that you're loading the `.env` file correctly

2. **Rate limit errors**
   - Reduce `OPENROUTER_LIMIT_RPS` value
   - Check your OpenRouter account limits

3. **Model not found errors**
   - Verify the model name is correct
   - Check OpenRouter's model availability
   - Some models may require special access

4. **API connection errors**
   - Check your internet connection
   - Verify your API key is valid
   - Check OpenRouter's status page

### Model Names

Get current model names from [OpenRouter's models page](https://openrouter.ai/models). Use the format:
```
openrouter:provider/model-name
```

Examples:
- `openrouter:anthropic/claude-3-5-sonnet-20241022`
- `openrouter:openai/gpt-4o`
- `openrouter:meta-llama/llama-3.1-8b-instruct`

## Benefits of Using OpenRouter

1. **Model Diversity**: Access to models from multiple providers
2. **Cost Optimization**: Competitive pricing and free tier options
3. **Reliability**: Fallback options if one provider has issues
4. **Simplicity**: Single API key for multiple models
5. **Flexibility**: Easy to switch between models for different tasks

## Migration from OpenAI

If you're migrating from OpenAI, your existing configuration:
```env
FAST_LLM=openai:gpt-4o-mini
SMART_LLM=openai:gpt-4o
```

Becomes:
```env
FAST_LLM=openrouter:openai/gpt-4o-mini
SMART_LLM=openrouter:openai/gpt-4o
```

You can access the same OpenAI models through OpenRouter, often at better prices.