from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
from flask import request
from config import Discord

class DiscordHandler:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    async def log(self, content, color):
        if Discord.WEBHOOK_ENABLE:
            webhook = DiscordWebhook(url=self.webhook_url)
            embed = DiscordEmbed(
                title = f"🔒 {content}",
                description = f"""```{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}```""",
                color = int(color[1:], 16)
            )
            embed.add_embed_field(name="🔧 IP:",value=f"`{request.remote_addr}`",inline=False)
            embed.add_embed_field(name="🎫 Endpoint:",value=f"`{request.endpoint}`",inline=False)
            embed.set_footer(text="WP-OW")
            
            webhook.add_embed(embed)
            webhook.execute()