import os
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

logger = logging.getLogger(__name__)

llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    temperature=0
)


def test_llm():
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
