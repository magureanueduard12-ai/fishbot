import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# === Fish prices dictionary ===
FISH_PRICES = {
    "Barracuda": 3850,
    "Calcan": 3500,
    "Dorada": 2345,
    "Merluciu": 2800,
    "Nisetru": 4025,
    "Piranha": 4900,
    "Tipar": 4550,
    "Anghila": 4200,
    "Rechin": 10000,
    "Ton": 8000,
    "Spada": 7500
}


# === Modal for entering all fish at once ===
class FishModalAll(discord.ui.Modal, title="Fish Earnings Calculator"):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.TextInput(
            label="Enter fish and amounts",
            placeholder="Example: Barracuda:2, Calcan:1, Dorada:3",
            required=True
        ))

    async def on_submit(self, interaction: discord.Interaction):
        text = self.children[0].value
        basket = {}
        for part in text.split(","):
            try:
                fish_name, amount = part.strip().split(":")
                fish_name = fish_name.strip()
                amount = int(amount.strip())
                if fish_name in FISH_PRICES and amount > 0:
                    basket[fish_name] = amount
            except:
                continue

        if not basket:
            return await interaction.response.send_message(
                "🛒 You didn't enter any valid fish.", ephemeral=True
            )

        total = sum(FISH_PRICES[fish] * amount for fish, amount in basket.items())
        basket_str = "\n".join(
            [f"- {fish}: {amount} × ${FISH_PRICES[fish]} = ${FISH_PRICES[fish]*amount}" 
             for fish, amount in basket.items()]
        )

        await interaction.response.send_message(
            f"🛒 **Your Basket:**\n{basket_str}\n\n💰 **Total Earnings: ${total}**",
            ephemeral=False
        )


# === Slash command ===
@bot.tree.command(name="fishcalc", description="Calculate your fish earnings")
async def fishcalc(interaction: discord.Interaction):
    await interaction.response.send_modal(FishModalAll())


# === Bot startup ===
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        print(e)


# === Run bot using environment variable token ===
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    raise Exception(
        "Please set your Discord bot token in the DISCORD_TOKEN environment variable."
    )

bot.run(DISCORD_TOKEN)
