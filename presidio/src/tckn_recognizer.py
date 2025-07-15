from collections import defaultdict
from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer, EntityRecognizer


class TcknRecognizer(PatternRecognizer):
    """Recognize TR kimlik number (TCKN) using regex and checksum.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern("TCKN", r"\b[1-9][0-9]{9}[02468]\b", 0.1),
    ]

    CONTEXT = [
        "kimlik",
        "numara"
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "tr",
        supported_entity: str = "TCKN",
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )
        EntityRecognizer.MAX_SCORE = 0.7

    def validate_result(self, pattern_text: str) -> bool:
        """
        Check if the pattern text follows TCKN checksum rules.

        :param pattern_text: Text detected as pattern by regex
        :return: True if validated
        """
        print(pattern_text)
        list_tc = list_tc = list(map(int, pattern_text))
        tc10 = (sum(list_tc[0:10:2]) * 7 - sum(list_tc[1:9:2])) % 10
        tc11 = (sum(list_tc[0:9]) + tc10) % 10
        return True if list_tc[9] == tc10 and list_tc[10] == tc11 else False