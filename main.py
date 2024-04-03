from textSummarizer.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from textSummarizer.logging import logger


STAGE_NAME = "data ingestion stage"

try: 
    logger.info(">>>> Starting {}<<<<".format(STAGE_NAME))
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(f">>>> {STAGE_NAME} completed.<<<<<\n\n================================")

except Exception as e:
    logger.exception(e)
    raise e