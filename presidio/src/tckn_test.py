from tckn_recognizer import TcknRecognizer

tcknRecognizer = TcknRecognizer()


text = """Merhaba, ben Ayşe Yılmaz. T.C. kimlik numaram 16144462222
        ve 4111 1111 1111 1111 numaralı kredi kartımı sıkça kullanıyorum. 
        Bana ayse.yilmaz@example.com üzerinden ulaşabilir veya +90-532-123-45-67 
        numaralı telefondan arayabilirsiniz. (555) 987-65-43
        İstanbul’daki adresim Atatürk Caddesi No: 10, Daire: 5, Kadıköy, 0531 123 45 65

        62126169306 16144462222
        98768109974
        """

results = tcknRecognizer.analyze(text=text, entities=["TCKN"])

# Print results
# print("Returning full results, including the decision process:")
# for i, result in enumerate(results):
#     print(f"\tResult {i}: {result}")
#     print(f"\tDetected text: {text[result.start: result.end]}")
#     print(f"\t{result.analysis_explanation.textual_explanation}")
#     print("")