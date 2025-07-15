import phonenumbers
from phonenumbers import PhoneNumberMatcher, PhoneNumberFormat
from phonenumbers.phonenumberutil import NumberParseException

text = """
Merhaba! Bana bu numaralardan birinden ulaşabilirsin:
• +90 532 123 45 67
• 0212 555 34 21
• (555) 987-65-43
"""

# 1. Create a matcher for text assumed to be in Turkey ("TR")
matcher = PhoneNumberMatcher(text, "TR")

# 2. Iterate over all matches
for match in matcher:
    # raw substring as found in the text
    raw = match.raw_string
    # the parsed phonenumbers.PhoneNumber object
    num = match.number
    # character positions of this match in `text`
    start, end = match.start, match.end

    # format in E.164 (international standard): +905321234567
    e164 = phonenumbers.format_number(num, PhoneNumberFormat.E164)
    # format in national format: 0 532 123 45 67
    national = phonenumbers.format_number(num, PhoneNumberFormat.NATIONAL)

    print(f"Found `{raw}` at [{start}:{end}]")
    print(f"  → E.164:    {e164}")
    print(f"  → National: {national}\n")