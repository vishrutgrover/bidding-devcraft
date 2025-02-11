from BidRequest import BidRequest
import joblib
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from functools import lru_cache
import lightgbm as lgb

class Bidder():
    def __init__(self, bidRatio=1.05, ctrThreshold=0.00045):
        self.bidRatio = bidRatio
        self.ctrThreshold = ctrThreshold

        self.classification_model = lgb.Booster(model_file='lightgbm_classification.txt')
        print('Loaded classification model')
        
        self.regression_model = lgb.Booster(model_file='lightgbm_regressor.txt')
        print('Loaded regression model')

        weights = pd.read_csv('region_city_weights.csv')
        self.city_weights = {row['city']: row['city_weight'] for index, row in weights.iterrows()}
        self.region_weights = {row['region']: row['region_weight'] for index, row in weights.iterrows()}
        print('Loaded weights')

        self.device_map = {'Desktop': 0, 'Mobile': 1, 'Tablet': 2, 'unknown': 3}
        self.advertiserid_map = {1458: 0, 3358: 1, 3386: 2, 3427: 3, 3476: 4}

    def predictCTR(self, inp):
        return self.classification_model.predict(inp)
    
    def predictBidPrice(self, inp):
        return self.regression_model.predict(inp)
    
    @lru_cache(maxsize=1000)
    def getDeviceType(self, userAgent):
        string = userAgent.lower()
        if 'windows nt' in string or "macintosh" in string or "linux" in string:
            return 'Desktop'
        
        elif 'android' in string or 'iphone' in string or 'mobile' in string:
            return 'Mobile'
        
        elif 'ipad' in string or 'tablet' in string:
            return 'Tablet'
        
        else:
            return 'unknown'
    
    def getFeatures(self, bidRequest: BidRequest):
        features = np.array([
            bidRequest.adExchange,
            bidRequest.adSlotFloorPrice,
            bidRequest.adSlotHeight,
            bidRequest.adSlotVisibility,
            bidRequest.adSlotWidth,
            self.advertiserid_map.get(bidRequest.advertiserId, -1),
            self.city_weights.get(bidRequest.city, 0),
            self.device_map.get(self.getDeviceType(bidRequest.userAgent), 3),
            self.region_weights.get(bidRequest.region, 0)
        ], dtype=np.float32)  # Using float32 to reduce memory

        return features