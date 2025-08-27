import logging
import logging.handlers
from discord.ext import commands
from typing import Any
import json

def motoko_log():
    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(logging.INFO)

    motoko_logger = logging.getLogger("motoko")
    motoko_logger.setLevel(logging.DEBUG)

    handler = logging.handlers.RotatingFileHandler(
        filename='motoko.log',
        encoding='utf-8',
        maxBytes=1*1024*1024,
        backupCount=1,
    )

    handler.setFormatter(logging.Formatter(
        '[{asctime}] [{levelname}] {name}: {message}',
        '%Y-%m-%d %H:%M:%S',
        style='{'
    ))

    discord_logger.addHandler(handler)
    motoko_logger.addHandler(handler)

logger = logging.getLogger("motoko")

class JSONFormatter(logging.Formatter):
    RESERVED: set[str] = {
        "name", "msg", "args", "levelname", "levelno", "pathname", "filename",
        "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName",
        "created", "msecs", "relativeCreated", "thread", "threadName",
        "processName", "process", "message", "asctime", "taskName"
    }

    def format(self, record: logging.LogRecord) -> str:
        log_record: dict[str, Any] = {
            "time": self.formatTime(record, self.datefmt),
            "id": int(record.getMessage())
        }

        for key, value in record.__dict__.items():
            if key not in self.RESERVED:
                log_record[key] = value

        return json.dumps(log_record, ensure_ascii=False)

def command_log():
    logger = logging.getLogger("commands")
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename="command.jsonl",
        encoding="utf-8",
        maxBytes=1*1024*1024,
        backupCount=1
    )

    handler.setFormatter(JSONFormatter(
        datefmt='%Y-%m-%d %H:%M:%S'
    ))

    logger.addHandler(handler)
    return logger

def log_command(ctx: commands.Context[Any]):
    if ctx.interaction is None:
        id = ctx.message.id
        prefix = '@' if ctx.prefix and ctx.prefix.startswith('<@') else ctx.prefix
        args = ctx.message.content[len(f'{ctx.prefix}{ctx.invoked_with} '):] or None
    else: # Interaction
        id = ctx.interaction.id
        prefix = ctx.prefix
        options: list[dict[str, Any]] = ctx.interaction.data.get('options', [])  # type: ignore
        args = ' '.join([str(opt['value']) for opt in options]) if options else None

    commandlog.info(
        id,
        extra = {
            'prefix': prefix,
            'command': ctx.invoked_with,
            'argument': str(args),
            'parent': str(ctx.command.parent) if ctx.command and ctx.command.parent else None,
            'cog': ctx.cog.qualified_name if ctx.cog else None,
            'user_name': ctx.author.name,
            'user_id': ctx.author.id,
            'guild_name': ctx.guild.name if ctx.guild else None,
            'guild_id': ctx.guild.id if ctx.guild else None
        }
    )

commandlog = command_log()