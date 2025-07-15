import transformers
from huggingface_hub import snapshot_download
from presidio_analyzer import AnalyzerEngine, Pattern
from presidio_analyzer.nlp_engine import NerModelConfiguration, TransformersNlpEngine
from transformers import AutoTokenizer, AutoModelForTokenClassification
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult, OperatorConfig
from presidio_analyzer.predefined_recognizers import CreditCardRecognizer
from phone_recognizer import *
from tckn_recognizer import TcknRecognizer

transformers_model = "akdeniz27/bert-base-turkish-cased-ner"

snapshot_download(repo_id=transformers_model)

AutoTokenizer.from_pretrained(transformers_model)
AutoModelForTokenClassification.from_pretrained(transformers_model)

model_config = [
    {"lang_code": "tr",
     "model_name": {
         "spacy": "xx_ent_wiki_sm", # for tokenization, lemmatization
         "transformers": "akdeniz27/bert-base-turkish-cased-ner" # for NER
    }
}]

mapping = dict(
    PER="PERSON",
    LOC="LOCATION",
    ORG="ORGANIZATION",
)

labels_to_ignore = ["O"]

ner_model_configuration = NerModelConfiguration(
    model_to_presidio_entity_mapping=mapping,
    alignment_mode="expand", # "strict", "contract", "expand"
    aggregation_strategy="max", # "simple", "first", "average", "max"
    labels_to_ignore = labels_to_ignore)

transformers_nlp_engine = TransformersNlpEngine(
    models=model_config,
    ner_model_configuration=ner_model_configuration)

analyzer = AnalyzerEngine(
    nlp_engine=transformers_nlp_engine,
    supported_languages=["tr"]
)
credit_card_patterns = [
        Pattern(
            "All Credit Cards (weak)",
            r"\b(?!1\d{12}(?!\d))((4\d{3})|(5[0-5]\d{2})|(6\d{3})|(1\d{3})|(3\d{3})|(2\d{3}))[- ]?(\d{3,4})[- ]?(\d{3,4})[- ]?(\d{3,5})\b",  # noqa: E501
            0.3,
        ),
    ]

tcknRecognizer = TcknRecognizer()
# print(analyzer.registry.get_supported_entities())
analyzer.registry.remove_recognizer(recognizer_name="InVoterRecognizer")
analyzer.registry.remove_recognizer(recognizer_name="PhoneRecognizer")
#print(analyzer.registry.get_supported_entities())
cardRecognizer = CreditCardRecognizer(supported_language="tr", context=["kredi", "kart", "numara", "harcama"], patterns=credit_card_patterns)
analyzer.registry.add_recognizer(cardRecognizer)
analyzer.registry.add_recognizer(phoneRecognizer)
analyzer.registry.add_recognizer(tcknRecognizer)
#print(analyzer.registry.get_supported_entities())



text = ("Merhaba, ben Ayşe Yılmaz. T.C. kimlik numaram 12345678901 "
        "ve 4647 5486 4862 8411 numaralı kredi kartımı sıkça kullanıyorum. "
        "Bana ayse.yilmaz@example.com üzerinden ulaşabilir veya +90 532 123 45 67 "
        "numaralı telefondan arayabilirsiniz."
        " İstanbul’daki adresim Atatürk Caddesi No: 10, Daire: 5, Kadıköy.")
results = analyzer.analyze(text=text, language="tr", return_decision_process=True)

# print("Returning full results, including the decision process:")
# for i, result in enumerate(results):
#     print(f"\tResult {i}: {result}")
#     print(f"\tDetected text: {text[result.start: result.end]}")
#     print(f"\t{result.analysis_explanation.textual_explanation}")
#     print("")


# anonymizer_engine = AnonymizerEngine()
#
# result = anonymizer_engine.anonymize(
#     text=text,
#     analyzer_results=results,
#     operators={"All": OperatorConfig("mask", {"masking_char":"*", "chars_to_mask":10, "from_end":False})},
# )
#
# print(result)