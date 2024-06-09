from flask import request, Blueprint, Response, jsonify, current_app
from src.dependencies import property_information
import re
from statistics import mean

general = Blueprint('general', __name__)

# basic health check


@general.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


@general.route('/info', methods=['GET'])
def get_property_info():
    json_data = request.json
    postcode = json_data.get('postcode')
    house_number = json_data.get('house_number')
    street = json_data.get('street', '')
    bedrooms = json_data.get('bedrooms')
    type = json_data.get('type')
    lon = json_data.get('lon', '')
    lat = json_data.get('lat', '')
    print(json_data)
    uprn = json_data.get('uprn', '')

    if postcode is None or house_number is None or bedrooms is None or type is None:
        print("Missing parameters")
        return Response("Missing parameters", status=400)

    house_types = [
        "flat",
        "terraced_house",
        "semi-detached_house",
        "detached_house"
    ]

    if type not in house_types:
        print(f"Invalid house type must be one of: {house_types}")
        return Response(f"Invalid house type must be one of: {house_types}", status=400)

    epc_data = property_information.get_epc_certs(postcode, house_number)
    if epc_data != {}:
        uprn = epc_data['uprn']
    else:
        uprn = property_information.get_uprn(house_number, street, postcode)

    if lon == '' or lat == '':
        if epc_data != {}:
            lon_lat = property_information.get_lat_lon_opti(uprn)
            lon = lon_lat.get('longitude', '')
            lat = lon_lat.get('latitude', '')
            lonlatgoogle = False

    else:
        lon_lat = {"longitude": lon, "latitude": lat}
        lonlatgoogle = True

    # get_oauth= property_information.get_when_fresh_oauth()

    # get_address_key= property_information.get_address_postcode_key(epc_data['postcode'], get_oauth.get('access_token'))
    # if "member" in get_address_key:
    #     for member in get_address_key['member']:
    #         if "label" in member:
    #             if house_number in member['label'] and street.lower().strip() in member['label'].lower().strip():
    #                 if 'key' in member:
    #                     get_key=member['key']
    # if get_key != '':

        # get_bedrooms= property_information.get_bedroom_number(get_key, get_oauth.get('access_token'))
        # if "member" in get_bedrooms:
        #     if "value" in get_bedrooms['member'][0]:
        #         get_bedroom_number=get_bedrooms['member'][0]['value']

    monthly_crime_rate = property_information.get_monthly_crime_rate(lon_lat)

    if epc_data != {}:
        epc_suggestions = property_information.get_epc_suggestions(
            epc_data['lmk-key'])
    else:
        epc_suggestions = {}

    price_paid_data = property_information.get_price_paid_data(
        postcode, house_number)
    nearby_schools = property_information.get_nearby_schools(postcode)
    flood_risk = property_information.get_flood_risk(postcode)
    internet_speed = property_information.get_internet_speed(postcode)
    council_tax_band = property_information.get_council_tax_band(
        postcode, house_number, street)
    planning_data = property_information.get_planning_applications(postcode)
    rent_data = property_information.get_rent_data(postcode, bedrooms, type)
    rental_demand = property_information.get_rent_demand_data(postcode)
    titles = property_information.get_uprn_title(uprn)
    bus_and_tubes = property_information.get_bus_stops_and_tube_stations(
        lon, lat)
    train_stations = property_information.get_train_stations(lon, lat)

    dentist_services = property_information.get_dentist_services(lon, lat)
    gp_services = property_information.get_gp_services(lon, lat)
    air_pollution = property_information.get_air_polution(lon, lat)

    cafes = property_information.get_cafes(lon, lat)
    supermarkets = property_information.get_supermarkets(lon, lat)
    # airports= property_information.get_airport(lon,lat)
    gyms = property_information.get_gyms(lon, lat)
    post_offcies = property_information.get_post_office(lon, lat)
    restaraunts = property_information.get_restaraunts(lon, lat)
    get_polygon_info = property_information.get_polygon_info(uprn)

    get_build_cost = {}
    if epc_data != {}:
        get_build_cost = property_information.get_build_cost(
            postcode, epc_data['total-floor-area'])

    return jsonify({
        "monthly_crime_rate": monthly_crime_rate,
        "lon_lat": lon_lat,
        "nearby_schools": nearby_schools,
        "flood_risk": flood_risk,
        "get_build_cost": get_build_cost,
        "epc_suggestions": epc_suggestions,
        "internet_speed": internet_speed,
        "council_tax": council_tax_band,
        "epc_data": epc_data,
        "price_paid_data": price_paid_data,
        "rental_demand": rental_demand,
        "lon": lon,
        "lat": lat,
        "air_pollution": air_pollution,
        "planning_data": planning_data,
        "rent_data": rent_data,
        "get_polygon_info": get_polygon_info,
        "get_bus_and_tubes": bus_and_tubes,
        "get_train_stations": train_stations,
        "get_gp_services": gp_services,
        "titles": titles,
        "get_dentist_services": dentist_services,
        "cafes": cafes,
        "supermarkets": supermarkets,
        "gyms": gyms,
        "post_offcies": post_offcies,
        "restaraunts": restaraunts,
        "lonlatgoogle": lonlatgoogle
    })


