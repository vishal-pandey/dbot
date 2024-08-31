from langchain_core.pydantic_v1 import BaseModel, Field, root_validator
from langchain_community.tools import BaseTool
from langchain_community.utilities.sql_database import SQLDatabase
from typing import Any, Dict, Optional, Sequence, Type, Union
import requests



class BaseSQLDatabaseTool(BaseModel):
    """Base tool for interacting with a SQL database."""

    db: SQLDatabase = Field(exclude=True)

    class Config(BaseTool.Config):
        pass

class _ElasticSearchToolInput(BaseModel):
    tool_input: str = Field("", description="Name of the entity not understood by llm")


def searchElastic(query: str):
    url = "http://server.vishalpandey.co.in:9200/table_search_index/_search?q="+query

    response = requests.post(url)

    return response.json()

class ElasticSearchTool(BaseSQLDatabaseTool, BaseTool):
    """Tool for getting the entity detail from the term asked by user. It is basically a search engine to get more information about the entity. From its value"""

    name: str = "elastic_search"
    description: str = "Input is term which not able to understand, output is the entity detail. In json format"
    args_schema: Type[BaseModel] = _ElasticSearchToolInput

    def _run(
        self,
        tool_input: str = "",
    ):
        """Get detail about the entity in json format"""
        # return ", ".join([
        #     "tag",
        #     "tag_usage",
        #     "table_entity"
        # ])
        return searchElastic(tool_input)



