#!/usr/bin/env python3


def samples_by_date(from_date, to_date, page=0, size=100):
    filt_string = f"dt:update:from={from_date}until={to_date}"
    req = requests.get('https://www.ebi.ac.uk/biosamples/samples',
                       params = {"filter":filt_string, "size":size, "page": page})
    return req
