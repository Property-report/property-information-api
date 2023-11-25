import requests
from urllib.parse import quote
import time
import json
import datetime


def get_last_12_months():
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    if str(current_month).zfill(2) == '01':
        current_year = datetime.datetime.now().year - 1

    current_month = current_month - 1
    last_12_months = []
    for i in range(12):
        month = current_month - i
        year = current_year
        if month < 1:
            month += 12
            year -= 1
        last_12_months.append(str(year) + "-" + str(month).zfill(2))
    return last_12_months


def get_when_fresh_oauth():
    url = "https://id.api.whenfresh.com/oauth2/token"

    payload = f"client_id=r5e6j0k1oevsfgmb9secod9qd&grant_type=refresh_token&refresh_token={config.whenfresh_refresh_token}"
    headers = {
        'accept': "application/json",
        'content-type': "application/x-www-form-urlencoded",
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    return json.loads(response.text)


def get_address_postcode_key(postcode, token):

    url = "https://api.whenfresh.com/world/GB/addresses"
    new_postcode = postcode.strip()
    print(new_postcode)
    if ' ' not in new_postcode:
        new_postcode = new_postcode[:3] + ' ' + new_postcode[3:]
    print(new_postcode)
    querystring = {"postcode": new_postcode}

    headers = {
        'accept': "application/ld+json",
        'authorization': f"Bearer {token}"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    return json.loads(response.text)


def get_uprn(house_number, street, postcode):
    uprn_results = requests.get(
        f"https://api.propertydata.co.uk/uprns?key={config.property_data_api_key}&postcode={postcode}")
    if uprn_results.json()["status"] == "error":
        # if error code is X14 wait 3 seconds and try again
        if uprn_results.json()["code"] == "X14":
            time.sleep(11)
            uprn_results = requests.get(
                f"https://api.propertydata.co.uk/uprns?key={config.property_data_api_key}&postcode={postcode}")
            if uprn_results.json()["status"] == "error":
                return {}
        else:
            return {}

    address_uprn = None
    input_address = f"{house_number} {street}, {postcode}"
    normalized_input_address = normalize_address(input_address)

    for uprns in uprn_results.json().get('data', []):
        normalized_uprns_address = normalize_address(uprns["address"])
        if normalized_input_address == normalized_dict_address:
            address_uprn = uprns['uprn']

    return address_uprn


def get_uprn_whenfresh(address_key, token):

    url = f"https://api.whenfresh.com/world/GB/addresses/{address_key}/catalog"
    payload = '{"@context": "http://api.whenfresh.com/.hydra/context.jsonld","@type": "PurchaseVariableAction","variables": ["https://api.whenfresh.com/vars/CLS/OS MasterMap#Ordnance Survey/Spatial/Address/Unique Property Reference Number"]}'

    headers = {
        'accept': "application/ld+json",
        'content-type': "application/ld+json",
        'authorization': f"Bearer {token}"
    }

    response = requests.request(
        "POST", url, data=payload.encode('utf-8'), headers=headers)
    return json.loads(response.text)


def get_bedroom_number2(address_key, token):

    url = f"https://api.whenfresh.com/world/GB/addresses/{address_key}/catalog"
    payload = '{"@context": "http://api.whenfresh.com/.hydra/context.jsonld","@type": "PurchaseVariableAction","variables": ["https://api.whenfresh.com/vars/Zoopla/Property Attribute#Dwelling/Rooms/Bedrooms/Bedroom Count"]}'

    headers = {
        'accept': "application/ld+json",
        'content-type': "application/ld+json",
        'authorization': f"Bearer {token}"
    }

    response = requests.request(
        "POST", url, data=payload.encode('utf-8'), headers=headers)
    return json.loads(response.text)


def get_bedroom_number(address_key, token):

    url = f"https://api.whenfresh.com/world/GB/addresses/{address_key}/catalog"
    payload = '{"@context": "http://api.whenfresh.com/.hydra/context.jsonld","@type": "PurchaseVariableAction","variables": ["https://api.whenfresh.com/vars/WhenFresh/Property Attribute#Dwelling/Rooms/Bedrooms/Bedroom Count"]}'

    headers = {
        'accept': "application/ld+json",
        'content-type': "application/ld+json",
        'authorization': f"Bearer {token}"
    }

    response = requests.request(
        "POST", url, data=payload.encode('utf-8'), headers=headers)
    return json.loads(response.text)


def get_parking(address_key, token):

    url = f"https://api.whenfresh.com/world/GB/addresses/{address_key}/catalog"

    payload = '{"@context": "http://api.whenfresh.com/.hydra/context.jsonld","@type": "PurchaseVariableAction","variables": ["https://api.whenfresh.com/vars/CLS/ParkingTypes#Property/Parking/Provision/Property has Off-Road Parking"]}'

    headers = {
        'accept': "application/ld+json",
        'content-type': "application/ld+json",
        'authorization': f"Bearer {token}"
    }

    response = requests.request(
        "POST", url, data=payload.encode('utf-8'), headers=headers)
    return json.loads(response.text)


def get_bathroom_number(address_key, token):

    url = f"https://api.whenfresh.com/world/GB/addresses/{address_key}/catalog"

    payload = '{"@context": "http://api.whenfresh.com/.hydra/context.jsonld","@type": "PurchaseVariableAction","variables": ["https://api.whenfresh.com/vars/WhenFresh/Property Insurance#Dwelling/Rooms/Bathrooms/Bathroom Count (1⋯5+)"]}'

    headers = {
        'accept': "application/ld+json",
        'content-type': "application/ld+json",
        'authorization': f"Bearer {token}"
    }

    response = requests.request(
        "POST", url, data=payload.encode('utf-8'), headers=headers)
    return json.loads(response.text)


def get_air_polution(lon, lat):

    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid=8e6d4af8a7669c2ef80462ec6c8fe147"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)


def get_restaraunts(lon, lat):

    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat}%2C{lon}&radius=1610&type=restaurant&key={config.google_maps_apikey}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)


