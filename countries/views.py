import random, requests, os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import CountryData
from .serializers import CountryDataSerializer

CACHE_DIR = os.path.join(settings.BASE_DIR, "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

SUMMARY_PATH = os.path.join(CACHE_DIR, "summary.png")

class RefreshCountryView(APIView):
    def post(self, request):
        try:
            country_resp = requests.get("https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies")
            exchange_resp = requests.get("https://open.er-api.com/v6/latest/USD")

            if country_resp.status_code != 200 or exchange_resp.status_code != 200:
                return Response({"error": "External data source unavailable"}, status=503)

            countries = country_resp.json()
            rates = exchange_resp.json().get("rates", {})

            CountryData.objects.all().delete()  # clear cache before new insert

            for c in countries:
                name = c.get("name")
                capital = c.get("capital")
                region = c.get("region")
                population = c.get("population", 0)
                flag_url = c.get("flag")
                currencies = c.get("currencies", [])
                currency_code = currencies[0]["code"] if currencies else None

                exchange_rate = rates.get(currency_code)
                gdp_random = random.randint(1000, 2000)
                estimated_gdp = (population * gdp_random / exchange_rate) if exchange_rate else None

                CountryData.objects.create(
                    name=name,
                    capital=capital,
                    region=region,
                    population=population,
                    currency_code=currency_code,
                    exchange_rate=exchange_rate,
                    estimated_gdp=estimated_gdp,
                    flag_url=flag_url,
                )

            # Generate summary image
            self.generate_summary_image()
            return Response({"message": "Refresh completed"}, status=200)

        except Exception as e:
            return Response({"error": "Internal server error", "details": str(e)}, status=500)

    def generate_summary_image(self):
        total = CountryData.objects.count()
        top5 = CountryData.objects.exclude(estimated_gdp=None).order_by("-estimated_gdp")[:5]
        last_refresh = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")

        img = Image.new("RGB", (600, 400), color="white")
        draw = ImageDraw.Draw(img)
        draw.text((20, 20), f"Total Countries: {total}", fill="black")
        draw.text((20, 60), "Top 5 by GDP:", fill="black")

        y = 100
        for c in top5:
            draw.text((40, y), f"{c.name}: {round(c.estimated_gdp or 0, 2)}", fill="black")
            y += 40

        draw.text((20, y + 20), f"Last Refreshed: {last_refresh}", fill="black")
        img.save(SUMMARY_PATH)


class CountryListView(APIView):
    def get(self, request):
        region = request.GET.get("region")
        currency = request.GET.get("currency")
        sort = request.GET.get("sort")

        queryset = CountryData.objects.all()

        if region:
            queryset = queryset.filter(region__iexact=region)
        if currency:
            queryset = queryset.filter(currency_code__iexact=currency)
        if sort == "gdp_desc":
            queryset = queryset.order_by("-estimated_gdp")

        serializer = CountryDataSerializer(queryset, many=True)
        return Response(serializer.data)


class CountryDetailView(APIView):
    def get(self, request, name):
        country = get_object_or_404(CountryData, name__iexact=name)
        serializer = CountryDataSerializer(country)
        return Response(serializer.data)

    def delete(self, request, name):
        country = get_object_or_404(CountryData, name__iexact=name)
        country.delete()
        return Response({"message": "Country deleted"}, status=200)


class StatusView(APIView):
    def get(self, request):
        total = CountryData.objects.count()
        last_refreshed = CountryData.objects.order_by("-last_refreshed_at").first()
        return Response({
            "total_countries": total,
            "last_refreshed_at": last_refreshed.last_refreshed_at if last_refreshed else None
        })


class SummaryImageView(APIView):
    def get(self, request):
        if not os.path.exists(SUMMARY_PATH):
            return Response({"error": "Summary image not found"}, status=404)
        from django.http import FileResponse
        return FileResponse(open(SUMMARY_PATH, "rb"), content_type="image/png")
