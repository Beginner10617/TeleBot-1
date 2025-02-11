import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import cv2
import numpy as np

def get_student_details(ROLL_NUMBER):
    """
    Fetch student details from IITK OA website for the given roll number.
    :param ROLL_NUMBER: The roll number to fetch details for
    """
    # Start a session to maintain cookies
    s = requests.Session()

    # Step 1: Simulate visiting necessary pages to establish session
    s.get("https://oa.cc.iitk.ac.in/Oa/Jsp/Main_Frameset.jsp")
    s.get("https://oa.cc.iitk.ac.in/Oa/Jsp/Main_Intro.jsp?frm='SRCH'")
    s.get("https://oa.cc.iitk.ac.in/Oa/Jsp/OAServices/IITK_Srch.jsp?typ=stud")

    # Define headers (same as your working script)
    headers = {
        "Referer": "https://oa.cc.iitk.ac.in/Oa/Jsp/OAServices/IITk_SrchStudRoll_new.jsp"
    }

    # Define payload with roll number
    payload = {
        'typ': 'stud',  # Searching for students
        'numtxt': ROLL_NUMBER,  # The roll number to fetch
        'sbm': 'Y'
    }

    # Step 2: Send request to get details for the roll number
    response = s.post("https://oa.cc.iitk.ac.in/Oa/Jsp/OAServices/IITk_SrchRes_new.jsp", headers=headers, data=payload)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract student details
        details = {}
        for para in soup.select('.TableContent p'):
            text = para.get_text().strip()
            if ":" in text:
                key, value = map(str.strip, text.split(":", 1))
                details[key] = value

        # Return extracted details
        if details:
            return details
        else:
            raise ValueError("No details found for the given roll number.")

    else:
        raise requests.RequestException(f"Failed to fetch details for roll number {ROLL_NUMBER}.")
    
def get_student_image(username, roll=000000):
    """
    Fetch student image from IITK OA website for the given username.
    :param username: The username to fetch image for
    Note that email = username + "@iitk.ac.in"

    <div style="width: 200px; height: 200px; position: relative; border-radius: 100%; flex-shrink: 0; background-image: url(&quot;https://home.iitk.ac.in/~shivanshg23/dp&quot;), 
    url(&quot;https://oa.cc.iitk.ac.in/Oa/Jsp/Photo/230976_0.jpg&quot;), url(&quot;/_next/static/media/GenericMale.592f9e48.png&quot;); background-position: center top; background-size: cover;"></div>
    """
    # Define the URL to fetch the student image
    url = f"https://home.iitk.ac.in/~{username}/dp"

    # Send request to fetch the image
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Open the image using PIL
        image = Image.open(BytesIO(response.content))
        return image
    else:
        response = requests.get(f"https://oa.cc.iitk.ac.in/Oa/Jsp/Photo/{roll}_0.jpg")
        if response.status_code == 200:
            # Open the image using PIL
            image = Image.open(BytesIO(response.content))
            return image
        else:
            print(f"Failed to fetch image for {username}.....")
            default_image = Image.new("RGB", (150, 150), (200, 200, 200))  # Placeholder gray image
            return default_image

def get_student(roll_number):
    """
    Fetch student details and image from IITK OA website for the given roll number.
    :param roll_number: The roll number to fetch details and image for
    """
    # Fetch student details
    details = get_student_details(roll_number)
    
    # Fetch student image
    details['username'] = details['E-Mail'].split('@')[0]
    image = get_student_image(details['username'], roll_number)
    
    return details, image

def generate_student_card(roll_number):

    # Need improvement
    
    # Define card size
    card_width, card_height = 500, 300
    background_color = (255, 255, 255)  # White background
    
    # Create a blank image
    card = Image.new("RGB", (card_width, card_height), background_color)
    draw = ImageDraw.Draw(card)

    # Fetch student details and image
    details, profile_img = get_student(roll_number)
    name = details['Name']
    program = details['Program']
    department = details['Department']
    hostel = details['Hostel Info'] 
    email = details['E-Mail']
    blood_group = details['Blood Group']
    gender = details['Gender'][0]

    # Load profile picture
    profile_max_size = (200, 200)
    profile_img.thumbnail(profile_max_size, Image.Resampling.LANCZOS)  


    # Paste profile picture
    card.paste(profile_img, (30, 30))

    # Load font (Ensure you have a .ttf font file available)
    try:
        font = ImageFont.truetype("Fonts/Courier.ttf", 15)  # Adjust font path if needed
    except:
        font = ImageFont.load_default()

    # Text color
    text_color = (0, 0, 0)

    # Student details text
    text_x = 200
    text_y = 30
    line_spacing = 40

    details = [
        f"Name: {name}",
        f"Program: {program}",
        f"Department: {department}",
        f"Hostel: {hostel}",
        f"E-Mail: {email}",
        f"Blood Group: {blood_group}",
        f"Gender: {gender}",
    ]

    for detail in details:
        draw.text((text_x, text_y), detail, font=font, fill=text_color)
        text_y += line_spacing

    return card

