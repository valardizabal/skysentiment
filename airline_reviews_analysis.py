import pandas as pd
import re
import nltk

nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)
nltk.download("punkt_tab", quiet=True)
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

"""
Cleans and analyzes data and then saves it to sea_airlines dict. Calls clean_review, sentiment_analysis, sentiment_analysis_report methods.

:param n: airline files
:type n: dict
"""


def data_analysis(files):
    # Reads all csv files
    for item in files:
        df = pd.read_csv(files[item])

        # Clean dataframe
        df.drop(
            ["status", "aircraft", "travel_type", "travel_class", "date"],
            axis=1,
            inplace=True,
        )

        df["seating_comfort"] = df["seating_comfort"].fillna(
            (df["seating_comfort"].mean().round(0))
        )
        df["staff_service"] = df["staff_service"].fillna(
            (df["staff_service"].mean().round(0))
        )
        df["food_quality"] = df["food_quality"].fillna(
            (df["food_quality"].mean().round(0))
        )
        df["entertainment"] = df["entertainment"].fillna(
            (df["entertainment"].mean().round(0))
        )
        df["wifi"] = df["wifi"].fillna((df["wifi"].mean().round(0)))
        df["ground_service"] = df["ground_service"].fillna(
            (df["ground_service"].mean().round(0))
        )
        df["value_for_money"] = df["value_for_money"].fillna(
            (df["value_for_money"].mean().round(0))
        )
        df["overall_rating"] = df["overall_rating"].fillna(
            (df["overall_rating"].mean().round(0))
        )

        # Cleaning the text in the review column
        df["cleaned_review"] = df["review"].apply(clean_reviews)

        # Sentiment Analysis
        df[["compound_score", "sentiment"]] = (
            df["cleaned_review"].apply(sentiment_analysis).tolist()
        )

        # Sentiment Analysis Report
        sentiment_scores = sentiment_analysis_report(
            item, df["compound_score"], df["sentiment"]
        )

        # Get average scores for each rating
        sc_score = df["seating_comfort"].mean().round(0).astype(int)
        ss_score = df["staff_service"].mean().round(0).astype(int)
        fq_score = df["food_quality"].mean().round(0).astype(int)
        e_score = df["entertainment"].mean().round(0).astype(int)
        w_score = df["wifi"].mean().round(0).astype(int)
        gs_score = df["ground_service"].mean().round(0).astype(int)
        vfm_score = df["value_for_money"].mean().round(0).astype(int)
        or_score = df["overall_rating"].mean().round(0).astype(int)

        ratings_dict = {
            "seating_comfort": sc_score,
            "staff_service": ss_score,
            "food_quality": fq_score,
            "entertainment": e_score,
            "wifi": w_score,
            "ground_service": gs_score,
            "value_for_money": vfm_score,
        }

        airline_dict = {}
        # Save to dictionary
        match item:
            case "air_asia":
                airline_dict = sea_airlines[0]
            case "singapore_airlines":
                airline_dict = sea_airlines[1]
            case "lion_air":
                airline_dict = sea_airlines[2]
            case "vietjet_air":
                airline_dict = sea_airlines[3]
            case "vietnam_airlines":
                airline_dict = sea_airlines[4]
            case "cebu_pacific":
                airline_dict = sea_airlines[5]
            case "garuda_indonesia":
                airline_dict = sea_airlines[6]
            case "philippine_airlines":
                airline_dict = sea_airlines[7]
            case "malaysia_airlines":
                airline_dict = sea_airlines[8]
            case "thai_airways":
                airline_dict = sea_airlines[9]

        airline_dict["ratings"] = ratings_dict
        airline_dict["overall_rating"] = or_score
        airline_dict["reviews"] = df.to_dict()
        airline_dict["sentiment_scores"] = sentiment_scores.to_dict()


"""
Cleans reviews using data analytics.

:param n: reviews column of a dataframe
:type n: df column
:return: cleaned reviews
:rtype: df column
"""


def clean_reviews(df):
    # Removes all special characters and numbers leaving the alphabets
    df = re.sub("[^A-Za-z]+", " ", str(df))

    # Convert all characters to lowercase
    df = df.lower()

    # Tokenize each review
    tokens = nltk.word_tokenize(df)

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    tokens = [token for token in tokens if token not in stop_words]

    # Lemmatize each word in each review
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Combine the cleaned tokens back into a string
    cleaned_text = " ".join(tokens)

    return cleaned_text


"""
Does sentiment analysis on clean reviews.

:param n: cleaned reviews
:type n: df column
:return: compound scores and sentiments
:rtype: df column
"""


def sentiment_analysis(clean_reviews):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(clean_reviews)
    compound_score = sentiment_dict["compound"]
    sentiment = ""

    if sentiment_dict["compound"] >= 0.05:
        sentiment = "Positive"
    elif sentiment_dict["compound"] <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return compound_score, sentiment


"""
Generates pie charts and bar charts according to an airline's compound scores and sentiments.

:param n: airline, compound score, sentiment
:type n: string, df column, df column
:return: sentiment scores
:rtype: df
"""


