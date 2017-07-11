from discord.ext import commands
import asyncio


class roles:
    def __init__(self, bot):
        self.bot = bot
        # Available roles
        self.roles_list = ["C++", "C", "SFML", "OpenGL", "Python", "SDL", "Allegro", "ASM", "Java", "PHP"]

    @commands.group(invoke_without_command=True)
    async def roles(self, ctx):
        s = "Available Roles:\n"
        for role in self.roles_list:
            s += f"{role}\n"
        await ctx.send(s)

    @roles.command()
    async def add(self, ctx, *roles_to_add):
        # Get user roles
        user_roles = []
        for role in ctx.author.roles:
            user_roles.append(role.name.lower())

        # Get a lowercase list of roles_list
        available_roles = []
        for role in self.roles_list:
            available_roles.append(role.lower())

        if not roles_to_add:
            await ctx.send("Am I supposed to make a role out of thin air?")
            return

        reply = ""
        for role in roles_to_add:
            if role.lower() not in available_roles:  # Invalid role
                reply += f"❌ {role} is not a valid role.\n"
                continue
            if role.lower() in user_roles:  # Checks if user already has role
                reply += f"❌ You already have the role {role}.\n"
                continue

            # Get a role instance for the api to process
            for instance in ctx.guild.roles:
                if role.lower() == instance.name.lower():
                    role = instance
                    break
            await ctx.author.add_roles(role)
            await asyncio.sleep(0.1)
            reply += f"✅ {role} has been added successfully.\n"

        await ctx.send(reply)

    @roles.command()
    async def remove(self, ctx, *roles_to_remove):
        # Get user roles
        user_roles = []
        for role in ctx.author.roles:
            user_roles.append(role.name.lower())

        if not roles_to_remove:
            await ctx.send("Am I supposed to make a role out of thin air?")
            return

        reply = ""
        for role in roles_to_remove:
            if role.lower() not in user_roles:  # Checks if user already has role1
                reply += "❌ How am I supposed to remove a role that you don't have?\n"
                continue

            # Get a role instance for the api to process
            for instance in ctx.guild.roles:
                if role.lower() == instance.name.lower():
                    role = instance
                    break
            await ctx.author.remove_roles(role)
            await asyncio.sleep(0.1)
            reply += f"✅ {role} has been removed successfully.\n"

        await ctx.send(reply)

    @roles.command()
    @commands.has_permissions(administrator=True)
    async def addRole(self, ctx, *roles_to_add):
        for role in roles_to_add:
            self.roles_list.append(role)

    @addRole.error
    async def addRole_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You're not an admin.")
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Am I supposed to remove a non-existent role?")

    @roles.command()
    @commands.has_permissions(administrator=True)
    async def removeRole(self, ctx, *roles_to_remove):
        for role in roles_to_remove:
            self.roles_list.remove(role)

    @removeRole.error
    async def removeRole_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You're not an admin.")
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Am I supposed to remove a non-existent role?")


def setup(bot):
    bot.add_cog(roles(bot))