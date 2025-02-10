from BidRequest import BidRequest
from Bidder import Bidder
import pandas as pd
import time
import warnings

warnings.filterwarnings('ignore')

class bidSimulator:
    def __init__(self):
        print('Initializing Bid Simulator')
        self.dataset = pd.read_pickle('bid.10.pkl')
        print('Dataset loaded')
        self.bidder = Bidder()
        print('Bidder initialized')
        print('Bid Simulator initialized')
        print("-"*25)

    def _get_random_sample(self):
        return self.dataset.sample()

    def _set_values(self, bidRequest, sample):
        sample = sample.iloc[0]
        bidRequest.setBidId(sample['BidId'])
        bidRequest.setTimestamp(sample['Timestamp'])
        bidRequest.setVisitorId(sample['iPinYouID'])
        bidRequest.setUserAgent(sample['User-Agent'])
        bidRequest.setIpAddress(sample['IP'])
        bidRequest.setRegion(sample['Region'])
        bidRequest.setCity(sample['City'])
        bidRequest.setAdExchange(sample['AdExchange'])
        bidRequest.setDomain(sample['Domain'])
        bidRequest.setUrl(sample['URL'])
        bidRequest.setAnonymousURLID(sample['AnonymousURLID'])
        bidRequest.setAdSlotID(sample['AdslotID'])
        bidRequest.setAdSlotWidth(sample['Adslotwidth'].tolist())
        bidRequest.setAdSlotHeight(sample['Adslotheight'].tolist())
        bidRequest.setAdSlotVisibility(sample['Adslotvisibility'].tolist())
        bidRequest.setAdSlotFormat(sample['Adslotformat'].tolist())
        bidRequest.setAdSlotFloorPrice(sample['Adslotfloorprice'].tolist())
        bidRequest.setCreativeID(sample['CreativeID'])
        bidRequest.setAdvertiserId(sample['AdvertiserID'].tolist())
        bidRequest.setUserTags(sample['UserProfileTags'])
    
    def simulate(self):
        sample = self._get_random_sample()
        bidRequest = BidRequest()
        self._set_values(bidRequest, sample)

        start = time.time()
        bidPrice = self.bidder.getBidPrice(bidRequest)
        end = time.time()

        print(f'Time taken: {end - start}')

        return bidPrice
    

if __name__ == '__main__':
    simulator = bidSimulator()
    for i in range(1):
        print("Bid Price:", simulator.simulate())
        print("-"*15)
        print()