def get_post_office(lon, lat):

    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat}%2C{lon}&radius=1610&type=post_office&key={config.google_maps_apikey}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)


def get_gyms(lon, lat):

    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat}%2C{lon}&radius=1610&type=gym&key={config.google_maps_apikey}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)


def get_airport(lon, lat):

    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat}%2C{lon}&radius=1610&type=airport&key={config.google_maps_apikey}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)


def get_supermarkets(lon, lat):

    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat}%2C{lon}&radius=1610&type=supermarket&key={config.google_maps_apikey}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)


def get_cafes(lon, lat):

    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat}%2C{lon}&radius=1610&type=cafe&key={config.google_maps_apikey}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)


def get_lat_lon_opti(uprn):
    url = f"https://geo.private.optibroker.co.uk/lonlat?uprn={uprn}"

    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'authorization': f"Basic {config.geo_api_auth}=="
    }

    response = requests.request("GET", url, headers=headers)
    newreposnse = json.loads(response.text)

    if newreposnse.get("lat", "") == "" or newreposnse.get("lon", "") == "":
        new_lats = {}
    else:
        new_lats = {
            "latitude": newreposnse.get("lat", ""),
            "longitude": newreposnse.get("lon", ""),
            "uprn": uprn
        }

    return new_lats


def get_polygon_info(uprn):
    """Get lon and lat from the postcode API"""
    # lon_lat = requests.get(f"https://api.postcodes.io/postcodes/{postcode}")
    # output = {
    #     "longitude": lon_lat.json()["result"]["longitude"],
    #     "latitude": lon_lat.json()["result"]["latitude"]
    # }

    url = f"https://geo.private.optibroker.co.uk/property?uprn={uprn}"

    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'authorization': f"Basic {config.geo_api_auth}=="
    }

    response = requests.request("GET", url, headers=headers)

    return json.loads(response.text)


