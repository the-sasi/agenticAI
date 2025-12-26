import logging
import sys
from agent.graph import agent
from tools.blob_tools import list_files
from config.settings import validate_env


def setup_logging():
    """
    Configure logging for the application
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('agent.log')
        ]
    )


def main():
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        # Validate environment variables
        logger.info("\n🧩 LANGGRAPH STRUCTURE")
        logger.info(agent.get_graph().draw_ascii())
        validate_env()

        # Get initial file list
        files = list_files()

        if not files:
            logger.warning("No files to process")
            return

        logger.info(f"Processing {len(files)} files")

        # Create initial state
        initial_state = {
            "files": list_files(),
            "current_file": None,
            "category": None,
            "step": 0
        }


        # Run agent
        # result = agent.invoke(initial_state)
        for event in agent.stream(initial_state):
            for node, state_update in event.items():
                logger.info(f"NODE: {node}")
                logger.info("STATE UPDATE:", state_update)


        logger.info("Agent completed successfully")
        # logger.info(f"Final state: {result}")

    except EnvironmentError as e:
        logger.error(f"Environment configuration error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Agent failed with error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":

    main()
