import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json

app = Flask(__name__)
app.secret_key = 'dev-key-12345'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    # Check if the user clicked the link from the church's Facebook page
    referer = request.headers.get('Referer', '')
    from_facebook = 'fbclid' in request.args or 'facebook.com' in referer.lower()
    
    if from_facebook:
        # Show the "Volunteers" menu item to Facebook visitors
        return render_template('index.html', show_menu=True)
    else:
        # Hide the "Volunteers" menu item for everyone else
        return render_template('index.html', show_menu=False)

@app.route('/chris')
def chris_page():
    json_path = os.path.join(BASE_DIR, 'json', 'chris.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        video_id = data.get("video", "")
    except Exception as e:
        print(f"Error reading chris.json: {e}")
        video_id = ""

    scripture_html = (
    "<div style='text-align: left; line-height: 1.6;'>"
    "<strong>23</strong> But now that there is no more place for me to work in these regions, and since I have been longing for many years to visit you,<br>"
    "<strong>24</strong> I plan to do so when I go to Spain. I hope to see you while passing through and to have you assist me on my journey there, after I have enjoyed your company for a while.<br>"
    "<strong>25</strong> Now, however, I am on my way to Jerusalem in the service of the Lord’s people there.<br>"
    "<strong>26</strong> For Macedonia and Achaia were pleased to make a contribution for the poor among the Lord’s people in Jerusalem.<br>"
    "<strong>27</strong> They were pleased to do it, and indeed they owe it to them. For if the Gentiles have shared in the Jews’ spiritual blessings, they owe it to the Jews to share with them their material blessings.<br>"
    "<strong>28</strong> So after I have completed this task and have made sure that they have received this contribution, I will go to Spain and visit you on the way.<br>"
    "<strong>29</strong> I know that when I come to you, I will come in the full measure of the blessing of Christ.<br>"
    "<strong>30</strong> I urge you, brothers and sisters, by our Lord Jesus Christ and by the love of the Spirit, to join me in my struggle by praying to God for me.<br>"
    "<strong>31</strong> Pray that I may be kept safe from the unbelievers in Judea and that the contribution I take to Jerusalem may be favorably received by the Lord’s people there,<br>"
    "<strong>32</strong> so that I may come to you with joy, by God’s will, and in your company be refreshed.<br>"
    "<strong>33</strong> The God of peace be with you all. Amen."
    "</div>"
    )
    outline_data = [
    {"label": "Verse 23", "text": "Paul was called to share the Gospel with the [BLANK] world."},
    {"label": "Verse 24", "text": "[BLANK] was the western end of the Roman Empire at the time of Paul."},
    {"label": "Verse 25-26", "text": "[BLANK] Christians recognize the need to help Jewish Christians."},
    {"label": "Verse 27", "text": "Paul reminds the church of a common debt of [BLANK]."},
    {"label": "", "text": "-Romans 13:8"},
    {"label": "Verse 28-29", "text": "-Acts 20:22-23"},
    {"label": "", "text": "Paul went, full of [BLANK] that God knew what he was doing."},
    {"label": "Verse 30-33", "text": "The Gospel is a message of [BLANK]."},
    {"label": "", "text": "The Gospel lived out allows us to live in peace with fellow [BLANK]."},
    {"label": "", "text": "The Gospel propels us to [BLANK] the message of peace with non-believers in an act of love."},
    {"label": "", "text": "The Gospel reminds me of God’s [BLANK], so I have peace even in times of turmoil."},
    {"label": "Conclusion", "text": "What [BLANK] do you need to allow Jesus to heal in your life?"},
    {"label": "", "text": "What [BLANK] do you need to be sharing with other believers?"}
]
    
    return render_template(
        'chris.html', 
        video_id=video_id, 
        scripture=scripture_html,
        outline=outline_data
    )

@app.route('/jason')
def jason_page():
    songs_data = [
        {"title": "I Will Follow", "youtube_id": "2cu5q_4zuRM"},
        {"title": "Come Thou Fount (I Will Sing)", "youtube_id": "LoE-uNsGc2E"},
        {"title": "Graves Into Gardens", "youtube_id": "NYA4DHdBKnY"},
        {"title": "My Worth Is Not In What I Own", "youtube_id": "vfFrJHuptUQ"}
    ]
    return render_template('jason.html', songs=songs_data)
    
"""@app.route('/youth_ministry')
@app.route('/patrick')
def youth_ministry():
    return "Youth Ministry page is under construction."""
    
@app.route('/mens_ministry')
def mens_ministry(): return render_template("mens_ministry.html")

@app.route('/womens-ministry')
def womens_ministry(): return render_template("womens-ministry.html")

@app.route('/volunteers')
def volunteers(): return render_template("volunteers.html")

@app.route('/announcements')
def announcements():
    json_path = os.path.join(BASE_DIR, 'json', 'announcements.json')
    try:
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                announcements_list = json.load(f)
            return render_template('announcements.html', announcements=announcements_list)
        return render_template('announcements.html', announcements=[])
    except Exception as e:
        print(f"Announcements Route Error: {e}")
        return render_template('announcements.html', announcements=[])  

@app.route("/senior-adults")
@app.route("/senior_adults")
def senior_adults():
    return render_template("senior-adults.html")    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)