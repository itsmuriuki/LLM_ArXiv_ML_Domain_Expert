from llm_arxiv.domain.base import VectorBaseDocument
from llm_arxiv.domain.cleaned_documents import CleanedPaperDocument
from llm_arxiv.domain.types import DataCategory


class Prompt(VectorBaseDocument):
    template: str
    input_variables: dict
    content: str
    num_tokens: int | None = None

    class Config:
        category = DataCategory.PROMPT


class GenerateDatasetSamplesPrompt(Prompt):
    data_category: DataCategory
    document: CleanedPaperDocument