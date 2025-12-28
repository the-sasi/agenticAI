import os
import logging
from dotenv import load_dotenv
from tools.llm_factory import create_llm

load_dotenv()

logger = logging.getLogger(__name__)

# Default LLM instance (backward compatible)
# Uses LLM_PROVIDER env var to determine which provider to use
llm = create_llm(
    provider=os.getenv("LLM_PROVIDER", "openai"),
    model=os.getenv("LLM_MODEL"),
    temperature=float(os.getenv("LLM_TEMPERATURE", "0"))
)


def test_llm():
    """Test LLM connectivity"""
    try:
        logger.info("Testing LLM connection...")
        response = llm.invoke("Say hello in one short sentence.")
        logger.info(f"LLM response: {response.content}")
        return True
    except Exception as e:
        logger.error(f"LLM test failed: {str(e)}")
        return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_llm()
