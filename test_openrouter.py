#!/usr/bin/env python3
"""
Test script to verify OpenRouter configuration for GPT Researcher.

This script tests:
1. OpenRouter API key configuration
2. LLM provider setup and connection
3. Basic chat completion functionality

Run this script to verify your OpenRouter setup before using GPT Researcher.
"""

import asyncio
import os
from dotenv import load_dotenv
from gpt_researcher.utils.llm import get_llm, create_chat_completion
from gpt_researcher.config.config import Config

# Load environment variables
load_dotenv()

async def test_openrouter_setup():
    """Test OpenRouter configuration and connectivity."""
    print("🔧 Testing OpenRouter Setup for GPT Researcher")
    print("=" * 60)
    
    # Check environment variables
    print("\n1. Checking environment variables...")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_key:
        print("❌ OPENROUTER_API_KEY not found in environment variables")
        return False
    else:
        print(f"✅ OPENROUTER_API_KEY found: {openrouter_key[:20]}...")
    
    # Check rate limiting setting
    rate_limit = os.getenv("OPENROUTER_LIMIT_RPS", "1.0")
    print(f"✅ Rate limit setting: {rate_limit} requests per second")
    
    # Load configuration
    print("\n2. Loading GPT Researcher configuration...")
    try:
        config = Config()
        print(f"✅ Configuration loaded successfully")
        print(f"   - FAST_LLM: {config.fast_llm_provider}:{config.fast_llm_model}")
        print(f"   - SMART_LLM: {config.smart_llm_provider}:{config.smart_llm_model}")
        print(f"   - STRATEGIC_LLM: {config.strategic_llm_provider}:{config.strategic_llm_model}")
    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")
        return False
    
    # Test LLM providers
    print("\n3. Testing LLM providers...")
    
    # Test FAST_LLM
    if config.fast_llm_provider == "openrouter":
        print(f"   Testing FAST_LLM ({config.fast_llm_model})...")
        try:
            fast_llm = get_llm(
                config.fast_llm_provider, 
                model=config.fast_llm_model,
                temperature=0.3,
                max_tokens=100
            )
            print(f"   ✅ FAST_LLM provider initialized successfully")
        except Exception as e:
            print(f"   ❌ Failed to initialize FAST_LLM: {e}")
            return False
    
    # Test SMART_LLM  
    if config.smart_llm_provider == "openrouter":
        print(f"   Testing SMART_LLM ({config.smart_llm_model})...")
        try:
            smart_llm = get_llm(
                config.smart_llm_provider,
                model=config.smart_llm_model, 
                temperature=0.4,
                max_tokens=200
            )
            print(f"   ✅ SMART_LLM provider initialized successfully")
        except Exception as e:
            print(f"   ❌ Failed to initialize SMART_LLM: {e}")
            return False
    
    # Test actual API call
    print("\n4. Testing API connectivity...")
    try:
        messages = [{"role": "user", "content": "Hello! Please respond with 'OpenRouter connection successful' to confirm the API is working."}]
        
        response = await create_chat_completion(
            messages=messages,
            model=config.fast_llm_model,
            temperature=0.3,
            max_tokens=50,
            llm_provider=config.fast_llm_provider,
            stream=False
        )
        
        print(f"   ✅ API call successful!")
        print(f"   📨 Response: {response}")
        
    except Exception as e:
        print(f"   ❌ API call failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 OpenRouter setup test completed successfully!")
    print("\nYour GPT Researcher is now configured to use OpenRouter.")
    print("You can now run research tasks using the configured models.")
    
    return True

async def test_research_example():
    """Test a simple research task using OpenRouter."""
    print("\n5. Testing simple research functionality...")
    
    try:
        from gpt_researcher import GPTResearcher
        
        # Simple research query
        query = "What are the latest developments in AI research?"
        researcher = GPTResearcher(query=query, report_type="research_report")
        
        print(f"   📝 Starting research: '{query}'")
        print("   ⏳ This may take a few minutes...")
        
        # Conduct research
        research_result = await researcher.conduct_research()
        report = await researcher.write_report()
        
        if report and len(report) > 100:
            print(f"   ✅ Research completed successfully!")
            print(f"   📊 Report length: {len(report)} characters")
            print(f"   📄 Report preview: {report[:200]}...")
        else:
            print(f"   ⚠️  Research completed but report seems short: {len(report) if report else 0} characters")
            
    except Exception as e:
        print(f"   ❌ Research test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    async def main():
        success = await test_openrouter_setup()
        
        if success:
            print("\n" + "=" * 60)
            choice = input("Would you like to test a simple research task? (y/n): ").lower().strip()
            if choice in ['y', 'yes']:
                await test_research_example()
        else:
            print("\n❌ Setup test failed. Please check your configuration and try again.")
    
    asyncio.run(main())