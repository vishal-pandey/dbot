from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.tools import BaseTool
from langchain_community.utilities.sql_database import SQLDatabase
from typing import Type
from dbragtool import getRelationshipsForTables



class BaseSQLDatabaseTool(BaseModel):
    """Base tool for interacting with a SQL database."""

    db: SQLDatabase = Field(exclude=True)

    class Config(BaseTool.Config):
        pass

class _RelationshipFetchToolInput(BaseModel):
    list_of_tables: str = Field("", description="List of tables for which relationships with other tables needed")



class RelationshipFetchTool(BaseSQLDatabaseTool, BaseTool):
    """Tool for getting relationships of tables with other tables in the database, these  relationship can be used to query further the db for the required information"""

    name: str = "relationship_fetch"
    description: str = "Input is a list of tables for which relationships with other tables needed, output is the relationships in json format"
    args_schema: Type[BaseModel] = _RelationshipFetchToolInput

    def _run(
        self,
        list_of_tables: str = "",
    ):
        """Get the relationships of tables with other tables in the database in json format"""
        # return ", ".join([
        #     "tag",
        #     "tag_usage",
        #     "table_entity"
        # ])
        return getRelationshipsForTables(list_of_tables)



