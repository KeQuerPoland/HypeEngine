from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
from flask import request
from config import Discord

class DiscordHandler:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    async def log(self, content, color):
        if Discord.WEBHOOK_ENABLE:
            try:
                webhook = DiscordWebhook(url=self.webhook_url)
                embed = DiscordEmbed(
                    title = f"🔒 {content}",
                    description = f"""```{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}```""",
                    color = int(color[1:], 16)
                )
                embed.add_embed_field(name="🔧 IP:",value=f"`{request.remote_addr}`",inline=False)
                embed.add_embed_field(name="🎫 Endpoint:",value=f"`{request.endpoint}`",inline=False)
                embed.set_footer(text="HypeEngine",icon_url="https://media.discordapp.net/attachments/1132393202419257407/1157326079523033098/HypeEngine_smaller.png?ex=65183367&is=6516e1e7&hm=c8b8abd09246051ba085ac9f9bbf42fdbfea4f036f43c14373e12205b95c8aea&=")
                
                webhook.add_embed(embed)
                webhook.execute()
            except Exception as e:
                raise e