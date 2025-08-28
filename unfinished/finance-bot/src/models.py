from tortoise import fields
from tortoise.models import Model


class UserMessages(Model):
    message_id = fields.IntField(True, description="")
    chat_id = fields.BigIntField(False, description="")
    user_id = fields.BigIntField(False, description="")
    message = fields.TextField(description="")
    datetime = fields.DatetimeField(auto_now_add=True, description="")

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        table = "user_messages"
        table_description = ""

    def __str__(self) -> str:
        return f"UserMessages(message_id={self.message_id}, chat_id={self.chat_id}, user_id={self.user_id}, message={self.message}, datetime={self.datetime})"


class UserCommands(Model):
    message_id = fields.IntField(True, description="")
    chat_id = fields.BigIntField(False, description="")
    user_id = fields.BigIntField(False, description="")
    command = fields.TextField(description="")
    datetime = fields.DatetimeField(auto_now_add=True, description="")

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        table = "user_commands"
        table_description = ""

    def __str__(self) -> str:
        return f"UserCommands(message_id={self.message_id}, chat_id={self.chat_id}, user_id={self.user_id}, command={self.command}, datetime={self.datetime})"


class LogRecordModel(Model):
    id = fields.IntField(True)
    datetime = fields.DatetimeField(auto_now_add=True)
    logger_name = fields.CharField(50)
    level_name = fields.CharField(20)
    level_value = fields.IntField()
    message = fields.TextField()
    module = fields.CharField(255, null=True)
    function = fields.CharField(255, null=True)
    line_no = fields.IntField(null=True)
    extra = fields.JSONField(default={})  # type: ignore[var-annotated]

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        table = "log_records"
        table_description = "Log records storage"
