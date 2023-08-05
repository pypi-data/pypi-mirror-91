import aiohttp
import asyncio
import click
import ujson as json


class Zooma(object):
    def __init__(self):
        self.url = "https://www.ebi.ac.uk/spot/zooma/v2/api/services/"


    async def annotate(self,
                       property_value: str,
                       property_type: str = None) -> dict:
        params = {"propertyValue": property_value}
   
        if(property_type is not None):
            params["propertyType"] = property_type
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url+"annotate", params=params) as resp:
                return await resp.json()



if __name__ == '__main__':
    z = Zooma()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(z.annotate("mus musculus"))