def sentiment_analysis_report(airline, compound_score, sentiment):
    # Pie chart
    counts = sentiment.value_counts()
    total = counts.values.sum()

    colors = {"Positive": "lightgreen", "Negative": "salmon", "Neutral": "grey"}
    colorsBar = []
    for val in compound_score:
        if val >= 0.05:
            colorsBar.append("lightgreen")
        elif val <= -0.05:
            colorsBar.append("salmon")
        else:
            colorsBar.append("grey")

    def pct_value(pct):
        return "{:.1f}%\n({:.0f})".format(pct, int(total * pct / 100))

    plt.pie(
        counts,
        labels=counts.index,
        colors=[colors[v] for v in counts.keys()],
        autopct=pct_value,
    )
    plt.title(f'Sentiment Analysis of {airline.replace("_"," ").title()} Reviews')
    plt.savefig(f"charts/{airline}-pie.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Bar Chart
    ax = compound_score.plot.hist(bins=20)
    for bar in ax.containers[0]:
        # get x midpoint of bar
        x = bar.get_x() + 0.5 * bar.get_width()

        # set bar color based on x
        if x <= -0.05:
            bar.set_color("salmon")
        elif x >= 0.05:
            bar.set_color("lightgreen")
        else:
            bar.set_color("grey")

    plt.title(
        f'Distribution for Sentiment Scores of {airline.replace("_"," ").title()} Reviews'
    )
    plt.xlabel("Compound Score")
    plt.ylabel("Count")
    plt.savefig(f"charts/{airline}-bar.png", dpi=300, bbox_inches="tight")
    plt.close()
    return counts


# List of dictionaries of Top airlines in SEA
sea_airlines = [
    {
        "airline": "AirAsia",
        "filename": "air_asia",
        "country": "Malaysia",
        "star": 3,
        "overall_rating": 9,
        "ratings": {"a": 1, "b": 2},
        "reviews": {},
        "sentiment_scores": {"a": 1, "c": 2},
    },
    {
        "airline": "Singapore Airlines",
        "filename": "singapore_airlines",
        "country": "Singapore",
        "star": 5,
        "overall_rating": 10,
        "ratings": {},
        "reviews": [],
        "sentiment_scores": {},
    },
    {
        "airline": "Lion Air",
        "country": "Indonesia",
        "filename": "lion_air",
        "star": 2,
        "overall_rating": 3,
        "ratings": {},
        "reviews": [],
        "sentiment_scores": {},
    },
    {
        "airline": "VietJet Air",
        "country": "Vietnam",
        "filename": "vietjet_air",
        "star": 0,
        "overall_rating": 2,
        "ratings": {},
        "reviews": [],
        "sentiment_scores": {},
    },
    {
        "airline": "Vietnam Airlines",
        "country": "Vietnam",
        "filename": "vietnam_airlines",
        "star": 4,
        "overall_rating": 4,
        "ratings": {},
        "reviews": [],
        "sentiment_scores": {},
    },
    {
        "airline": "Cebu Pacific",
        "filename": "cebu_pacific",
        "country": "Philippines",
        "star": 3,
        "overall_rating": 1,
        "ratings": {},
        "reviews": [],
        "sentiment_scores": {},
    },
    {
        "airline": "Garuda Indonesia",
        "filename": "garuda_indonesia",
        "country": "Indonesia",
        "star": 5,
        "overall_rating": 8,
        "ratings": {},
        "reviews": [],
        "sentiment_scores": {},
    },
    {
        "airline": "Philippine Airlines",
        "filename": "philippine_airlines",
        "country": "Philippines",
        "star": 4,
        "overall_rating": 7,
        "ratings": {},
        "reviews": [],
        "sentiment_scores": {},
    },
    {
        "airline": "Malaysia Airlines",
        "filename": "malaysia_airlines",
        "country": "Malaysia",
        "star": 4,
        "overall_rating": 6,
        "ratings": {},
        "reviews": [],
        "sentiment_scores": {},
    },
    {
        "airline": "Thai Airways",
        "filename": "thai_airways",
        "country": "Thailand",
        "star": 4,
        "overall_rating": 5,
        "ratings": {},
        "reviews": [],
        "sentiment_scores": {},
    },
]

# path to csv files of raw data
airline_files = {
    "air_asia": "data/AirAsia.csv",
    "cebu_pacific": "data/Cebu Pacific.csv",
    "garuda_indonesia": "data/Garuda Indonesia.csv",
    "lion_air": "data/Lion Air.csv",
    "malaysia_airlines": "data/Malaysia Airlines.csv",
    "philippine_airlines": "data/Philippine Airlines.csv",
    "singapore_airlines": "data/Singapore Airlines.csv",
    "thai_airways": "data/Thai Airways.csv",
    "vietjet_air": "data/VietJet Air.csv",
    "vietnam_airlines": "data/Vietnam Airlines.csv",
}

if __name__ == "__main__":
    main()
