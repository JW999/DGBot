from .helpers import jsonTest
from discord.ext import commands


async def mute_member():
    pass


class mute:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(adminstrator=True)
    async def warn(self, ctx, *, message):
        """Send a warning message to a user, and record number of warnings and time."""
        json_data = jsonTest.import_data("assets/warned_members")
        member_id = ctx.message.mentions[0].id

        if jsonTest.check_user_id(member_id):
            jsonTest.increase_count(member_id)
        else:
            jsonTest.add_user(member_id)

        jsonTest.export_data("assets/warned_members")



if __name__ == "__main__":
    pass