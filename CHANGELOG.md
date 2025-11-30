# Changelog

## 5.0.0
Date: 2025-11-01

- CloudCIX Major release of Version 5
- Implement version management for services. It no version is sent, it will default to the latest supported major.minor version
- Supported version:
    - v5.0/{ service }/

## 4.4.0
Date 2025-10-28

- Added `UCCIX-Mistral-24B` as a choice for the `nn_llm` and `reranker` properites of the Chatbot service.
- Removed `deepseek` as a choice for the `nn_llm` and `reranker` properites of the Chatbot service.

## 4.3.0
Date 2025-09-26

- Add capability to the Contact Chatbot to handle user's uploaded images 

## 4.2.0
Date 2025-07-15

- Increased timeout for requests to ML services

## 4.1.1
Date 2025-06-17

- Minor bugfixes

## 4.1.0
Date 2025-05-28

- Enhancements: 
    - Updated Chatbot to comsume Corpus from Embedding DB Api
    - Removed Embeddings service from Contact. It is available in the ML Workbench App for testing a Corpus in the Embedding DB Api

## 4.0.2
Date 2025-05-15

- Enhancement: Added `api_key` and `corpus_names` properites to the Chatbot service to support a Chatbot consumming the CloudCIX Embedding DB API.


## 4.0.1
Date 2025-04-29

- Enhancement: Added `chatgpt4.1` as a choice for the `nn_llm` and `reranker` properites of the Chatbot service.


## 4.0.0
Date 2025-03-18

- CloudCIX Major release of Version 4
- CloudCIX Framework base incremented to Python 3.10
- CloudCIX Framework base incremented to Django 5.0.10

## 3.4.0
Date 2025-01-09

- Enhancement: Re-enable smalltalk 

## 3.3.11
Date: 2024-12-19

- Enhancement: Improved error catching in vector.py

## 3.3.10
Date: 2024-12-16

- Enhancement: In a Corpus if a hyperlink ends in ".pdf" and the content-type from the requests library is "applications/octet-stream", set as "applications/pdf". 

## 3.3.9
Date: 2024-12-16

- Enhancement: Added properties `content_type` and `status` to Corpus service to improve the the processing of vectors for a `hyperlink` in the Corpus.
- Enhancement: To give users more control over the position of the Chatbot button in the iframe to be emvedded on their website. The following changes were made to the Chatbot model:
    - Removed `button_position_from_bottom` and `button_position_from_right`
    - Added `horizontal_percentage`, `horizontal_position`, `vertical_position` and `vertical_percentage`


## 3.3.8
Date: 2024-11-27

- Enhancement: Added `chatbot_header_title` and `chatbot_header_description` as optional parameters to the Chatbot model.

## 3.3.7
Date: 2024-11-25

- Enhancement: Use Recursive splitter to always ensure desired chunk length for embseddings.

## 3.3.6
Date: 2024-11-19

- Enhancement: Added `pdf_scraping` option to the Chatbot service. Supported values are `pdf` and `pdf_hi_res`.
- Enhancement: Added ``layout` option to the Chatbot service. Supported values are `window` and `widget`.
- Enhancement: Added `uccix_instruct` as an value for the `nn_llm` of the Chatbot service.

## 3.3.5
Date: 2024-10-31

- Bug Fix: Fix bug where PDF HTML urls were not scrapped. 
- Enhancement: Added `cookie_consent_text` option to the Chatbot Service. 

## 3.3.4
Date: 2024-10-18

- Enhancement: Added support in Chatbot service to disable Keyword Search during the Embedding process by setting `bm25_limit` to 0.
