import allure  # Импортируем allure

from elements.base_element import BaseElement
from tools.logger import get_logger

logger = get_logger("FILE_INPUT")

class FileInput(BaseElement):
    @property
    def type_of(self) -> str:  # Переопределяем свойство type_of
        return "file input"

    def set_input_files(self, file: str, nth: int = 0, **kwargs):
        step = f'Set file {file} to {self.type_of} "{self.name}"'
        with allure.step(step):
            logger.info(step)
            locator = self.get_locator(nth, **kwargs)
            locator.set_input_files(file)