@general.route('/pre_pop_info', methods=['GET'])
def pre_pop_info():
    json_data = request.json

    postcode = json_data.get('postcode').replace("_", " ")
    house_number = json_data.get('house_number').replace("_", " ")
    street = json_data.get('street', '').replace("_", " ")

    lon = json_data.get('lon', '')
    lat = json_data.get('lat', '')
    lon_lat = {"longitude": lon, "latitude": lat}

    if postcode is None or house_number is None:
        print("Missing parameters")
        return Response("Missing parameters", status=400)

    if lon == '' or lat == '':
        lon_lat = property_information.get_lon_lat(
            postcode, house_number, street)

    epc_data = property_information.get_epc_certs(postcode, house_number)
    price_paid_data = property_information.get_price_paid_data(
        postcode, house_number)
    # flood_risk = property_information.get_flood_risk(postcode)
    # council_tax_band = property_information.get_council_tax_band(postcode, house_number, street)
    titles = property_information.get_uprn_title(epc_data['uprn'])
    # get_polygon_info= property_information.get_polygon_info(epc_data['uprn'])

    # get_oauth= property_information.get_when_fresh_oauth()

    get_key = ''
    get_bedroom_number = ''
    get_parking_number = ''
    get_bathroom_number = ''

    # get_address_key= property_information.get_address_postcode_key(epc_data['postcode'], get_oauth.get('access_token'))
    # if "member" in get_address_key:
    #     for member in get_address_key['member']:
    #         if "label" in member:
    #             if house_number in member['label'] and street.lower().strip() in member['label'].lower().strip():
    #                 if 'key' in member:
    #                     get_key=member['key']
    # if get_key != '':

    # get_bedrooms= property_information.get_bedroom_number(get_key, get_oauth.get('access_token'))
    # if "member" in get_bedrooms:
    #     if "value" in get_bedrooms['member'][0]:
    #         get_bedroom_number=get_bedrooms['member'][0]['value']

    # get_bathrooms= property_information.get_bathroom_number(get_key, get_oauth.get('access_token'))

    # if "member" in get_bathrooms:
    #     if "value" in get_bathrooms['member'][0]:
    #         get_bathroom_number=get_bathrooms['member'][0]['value']

    # get_parking= property_information.get_parking(get_key, get_oauth.get('access_token'))

    # if "member" in get_bathrooms:
    #     if "value" in get_bathrooms['member'][0]:
    #         get_parking_number=get_bathrooms['member'][0]['value']

    # listed_match=None

    # if "listed_buildings" in get_polygon_info:
    #     if get_polygon_info['listed_buildings'] != [] and get_polygon_info['listed_buildings'] != None:
    #         for listed in get_polygon_info['listed_buildings']:
    #             sort_description=" ".join(listed['description'].split())
    #             if postcode.replace(" ","").lower() in sort_description.lower()
    leasehold = False
    if titles.get('title_data', {}) != {}:
        for freeholdleasetype in titles['title_data']:
            if "leasehold" in freeholdleasetype.get('title_class'):
                leasehold = True
    WALL_MATERIAL = ""
    if "Cavity" in epc_data['walls-description'] or "cavity" in epc_data['walls-description']:
        WALL_MATERIAL = "Brick"
    elif "Timber frame" in epc_data['walls-description'] or "timber frame" in epc_data['walls-description']:
        WALL_MATERIAL = "Timber"
    elif "Granite" in epc_data['walls-description'] or "granite" in epc_data['walls-description']:
        WALL_MATERIAL = "Stone"
    elif "Cob" in epc_data['walls-description'] or "cob" in epc_data['walls-description']:
        WALL_MATERIAL = "Other"
    elif "Sandstone" in epc_data['walls-description'] or "sandstone" in epc_data['walls-description']:
        WALL_MATERIAL = "Stone"
    proptype = ""
    if "Terrace" in epc_data['built-form'] or "terrace" in epc_data['built-form']:
        if "Flat" in epc_data['property-type']:
            proptype = "Flat"
        else:
            proptype = "Terraced House"
    elif "Semi-Detached" in epc_data['built-form'] or "semi-detached" in epc_data['built-form']:
        if "Bungalow" in epc_data['property-type']:
            proptype = "Semi-Detached Bungalow"
        elif "Flat" in epc_data['property-type']:
            proptype = "Flat"
        else:
            proptype = "Semi-Detached House"
    elif "Detached" in epc_data['built-form']:
        if "Bungalow" in epc_data['property-type']:
            proptype = "Detached Bungalow"
        elif "Flat" in epc_data['property-type']:
            proptype = "Flat"
        else:
            proptype = "Detached House"

    age_band = epc_data['construction-age-band']
    age_band_list = re.findall("\d+", age_band)

    get_average = ""
    new_int_list = [int(age) for age in age_band_list]
    if age_band_list != []:
        get_average = mean(new_int_list)

    freeholdleasehold = ""
    if leasehold == True:
        freeholdleasehold = 'Leasehold'
    else:
        freeholdleasehold = 'Freehold'

    # newbuild = "false"
    # if price_paid_data == []:
    #     newbuild = "true"

    roofdesc = ''
    if 'Thatched' in epc_data['roof-description'] or 'thatched' in epc_data['roof-description']:
        roofdesc = 'Thatch Reed'
    else:
        roofdesc = ''
    construct_date = ''
    if get_average != "":
        if get_average >= 1914 and get_average <= 2000:
            construct_date = '1914_2000'
        elif get_average < 1914:
            construct_date = 'pre_1914'
        elif get_average > 2000:
            construct_date = '2000_onwards'

    # if epc_data['total-floor-area'] != None and epc_data['total-floor-area'] != "":
    #     get_feet = float(epc_data['total-floor-area'])/0.0929

    # valuation1=''
    # valuation2=''
    # valuation3=''

    # if proptype != "Flat":
    #     valuation1 = property_information.get_valuation(epc_data['postcode'], epc_data['property-type'], construct_date, get_feet, get_bedroom_number ,get_bathroom_number, 'average', "garden",get_parking)
    #     valuation2 = property_information.get_valuation(epc_data['postcode'], epc_data['property-type'], construct_date, get_feet, get_bedroom_number ,get_bathroom_number, 'average', "garden",get_parking)
    #     valuation3 = property_information.get_valuation(epc_data['postcode'], epc_data['property-type'], construct_date, get_feet, get_bedroom_number ,get_bathroom_number, 'average', "garden",get_parking)
    newget_average = ""
    if get_average != "":
        newget_average = round(get_average)
    return jsonify({
        "build-year": newget_average,
        "walls-description": WALL_MATERIAL,
        "roof-description": roofdesc,
        "roof-note": epc_data['roof-description'],
        "prop-type": proptype,
        "lease-or-freehold": freeholdleasehold,
        "current-eff-rating": epc_data['current-energy-rating'],
        "new-build": ''
        # "get_bathroom_number":get_bathroom_number,
        # "get_bedroom_number":get_bedroom_number
    })


