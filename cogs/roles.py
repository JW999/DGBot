from discord.ext import commands
import asyncio


class roles:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def roles(self, ctx):
        output_msg = "Available Roles:\n"

        available_roles = open("assets/roles.txt", "r").readlines()

        for role in available_roles:
            output_msg += role

        await ctx.send(output_msg)

    @roles.command()
    async def add(self, ctx, *roles_to_add):
        # Get user roles
        user_roles = []
        for role in ctx.author.roles:
            user_roles.append(role.name.lower())

        # Get the current list of available roles
        available_roles = open("assets/roles.txt", "r").readlines()
        # Remove whitespace and make all roles lower case.
        available_roles = [role.lower().strip() for role in available_roles]

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
        """Add roles to the available_roles file"""
        already_present_roles = []  # roles that will be deleted from "roles_to_add"

        available_roles = open("assets/roles.txt", "r").readlines()
        available_roles = [role.lower().strip() for role in available_roles]

        output_msg = ""

        for role_to_add in roles_to_add:
            for role in available_roles:
                if role_to_add.lower() == role:
                    output_msg += f"Failed to add {role_to_add}: role already exists.\n"
                    already_present_roles.append(role_to_add)
                    break

        for role in already_present_roles:
            roles_to_add.remove(role)

        if roles_to_add:
            with open("assets/roles.txt", "a") as f:
                for role in roles_to_add:
                    f.write(f"{role}\n")
                    output_msg += f"{role} has been added successfully.\n"

        await ctx.send(output_msg)

    @addRole.error
    async def addRole_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You're not an admin.")
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Am I supposed to remove a non-existent role?")

    @roles.command()
    @commands.has_permissions(administrator=True)
    async def removeRole(self, ctx, *roles_to_remove):
        invalid_roles = []  # roles that will be deleted from "roles_to_remove"

        available_roles = open("assets/roles.txt", "r").readlines()
        available_roles = [role.lower().strip() for role in available_roles]

        output_msg = ""

        for role_to_remove in roles_to_remove:
            if role_to_remove.lower() not in available_roles:
                output_msg += f"{role_to_remove} is an invalid role.\n"
                invalid_roles.append(role_to_remove)

        for role in invalid_roles:
            roles_to_remove.remove(role)

        if roles_to_remove:
            with open("assets/roles.txt", "r+") as f:
                # Store lines in a buffer
                lines = f.readlines()
                # Remove lines from the buffer
                for role in roles_to_remove:
                    for line in lines:
                        if role.lower() == line.lower().strip():
                            lines.remove(line)
                            output_msg += f"{role} has been removed successfully.\n"
                            break
                f.seek(0)
                # Write the modified buffer
                for line in lines:
                    f.write(line)
                f.truncate()

        await ctx.send(output_msg)

    @removeRole.error
    async def removeRole_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You're not an admin.")
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Am I supposed to remove a non-existent role?")


def setup(bot):
    bot.add_cog(roles(bot))