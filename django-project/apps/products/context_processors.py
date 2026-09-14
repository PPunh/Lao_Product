from .models import CurrencyModel

def default_currency(request):
    try:
        # Get Default
        currency = CurrencyModel.objects.filter(is_default=True).first()
        
        # of not checked is_default will get from DB instead
        if not currency:
            currency = CurrencyModel.objects.first()

        # if in DB is empty will Hardcode for checking the Context Processor are still working?
        symbol = currency.get_currency_symbol() if currency else '₭ (Fallback)'
        
        return {
            'DEFAULT_CURRENCY_SYMBOL': symbol
        }
    except Exception as e:
        # Print Error
        print("--- CONTEXT PROCESSOR ERROR ---:", e)
        return {
            'DEFAULT_CURRENCY_SYMBOL': 'ERROR'
        }