from django.contrib import admin
from .models import QuoteRequest, BrokerQuote

admin.site.register(QuoteRequest)
admin.site.register(BrokerQuote)