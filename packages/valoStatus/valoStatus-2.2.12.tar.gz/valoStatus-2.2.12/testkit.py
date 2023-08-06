# VALOSTATUS/valStatus.py
"""
MIT License

Copyright (c) 2020 D3crypt360 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import asyncio
import aiohttp

class Region:
    """
    NA - North America
    
    EU - Europe
    
    BR - Brazil
    
    AP - Asia Pacific
    
    KR - Korea
    
    LATAM - Latin America
    """
    def __init__(self, region):
        self.region = region
        
    def requests(self):
        async def getstatusurl():
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://valorant.secure.dyn.riotcdn.net/channels/public/x/status/{self.region.lower()}.json") as response:
                    global j
                    global r
                    r = response
                    j = await r.json()
                    await session.close()
        asyncio.run(getstatusurl())
        if r.status == 200:
            return j
        else:
            return
   
    def get_status(self):
        return {
                'issue':True,
                'incidents':[],
                'maintenances':[{"titles":{"content":"something2"}}]
               }
    
    def get_status_issue(self):
        """
        `self.get_status_issue()` would
        return either:
        True == There is an issue
        False == There is no issue
        """
        return (self.get_status()['issue'])
                
    def incidents_title(self):
        """to get the title of the incident:"""
        try:
            return self.get_status()["incidents"][0]['titles']['content']
        except IndexError:
            return
        
    def incidents_date(self):
        """to get the date of the incident:"""
        try:
            return self.get_status()['incidents'][0]['updates'][0]['created_at'][:10]
        except IndexError:
            return
        
    def incidents_reason(self):
        """to get the reason of the incident:"""
        try:
            return self.get_status()['incidents'][0]['updates'][0]['translations'][0]['content']
        except IndexError:
            return
        
    def maintenances_title(self):
        """to get the title of the maintenance:"""
        try:
            return self.get_status()["maintenances"][0]['titles']['content']
        except IndexError:
            return
        
    def maintenances_date(self):
        """to get the date of the maintenance:"""
        try:
            return self.get_status()['maintenances'][0]['updates'][0]['created_at'][:10]
        except IndexError:
            return
        
    def maintenances_reason(self):
        """to get the reason of the maintenance:"""
        try:
            return self.get_status()['maintenances'][0]['updates'][0]['translations'][0]['content']
        except IndexError:
            return
        
    def maintenence_check(self):
        """
        `self.maintenence_check()`would return:
        True == There is an issue.

        **we are not doing False here
        since we already have a check for that
        via `self.get_issue()`**
        """
        if self.get_status()['maintenances'] != []:
            return True
        
        
    def incident_check(self):
        """
        `self.incident_check()`would return:
        True == There is an issue.

        **we are not doing False here
        since we already have a check for that
        via `self.get_issue()`**
        """
        if self.get_status()['incidents'] != []:
            return True

if __name__ == "__main__":
    region = Region("EU")
    # print(region.get_status_issue())
    # print(region.maintenence_check())
    # print(region.incident_check())
    # print(region.maintenances_title())
    # print(region.incidents_title())

    if region.get_status_issue() == True: 
        if region.maintenence_check() == True:
            print(region.maintenances_title())

        if region.incident_check() == True:
            print(region.incidents_title())