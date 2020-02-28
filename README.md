# Patiently Waiting

Check emergency room wait times around Toronto by choosing a day: https://patientlywaiting.herokuapp.com/

## **Goal**

Generate emergency wait times around Toronto based on the day of the week


## Problem Statement

Have you ever stepped foot in the emergency room of a hospital in Toronto either for a loved one or perhaps yourself, only to be met with a grueling long wait until you see any medical professional?

It sucks. And there should definitely be a better system, right? Having volunteered at Toronto Western Hospital Emergency Department and being able to experience both sides of the system, I wanted to dig deep at what's really going on and to actually do something about it.

<img src="https://github.com/anitatea/patiently_waiting/blob/master/static/img/ss.png?raw=true">


### Technologies Used

- Python
- Pandas
- pipenv - for local storage of credentials
- Beautiful Soup - Web Scraping
- SKLearn pipelines
- DataFrameMapper
- HDBSCAN clustering
- Flask
- Google Maps Api
<!-- - Altair -- plotting
- Folium -- plotting -->

## Project Notes

### Data Gathering ###
Detailed administrative data on date, patient flow, current and past examinations in Ontario was provided by:
* [National Ambulatory Care Reporting System (NACRS)](https://www.cihi.ca/en/national-ambulatory-care-reporting-system-metadata)

* [Canadian Institude for Health Information (CIHI)](https://www.cihi.ca/en/access-data-and-report)


### Data Modeling ###
The ability to accurately and reliably predict waiting times at walk-in hospital facilities can increase both patient satisfaction and hospital efficiency via a better management of patient flow. My web-app implements machine learning (ML) models to predict waiting times in the Emergency Room (ER) of the largest public hospital in the Greater Toronto Area (GTA).

 Several ML algorithms were evaluated to find the most accurate and useful prediction to a user. I chose [Gradient Boosting](https://medium.com/mlreview/gradient-boosting-from-scratch-1e317ae4587d) among other regression models explored for predicting wait times.


**PATIENTLY WAITING** is currently in beta testing. If you notice any bugs, have any questions or suggestions, I'd love to hear from you: [anita.tran38@gmail.com](anita.tran38@gmail.com?subject=Feedback on PatientlyWaiting).


<img src="https://media.makeameme.org/created/me-patiently-waiting-399b1150e6.jpg" width=300>


### Planned Future Enhancements ###

* Docker for hosting database, nginx and flask web app
* Google API to read your location
* Actively scrape hospital data as it is released per month on hqontatio.ca
* Generate best route to hospital using combinatorial optimization
