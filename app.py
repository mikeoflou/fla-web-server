import os
from flask import Flask, render_template, request, redirect, url_for, session
from textwrap import dedent
from datetime import datetime, timedelta

# 1. Unified Setup
base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, 
            static_folder=os.path.join(base_dir, 'static'),
            template_folder=os.path.join(base_dir, 'templates'))

app.secret_key = 'dev-key-12345'

# ==========================================
# 2. PUBLIC ROUTES
# ==========================================

@app.route('/')
def index():
    home_page_data = {
        "title": "Eastern Heights Baptist Church",
        "content": "We Exist to Make Jesus Known"
    }
    
    # Home page cards (using the updated route names)
    ministry_cards = [
        {"url": "/Chris", "name": "Pastor Chris", "label": "Scripture and Outline", "filename": "images/staff/Chris.jpg"},
        {"url": "/worship", "name": "Pastor Jason", "label": "Order of Worship", "filename": "images/staff/Jason.jpg"},
        {"url": "/youth_ministry", "name": "Pastor Patrick", "label": "Youth Ministry", "filename": "images/staff/Patrick.jpg"},
        {"url": "/senior_adults", "name": "Pastor Kevin", "label": "Senior Adults", "filename": "images/staff/Kevin.jpg"}
    ]
    
    return render_template('index.html', 
                           home_page=home_page_data, 
                           home_ministry_cards=ministry_cards)

@app.route('/Chris')
def chris():
    # --- AUTOMATIC DATE LOGIC ---
    today = datetime.now()
    # Finds the most recent Sunday (Service Date)
    days_since_sunday = (today.weekday() + 1) % 7
    last_sunday = today - timedelta(days=days_since_sunday)
    # Finds the upcoming Sunday
    next_sunday = last_sunday + timedelta(days=7)
    
    vid_id = "rG8e3dU-bAc"
    
    scripture_text = dedent("""
    Romans 13:8-14 (NIV)
    8 Let no debt remain outstanding, except the continuing debt to love one another, for whoever loves others has fulfilled the law. 9 The commandments, “You shall not commit adultery,” “You shall not murder,” “You shall not steal,” “You shall not covet,” and whatever other command there may be, are summed up in this one command: “Love your neighbor as yourself.” 10 Love does no harm to a neighbor. Therefore love is the fulfillment of the law.

    11 And do this, understanding the present time: The hour has already come for you to wake up from your slumber, because our salvation is nearer now than when we first believed. 12 The night is nearly over; the day is almost here. So let us put aside the deeds of darkness and put on the armor of light. 13 Let us behave decently, as in the daytime, not in carousing and drunkenness, not in sexual immorality and debauchery, not in dissension and jealousy. 14 Rather, clothe yourselves with the Lord Jesus Christ, and do not think about how to gratify the desires of the flesh.
    """).strip()

    big_outline = dedent("""
    Verse 8
    Proverbs 22:7
    In Jesus Christ, all our sins, both present and future, are __________ ________.  

    How is loving others a _________________ of the _______?         
    How is loving others a __________?
    Why should I even __________?

    Verse 9
    -Matthew 19: 17-22 
    -Matthew 22: 35-40

    Verse 10
    It is by _________ that we are to keep the commandments.
    Love is a _________ because of God’s endless love for us.
             
    Verse 11
    ________ is the time to love God and others.
    You are more likely to reach your end before the ___________ _______.

    Verse 12-13
    We are to bring the light of the Gospel into the _________________.  

    Verse 14
    The command is to put on Christ, then deal with ______________ __________.
         
    Conclusion:
    _____________ others is hard.  
          
    Do I __________________ the love God has for me?
    Where do I need _________ _________ in loving others?
    """).strip()
    
    page_info = {
        "title": "Romans 13: 8-14",
        "last_service": last_sunday.strftime("%B %d, %Y"),
        "next_service": next_sunday.strftime("%B %d, %Y")
    }
   
    return render_template('Chris.html', 
                           scripture=scripture_text, 
                           outline=big_outline, 
                           video_id=vid_id, 
                           info=page_info)

