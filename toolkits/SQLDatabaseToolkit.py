"""Toolkit for interacting with an SQL database."""

from typing import List

from langchain_core.language_models import BaseLanguageModel
from langchain_core.pydantic_v1 import Field
from langchain_core.tools import BaseToolkit

from langchain_community.tools import BaseTool
from langchain_community.tools.sql_database.tool import (
    # InfoSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.pydantic_v1 import BaseModel, Field, root_validator
from typing import Any, Dict, Optional, Sequence, Type, Union
from State import State
from dbragtool import getListOfAllTables, getListOfTables

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

from toolkits.ElasticSearchTool import ElasticSearchTool
from toolkits.SchemaFetchTool import SchemaFetchTool
from toolkits.RelationshipFetchTool import RelationshipFetchTool

class BaseSQLDatabaseTool(BaseModel):
    """Base tool for interacting with a SQL database."""

    db: SQLDatabase = Field(exclude=True)

    class Config(BaseTool.Config):
        pass

class _ListSQLDataBaseToolInput(BaseModel):
    tool_input: str = Field("", description="An empty string")


class ListSQLDatabaseTool(BaseSQLDatabaseTool, BaseTool):
    """Tool for getting tables names related to application, do not use it if user is asking for the table, for that you should query table_entity."""

    name: str = "sql_db_list_tables"
    description: str = "Input is an empty string, output is a comma-separated list of tables in the application database."
    args_schema: Type[BaseModel] = _ListSQLDataBaseToolInput

    def _run(
        self,
        tool_input: str = "",
    ) -> str:
        """Get a comma-separated list of table names."""
        # return ", ".join([
        #     "tag",
        #     "tag_usage",
        #     "table_entity"
        # ])
        return getListOfAllTables()




class _InfoSQLDatabaseToolInput(BaseModel):
    table_names: str = Field(
        ...,
        description=(
            "A comma-separated list of the table names for which to return the schema. "
            "Example input: 'table1, table2, table3'"
        ),
    )


class InfoSQLDatabaseTool(BaseSQLDatabaseTool, BaseTool):
    """Tool for getting metadata about a SQL database."""

    name: str = "sql_db_schema"
    description: str = "Get the schema and sample rows for the specified SQL tables."
    args_schema: Type[BaseModel] = _InfoSQLDatabaseToolInput

    def _run(
        self,
        table_names: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Get the schema for tables in a comma-separated list."""

        tables = table_names.split(",")

        x = self.db.get_table_info_no_throw(
            [t.strip() for t in tables]
        )
        # y = getListOfTables(table_names)
        # print(x)
        return x


class SQLDatabaseToolkit(BaseToolkit):
    """Toolkit for interacting with SQL databases.

    Parameters:
        db: SQLDatabase. The SQL database.
        llm: BaseLanguageModel. The language model.
    """

    db: SQLDatabase = Field(exclude=True)
    llm: BaseLanguageModel = Field(exclude=True)

    @property
    def dialect(self) -> str:
        """Return string representation of SQL dialect to use."""
        return self.db.dialect

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        list_sql_database_tool = ListSQLDatabaseTool(db=self.db)
        info_sql_database_tool_description = (
            "Input to this tool is a comma-separated list of tables, output is the "
            "schema and sample rows for those tables. "
            "Be sure that the tables actually exist by calling "
            f"{list_sql_database_tool.name} first! "
            "Example Input: table1, table2, table3"
        )
        info_sql_database_tool = InfoSQLDatabaseTool(
            db=self.db, description=info_sql_database_tool_description
        )
        query_sql_database_tool_description = (
            "Input to this tool is a detailed and correct SQL query, output is a "
            "result from the database. If the query is not correct, an error message "
            "will be returned. If an error is returned, rewrite the query, check the "
            "query, and try again. If you encounter an issue with Unknown column "
            f"'xxxx' in 'field list', use {info_sql_database_tool.name} "
            # f"You can also use the relevent tables schema from here, {self.state["relevant_tables_schemas"]} please make sure you read the talble names, column name correctly and use it."
            "to query the correct table fields."
        )
        query_sql_database_tool = QuerySQLDataBaseTool(
            db=self.db, description=query_sql_database_tool_description
        )
        query_sql_checker_tool_description = (
            "Use this tool to double check if your query is correct before executing "
            "it. Always use this tool before executing a query with "
            f"{query_sql_database_tool.name}!"
        )
        query_sql_checker_tool = QuerySQLCheckerTool(
            db=self.db, llm=self.llm, description=query_sql_checker_tool_description
        )

        # Custom Tools below
        elastic_search_tool = ElasticSearchTool(db=self.db)
        schema_fetch_tool = SchemaFetchTool(db=self.db)
        relationship_fetch_tool = RelationshipFetchTool(db=self.db)


        return [
            query_sql_database_tool,
            # info_sql_database_tool,
            list_sql_database_tool,
            query_sql_checker_tool,
            elastic_search_tool,
            schema_fetch_tool,
            relationship_fetch_tool
        ]


    def get_less_tools(self) -> List[BaseTool]:
        list_sql_database_tool = ListSQLDatabaseTool(db=self.db)
        schema_fetch_tool = SchemaFetchTool(db=self.db)
        relationship_fetch_tool = RelationshipFetchTool(db=self.db)

        return [
            list_sql_database_tool,
            schema_fetch_tool,
            relationship_fetch_tool
        ]


    def get_context(self) -> dict:
        """Return db context that you may want in agent prompt."""
        return self.db.get_context()
    


