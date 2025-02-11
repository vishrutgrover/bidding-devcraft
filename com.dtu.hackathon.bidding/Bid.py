from BidRequest import BidRequest
from Bidder import Bidder
import random

class Bid(Bidder):
    def getBidPrice(self, bidRequest: BidRequest) -> int:
        features = self.getFeatures(bidRequest)

        shouldClick = self.predictCTR([features])[0]
        bidPrice = self.predictBidPrice([features])[0]

        if shouldClick > self.ctrThreshold:
            return round(bidPrice * self.bidRatio, 2)
        else:
            return -1