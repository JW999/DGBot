from discord.ext import commands
import asyncio


class roles:
    def __init__(self, bot):
        self.bot = bot
        # Available roles
        self.roles_list = ["C++", "C", "SFML", "OpenGL", "Python", "SDL", "Allegro", "ASM", "Java"]

    @commands.group(invoke_without_command=True)
    async def roles(self, ctx):
        s = "Available Roles:\n"
        for role in self.roles_list:
            s += "{}\n".format(role)
        await ctx.send(s)

    @roles.command()
    async def add(self, ctx, *roles_to_add):
        # Get user roles
        user_roles = []
        for role in ctx.author.roles:
            user_roles.append(role.name)

        if not roles_to_add:
            await ctx.send("Am I supposed to make a role out of thin air?")
            return

        reply = ""
        for role in roles_to_add:
            if role not in self.roles_list:  # Invalid role
                reply += "❌ {} is not a valid role.\n".format(role)
                continue
            if role in user_roles:  # Checks if user already has role
                reply += "❌ You already have the role {}.\n".format(role)
                continue

            # Get a role instance for the api to process
            for instance in ctx.guild.roles:
                if role == instance.name:
                    role = instance
            await ctx.author.add_roles(role)
            await asyncio.sleep(0.1)
            reply += "✅ {} has been added successfully.\n".format(role)

        await ctx.send(reply)

    @roles.command()
    async def remove(self, ctx, *roles_to_remove):
        # Get user roles
        user_roles = []
        for role in ctx.author.roles:
            user_roles.append(role.name)

        if not roles_to_remove:
            await ctx.send("Am I supposed to make a role out of thin air?")
            return

        reply = ""
        for role in roles_to_remove:
            if role not in user_roles:  # Checks if user already has role1
                reply += "❌ How am I supposed to remove a role that you don't have?\n".format(role)
                continue

            # Get a role instance for the api to process
            for instance in ctx.guild.roles:
                if role == instance.name:
                    role = instance
            await ctx.author.remove_roles(role)
            await asyncio.sleep(0.1)
            reply += "✅ {} has been removed successfully.\n".format(role)

        await ctx.send(reply)


def setup(bot):
    bot.add_cog(roles(bot))