from langchain_core.pydantic_v1 import BaseModel, Field, root_validator
from langchain_community.tools import BaseTool
from langchain_community.utilities.sql_database import SQLDatabase
from typing import Any, Dict, Optional, Sequence, Type, Union
from dbragtool import getShcemaForTables



class BaseSQLDatabaseTool(BaseModel):
    """Base tool for interacting with a SQL database."""

    db: SQLDatabase = Field(exclude=True)

    class Config(BaseTool.Config):
        pass

class _SchemaFetchToolInput(BaseModel):
    table_name: str = Field("", description="Name of the table for which schema to be fetched.")


def fetchSchema(table_name: str):
    

    return getShcemaForTables([table_name])

class SchemaFetchTool(BaseSQLDatabaseTool, BaseTool):
    """Tool to fetchh the shcma of the table. The table name should be passed as input. This tool should be called before creating the sql qeury, to make effective query to answer the question."""

    name: str = "schema_fetch"
    description: str = "Input is the name of the table on which query to be name, output is the schema of the table"
    args_schema: Type[BaseModel] = _SchemaFetchToolInput

    def _run(
        self,
        table_name: str = "",
    ):
        """Get detail about the entity in json format"""
        # return ", ".join([
        #     "tag",
        #     "tag_usage",
        #     "table_entity"
        # ])
        return fetchSchema(table_name)



