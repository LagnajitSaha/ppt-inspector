"""
Configuration file for PowerPoint Inconsistency Detector

This file contains configurable parameters for the analysis engine.
"""

import os
from typing import Dict, Any

# AI Model Configuration
AI_CONFIG = {
    "model_name": "gemini-2.0-flash-exp",
    "max_tokens": 8192,
    "temperature": 0.1,
    "top_p": 0.8,
    "top_k": 40,
}

# Analysis Configuration
ANALYSIS_CONFIG = {
    "min_confidence_threshold": 0.7,
    "max_slides_per_batch": 10,
    "enable_rule_based_checks": True,
    "enable_ai_analysis": True,
    "enable_mathematical_validation": True,
    "enable_claim_consistency_check": True,
}

# Numerical Data Patterns
NUMERICAL_PATTERNS = {
    "currency": [
        r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)([MBK]?)',  # $2M, $3M, etc.
        r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*([MBK]?)\s*dollars?',  # 2M dollars
        r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*USD',  # 2M USD
    ],
    "time": [
        r'(\d+)\s*(?:mins?|minutes?)',  # 15 mins, 20 minutes
        r'(\d+)\s*(?:hours?|hrs?)',    # 10 hours, 50 hrs
        r'(\d+)\s*(?:days?)',          # 5 days
        r'(\d+)\s*(?:weeks?)',         # 2 weeks
        r'(\d+)\s*(?:months?)',        # 6 months
        r'(\d+)\s*(?:years?)',         # 1 year
    ],
    "percentage": [
        r'(\d+(?:\.\d+)?)\s*%',  # 25%, 12.5%
        r'(\d+(?:\.\d+)?)\s*percent',  # 25 percent
        r'(\d+(?:\.\d+)?)\s*per\s*cent',  # 25 per cent
    ],
    "multiplier": [
        r'(\d+)x\s*faster',  # 2x faster, 3x faster
        r'(\d+)\s*times\s*faster',  # 2 times faster
        r'(\d+)x\s*improvement',  # 2x improvement
        r'(\d+)\s*times\s*more',  # 2 times more
    ],
    "ratio": [
        r'(\d+):(\d+)',  # 3:1 ratio
        r'(\d+)\s*to\s*(\d+)',  # 3 to 1
        r'(\d+)\s*out\s*of\s*(\d+)',  # 3 out of 4
    ],
}

# Key Claims Keywords
KEY_CLAIMS_KEYWORDS = [
    "AI-powered", "automated", "faster", "efficient", "streamlined",
    "competitive", "market leader", "innovative", "cutting-edge",
    "time-saving", "productivity", "efficiency", "accuracy",
    "revolutionary", "breakthrough", "best-in-class", "superior",
    "cost-effective", "affordable", "premium", "luxury",
    "sustainable", "eco-friendly", "green", "environmental",
]

# Inconsistency Types
INCONSISTENCY_TYPES = {
    "numerical_conflict": {
        "description": "Conflicting numerical values across slides",
        "severity": "high",
        "confidence_threshold": 0.9,
    },
    "performance_claim_conflict": {
        "description": "Conflicting performance improvement claims",
        "severity": "high",
        "confidence_threshold": 0.85,
    },
    "financial_data_mismatch": {
        "description": "Inconsistent financial figures or metrics",
        "severity": "high",
        "confidence_threshold": 0.9,
    },
    "timeline_conflict": {
        "description": "Conflicting dates, timelines, or forecasts",
        "severity": "medium",
        "confidence_threshold": 0.8,
    },
    "brand_inconsistency": {
        "description": "Inconsistent brand or product information",
        "severity": "medium",
        "confidence_threshold": 0.8,
    },
    "claim_contradiction": {
        "description": "Contradictory statements or claims",
        "severity": "medium",
        "confidence_threshold": 0.75,
    },
    "mathematical_error": {
        "description": "Mathematical inconsistencies or calculation errors",
        "severity": "high",
        "confidence_threshold": 0.95,
    },
}

# Output Configuration
OUTPUT_CONFIG = {
    "default_format": "console",
    "supported_formats": ["console", "json", "csv", "txt"],
    "include_confidence_scores": True,
    "include_recommendations": True,
    "include_evidence": True,
    "group_by_type": True,
    "sort_by_severity": True,
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": None,  # Set to file path to enable file logging
    "max_file_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5,
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    "max_concurrent_requests": 3,
    "request_timeout": 30,
    "retry_attempts": 3,
    "retry_delay": 1,
    "batch_size": 5,
}

def get_config() -> Dict[str, Any]:
    """Get the complete configuration dictionary."""
    return {
        "ai": AI_CONFIG,
        "analysis": ANALYSIS_CONFIG,
        "numerical_patterns": NUMERICAL_PATTERNS,
        "key_claims_keywords": KEY_CLAIMS_KEYWORDS,
        "inconsistency_types": INCONSISTENCY_TYPES,
        "output": OUTPUT_CONFIG,
        "logging": LOGGING_CONFIG,
        "performance": PERFORMANCE_CONFIG,
    }

def get_ai_config() -> Dict[str, Any]:
    """Get AI-specific configuration."""
    return AI_CONFIG

def get_analysis_config() -> Dict[str, Any]:
    """Get analysis-specific configuration."""
    return ANALYSIS_CONFIG

def get_output_config() -> Dict[str, Any]:
    """Get output-specific configuration."""
    return OUTPUT_CONFIG

def update_config(key: str, value: Any) -> None:
    """Update a configuration value."""
    if key in globals():
        globals()[key] = value
    else:
        raise ValueError(f"Configuration key '{key}' not found")

def validate_config() -> bool:
    """Validate the configuration for consistency."""
    try:
        # Check required fields
        required_fields = ["ai", "analysis", "output"]
        config = get_config()
        
        for field in required_fields:
            if field not in config:
                print(f"❌ Missing required configuration field: {field}")
                return False
        
        # Validate AI config
        ai_config = config["ai"]
        if "model_name" not in ai_config:
            print("❌ Missing AI model name in configuration")
            return False
        
        # Validate analysis config
        analysis_config = config["analysis"]
        if "min_confidence_threshold" not in analysis_config:
            print("❌ Missing confidence threshold in analysis configuration")
            return False
        
        # Validate output config
        output_config = config["output"]
        if "supported_formats" not in output_config:
            print("❌ Missing supported formats in output configuration")
            return False
        
        print("✅ Configuration validation passed")
        return True
        
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

if __name__ == "__main__":
    # Test configuration
    print("🔧 Testing PowerPoint Inconsistency Detector Configuration")
    print("=" * 60)
    
    config = get_config()
    print(f"Configuration loaded with {len(config)} main sections")
    
    # Validate configuration
    if validate_config():
        print("\n📋 Configuration Summary:")
        print(f"   • AI Model: {config['ai']['model_name']}")
        print(f"   • Confidence Threshold: {config['analysis']['min_confidence_threshold']}")
        print(f"   • Supported Output Formats: {', '.join(config['output']['supported_formats'])}")
        print(f"   • Inconsistency Types: {len(config['inconsistency_types'])}")
        print(f"   • Numerical Patterns: {len(config['numerical_patterns'])}")
        print(f"   • Key Claims Keywords: {len(config['key_claims_keywords'])}")
    else:
        print("\n❌ Configuration validation failed")
        sys.exit(1)
