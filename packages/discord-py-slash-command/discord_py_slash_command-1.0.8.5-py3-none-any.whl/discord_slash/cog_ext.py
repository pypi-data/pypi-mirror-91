import typing
from .model import CogCommandObject, CogSubcommandObject


def cog_slash(*,
              name: str = None,
              description: str = None,
              auto_convert: dict = None,
              guild_ids: typing.List[int] = None,
              options: typing.List[dict] = None):
    """
    Decorator for Cog to add slash command.\n
    Almost same as :func:`.client.SlashCommand.slash`.

    Example:

    .. code-block:: python

        class ExampleCog(commands.Cog):
            def __init__(self, bot):
                if not hasattr(bot, "slash"):
                    # Creates new SlashCommand instance to bot if bot doesn't have.
                    bot.slash = SlashCommand(bot, override_type=True)
                self.bot = bot
                self.bot.slash.get_cog_commands(self)

            def cog_unload(self):
                self.bot.slash.remove_cog_commands(self)

            @cog_ext.cog_slash(name="ping")
            async def ping(self, ctx: SlashContext):
                await ctx.send(content="Pong!")

    :param name: Name of the slash command. Default name of the coroutine.
    :type name: str
    :param description: Description of the slash command. Default ``None``.
    :type description: str
    :param auto_convert: Dictionary of how to convert option values. Default ``None``.
    :type auto_convert: dict
    :param guild_ids: List of Guild ID of where the command will be used. Default ``None``, which will be global command.
    :type guild_ids: List[int]
    :param options: Options of the slash command. This will affect ``auto_convert`` and command data at Discord API. Default ``None``.
    :type options: List[dict]
    """
    if options:
        # Overrides original auto_convert.
        auto_convert = {}
        for x in options:
            if x["type"] < 3:
                raise Exception("Please use `cog_subcommand()` decorator for cog subcommands!")
            auto_convert[x["name"]] = x["type"]

    def wrapper(cmd):
        _cmd = {
            "func": cmd,
            "description": description if description else "No description.",
            "auto_convert": auto_convert,
            "guild_ids": guild_ids if guild_ids else [],
            "api_options": options if options else [],
            "has_subcommands": False
        }
        return CogCommandObject(cmd.__name__ if not name else name, _cmd)
    return wrapper


def cog_subcommand(*,
                   base,
                   subcommand_group=None,
                   name=None,
                   description: str = None,
                   base_description: str = None,
                   base_desc: str = None,
                   subcommand_group_description: str = None,
                   sub_group_desc: str = None,
                   auto_convert: dict = None,
                   guild_ids: typing.List[int] = None,
                   options: typing.List[dict] = None):
    """
    Decorator for Cog to add subcommand.\n
    Almost same as :func:`.client.SlashCommand.subcommand`.

    Example:

    .. code-block:: python

        class ExampleCog(commands.Cog):
            def __init__(self, bot):
                if not hasattr(bot, "slash"):
                    # Creates new SlashCommand instance to bot if bot doesn't have.
                    bot.slash = SlashCommand(bot, override_type=True)
                self.bot = bot
                self.bot.slash.get_cog_commands(self)

            def cog_unload(self):
                self.bot.slash.remove_cog_commands(self)

            @cog_ext.cog_subcommand(base="group", name="say")
            async def group_say(self, ctx: SlashContext, text: str):
                await ctx.send(content=text)

    :param base: Name of the base command.
    :type base: str
    :param subcommand_group: Name of the subcommand group, if any. Default ``None`` which represents there is no sub group.
    :type subcommand_group: str
    :param name: Name of the subcommand. Default name of the coroutine.
    :type name: str
    :param description: Description of the subcommand. Default ``None``.
    :type description: str
    :param base_description: Description of the base command. Default ``None``.
    :type base_description: str
    :param base_desc: Alias of ``base_description``.
    :param subcommand_group_description: Description of the subcommand_group. Default ``None``.
    :type subcommand_group_description: str
    :param sub_group_desc: Alias of ``subcommand_group_description``.
    :param auto_convert: Dictionary of how to convert option values. Default ``None``.
    :type auto_convert: dict
    :param guild_ids: List of guild ID of where the command will be used. Default ``None``, which will be global command.
    :type guild_ids: List[int]
    :param options: Options of the subcommand. This will affect ``auto_convert`` and command data at Discord API. Default ``None``.
    :type options: List[dict]
    """

    if options:
        # Overrides original auto_convert.
        auto_convert = {}
        for x in options:
            if x["type"] < 3:
                raise Exception("You can't use subcommand or subcommand_group type!")
            auto_convert[x["name"]] = x["type"]

    base_description = base_description if base_description else base_desc
    subcommand_group_description = subcommand_group_description if subcommand_group_description else sub_group_desc

    def wrapper(cmd):
        _sub = {
            "func": cmd,
            "name": cmd.__name__ if not name else name,
            "description": description if description else "No Description.",
            "base_desc": base_description if base_description else "No Description.",
            "sub_group_desc": subcommand_group_description if subcommand_group_description else "No Description.",
            "auto_convert": auto_convert,
            "guild_ids": guild_ids if guild_ids else [],
            "api_options": options if options else []
        }
        return CogSubcommandObject(_sub, base, cmd.__name__ if not name else name, subcommand_group)
    return wrapper