@general.route('/get_lon_lat', methods=['GET'])
def get_lon_latmm():
    postcode = request.args.get('postcode').replace("_", " ")
    house_number = request.args.get('house_number').replace("_", " ")
    street = request.args.get('street').replace("_", " ")

    if postcode is None or house_number is None:
        print("Missing parameters")
        return Response("Missing parameters", status=400)

    epc_data = property_information.get_epc_certs(postcode, house_number)
    if epc_data != {}:
        lat_lons = property_information.get_lat_lon_opti(epc_data['uprn'])
        return jsonify(lat_lons)
    else:
        return jsonify({})
        # get_key=""
        # get_oauth= property_information.get_when_fresh_oauth()
        # get_address_key= property_information.get_address_postcode_key(postcode, get_oauth.get('access_token'))
        # housenumbercheck =re.findall("\d+", house_number)

        # if "member" in get_address_key:
        #     for member in get_address_key['member']:
        #         if "label" in member:
        #             get_number = re.findall("\d+", member['label'])

        #             if get_number != [] and housenumbercheck != []:
        #                 if house_number.lower().strip() in get_number[0].lower().strip():
        #                     if street != '' and street != None:
        #                         if  street.lower().strip() in member['label'].lower().strip():
        #                             if 'key' in member:
        #                                 get_key=member['key']
        #                     else:
        #                         if 'key' in member:
        #                             get_key=member['key']
        #             else:
        #                 if house_number.lower().strip() in member['label'].lower().strip():
        #                     if street != '' and street != None:
        #                         if  street.lower().strip() in member['label'].lower().strip():
        #                             if 'key' in member:
        #                                 get_key=member['key']
        #                     else:
        #                         if 'key' in member:
        #                             get_key=member['key']

        # if get_key != '':

        getuprn = getuprn.get_uprn(house_number, street, postcode)

        if getuprn is not None:

            uprn = getuprn
            lat_lons = property_information.get_lat_lon_opti(uprn)
            lat_lons.update({'uprn': uprn})
            return jsonify(lat_lons)

    return jsonify({})


