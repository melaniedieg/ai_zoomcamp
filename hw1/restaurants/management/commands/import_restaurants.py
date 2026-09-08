import json
import urllib.parse
import urllib.request

from django.core.management.base import BaseCommand

from restaurants.models import Restaurant

# NYC Open Data: DOHMH Restaurant Inspection Results
# https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j
API_URL = "https://data.cityofnewyork.us/resource/43nn-pn8j.json"


class Command(BaseCommand):
    help = "Import restaurant records from the NYC DOHMH restaurant inspection dataset."

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=2000,
            help="Number of inspection rows to fetch before deduplicating by restaurant.",
        )

    def handle(self, *args, **options):
        limit = options["limit"]
        query = {
            "$select": "camis,dba,boro,building,street,zipcode,cuisine_description",
            "$where": "dba IS NOT NULL",
            "$order": "camis",
            "$limit": limit,
        }
        url = f"{API_URL}?{urllib.parse.urlencode(query)}"

        request = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(request, timeout=30) as response:
            rows = json.load(response)

        # The dataset has one row per inspection, so keep only the first
        # row seen for each restaurant (identified by its CAMIS id).
        restaurants_by_id = {}
        for row in rows:
            camis = row.get("camis")
            if camis and camis not in restaurants_by_id:
                restaurants_by_id[camis] = row

        created_count = 0
        updated_count = 0
        for camis, row in restaurants_by_id.items():
            address_parts = [row.get("building", ""), row.get("street", "").title()]
            address = " ".join(part for part in address_parts if part).strip()
            if row.get("zipcode"):
                address = f"{address}, {row['zipcode']}" if address else row["zipcode"]

            _, created = Restaurant.objects.update_or_create(
                external_id=camis,
                defaults={
                    "name": row.get("dba", "").title(),
                    "borough": row.get("boro", "").title(),
                    "cuisine": row.get("cuisine_description", "").title(),
                    "address": address,
                },
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {len(restaurants_by_id)} restaurants "
                f"({created_count} created, {updated_count} updated)."
            )
        )
