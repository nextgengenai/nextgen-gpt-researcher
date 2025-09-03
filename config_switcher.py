#!/usr/bin/env python3
"""
Quick configuration switcher for GPT Researcher LLM providers.

This script helps you quickly switch between OpenAI, OpenRouter, and other LLM providers
by updating your .env file with predefined configurations.
"""

import os
import re
from pathlib import Path

def backup_env():
    """Create a backup of the current .env file."""
    env_path = Path(".env")
    if env_path.exists():
        backup_path = Path(".env.backup")
        backup_path.write_text(env_path.read_text())
        print(f"✅ Created backup: {backup_path}")

def update_env_variable(content, key, value):
    """Update or add an environment variable in the content."""
    pattern = rf'^{key}=.*$'
    replacement = f'{key}={value}'
    
    if re.search(pattern, content, re.MULTILINE):
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    else:
        content += f'\n{replacement}'
    
    return content

def apply_config(config_name, config):
    """Apply a configuration to the .env file."""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ .env file not found. Creating new one...")
        content = ""
    else:
        content = env_path.read_text()
    
    print(f"🔧 Applying {config_name} configuration...")
    
    for key, value in config.items():
        content = update_env_variable(content, key, value)
    
    env_path.write_text(content)
    print(f"✅ Configuration updated successfully!")

def get_configurations():
    """Define available configurations."""
    return {
        "openrouter": {
            "name": "OpenRouter (Latest Anthropic)",
            "config": {
                "FAST_LLM": "openrouter:anthropic/claude-3.5-haiku",
                "SMART_LLM": "openrouter:anthropic/claude-sonnet-4", 
                "STRATEGIC_LLM": "openrouter:anthropic/claude-opus-4.1",
                "OPENROUTER_LIMIT_RPS": "2.0"
            },
            "required_keys": ["OPENROUTER_API_KEY"],
            "description": "Uses OpenRouter with the latest Anthropic models (Opus 4.1, Sonnet 4, Haiku 3.5)."
        },
        "openrouter_budget": {
            "name": "OpenRouter (Budget)",
            "config": {
                "FAST_LLM": "openrouter:anthropic/claude-3-haiku",
                "SMART_LLM": "openrouter:anthropic/claude-3.5-sonnet",
                "STRATEGIC_LLM": "openrouter:anthropic/claude-3.7-sonnet",
                "OPENROUTER_LIMIT_RPS": "1.0"
            },
            "required_keys": ["OPENROUTER_API_KEY"],
            "description": "Cost-optimized OpenRouter configuration with older but reliable Anthropic models."
        },
        "openrouter_premium": {
            "name": "OpenRouter (Premium)",
            "config": {
                "FAST_LLM": "openrouter:anthropic/claude-sonnet-4",
                "SMART_LLM": "openrouter:anthropic/claude-opus-4",
                "STRATEGIC_LLM": "openrouter:anthropic/claude-opus-4.1",
                "OPENROUTER_LIMIT_RPS": "2.0"
            },
            "required_keys": ["OPENROUTER_API_KEY"],
            "description": "High-performance OpenRouter configuration with the absolute latest Anthropic models."
        },
        "openai": {
            "name": "OpenAI (Direct)",
            "config": {
                "FAST_LLM": "openai:gpt-4o-mini",
                "SMART_LLM": "openai:gpt-4o",
                "STRATEGIC_LLM": "openai:o1-mini"
            },
            "required_keys": ["OPENAI_API_KEY"],
            "description": "Direct OpenAI API access with their latest models."
        },
        "ollama": {
            "name": "Ollama (Local)",
            "config": {
                "FAST_LLM": "ollama:llama3",
                "SMART_LLM": "ollama:llama3",
                "STRATEGIC_LLM": "ollama:llama3",
                "OLLAMA_BASE_URL": "http://localhost:11434"
            },
            "required_keys": [],
            "description": "Local Ollama models (requires Ollama to be running locally)."
        },
        "anthropic": {
            "name": "Anthropic (Direct)",
            "config": {
                "FAST_LLM": "anthropic:claude-3-haiku-20240307",
                "SMART_LLM": "anthropic:claude-3-5-sonnet-20241022",
                "STRATEGIC_LLM": "anthropic:claude-3-opus-20240229"
            },
            "required_keys": ["ANTHROPIC_API_KEY"],
            "description": "Direct Anthropic API access with Claude models."
        }
    }

def check_required_keys(config_data):
    """Check if required API keys are set."""
    env_path = Path(".env")
    if not env_path.exists():
        return []
    
    content = env_path.read_text()
    missing_keys = []
    
    for key in config_data["required_keys"]:
        pattern = rf'^{key}=(.+)$'
        match = re.search(pattern, content, re.MULTILINE)
        if not match or not match.group(1).strip():
            missing_keys.append(key)
    
    return missing_keys

def main():
    print("🔧 GPT Researcher LLM Configuration Switcher")
    print("=" * 60)
    
    configurations = get_configurations()
    
    print("\nAvailable configurations:")
    for i, (key, config_data) in enumerate(configurations.items(), 1):
        missing_keys = check_required_keys(config_data)
        status = "⚠️  Missing keys" if missing_keys else "✅ Ready"
        print(f"{i:2d}. {config_data['name']} - {status}")
        print(f"     {config_data['description']}")
        if missing_keys:
            print(f"     Missing: {', '.join(missing_keys)}")
        print()
    
    while True:
        try:
            choice = input("Select configuration (1-{}) or 'q' to quit: ".format(len(configurations)))
            
            if choice.lower() == 'q':
                print("👋 Goodbye!")
                break
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(configurations):
                config_key = list(configurations.keys())[choice_num - 1]
                config_data = configurations[config_key]
                
                missing_keys = check_required_keys(config_data)
                if missing_keys:
                    print(f"\n⚠️  Warning: Missing required API keys: {', '.join(missing_keys)}")
                    print("You'll need to add these to your .env file manually.")
                    confirm = input("Continue anyway? (y/n): ").lower().strip()
                    if confirm != 'y':
                        continue
                
                # Create backup before applying changes
                backup_env()
                
                # Apply configuration
                apply_config(config_data['name'], config_data['config'])
                
                print(f"\n🎉 Successfully configured for {config_data['name']}!")
                if missing_keys:
                    print(f"\n📝 Don't forget to add your API key(s):")
                    for key in missing_keys:
                        print(f"   {key}=your_key_here")
                
                print(f"\n🧪 Test your configuration with: python test_openrouter.py")
                break
            else:
                print("❌ Invalid choice. Please try again.")
        except ValueError:
            print("❌ Invalid input. Please enter a number or 'q'.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()