@app.route('/Jason')
def worship():
    song_list = [
        {'title': 'This is Amazing Grace', 'id': 'rG8e3dU-bAc'},
        {'title': 'I Stand Amazed', 'id': 'tK1AWAwqFy0'},
        {'title': 'Behold Our God', 'id': '3_M_ZdWrCjs'},
        {'title': 'Build My Life', 'id': 'xLSDBG1OcGE'}
    ]
    return render_template('Jason.html', videos=song_list)

@app.route('/youth_ministry')
def youth_ministry():
    return render_template('youth_ministry.html')

@app.route('/senior_adults')
def senior_adults():
    senior_gallery = [
        {
            "filename": "images/gallery/20260402115341_0_SeniorBibleStudy.jpg",
            "alt": "Senior Bible Study",
            "w": "400",
            "h": "300"
        },
        {
            "filename": "images/gallery/20260402115341_2_SeniorBibleStudy2.png",
            "alt": "Senior Bible Study",
            "w": "400",
            "h": "300"
        },
       
    ]

    logo_path = "images/gallery/20260402121942_49_images_seniorLogo.png"
    
    # You must add the variables here:
    return render_template('Senior_Adults.html', gallery=senior_gallery, logo=logo_path)

# Placeholder routes for the rest of your menu
@app.route('/announcements')
def announcements(): 
    weekly_bulletin = [
        {
            "date": "Sunday, April 12, 2026",
            "title": "Weekly Church Bulletin",
            "content": """
             CHUPPER (Church + Supper) is back!
            Wednesday Nights at 5:30pm.
            Sign up at the Greeter Station.
            Cost is $2 per person with $10 max per family
                    
            Wednesday Night
            2 Samuel 24

            Thank you to those that provided food, money toward the cost 
            of food, and helped serve the CSF meal at IUS.  
            The students always appreciate it!

            Register today through April 26th for the Sisters in Christ Spring Tea 
            which will be May 9th at 2:00pm at Eastern Heights Baptist Church.
            Cost is $15 adults; $10 children ages 3-9; free for children 0-2 years.
                
            Thank you to those who helped support our youth by participating 
            in the walk-through breakfast today!

            On April 16th, the Young @ Heart will be going to lunch at Mike Linnig's Seafood Restaurant.  
            We will meet at the church at 11:15am and carpool to the restaurant.  
            Today is the last day to let Kevin McLendon know 
            if you are going and if you will need a ride.  

            On Saturday, April 18th at 3:00pm, the Deacons will host a special luncheon for the 
            widows and widowers of our congregation.  
            Please RSVP to the church at ehbcjeff@gmail.com or to 
            Noel Garcia at (787)505-8681.

            The Lockout 2.0 - For students grade 6-12, we will have our second annual Lockout Event on Friday, 
            May 15th from 8:00pm to 7:30 AM. The cost is $60. A deposit of $20 is due to hold your spot 
            because space is limited. We will be going to Malibu Jacks; 
            The Main Event; Breakout Louisville, and The New Albany Clay Collective.  
            Please see Pastor Patrick for More information. 

            Thank you to those who helped support our youth by participating 
            in the walk-through breakfast today!
            """
        }
    ]
    return render_template("announcements.html", bulletin=weekly_bulletin)

@app.route('/contact')
def contact():
    church_info = {
        "address": "4202 Helen Road, Jeffersonville, Indiana 47130",
        "phone": "(812) 283-6998",
        "email": "ehbcjeff@gmail.com",
        "office_hours": "Contact office for current hours"
    }
    return render_template('contact.html', info=church_info)
@app.route('/events')
def events(): 
    return render_template("events.html")

@app.route('/prayer_requests')
def prayer_requests(): 
    return "<h1>Prayer Requests Coming Soon</h1>"

# ==========================================
# 3. ADMIN & AUTH ROUTES
# ==========================================

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Using host 0.0.0.0 for network access if needed
    app.run(host='0.0.0.0', port=5000, debug=True)