def get_lon_lat(postcode, house_number, street):
    """Get lon and lat from the postcode API"""
    lon_lat = requests.get(f"https://api.postcodes.io/postcodes/{postcode}")
    if "result" in lon_lat.json():
        output = {
            "longitude": lon_lat.json()["result"]["longitude"],
            "latitude": lon_lat.json()["result"]["latitude"]
        }
    else:
        output = {
            "longitude": "",
            "latitude": ""
        }
    return output

# get monthly crime rate from lon and lat


def get_monthly_crime_rate(lon_lat):
    """Get monthly crime rate from the Police API"""
    monthly_crime_rate = requests.get(
        f"https://data.police.uk/api/crimes-street/all-crime?lat={lon_lat['latitude']}&lng={lon_lat['longitude']}")
    # group and count crimes
    crime_count = {}
    for crime in monthly_crime_rate.json():
        if crime["category"] in crime_count:
            crime_count[crime["category"]] += 1
        else:
            crime_count[crime["category"]] = 1
    return crime_count


def get_monthly_crime_rate_12_months(lon_lat):
    crime_count = {}
    """Get monthly crime rate from the Police API"""
    for x in get_last_12_months():
        monthly_crime_rate = requests.get(
            f"https://data.police.uk/api/crimes-street/all-crime?lat={lon_lat['latitude']}&lng={lon_lat['longitude']}&date={x}")
    # group and count crimes
        for crime in monthly_crime_rate.json():
            if crime["category"] in crime_count:
                crime_count[crime["category"]] += 1
            else:
                crime_count[crime["category"]] = 1
    return crime_count


# get flood risk from propertydata.co.uk
def get_flood_risk(postcode):
    """Get flood risk from the Flood Information Service API"""
    flood_risk = requests.get(
        f"https://api.propertydata.co.uk/flood-risk?key={config.property_data_api_key}&postcode={postcode}")
    if flood_risk.json()["status"] == "error":
        # if error code is X14 wait 3 seconds and try again
        if flood_risk.json()["code"] == "X14":
            time.sleep(11)
            flood_risk = requests.get(
                f"https://api.propertydata.co.uk/flood-risk?key={config.property_data_api_key}&postcode={postcode}")
            if flood_risk.json()["status"] == "error":
                return {}
        else:
            return {}

    return flood_risk.json()

# get nearby schools from propertydata.co.uk


def get_nearby_schools(postcode):
    """Get nearby schools from the Ofsted API"""
    nearby_schools = requests.get(
        f"https://api.propertydata.co.uk/schools?key={config.property_data_api_key}&postcode={postcode}")
    if nearby_schools.json()["status"] == "error":
        # if error code is X14 wait 3 seconds and try again
        if nearby_schools.json()["code"] == "X14":
            time.sleep(11)
            nearby_schools = requests.get(
                f"https://api.propertydata.co.uk/schools?key={config.property_data_api_key}&postcode={postcode}")
            if nearby_schools.json()["status"] == "error":
                return {}
        else:
            return {}

    # group state schools by phase
    state_schools = {}
    for school in nearby_schools.json()["data"]["state"]["nearest"]:
        if school["phase"] in state_schools.keys():
            state_schools[school["phase"]].append(school)
        else:
            state_schools[school["phase"]] = [school]

    # group independent schools by type
    independent_schools = {}
    for school in nearby_schools.json()["data"]["independent"]["nearest"]:
        if school["type"] in independent_schools.keys():
            independent_schools[school["type"]].append(school)
        else:
            independent_schools[school["type"]] = [school]
    return {
        "state": state_schools,
        "independent": independent_schools
    }


# get title from uprn from propertydata.co.uk
def get_uprn_title(uprn):
    """Get title from upr"""

    titles = requests.get(
        f"https://api.propertydata.co.uk/uprn-title?key={config.property_data_api_key}&uprn={uprn}")
    if titles.json()["status"] == "error":
        # if error code is X14 wait 3 seconds and try again
        if titles.json()["code"] == "X14":
            time.sleep(11)
            titles = requests.get(
                f"https://api.propertydata.co.uk/uprn-title?key={config.property_data_api_key}&uprn={uprn}")
            if titles.json()["status"] == "error":
                return {}
        else:
            return {}

    return titles.json()["data"]


