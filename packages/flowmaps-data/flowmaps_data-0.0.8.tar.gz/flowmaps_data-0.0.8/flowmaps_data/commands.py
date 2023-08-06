import requests
import json
import pandas as pd
import pytz
from datetime import datetime, timedelta
from dateutil.parser import parse
from progress.bar import Bar

tz = pytz.timezone('Europe/Madrid')

API_URL = "https://flowmaps.life.bsc.es/api"


def date_rfc1123(dt):
    """Return a string representation of a date according to RFC 1123
    (HTTP/1.1).

    The supplied date must be in UTC.

    """
    weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
             "Oct", "Nov", "Dec"][dt.month - 1]
    return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month,
        dt.year, dt.hour, dt.minute, dt.second)


def parse_date(date_str):
    return tz.localize(datetime.strptime(date_str, "%Y-%m-%d")) 


def clean_docs(docs):
    skip_fields = ['_links', '_created', '_updated', 'href', '_etag']
    for doc in docs:
        for field in skip_fields:
            if field in doc:
                del doc[field]
    return docs


def fetch_first(collection, query, projection={}):
    base_url = API_URL
    url = f"{base_url}/{collection}"
    params = {'where': json.dumps(query), 'max_results': 1, 'projection': json.dumps(projection)}
    # print(f"API url: {base_url}/{collection}?where={params['where']}&max_results={params['max_results']}&projection={params['projection']}")
    response = requests.get(url, params=params).json()
    if not response or not response.get('_items'):
        return None
    return response['_items'][0]


def fetch_all_pages(collection, query, batch_size=1000, projection={}, sort=None, progress=True, print_url=False):
    base_url = API_URL
    url = f"{base_url}/{collection}"
    params = {'where': json.dumps(query), 'max_results': batch_size, 'projection': json.dumps(projection)}
    if sort:
        params['sort'] = sort
    data = []
    if print_url:
        print(f"API request: {base_url}/{collection}?where={params['where']}")
    response = requests.get(url, params=params).json() # get first page
    data.extend(response['_items'])
    if '_links' not in response:
        return data
    num_docs = response['_meta']['total']
    if num_docs <= 0:
        return data
    num_pages = int(num_docs/batch_size)
    if progress: bar = Bar('Dowloading documents', max=num_docs)
    while 'next' in response['_links']:
        if progress: bar.goto(len(data))
        url = f"{base_url}/{response['_links']['next']['href']}"
        response = requests.get(url).json()
        data.extend(response['_items'])
    if progress: bar.goto(len(data))
    if progress: bar.finish()
    return data


def list_layers():
    print('Listing layers:')
    # filters = {
    #     'collection': 'layers', 
    #     'field': 'layer', 
    # }
    # data = fetch_all_pages('distinct', filters)
    # print("\n".join(data))
    filters = {
        'storedIn': 'layers', 
    }
    data = fetch_all_pages('provenance', filters, progress=False)
    for doc in data:
        print(f"{doc['keywords']['layer']}:  \t{doc['keywords']['layerDesc']}, {doc['numEntries']} polygons")


def describe_layer(layer, provenance=False, plot=False):
    print(f'Describing layer={layer}')
    filters = {
        'storedIn': 'layers',
        'keywords.layer': layer,
    }
    doc = fetch_first('provenance', filters)
    if not doc:
        print(f"No data for layer={layer}")
        return
    print(f"Description: {doc.get('keywords', {}).get('layerDesc')}")
    print(f"Layer in geojson format (https://en.wikipedia.org/wiki/GeoJSON)")
    print(f"Number of polygons: {doc.get('numEntries', '')}")

    if provenance:
        print(f"Full provenance: {json.dumps(doc, indent=4)}")

    if plot:
        download_layer(layer, None, plot=True, no_save=True)


def download_layer(layer, output_file, plot=False, no_save=False):
    if output_file is None:
        output_file = layer+'.geojson'
    print(f'Dowloading layer {layer}')
    filters = {
        'layer': layer
    }
    data = fetch_all_pages('layers', filters, print_url=True)
    featureCollection = {
        "type": "FeatureCollection",
        "features": [doc['feat'] for doc in data],
    }

    if not no_save:
        print(f'Saving layer to file: {output_file}')
        with open(output_file, 'w') as f:
            json.dump(featureCollection, f, indent=2)

    if plot:
        try:
            import geopandas as gpd
            import descartes
            import matplotlib.pylab as plt
            gpd.GeoDataFrame.from_features(featureCollection['features']).plot()
            plt.show()
        except ImportError as e:
            # import traceback
            # traceback.print_exc()
            print(f"\n\n  WARN: {e}. \n  To use the --plot option you need to install the following packages: geopandas, descartes, matplotlib. \n  For example, use:  pip install geopandas descartes matplotlib")


