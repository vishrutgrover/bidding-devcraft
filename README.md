![679df1512b30b_adobe-devcraft](https://github.com/user-attachments/assets/c44c94fb-d730-433c-a9a7-42f40b629c67)

# Real-Time Bidding Automation Using Bidding Algorithms

Real-Time Bidding (RTB) is transforming digital advertising by enabling advertisers to bid on ad impressions in real time. This project leverages efficient bidding algorithms to maximize the number of clicks and conversions under a fixed advertising budget.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Dataset Description](#dataset-description)
- [DSP Bidding Optimization Task](#dsp-bidding-optimization-task)
- [Architecture and File Structure](#architecture-and-file-structure)
- [Setup and Running the Code](#setup-and-running-the-code)
- [Team Information](#team-information)
- [Approach](#approach)
  - [Data Preprocessing & Feature Engineering](#data-preprocessing-&-feature-engineering)
  - [Bidding Strategy & Model Selection](#bidding-strategy-&-model-selection)
  - [Final Bidding Decision](#final-bidding-decision)
  - [Evaluation Strategy](#evaluation-strategy)
- [Final Prediction Pipeline](#final-prediction-pipeline)
- [Our Validation Results](#our-validation-results)

---

## Project Overview
This repository contains our implementation for optimizing DSP bidding strategies in a real-time auction environment. Our objective is to maximize the score defined as:

> **Score = (Number of Clicks) + N * (Number of Conversions)**

where **N** is a conversion weight factor that varies per advertiser.

### How RTB Works
- **Ad Exchange**: Collects ad slot details (e.g., size, URL, audience data) and sends bid requests to multiple DSPs.
- **Demand Side Platform (DSP)**: Evaluates each bid request against targeting criteria and decides whether to bid. If bidding, it sets the bid price using custom algorithms.
- **Auction**: A second-price auction where the highest bidder wins, but pays the second-highest bid.

---

## Dataset Description
The dataset consists of processed logs for bidding, impressions, clicks, and conversions. Each log file is a plain text file with fields separated by tabs.

### Files Provided:
- **Bid Dataset:**  
  `dataset/bid.06.txt`, `dataset/bid.07.txt`, ..., `dataset/bid.12.txt`
- **Click Dataset:**  
  `dataset/clk.06.txt`, `dataset/clk.07.txt`, ..., `dataset/clk.12.txt`
- **Conversion Dataset:**  
  `dataset/conv.06.txt`, `dataset/conv.07.txt`, ..., `dataset/conv.12.txt`
- **Impression Dataset:**  
  `dataset/imp.06.txt`, `dataset/imp.07.txt`, ..., `dataset/imp.12.txt`
- **Supplementary Files:**  
  - `city.txt`
  - `region.txt`
  - `user.profile.tags.txt`
  - `bidder.submission.code` (contains implementation files for Java and Python)

---

## DSP Bidding Optimization Task
Participants must implement a bidding algorithm that, for each bid request, determines:
- **Whether to bid** (or return `-1` if not bidding).
- **What bid price to submit** if bidding.

The algorithm must operate under the following constraints:
- **Memory Usage:** ≤ 512 MB  
- **Execution Time:** ≤ 5 ms per bid request  
- **Auction Mechanism:** Second-price auction  
- **Budget Constraint:** Total spending must remain within the advertiser’s fixed budget

---

## Architecture and File Structure
```
.
├── README.md
├── requirements.txt
├── com.dtu.hackathon.bidding
│   ├── python
│       ├── bid.py
```

---

## Setup and Running the Code

### Prerequisites
- **Python:** Version 3.9  
- **Additional Libraries:** Install via `requirements.txt` if provided.

### Running the Code

#### For Python:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python Bid.py
```

---

## Team Information
- **Team Name:** *AboveGods*
- **Team Members:**
  - Hemang Jain, DTU CSE'27
  - Sanchali Thareja, DTU CSE'27
  - Vansh Sachdeva, DTU ME'27
  - Vishrut Grover, DTU CSE'27

---

## Approach

### 1. **Data Preprocessing & Feature Engineering**

Our approach begins by processing the four datasets: **bids, impressions, clicks, and conversions**. Since the bidding dataset contains only the bid request logs, we primarily focus on the impressions dataset to derive core features.

#### **Impressions Data Processing**
- We group the dataset based on `CreativeID` and `AdslotID`, as these attributes define an ad's placement and characteristics.
- We extract relevant features including `User-Agent`, `AdExchange`, `AdslotWidth`, `AdslotHeight`, `AdslotVisibility`, `AdslotFormat`, and `AdslotFloorPrice`.
- The **total number of impressions** for each unique ad is calculated, giving insights into how frequently an ad is displayed.

#### **Click & Conversion Data Processing**
- Click logs are processed to determine the **number of clicks per ad**.
- Conversion logs are used to compute the **number of successful conversions**.
- These values are incorporated as new features into our main dataset.
- We derive the **Click-Through Rate (CTR)** using:
  
  \[ \text{CTR} = \frac{\text{Number of Clicks}}{\text{Number of Impressions}} \]
  
  This provides a measure of ad engagement and helps optimize bidding strategies.

#### **Time-Based Feature Engineering**
- We convert timestamps into an **hour-based format**, allowing us to analyze **temporal trends** in user engagement.
- The dataset is further grouped by **hourly impressions and clicks**, leading to the calculation of **hourly CTR**, a crucial factor in optimizing bidding decisions.

#### **Device Type Classification**
- A new feature, `DeviceType`, is engineered based on `User-Agent`, categorizing whether the ad was viewed on **mobile, tablet, or desktop**.
- This feature aids in **predicting ad visibility** and its impact on user engagement.

#### **Geographical Feature Engineering**
- We utilize **TF-IDF clustering** on `Region` and `City` data to classify locations into **region-tier groups**.
- This helps in understanding how different locations impact CTR and conversion rates, influencing bid adjustments.

### 2. **Bidding Strategy & Model Selection**

We implement a **multi-threading approach** to maximize efficiency in bid calculations. Our strategy is divided into two simultaneous processes:

#### **CTR Prediction Pipeline**
- We employ a **Linear Support Vector Machine (SVM)** to predict the probability of an ad receiving a click.
- A **thresholding mechanism** is applied:
  - If `CTR Probability < 0.7`, **no bid is placed**, ensuring cost-effectiveness.

#### **Bid Price Prediction Pipeline**
- While the CTR model operates, a separate process predicts the **optimal bid price** using extracted features.
- This ensures that bids are placed at competitive yet cost-effective rates.

### 3. **Final Bidding Decision**

After obtaining the **CTR probability** and **predicted bid price**, we make the final bidding decision:
- If `CTR Probability > 0.7`, we place an aggressive bid:
  
  \[ \text{Bid} = \text{BiddingPrice} \times 1.2 \]
  
- Otherwise, we place a conservative bid:
  
  \[ \text{Bid} = \text{BiddingPrice} \]
  
  This ensures that we only invest in high-potential opportunities while avoiding excessive spending on low-engagement ads.

### 4. **Evaluation Strategy**
To measure the effectiveness of our approach, we conduct **real-time simulations** replicating the live bidding environment.

- **Performance Metrics:**
  - **Clicks Achieved**
  - **Conversions Achieved**
  - **Overall Score** (Clicks + N × Conversions)
  - **Budget Utilization**
  - **Execution Time ≤ 5ms**, **Memory Usage ≤ 512MB**

This structured approach ensures an **efficient and scalable** bidding strategy while optimizing costs and maximizing conversions.

---

## Final Prediction Pipeline
- First, we receive the complete bid request.
- 

## Our Validation Results
- **Clicks Achieved:** 
- **Conversions Achieved:** 
- **Overall Score:** 
- **Budget Utilization:** 
