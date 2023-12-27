from langchain.retrievers import EnsembleRetriever as OriginEnsembleRetriever
from typing import Any, Dict, List

from langchain.callbacks.manager import (
    AsyncCallbackManagerForRetrieverRun,
    CallbackManagerForRetrieverRun,
)
#from langchain.pydantic.v1 import root_validator
from pydantic import root_validator
from langchain.schema import BaseRetriever, Document

class EnsembleRetriever(OriginEnsembleRetriever):
  def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun,
    ) -> List[Document]:
    res = super()._get_relevant_documents(query, run_manager=run_manager)
    #print([r.page_content for r in res])
    return res