def list_health():
    print('Listing consolidated ev:')
    # filters = {
    #     'collection': 'layers.data.consolidated', 
    #     'field': 'ev',
    #     'query': {'type': 'covid19'},
    # }
    # data = fetch_all_pages('distinct', filters)
    # print("\n".join(data))
    filters = {
        'storedIn': 'layers.data.consolidated',
        'keywords.type': 'covid19', 
    }
    data = fetch_all_pages('provenance', filters, progress=False)
    for doc in data:
        print(f"{doc['keywords']['ev']}\n\tDescription: {doc.get('processedFrom', [{}])[0].get('keywords', {}).get('evDesc')}\n\tNumber of entries: {doc['numEntries']}\n\tlayer: {doc['keywords']['layer']}\n")


def describe_health(ev, provenance=False):
    print(f'Describing consolidated ev={ev}')
    filters = {
        'storedIn': 'layers.data.consolidated',
        'keywords.ev': ev,
    }
    prov = fetch_first('provenance', filters)
    print(f"Description: {prov.get('processedFrom', [{}])[0].get('keywords', {}).get('evDesc')}")
    print(f"Original data url: {[x.get('from') for x in prov.get('processedFrom', [{}])[0].get('fetched', [{}])]}")
    print(f"Original data downloaded at: {prov.get('processedFrom', [{}])[0].get('storedAt')}")
    print(f"Processed at: {prov.get('storedAt')}")
    print(f"Number of entries: {prov.get('numEntries', '')}")
    filters = {
        'collection': 'layers.data.consolidated', 
        'field': 'date',
        'query': {'type': 'covid19', 'ev': ev},
    }
    data = fetch_all_pages('distinct', filters, progress=False)
    print(f"Available dates: min={min(data)}, max={max(data)}")
    if provenance:
        print(f"Full provenance: {json.dumps(prov, indent=4)}")

    example = fetch_first('layers.data.consolidated', {'type': 'covid19', 'ev': ev})
    print("Example document:\n"+json.dumps(example, indent=4))


def download_health(ev, output_file, output_format='csv', start_date=None, end_date=None):
    print(f'Dowloading consolidated health data for ev={ev}')
    filters = {
        'ev': ev,
        'type': 'covid19',
    }
    if start_date and end_date:
        filters['date'] = {'$gte': start_date, '$lte': end_date}
    elif start_date:
        filters['date'] = {'$gte': start_date}
    elif end_date:
        filters['date'] = {'$lte': end_date}
    data = fetch_all_pages('layers.data.consolidated', filters, print_url=True)
    if output_format == 'csv':
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
        print(f'{df.shape[0]} rows written to file:', output_file)
    elif output_format == 'json':
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        print('Saved to file:', output_file)
    else:
        print('Unrecognized output_format. Choose one from: csv, json')


def list_data():
    print('Listing ev:')
    # filters = {
    #     'collection': 'layers.data', 
    #     'field': 'ev',
    #     'query': {},
    # }
    # data = fetch_all_pages('distinct', filters)
    # print("\n".join(data))
    filters = {
        'storedIn': 'layers.data',
    }
    data = fetch_all_pages('provenance', filters, progress=False)
    for doc in data:
        print(f"{doc['keywords']['ev']}\n\tDescription: {doc['keywords'].get('evDesc', '')}\n\tlayer: {doc['keywords'].get('layer')}\n")




def describe_data(ev, provenance=False):
    print(f'Describing ev={ev}')
    filters = {
        'storedIn': 'layers.data',
        'keywords.ev': ev,
    }
    prov = fetch_first('provenance', filters)
    print(f"Description: {prov.get('keywords', {}).get('evDesc')}")
    print(f"Original data url: {[x.get('from') for x in prov.get('fetched', [{}])]}")
    print(f"Last downloaded at: {prov.get('storedAt')}")
    print(f"Data associated to layer: {prov.get('keywords').get('layer')}")
    # print(f"Number of entries: {prov.get('numEntries', '')}")
    filters = {
        'collection': 'layers.data', 
        'field': 'evstart',
        'query': {'ev': ev},
    }
    dates = fetch_all_pages('distinct', filters, progress=False)
    dates = [parse(date) for date in dates]
    print(f"Available dates: min={min(dates)}, max={max(dates)}")
    if provenance:
        print(f"Full provenance: {json.dumps(prov, indent=4)}")

    example = fetch_first('layers.data', {'ev': ev})
    print("Example document:\n"+json.dumps(example, indent=4))