# get internet speed from propertydata.co.uk
def get_internet_speed(postcode):
    internet_speed = requests.get(
        f"https://api.propertydata.co.uk/internet-speed?key={config.property_data_api_key}&postcode={postcode}")
    # if internet_speed status is error, return error
    if internet_speed.json()["status"] == "error":
        # if error code is X14 wait 3 seconds and try again
        if internet_speed.json()["code"] == "X14":
            time.sleep(11)
            internet_speed = requests.get(
                f"https://api.propertydata.co.uk/internet-speed?key={config.property_data_api_key}&postcode={postcode}")
        else:
            return "unable to get data"
    return internet_speed.json()["internet"]

# get council tax band for property


def get_council_tax_band(postcode, house_number, street):
    council_tax_band = requests.get(
        f"https://api.propertydata.co.uk/council-tax?key={config.property_data_api_key}&postcode={postcode}")
    if council_tax_band.json()["status"] == "error":
        # if error code is X14 wait 3 seconds and try again
        if council_tax_band.json()["code"] == "X14":
            time.sleep(11)
            council_tax_band = requests.get(
                f"https://api.propertydata.co.uk/council-tax?key={config.property_data_api_key}&postcode={postcode}")
        else:
            return "unable to get data"
    band_prices = council_tax_band.json()["council_tax"]
    properties = council_tax_band.json()["properties"]
    output = {}
    for property in properties:
        current_house_number = property["address"].split(",")[0]
        if current_house_number == house_number:

            if street != '':
                if street.lower().strip() in property["address"].lower().strip():
                    output = {
                        "band": property["band"],
                        "price": band_prices[f'band_{property["band"].lower()}']
                    }
            else:
                output = {
                    "band": property["band"],
                    "price": band_prices[f'band_{property["band"].lower()}']
                }
    return output


