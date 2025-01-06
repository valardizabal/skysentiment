 # SkySentiment: SEA Airline Review Insights
#### Video Demo:  [SkySentiment Video](https://youtu.be/SXduPGu4eO0)

#### Description:
This project is a Python-based program that provides insights into customer satisfaction with the top 10 Southeast Asian (SEA) airlines using sentiment analysis of SkyTrax reviews. It analyzes review data to gauge public sentiment and presents the results through clear visual reports. The insights can help you decide which airline to book for your next trip, ensuring a better travel experience.

## Features
**1. Sentiment Analysis:**
Perform sentiment analysis using VADER sentiment on top Southeast Asian airlines, showing percentages of positive, neutral, and negative sentiments, along with average service ratings and an overall score.

**2. Data Visualization:**
Results are visualized through interactive charts, making it easy to understand airline performance at a glance

**3. Export Options:**
Export results to a PDF file, with options to include all 10 airlines, filter by specific country, or focus on a particular airline.

**4. Top 3 Airlines:**
View the top 3 highest-rated airlines, along with details on what makes them stand out.

**5. Bottom 3 Airlines:**
Explore the 3 lowest-rated airlines and the key factors contributing to their low ratings.

**6. Country-Specific Ratings:**
Select a country to view its list of airlines and see their individual ratings.

## Installation
1. Clone the Repository:
Clone the repository to your local machine using the command:
```git clone <repository-url>```
2. Install Required Libraries:
Navigate to the project directory and install the required libraries listed in the requirements.txt file by running:
```pip install -r requirements.txt```

## Folders and Files
Make sure to have all folders and files as well as install all dependencies before running the project.
- **charts** - empty; folder for all pie and bar chart from sentiment analysis for different airlines.
- **data** - with raw csv files; folder for all csv files of raw data
- **img** - with png images; contains the logos of different airlines for the pdf file
- **pdfs** - empty; folder where generated pdf file will be stored
- **airline_reviews_analysis.py** - for sentiment analysis and visualization
- **generate_pdf.py** - for generating pdf
- **project.py** - main program
- **test_project.py** - tester for main program

## Usage
1. Open the command prompt and navigate to the project directory using:
```cd path/to/project-directory```
2. Execute the project by running the following command:
```python project.py```
3. When prompted, select "Yes" and press Enter to begin the sentiment analysis.
4. Wait for analysis.
* The sentiment analysis may take some time as it processes reviews from various airlines and generates visual charts.
5. After the analysis, choose from the available options such as generating a PDF report, viewing results, or exploring further details.
6. Exit the program when you are done.

## Dependencies
- pandas
- re
- nltk
- vaderSentiment
- matplotlib
- fpdf2
- pyfiglet
- beaupy