def download_data(ev, output_file, output_format='csv', start_date=None, end_date=None):
    print(f'Dowloading data for ev={ev}')
    filters = {
        'ev': ev,
    }
    if start_date and end_date:
        filters['evstart'] = {'$gte': date_rfc1123(parse_date(start_date)), '$lte': date_rfc1123(parse_date(end_date) + timedelta(days=1))}
    elif start_date:
        filters['evstart'] = {'$gte': date_rfc1123(parse_date(start_date))}
    elif end_date:
        filters['evstart'] = {'$lte': date_rfc1123(parse_date(end_date) + timedelta(days=1))}
    data = fetch_all_pages('layers.data', filters, print_url=True)
    if output_format == 'csv':
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
        print(f'{df.shape[0]} rows written to file:', output_file)
    elif output_format == 'json':
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        print('Saved to file:', output_file)
    else:
        print('Unrecognized output_format. Choose one from: csv, json')


def list_daily_mobility_matrix():
    print('Listing available mobility layers:')
    # filters = {
    #     'collection': 'mitma_mov.daily_mobility_matrix', 
    #     'field': 'source_layer',
    #     'query': {'date': '2020-10-10'},
    # }
    # data = fetch_all_pages('distinct', filters)
    # print("\n".join(data))

    pairs = [["mitma_mov", "mitma_mov"],
        ["cnig_provincias", "cnig_provincias"],
        ["cnig_ccaa", "cnig_ccaa"],
        ["abs_09", "abs_09"],
        ["zbs_15", "zbs_15"],
        ["zbs_07", "zbs_07"],
        ["oe_16", "oe_16"],
        ["zon_bas_13", "zon_bas_13"],
        ["cnig_provincias", "abs_09"],
        ["abs_09", "cnig_provincias"],
        ["cnig_provincias", "zbs_15"],
        ["zbs_15", "cnig_provincias"],
        ["cnig_provincias", "zbs_07"],
        ["zbs_07", "cnig_provincias"],
        ["cnig_provincias", "oe_16"],
        ["oe_16", "cnig_provincias"],
        ["cnig_provincias", "zon_bas_13"],
        ["zon_bas_13", "cnig_provincias"]]

    for source_layer, target_layer in pairs:
        print(json.dumps({"source_layer": source_layer, "target_layer": target_layer}))


def describe_daily_mobility_matrix(provenance=False):
    print(f'Describing daily mobility matrix')
    print(f"Description: Daily Origin-Destination matrix, based on anonymized mobile phone records from MITMA dataset (https://www.mitma.gob.es/ministerio/covid-19/evolucion-movilidad-big-data).")
    filters = {
        'storedIn': 'mitma_mov.daily_mobility_matrix',
        'numEntries': {'$gt': 0},
    }
    prov = fetch_all_pages('provenance', filters, sort='keywords.date', progress=False)
    print(f"Original data url: {[x.get('from') for x in prov[-1].get('processedFrom', [{}])[0].get('fetched', [{}])]}")
    print(f"Original data downloaded at: {prov[-1].get('processedFrom', [{}])[0].get('storedAt')}")
    print(f"Processed at: {prov[-1]['storedAt']}")
    print(f"Available dates: min={prov[0]['keywords']['date']}, max={prov[-1]['keywords']['date']}")
    
    if provenance:
        print(f"Full provenance: {json.dumps(prov, indent=4)}")
    
    example = fetch_first('mitma_mov.daily_mobility_matrix', {'source_layer': 'cnig_provincias', 'target_layer': 'cnig_provincias'})
    print("Example document:\n"+json.dumps(example, indent=4))


def download_daily_mobility_matrix(source_layer, target_layer, date, output_file, output_format='csv', source=None, target=None):
    print(f'Dowloading mobility matrix for source_layer={source_layer} target_layer={target_layer} date={date}')
    filters = {
        'date': date,
        'source_layer': source_layer,
        'target_layer': target_layer,
    }
    if source:
        filters['source'] = source
    if target:
        filters['target'] = target
    data = fetch_all_pages('mitma_mov.daily_mobility_matrix', filters, print_url=True)
    if output_format == 'csv':
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
        print(f'{df.shape[0]} rows written to file:', output_file)
    elif output_format == 'json':
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        print('Saved to file:', output_file)
    else:
        print('Unrecognized output_format. Choose one from: csv, json')


def list_population_layers():
    print('Listing available population layers:')
    filters = {
        'collection': 'layers.data.consolidated', 
        'field': 'layer',
        'query': {'type': 'population'},
    }
    data = fetch_all_pages('distinct', filters)
    print("\n".join(data))


