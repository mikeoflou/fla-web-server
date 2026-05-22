import functions_framework

@functions_framework.http
def hello_serverless(request):
    # 1. THE BASE TESTING URL
    # Updated to point to your specific desktop directory on the server
    base_url = "https://129.121.84.30"

    # 2. STAFF DATA
    staff_members = [
        {"name": "Chris", "role": "Pastor", "img": "pastor_chris.jpg", "route": f"{base_url}/chris"},
        {"name": "Jason", "role": "Worship Leader", "img": "jason.jpg", "route": f"{base_url}/jason"},
        {"name": "Patrick", "role": "Youth & Children's Pastor", "img": "patrick.jpg", "route": f"{base_url}/patrick"},
        {"name": "Kevin", "role": "Senior & Men's Pastor", "img": "kevin.jpg", "route": f"{base_url}/kevin"}
    ]
    
    # 3. BUILD THE CLICKABLE CARDS
    cards_html = ""
    for person in staff_members:
        cards_html += f'''
        <a href="{person['route']}" style="text-decoration: none; color: inherit;" target="_blank">
            <div style="width: 280px; border: 4px solid black; border-radius: 15px; padding: 15px; background-color: #D3D3D3; text-align: center; cursor: pointer;">
                
                <img src="/static/images/staff/{person['img']}" 
                     alt="{person['name']}" 
                     style="width: 100%; height: 280px; object-fit: cover; border-radius: 10px; border: 2px solid black; background-color: #999;">
                
                <h2 style="font-size: 32px; font-weight: 900; color: black; margin: 15px 0 5px 0;">{person['name']}</h2>
                <p style="font-size: 20px; font-weight: 900; color: black;">{person['role']}</p>
            </div>
        </a>
        '''

    # 4. FULL PAGE RENDER
    return f"""
    <div style="font-family: Arial, sans-serif; text-align: center; background-color: white; padding-bottom: 100px;">
        
        <div style="width: 100%; background-color: #2c3e50; padding: 20px 0; margin-bottom: 40px;">
            <img src="/static/images/church_exterior.jpg" 
                 style="width: 90%; max-width: 800px; border-radius: 15px; border: 5px solid white;">
        </div>

        <h1 style="font-size: 65px; font-weight: 900; color: black; margin-bottom: 50px;">EHBC Staff</h1>
        
        <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 40px; padding: 0 20px;">
            {cards_html}
        </div>
    </div>
    """