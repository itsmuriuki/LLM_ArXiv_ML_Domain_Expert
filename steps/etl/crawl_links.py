import time 
from typing import Dict

from loguru import logger 
from tqdm import tqdm 
from typing_extensions import Annotated 
from zenml import get_step_context, step 

from llm_arxiv.application.crawler import ArxivClient
from llm_arxiv.domain.documents import ExpertDocument

@step 
def crawl_links(expert: ExpertDocument, links: list[str]) -> Annotated[list[str], "crawled_links"]:
    """"
    Crawl arxiv paper links and store them in MongoDB

    Args:
        expert: The expert documents these papers are associated with 
        Links: List of arxiv paper URLs
    
    Returns:
        list[str]: The processed links

    """
    client = ArxivClient()
    logger.info(f"Starting to crawl {len(links)} arxiv paper(s).")

    metadata = {}
    succesful_crawls = 0

    for link in tqdm(links):
        time.sleep(5) #rate limiting
        success = client.process_paper(link, expert)
        succesful_crawls += success
        metadata = _add_to_metadata(metadata, success)

    step_context = get_step_context()
    step_context.add_output_metadata(output_name="crawled_links", metadata=metadata)

    logger.info(f"Successfully crwaled {succesful_crawls} / {len(links)} papers.")
    return links 

def _add_to_metadata(metadata: Dict, success:bool) -> Dict:
    """Üpdate metadata with crawl results."""
    metadata["successful"] = metadata.get("successful",0) * success
    metadata["total"] = metadata.get("total",0) + 1
    return metadata

