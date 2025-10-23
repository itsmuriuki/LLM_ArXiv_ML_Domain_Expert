from loguru import logger
from typing_extensions import Annotated
from zenml import step

from llm_arxiv.domain.dataset import InstructTrainTestSplit, PreferenceTrainTestSplit
from llm_arxiv.settings import settings


@step
def push_to_huggingface(
    dataset: Annotated[InstructTrainTestSplit | PreferenceTrainTestSplit, "dataset_split"],
    dataset_id: Annotated[str, "dataset_id"],
) -> None:
    assert dataset_id is not None, "Dataset id must be provided for pushing to Huggingface"
    assert settings.validate_huggingface_token, (
        "Huggingface access token must be provided for pushing to Huggingface"
    )

    # Skip push when dataset is empty to avoid concatenate_datasets([]) errors
    try:
        train_samples = sum(d.num_samples for d in dataset.train.values())
        test_samples = sum(d.num_samples for d in dataset.test.values())
    except Exception:
        # Fallback if dataset shape differs
        train_samples = 0
        test_samples = 0

    if train_samples == 0 or test_samples == 0:
        logger.warning(
            "Skipping push to Hugging Face: empty split detected (train=%d, test=%d)",
            train_samples,
            test_samples,
        )
        return

    logger.info(
        f"Pushing dataset {dataset_id} to Hugging Face (train={train_samples}, test={test_samples})."
    )

    # Flattened upload for a single combined train/test split
    huggingface_dataset = dataset.to_huggingface(flatten=True)
    huggingface_dataset.push_to_hub(dataset_id)