def describe_population(layer, provenance=False):
    print(f'Describing population data for layer={layer}')
    filters = {
        'storedIn': 'layers.data.consolidated',
        'keywords.layer': layer,
    }
    prov = fetch_first('provenance', filters)
    print(f"Description: population calculated based on anonymized mobile phone records from MITMA dataset (https://www.mitma.gob.es/ministerio/covid-19/evolucion-movilidad-big-data).")
    print(f"Original data url: {[x.get('from') for x in prov.get('processedFrom', [{}])[0].get('fetched', [{}])]}")
    print(f"Original data downloaded at: {prov.get('processedFrom', [{}])[0].get('storedAt')}")
    print(f"Processed at: {prov.get('storedAt')}")
    print(f"Number of entries: {prov.get('numEntries', '')}")
    filters = {
        'collection': 'layers.data.consolidated', 
        'field': 'date',
        'query': {'type': 'population', 'layer': layer},
    }
    data = fetch_all_pages('distinct', filters, progress=False)
    print(f"Available dates: min={min(data)}, max={max(data)}")

    example = fetch_first('layers.data.consolidated', {'type': 'population', 'layer': layer})
    print("Example document:\n"+json.dumps(example, indent=4))

    if provenance:
        print(f"Full provenance: {json.dumps(prov, indent=4)}")


def download_population(layer, output_file, output_format='csv', start_date=None, end_date=None):
    print(f'Dowloading population for layer={layer}')
    filters = {
        'layer': layer,
        'type': 'population',
    }
    if start_date and end_date:
        filters['date'] = {'$gte': start_date, '$lte': end_date}
    elif start_date:
        filters['date'] = {'$gte': start_date}
    elif end_date:
        filters['date'] = {'$lte': end_date}
    data = fetch_all_pages('layers.data.consolidated', filters, print_url=True)
    if output_format == 'csv':
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
        print(f'{df.shape[0]} rows written to file:', output_file)
    elif output_format == 'json':
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        print('Saved to file:', output_file)
    else:
        print('Unrecognized output_format. Choose one from: csv, json')


def list_zone_movements():
    print('Listing available zone_movements layers:')
    filters = {
        'collection': 'layers.data.consolidated', 
        'field': 'layer',
        'query': {'type': 'zone_movements'},
    }
    data = fetch_all_pages('distinct', filters)
    print("\n".join(data))


def describe_zone_movements(provenance=False):
    print(f'Describing zone_movements')
    filters = {
        'storedIn': 'layers.data.consolidated',
        'keywords.type': 'zone_movements',
        'numEntries': {'$gt': 0},
    }
    provs = fetch_all_pages('provenance', filters, sort='keywords.date', progress=False)
    prov = provs[-1]

    print(f"Description: mobility data from MITMA dataset (https://www.mitma.gob.es/ministerio/covid-19/evolucion-movilidad-big-data), aggregated at different layers. Original data is based on anonymized mobile phone records. It contains the number of people in each geographical area that has done 0,1,2,3+ trips. NOTE: 3 or more trips are encoded as '-1'.")
    print(f"Original data url: {[x.get('from') for x in prov.get('processedFrom', [{}])[0].get('fetched', [{}])]}")
    print(f"Original data downloaded at: {prov.get('processedFrom', [{}])[0].get('storedAt')}")
    print(f"Processed at: {prov.get('storedAt')}")
    print(f"Number of entries: {prov.get('numEntries', '')}")
    filters = {
        'collection': 'layers.data.consolidated', 
        'field': 'date',
        'query': {'type': 'zone_movements'},
    }
    data = fetch_all_pages('distinct', filters, progress=False)
    print(f"Available dates: min={min(data)}, max={max(data)}")

    example = fetch_first('layers.data.consolidated', {'type': 'zone_movements'})
    print("Example document:\n"+json.dumps(example, indent=4))

    if provenance:
        print(f"Full provenance: {json.dumps(provs, indent=4)}")


def download_zone_movements(layer, output_file, output_format='csv', start_date=None, end_date=None):
    print(f'Dowloading population for layer={layer}')
    filters = {
        'layer': layer,
        'type': 'zone_movements',
    }
    if start_date and end_date:
        filters['date'] = {'$gte': start_date, '$lte': end_date}
    elif start_date:
        filters['date'] = {'$gte': start_date}
    elif end_date:
        filters['date'] = {'$lte': end_date}
    data = fetch_all_pages('layers.data.consolidated', filters, print_url=True)
    if output_format == 'csv':
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
        print(f'{df.shape[0]} rows written to file:', output_file)
    elif output_format == 'json':
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        print('Saved to file:', output_file)
    else:
        print('Unrecognized output_format. Choose one from: csv, json')
