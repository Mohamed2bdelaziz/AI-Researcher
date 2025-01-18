import random
import time
from datetime import datetime
from typing import Dict

# List of User-Agent strings
user_agents = [
    # Windows Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    
    # Windows Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    
    # Windows Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    
    # macOS Chrome
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    
    # macOS Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    
    # macOS Firefox
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
    
    # Linux Chrome
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    
    # Linux Firefox
    "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    
    # Ubuntu Firefox
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    
    # iOS Safari (iPhone)
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    
    # iOS Chrome (iPhone)
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/121.0.6167.66 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.119 Mobile/15E148 Safari/604.1",
    
    # iPadOS Safari
    "Mozilla/5.0 (iPad; CPU OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    
    # Android Chrome
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.101 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.210 Mobile Safari/537.36",
    
    # Android Firefox
    "Mozilla/5.0 (Android 14; Mobile; rv:122.0) Gecko/122.0 Firefox/122.0",
    "Mozilla/5.0 (Android 13; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0"
]



class HeadersGenerator:
    def __init__(self, user_agents: list = user_agents):
        self.user_agents = user_agents
        self.used_agents = {}  # Track when each agent was last used
        self.min_reuse_delay = random.randint(240, 360)  # Random delay between 4-6 minutes
        self.browser_profiles = {}  # Store consistent fingerprint data per browser
        
    def _generate_browser_profile(self, user_agent: str) -> Dict[str, str]:
        """Generate consistent browser fingerprint data"""
        if user_agent not in self.browser_profiles:
            # Common screen resolutions
            resolutions = [
                "1920x1080", "1366x768", "1440x900", "1536x864", 
                "2560x1440", "1680x1050", "1280x720"
            ]
            
            # Common color depths
            color_depths = ["24", "32"]
            
            # Language preferences focusing on Arabic and English
            accept_languages = [
                # Arabic primary
                "ar,en-US;q=0.9,en;q=0.8",
                "ar-SA,ar;q=0.9,en-US;q=0.8,en;q=0.7",
                "ar-EG,ar;q=0.9,en-GB;q=0.8,en;q=0.7",
                "ar-AE,ar;q=0.9,en-US;q=0.8,en;q=0.7",
                # English primary with Arabic
                "en-US,en;q=0.9,ar;q=0.8",
                "en-GB,en;q=0.9,ar;q=0.8",
                "en,ar;q=0.9,en-US;q=0.8",
                # Regional variations
                "ar-KW,ar;q=0.9,en-US;q=0.8,en;q=0.7",
                "ar-QA,ar;q=0.9,en-US;q=0.8,en;q=0.7",
                "ar-BH,ar;q=0.9,en-GB;q=0.8,en;q=0.7"
            ]
            
            # Common platform behaviors
            if "Windows" in user_agent:
                platform = "Windows"
                oscpu = "Windows NT 10.0"
            elif "Macintosh" in user_agent:
                platform = "MacIntel"
                oscpu = "Intel Mac OS X 10_15_7"
            elif "Linux" in user_agent:
                platform = "Linux x86_64"
                oscpu = "Linux x86_64"
            else:
                platform = "Unknown"
                oscpu = "Unknown"
            
            # Store consistent profile
            self.browser_profiles[user_agent] = {
                "resolution": random.choice(resolutions),
                "color_depth": random.choice(color_depths),
                "platform": platform,
                "oscpu": oscpu,
                "accept_language": random.choice(accept_languages)
            }
        
        return self.browser_profiles[user_agent]

    def _calculate_next_delay(self) -> float:
        """Calculate delay mimicking human behavior"""
        # Base delay (majority of cases)
        if random.random() < 0.7:  # 70% of requests
            return random.uniform(2, 7)
        
        # Occasional longer pauses (checking other tabs, short breaks)
        elif random.random() < 0.9:  # 20% of requests
            return random.uniform(10, 30)
        
        # Rare long pauses (bathroom breaks, getting coffee, etc)
        else:  # 10% of requests
            return random.uniform(60, 180)

    def get_headers(self) -> Dict[str, str]:
        """Get complete headers with smart rotation and consistent fingerprinting"""
        current_time = datetime.now()
        
        # Filter available agents
        available_agents = [
            agent for agent in self.user_agents
            if agent not in self.used_agents or 
            (current_time - self.used_agents[agent]).total_seconds() > self.min_reuse_delay
        ]
        
        # Select user agent
        if not available_agents:
            user_agent = min(self.used_agents.items(), key=lambda x: x[1])[0]
        else:
            user_agent = random.choice(available_agents)
        
        # Update usage timestamp
        self.used_agents[user_agent] = current_time
        
        # Get consistent browser profile
        profile = self._generate_browser_profile(user_agent)
        
        # Generate headers based on browser type
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': profile['accept_language'],
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': self._generate_browser_version(user_agent),
            'sec-ch-ua-mobile': '?0' if 'Mobile' not in user_agent else '?1',
            'sec-ch-ua-platform': f'"{profile["platform"]}"',
            'Viewport-Width': profile['resolution'].split('x')[0],
            'Device-Memory': random.choice(['4', '8', '16']),
            'Sec-CH-Prefers-Color-Scheme': random.choice(['light', 'dark'])
        }
        
        # Add browser-specific headers
        if 'Firefox' in user_agent:
            headers.update({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'TE': 'trailers'
            })
        elif 'Chrome' in user_agent:
            headers.update({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
            })
        
        return headers

    def _generate_browser_version(self, user_agent: str) -> str:
        """Generate consistent browser version string with better error handling"""
        try:
            if 'Chrome' in user_agent:
                version = user_agent.split('Chrome/')[1].split('.')[0]
                return f'"Google Chrome";v="{version}", "Chromium";v="{version}"'
            elif 'Firefox' in user_agent:
                version = user_agent.split('Firefox/')[1].split('.')[0]
                return f'"Firefox";v="{version}"'
            elif 'Safari' in user_agent:
                if 'Version/' in user_agent:
                    version = user_agent.split('Version/')[1].split(' ')[0]
                    return f'"Safari";v="{version}"'
                # For Safari agents without explicit version
                return '"Safari"'
            elif 'Edge' in user_agent:
                version = user_agent.split('Edg/')[1].split('.')[0]
                return f'"Edge";v="{version}"'
        except (IndexError, KeyError):
            # If any parsing fails, return a generic string
            return '"Not/A)Brand";v="99"'

# # Example usage:
# if __name__ == '__main__':
#     from pprint import pprint
#     # Initialize rotator with user agents list
#     rotator = HeadersGenerator()
        

#     for _ in range(20):
#         # Get headers
#         headers = rotator.get_headers()

#         print("\n\n", "=="*50, "\n", f"agent #{_}")
#         pprint(headers)
#         time.sleep(1.5)