@general.route('/get_gi_risk', methods=['GET'])
def get_gi_risk():
    postcode = request.args.get('postcode').replace("_", " ")
    house_number = request.args.get('house_number').replace("_", " ")
    street = request.args.get('street').replace("_", " ")

    if postcode is None or house_number is None:
        print("Missing parameters")
        return Response("Missing parameters", status=400)
    monthly_crime_rate = {}
    fire_and_rescue_authority_data = {}
    epc_data = property_information.get_epc_certs(postcode, house_number)
    flood_risk = property_information.get_flood_risk(postcode)
    print(epc_data)
    uprn = ""
    if epc_data != {}:
        uprn = epc_data['uprn']

    else:
        # get_key=""
        # get_oauth= property_information.get_when_fresh_oauth()
        # get_address_key= property_information.get_address_postcode_key(postcode, get_oauth.get('access_token'))
        # housenumbercheck =re.findall("\d+", house_number)

        # if "member" in get_address_key:
        #     for member in get_address_key['member']:
        #         if "label" in member:
        #             get_number = re.findall("\d+", member['label'])

        #             if get_number != [] and housenumbercheck != []:
        #                 if house_number.lower().strip() in get_number[0].lower().strip():
        #                     if street != '' and street != None:
        #                         if  street.lower().strip() in member['label'].lower().strip():
        #                             if 'key' in member:
        #                                 get_key=member['key']
        #                     else:
        #                         if 'key' in member:
        #                             get_key=member['key']
        #             else:
        #                 if house_number.lower().strip() in member['label'].lower().strip():
        #                     if street != '' and street != None:
        #                         if  street.lower().strip() in member['label'].lower().strip():
        #                             if 'key' in member:
        #                                 get_key=member['key']
        #                     else:
        #                         if 'key' in member:
        #                             get_key=member['key']
        getuprn = getuprn.get_uprn(house_number, street, postcode)

        if getuprn is not None:

            uprn = getuprn
            lat_lons = property_information.get_lat_lon_opti(uprn)
            lat_lons.update({'uprn': uprn})
            return jsonify(lat_lons)

    if uprn != "":
        lat_lons = property_information.get_lat_lon_opti(uprn)
        lon = lat_lons.get('longitude', '')
        lat = lat_lons.get('latitude', '')
        lon_lat = {"longitude": lon, "latitude": lat}
        monthly_crime_rate = property_information.get_monthly_crime_rate_12_months(
            lon_lat)
        fire_and_rescue_authority_data = property_information.get_polygon_info(
            uprn).get('fire_and_rescue_authority_data', {})
    print(monthly_crime_rate)
    print(fire_and_rescue_authority_data)

    new_dict = {
        "flood_risk": flood_risk,
        "monthly_crime_rate": monthly_crime_rate,
        "fire_data": fire_and_rescue_authority_data
    }

    return jsonify(new_dict)
