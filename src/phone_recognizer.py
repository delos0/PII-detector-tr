from presidio_analyzer.predefined_recognizers import PhoneRecognizer

tr_context = ["numara", "telefon", "aramak"]

phoneRecognizer = PhoneRecognizer(context=tr_context, supported_language="tr", supported_regions=["TR"])

text = """Merhaba, ben Ayşe Yılmaz. T.C. kimlik numaram  90212 555 34 21
        ve 4111 1111 2222 3333 numaralı kredi kartımı sıkça kullanıyorum. 
        Bana ayse.yilmaz@example.com üzerinden ulaşabilir veya +90-532-123-45-67 
        numaralı telefondan arayabilirsiniz. (555) 987-65-43
        İstanbul’daki adresim Atatürk Caddesi No: 10, Daire: 5, Kadıköy, 0531 123 45 65.
        """

results = phoneRecognizer.analyze(text=text, entities=["PHONE_NUMBER"])

# Print results
# print("Returning full results, including the decision process:")
# for i, result in enumerate(results):
#     print(f"\tResult {i}: {result}")
#     print(f"\tDetected text: {text[result.start: result.end]}")
#     print(f"\t{result.analysis_explanation.textual_explanation}")
#     print("")