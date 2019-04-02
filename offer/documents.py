import coreapi, coreschema
from rest_framework.schemas import AutoSchema

offer_schema = AutoSchema(manual_fields=[
    coreapi.Field("member_id", required=False, location="query", type="integer",
                  schema=coreschema.String(description="ForeingKey -> Member"))
])
