# IIMMPACT - The Python library for IIMMPACT API
 
## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import iimmpact 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import iimmpact
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import iimmpact
from iimmpact.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = iimmpact.AuthorizationTokenApi(iimmpact.ApiClient(configuration))
token_request = iimmpact.TokenRequest() # TokenRequest | 

try:
    api_response = api_instance.v1_token_post(token_request)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuthorizationTokenApi->v1_token_post: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *https://api.iimmpact.com*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AuthorizationTokenApi* | [**v1_token_post**](docs/AuthorizationTokenApi.md#v1_token_post) | **POST** /v1/token | 
*AuthorizationTokenApi* | [**v1_token_refresh_post**](docs/AuthorizationTokenApi.md#v1_token_refresh_post) | **POST** /v1/token/refresh | 
*CallbackUrlApi* | [**v1_callback_url_get**](docs/CallbackUrlApi.md#v1_callback_url_get) | **GET** /v1/callback-url | 
*CallbackUrlApi* | [**v1_callback_url_post**](docs/CallbackUrlApi.md#v1_callback_url_post) | **POST** /v1/callback-url | 
*CarInsuranceApi* | [**v1_car_insurance_get**](docs/CarInsuranceApi.md#v1_car_insurance_get) | **GET** /v1/car-insurance | 
*JPJRecordsApi* | [**v1_jpj_driving_license_get**](docs/JPJRecordsApi.md#v1_jpj_driving_license_get) | **GET** /v1/jpj/driving-license | 
*JPJRecordsApi* | [**v1_jpj_driving_test_results_get**](docs/JPJRecordsApi.md#v1_jpj_driving_test_results_get) | **GET** /v1/jpj/driving-test-results | 
*JPJRecordsApi* | [**v1_jpj_motor_vehicle_expiry_get**](docs/JPJRecordsApi.md#v1_jpj_motor_vehicle_expiry_get) | **GET** /v1/jpj/motor-vehicle-expiry | 
*JPJRecordsApi* | [**v1_jpj_summons_get**](docs/JPJRecordsApi.md#v1_jpj_summons_get) | **GET** /v1/jpj/summons | 
*LowBalanceWarningApi* | [**v1_low_balance_threshold_get**](docs/LowBalanceWarningApi.md#v1_low_balance_threshold_get) | **GET** /v1/low-balance-threshold | 
*LowBalanceWarningApi* | [**v1_low_balance_threshold_post**](docs/LowBalanceWarningApi.md#v1_low_balance_threshold_post) | **POST** /v1/low-balance-threshold | 
*MyAccountApi* | [**v1_auth_change_password_post**](docs/MyAccountApi.md#v1_auth_change_password_post) | **POST** /v1/auth/change-password | 
*MyAccountApi* | [**v1_auth_new_password_challenge_post**](docs/MyAccountApi.md#v1_auth_new_password_challenge_post) | **POST** /v1/auth/new-password-challenge | 
*MyAccountApi* | [**v1_balance_get**](docs/MyAccountApi.md#v1_balance_get) | **GET** /v1/balance | 
*ProductEnquiryApi* | [**v1_products_get**](docs/ProductEnquiryApi.md#v1_products_get) | **GET** /v1/products | 
*ServicesApi* | [**v1_bill_presentment_get**](docs/ServicesApi.md#v1_bill_presentment_get) | **GET** /v1/bill-presentment | 
*ServicesApi* | [**v1_networkstatus_get**](docs/ServicesApi.md#v1_networkstatus_get) | **GET** /v1/networkstatus | 
*ServicesApi* | [**v1_topup_post**](docs/ServicesApi.md#v1_topup_post) | **POST** /v1/topup | 
*TransactionHistoryApi* | [**v1_balance_statement_get**](docs/TransactionHistoryApi.md#v1_balance_statement_get) | **GET** /v1/balance-statement | 
*TransactionHistoryApi* | [**v1_transactions_get**](docs/TransactionHistoryApi.md#v1_transactions_get) | **GET** /v1/transactions | 


## Documentation For Models

 - [BalanceResponse](docs/BalanceResponse.md)
 - [BalanceResponseData](docs/BalanceResponseData.md)
 - [BalanceStatementResponse](docs/BalanceStatementResponse.md)
 - [BalanceStatementResponseData](docs/BalanceStatementResponseData.md)
 - [BalanceStatementResponseLinks](docs/BalanceStatementResponseLinks.md)
 - [BalanceStatementResponseMeta](docs/BalanceStatementResponseMeta.md)
 - [BillPresentmentResponse](docs/BillPresentmentResponse.md)
 - [BillPresentmentResponseData](docs/BillPresentmentResponseData.md)
 - [BillPresentmentResponseMetadata](docs/BillPresentmentResponseMetadata.md)
 - [CallbackUrlResponse](docs/CallbackUrlResponse.md)
 - [CallbackUrlResponseData](docs/CallbackUrlResponseData.md)
 - [CallbackUrlResponseMetadata](docs/CallbackUrlResponseMetadata.md)
 - [CarInsuranceRespone](docs/CarInsuranceRespone.md)
 - [CarInsuranceResponeVariant](docs/CarInsuranceResponeVariant.md)
 - [ChangePasswordRequest](docs/ChangePasswordRequest.md)
 - [DepositRequest](docs/DepositRequest.md)
 - [DrivingLicenseRespone](docs/DrivingLicenseRespone.md)
 - [DrivingLicenseResponeInner](docs/DrivingLicenseResponeInner.md)
 - [DrivingTestRespone](docs/DrivingTestRespone.md)
 - [DrivingTestResponeEnquiryTestPart1](docs/DrivingTestResponeEnquiryTestPart1.md)
 - [Empty](docs/Empty.md)
 - [Error](docs/Error.md)
 - [InlineResponse200](docs/InlineResponse200.md)
 - [InlineResponse2001](docs/InlineResponse2001.md)
 - [InlineResponse2002](docs/InlineResponse2002.md)
 - [InlineResponse2002Data](docs/InlineResponse2002Data.md)
 - [InlineResponse200Data](docs/InlineResponse200Data.md)
 - [JPJRecordsResponse](docs/JPJRecordsResponse.md)
 - [JPJSummonsResponse](docs/JPJSummonsResponse.md)
 - [LowBalanceWarningResponse](docs/LowBalanceWarningResponse.md)
 - [LowBalanceWarningResponseData](docs/LowBalanceWarningResponseData.md)
 - [LowBalanceWarningResponseMetadata](docs/LowBalanceWarningResponseMetadata.md)
 - [NetworkStatusResponse](docs/NetworkStatusResponse.md)
 - [NetworkStatusResponseData](docs/NetworkStatusResponseData.md)
 - [NetworkStatusResponseMetadata](docs/NetworkStatusResponseMetadata.md)
 - [NewPasswordRequest](docs/NewPasswordRequest.md)
 - [NewPasswordResponses](docs/NewPasswordResponses.md)
 - [OnlyMessageRespone](docs/OnlyMessageRespone.md)
 - [RefreshTokenRequest](docs/RefreshTokenRequest.md)
 - [TokenRequest](docs/TokenRequest.md)
 - [TokenResponse](docs/TokenResponse.md)
 - [TokenResponseAuthenticationResult](docs/TokenResponseAuthenticationResult.md)
 - [TopupRequest](docs/TopupRequest.md)
 - [TopupResponse](docs/TopupResponse.md)
 - [TopupResponseData](docs/TopupResponseData.md)
 - [TransactionsResponse](docs/TransactionsResponse.md)
 - [TransactionsResponseBalance](docs/TransactionsResponseBalance.md)
 - [TransactionsResponseData](docs/TransactionsResponseData.md)
 - [TransactionsResponseMeta](docs/TransactionsResponseMeta.md)
 - [TransactionsResponseProduct](docs/TransactionsResponseProduct.md)
 - [TransactionsResponseStatus](docs/TransactionsResponseStatus.md)
 - [VehicleExpiryResponse](docs/VehicleExpiryResponse.md)


## Documentation For Authorization


## IIMMPACT-COGNITO

- **Type**: API key
- **API key parameter name**: Authorization
- **Location**: HTTP header

## SSO

- **Type**: API key
- **API key parameter name**: Authorization
- **Location**: HTTP header

## api_key

- **Type**: API key
- **API key parameter name**: x-api-key
- **Location**: HTTP header