def get_epc_certs(postcode, house_number):
    headers = {
        "Authorization": f"Basic {config.epc_auth}=",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    print(house_number)
    print(
        f"https://epc.opendatacommunities.org/api/v1/domestic/search?postcode={postcode}&address={house_number}")
    epc_certs = requests.get(
        f"https://epc.opendatacommunities.org/api/v1/domestic/search?postcode={postcode}&address={house_number}", headers=headers)
    print(epc_certs)
    print(epc_certs.text)


    if epc_certs.text != None and epc_certs.text != '':
        return epc_certs.json()["rows"][0]
    else:
        return {}


def get_epc_suggestions(lmk):
    headers = {
        "Authorization": f"Basic {config.epc_auth}=",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    epc_certs = requests.get(
        f"https://epc.opendatacommunities.org/api/v1/domestic/recommendations/{lmk}", headers=headers)
    return epc_certs.json()["rows"]


# get price paid data from land registry SPARQL endpoint
def get_price_paid_data(postcode, house_number):
    # get data from sparql query
    url = 'https://landregistry.data.gov.uk/landregistry/query'
    query = quote("""
            prefix lrcommon: <http://landregistry.data.gov.uk/def/common/>
            prefix xsd: <http://www.w3.org/2001/XMLSchema#>
            prefix lrppi: <http://landregistry.data.gov.uk/def/ppi/>
            prefix skos: <http://www.w3.org/2004/02/skos/core#>
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix owl: <http://www.w3.org/2002/07/owl#>
            prefix sr: <http://data.ordnancesurvey.co.uk/ontology/spatialrelations/>
            prefix ukhpi: <http://landregistry.data.gov.uk/def/ukhpi/>

            SELECT ?paon ?saon ?street ?town ?county ?postcode ?amount ?date ?category
            WHERE
            {
              VALUES ?postcode {'""" + format_postcode(postcode) + """'^^xsd:string}

              ?addr lrcommon:postcode ?postcode.

              ?transx lrppi:propertyAddress ?addr ;
                      lrppi:pricePaid ?amount ;
                      lrppi:transactionDate ?date ;
                      lrppi:transactionCategory/skos:prefLabel ?category.

              OPTIONAL {?addr lrcommon:county ?county}
              OPTIONAL {?addr lrcommon:paon ?paon}
              OPTIONAL {?addr lrcommon:saon ?saon}
              OPTIONAL {?addr lrcommon:street ?street}
              OPTIONAL {?addr lrcommon:town ?town}
            }
            ORDER BY ?amount""")

    r = requests.get(f"{url}?query={query}&format=json")
    data = r.json()
    output = []
    for result in data["results"]["bindings"]:
        # check if result["paon"]["value"] has , in it
        if "," in result["paon"]["value"]:
            check_house_number = result["paon"]["value"].split(",")[1].strip()
        else:
            check_house_number = result["paon"]["value"]

        if check_house_number == house_number:
            output.append({
                "price": result["amount"]["value"],
                "date": result["date"]["value"]
            })
    return output

# function which returns uk postcode with spaces


def format_postcode(postcode):
    postcode = postcode.upper().replace(" ", "")
    postcode = postcode[:-3] + " " + postcode[-3:]
    return postcode

# function which returns planning applications for property


def get_build_cost(postcode, internal_area):
    get_feet = float(internal_area)/0.0929
    build_cost = requests.get(
        f"https://api.propertydata.co.uk/build-cost?key={config.property_data_api_key}&postcode={postcode}&internal_area={get_feet}&finish_quality=medium")
    if build_cost.json()["status"] == "error":
        # if error code is X14 wait 3 seconds and try again
        if build_cost.json()["code"] == "X14":
            time.sleep(11)
            build_cost = requests.get(
                f"https://api.propertydata.co.uk/build-cost?key={config.property_data_api_key}&postcode={postcode}&internal_area={get_feet}&finish_quality=medium")
            if build_cost.json()["status"] == "error":
                return {}
        else:
            return {}
    return build_cost.json()["data"]

# function which returns planning applications for property


def get_valuation(postcode, property_type, construction_date, internal_area, bedrooms, bathrooms, finish_quality, outdoor_space, off_street_parking):
    get_feet = float(internal_area)/0.0929
    valuation = requests.get(
        f"https://api.propertydata.co.uk/valuation-sale?key={config.property_data_api_key}&postcode={postcode}&internal_area={get_feet}&property_type={property_type}&construction_date={construction_date}&bedrooms={bedrooms}&bathrooms={bathrooms}&finish_quality={finish_quality}&outdoor_space={outdoor_space}&off_street_parking={off_street_parking}")
    if valuation.json()["status"] == "error":
        # if error code is X14 wait 3 seconds and try again
        if valuation.json()["code"] == "X14":
            time.sleep(11)
            valuation = requests.get(
                f"https://api.propertydata.co.uk/valuation-sale?key={config.property_data_api_key}&postcode={postcode}&internal_area={get_feet}&property_type={property_type}&construction_date={construction_date}&bedrooms={bedrooms}&bathrooms={bathrooms}&finish_quality={finish_quality}&outdoor_space={outdoor_space}&off_street_parking={off_street_parking}")
            if valuation.json()["status"] == "error":
                return {}
        else:
            return {}
    return planning_applications.json()["result"]

# function which returns planning applications for property


def get_planning_applications(postcode):
    planning_applications = requests.get(
        f"https://api.propertydata.co.uk/planning?key={config.property_data_api_key}&postcode={postcode}")
    if planning_applications.json()["status"] == "error":
        # if error code is X14 wait 3 seconds and try again
        if planning_applications.json()["code"] == "X14":
            time.sleep(11)
            planning_applications = requests.get(
                f"https://api.propertydata.co.uk/planning?key={config.property_data_api_key}&postcode={postcode}")
            if planning_applications.json()["status"] == "error":
                return {}
        else:
            return {}
    return planning_applications.json()["data"]["planning_applications"]


def get_rent_data(postcode, bedrooms, type):
    rents = requests.get(
        f"https://api.propertydata.co.uk/rents?key={config.property_data_api_key}&postcode={postcode}&bedrooms={bedrooms}&type={type}")
    if rents.json()["status"] == "error":
        # if error code is X14 wait 3 seconds and try again
        if rents.json()["code"] == "X14":
            time.sleep(11)
            rents = requests.get(
                f"https://api.propertydata.co.uk/rents?key={config.property_data_api_key}&postcode={postcode}&bedrooms={bedrooms}&type={type}")
            if rents.json()["status"] == "error":
                return {}
        else:
            return {}
    return rents.json()["data"]


def get_rent_demand_data(postcode):
    rents = requests.get(
        f"https://api.propertydata.co.uk/demand-rent?key={config.property_data_api_key}&postcode={postcode}")

    if rents.json()["status"] == "error":
        # if error code is X14 wait 3 seconds and try again
        if rents.json()["code"] == "X14":
            time.sleep(11)
            rents = requests.get(
                f"https://api.propertydata.co.uk/demand-rent?key={config.property_data_api_key}&postcode={postcode}")
            if rents.json()["status"] == "error":
                return {}
        else:
            return {}
    return rents.json()


def get_bus_stops_and_tube_stations(lon, lat):

    resp = requests.get(
        f"http://transportapi.com/v3/uk/places.json?app_id=416ad2d6&app_key={config.property_data_api_key}&lon={lon}&lat={lat}&type=bus_stop,tube_station")
    get_json = resp.json()

    new_list = []
    for stop in get_json.get('member', []):
        if float(stop.get('distance')) < 1000:
            new_list.append(stop)
    return new_list


def get_train_stations(lon, lat):
    resp = requests.get(
        f"http://transportapi.com/v3/uk/places.json?app_id=416ad2d6&app_key={config.transport_api_key}&lon={lon}&lat={lat}&type=train_station")
    get_json = resp.json()
    new_list = []
    for stop in get_json.get('member', []):
        if float(stop.get('distance')) <= 4000:
            new_list.append(stop)
    return new_list


def get_dentist_services(lon, lat):

    response = requests.request(
        method='POST',
        url=f'https://api.nhs.uk/service-search/search-postcode-or-place?api-version=1&search=postcode&latitude={lat}&longitude={lon}',
        headers={
            "Content-Type": "application/json",
            "subscription-key": f"{config.nhs_api_key}"
        },
        data=u'''
        {
            "filter": "OrganisationTypeID eq 'DEN'",
            "select": "OrganisationName,Address1,Address2,Address3,City,County,Postcode,Contacts",
            "top": 5,
            "skip": 0,
            "count": true
        }
        ''')
    if 'errorName' in response.json():
        return {"value": []}
    return response.json()


def get_gp_services(lon, lat):

    response = requests.request(
        method='POST',
        url=f'https://api.nhs.uk/service-search/search-postcode-or-place?api-version=1&search=postcode&latitude={lat}&longitude={lon}',
        headers={
            "Content-Type": "application/json",
            "subscription-key": f"{config.nhs_api_key}"
        },
        data=u'''
        {
            "filter": "(OrganisationTypeID eq 'GPB') or (OrganisationTypeID eq 'GPP')",
            "select": "OrganisationName,Address1,Address2,Address3,City,County,Postcode,Contacts",
            "top": 5,
            "skip": 0,
            "count": true
        }
        ''')
    if 'errorName' in response.json():
        return {"value": []}
    return response.json()


def normalize_address(address):
    # Remove commas and periods, convert to upper case, and split into words
    words = address.replace(",", "").replace(".", "").upper().split()

    # Join the words without spaces
    normalized = ''.join(words)

    return normalized
