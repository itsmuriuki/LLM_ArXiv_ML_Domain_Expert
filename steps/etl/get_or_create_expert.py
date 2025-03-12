from loguru import logger
from typing_extensions import Annotated
from zenml import get_step_context, step 

from llm_arxiv.domain.document import ExpertDocument

@step 
def get_or_create_expert(domain: str) -> Annotated[ExpertDocument, "expert"]:
    """"
    ZenML step to get or create an ML domain expert.

    Args:
        domain: The ML domain of expertise (e.g "machine Learning", "deep learning", "nlp")

    Returns:
        ExpertDocument: The expert document from MongoDB
    """
    logger.info(f"Getting or creating expert for domain:{domain}")
    expert = ExpertDocument.get_or_create(domain=domain)
    step_context = get_step_context()
    # helps track queries and retrived experts by attaching metadata to ZenML tracking system
    step_context.add_output_metadata(output_name="expert", metadata=_get_metadata(domain, expert))

    return expert 

def _get_metadata(domain:str, expert: ExpertDocument) -> dict:
    """
    Get metadata about the expert from ZenML tracking.

    Args:
        domain: The queried domain
        expert: The expert document
    Returns:
        dict: Metadata about the query and retrived expert 
    """
    return {
        "query":{
            "domain": domain, #The ML domain being queried
        },
        "retrieved":{
            "expert_id": str(expert.id), # The mongo DB document ID
        },
    }


