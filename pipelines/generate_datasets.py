from zenml import pipeline

from llm_arxiv.domain.dataset import DatasetType
from llm_arxiv.settings import settings
from steps import generate_datasets as cd_steps
from steps.generate_datasets.push_to_huggingface import (
    push_to_huggingface as push_to_hf_step,
)


@pipeline
def generate_datasets(
    dataset_type: DatasetType = DatasetType.INSTRUCTION,
    test_split_size: float = 0.1,
    push_to_huggingface: bool = True,
    dataset_id: str | None = "itsmuriuki/arxiv-ml-instructions",
    mock: bool = False,  # Default to True for faster development
    max_documents: int = 5,  # Limit documents for faster testing
    wait_for: str | list[str] | None = None,
) -> None:
    cleaned_documents = cd_steps.query_feature_store(after=wait_for, max_documents=max_documents)
    prompts = cd_steps.create_prompts(documents=cleaned_documents, dataset_type=dataset_type)
    if dataset_type == DatasetType.INSTRUCTION:
        dataset = cd_steps.generate_instruction_dataset(prompts=prompts, test_split_size=test_split_size, mock=mock)
    elif dataset_type == DatasetType.PREFERENCE:
        dataset = cd_steps.generate_preference_dataset(prompts=prompts, test_split_size=test_split_size, mock=mock)
    else:
        raise ValueError(f"Invalid dataset type: {dataset_type}")

    if push_to_huggingface and dataset_id and settings.validate_huggingface_token:
        push_to_hf_step(dataset=dataset, dataset_id=dataset_id)