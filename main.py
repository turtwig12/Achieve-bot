import requests
from bs4 import BeautifulSoup
from time import sleep
import asyncio
from concurrent.futures import ThreadPoolExecutor

#note if you have a browser open with achieve stuff on it some stuff may act unusual


#starts the session making sure stay logged in for the whole presses


#Gets the token to login
# --------------------------------------------------
def function(session):
    print("hi")
    login_url = "https://achieve.hashtag-learning.co.uk/accounts/login/"
    protected_url = "https://achieve.hashtag-learning.co.uk/assess/761/topic/choose-questions/"


    session = requests.Session()

    response = session.get(login_url)

    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

    #logs in
    # --------------------------------------------------
    login_payload = {
        "csrfmiddlewaretoken": csrf_token,
        "login": "username",  # replace with real username
        "password": "password",  # replace with real password
    }

    login_response = session.post(
        login_url,
        data=login_payload,
        headers={
            "Referer": login_url,
            "Origin": "https://achieve.hashtag-learning.co.uk",
            "X-CSRFToken": session.cookies.get("csrftoken"),
            "Content-Type": "application/x-www-form-urlencoded",
        },
        allow_redirects=True,
    )

    if "sessionid" not in session.cookies:
        raise Exception("Login failed")

    #is used later but don't want it in the loop
    def work_out_which_button(correct_answer, one_answer, two_answers, three_answers, page):
        position = 1
        correct = page.find(correct_answer)
        one = page.find(one_answer)
        two = page.find(two_answers)
        three = page.find(three_answers)

        if one < correct:
            position += 1
        if two < correct:
            position += 1
        if three < correct:
            position += 1

        return position

    #Load question selection page
    # --------------------------------------------------
    for x in range(5):
        protected_response = session.get(
            protected_url,
            headers={ "Referer": login_url}
        )

        soup = BeautifulSoup(protected_response.text, "html.parser")
        form = soup.find("form")
        if not form:
            raise Exception("the form to choose the questions does not exist, something has gone badly")

        #Builds the payload to select the questions
        payload = {}

        submit_btn = form.find("button", {"type": "submit"})
        if submit_btn and submit_btn.get("name"):
            payload[submit_btn["name"]] = submit_btn.get("value", "")

        # Override with required values
        payload.update({
            "questions": "3",
            "subject_id": "3",
            "level_id": "5",
        })


        #submits the question selection form
        # --------------------------------------------------
        button_response = session.post(
            protected_url,
            data=payload,
            headers={
                "Referer": protected_url,
                "Origin": "https://achieve.hashtag-learning.co.uk",
                "X-CSRFToken": session.cookies.get("csrftoken"),
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
            allow_redirects=True,
        )

        if button_response.status_code != 200:
            raise Exception("the form to choose the questions does exist, but did not submit with a post:200, so the form did bad thing")


        #Determine what question and button to press
        # --------------------------------------------------

        for i in range(3):
            sleep(2)
            page_text = button_response.text
            if "Which of the following is NOT an environmental benefit to using an intelligent heating system" in page_text:
                question = 1
                button = work_out_which_button(
                    "Switch heating on / off using a timer",
                    "Switch on heating when homeowner is near to the property",
                    "Heating is switched off when everyone leaves the house",
                    "Adapt heating by responding to weather conditions",
                    page_text)
            elif "Which of the following is an environmental benefit to using an intelligent traffic control system" in page_text:
                question = 2
                button = work_out_which_button(
                    "Software, sensors and cameras can be used to reduce traffic flow",
                    "Garage door opens as soon as driver pulls up in driveway",
                    "Road workers can watch traffic and change traffic lights via an app",
                    "Service stations can send deals to drivers phones when they are within a certain radius",
                    page_text)
            elif "Which of the following is an environmental benefit to using an intelligent car management system" in page_text:
                question = 3
                button = work_out_which_button(
                    "Start-stop systems shut down the engine when they detect that the car is stationary",
                    "Car doors unlock automatically as driver gets close to the car",
                    "Driver can use voice control to change audio tracks",
                    "Driver alerts when car is running low on fuel",
                    page_text)
            else:
                raise Exception("The question was not one of the normal 3 Question so was not recognised and caused this error")


            #submits the answer
            # --------------------------------------------------

            cookies = {
                'csrftoken': str(csrf_token),
            }

            headers = {
                "Accept": "application/json, text/javascript, */*; q=0.01",  # Accept JSON/XHR
                "Content-Type": "application/x-www-form-urlencoded",  # Match POST form type
                "Origin": "https://achieve.hashtag-learning.co.uk",  # Required for CSRF/XHR
                "Referer": "https://achieve.hashtag-learning.co.uk/assess/question-page/",  # Required for CSRF/XHR
                "X-CSRFToken": csrf_token,  # MUST match form CSRF
                "X-Requested-With": "XMLHttpRequest",  # Tells server this is an XHR request
            }

            data = {
                'button_value': button,
                'actual_question': question,
                'response_time': '2.103',
                'csrfmiddlewaretoken': csrf_token,
            }

            response = session.post(
                'https://achieve.hashtag-learning.co.uk/assess/mc-button-clicked/',
                cookies=cookies,
                headers=headers,
                data=data,
            )

            if response.status_code!=200:
                raise Exception(f"the question did not come back with status code 200 so bad thing probly happened\n status_code: {response.status_code}")

            if i!=2:
                #gets the next question up
                headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Origin': 'https://achieve.hashtag-learning.co.uk',
                    'Referer': 'https://achieve.hashtag-learning.co.uk/assess/question-page/',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
                    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    # 'Cookie': 'csrftoken=SPwJ5hSCTuidNMfSVqIYBslMcgeERVUY; sessionid=d1p3aivqcj90j2bo7jsigrmgggqjoqf3',
                }

                data = {
                    'csrfmiddlewaretoken': csrf_token,
                    'next': 'next',
                }


                button_response = session.post(
                    'https://achieve.hashtag-learning.co.uk/assess/question-page/',
                    cookies=cookies,
                    headers=headers,
                    data=data,
                )


def chunked(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

def function_batch(batch):
    for b in batch:
        function(b)   # your existing function

executor = ThreadPoolExecutor(max_workers=250)

async def main():
    loop = asyncio.get_running_loop()

    jobs = list(range(1000))
    batches = list(chunked(jobs, 10))  # 10 jobs per worker task

    tasks = [
        loop.run_in_executor(executor, function_batch, batch)
        for batch in batches
    ]

    await asyncio.gather(*tasks)

asyncio.run(main())