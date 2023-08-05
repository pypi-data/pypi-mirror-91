# Quantumdata sdk

# auth token

    write to me on rafalniewinski95@gmail.com 
    if you want get access to our database

# simple usage:

    get companies:

        api = QuantumDataApi(API_TOKEN)
        response = api.get_companies()


    get quotations:
    
        api = QuantumDataApi(API_TOKEN)
        response = api.get_quotations("KGHM")


    get reports:

        api = QuantumDataApi(API_TOKEN)
        response = api.get_reports("KGHM")
