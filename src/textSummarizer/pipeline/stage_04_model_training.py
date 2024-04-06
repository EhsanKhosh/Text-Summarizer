from textSummarizer.entity import ModelTrainerConfig
from  textSummarizer.components.model_trainer import ModelTrainer
from textSummarizer.config.configuration import ConfigurationManager

class ModelTrainerTrainingPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config_manager = ConfigurationManager()
        config = config_manager.get_model_trainer_config()
        model_trainer = ModelTrainer(config)
        model_trainer.train()

    