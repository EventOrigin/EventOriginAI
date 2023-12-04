from kor import Object
from kor.nodes import Object, Text, Number

bands = Object(
    id="bands",
    attributes=[
        Text(id="title")
    ],
    isMany=True
)

event = Object(
    id="event",
    description="Event model",
    attributes=[
        Text(id="date"),
        Text(id="country"),
        Text(id="city"),
        Text(id="participants"),
        bands
    ],
    examples=[
        (
            "\n"
           "The event is a hard-rock music hybrid festival "
           "with less than 20000 participants. Festival will take place in Warsaw from Mar 15 to 22 2024. There "
           "will be next musical groups in total: AC/DC, Guns N' Roses, "
           "Deep Purple. "
           "They are spread out over the week. Each concert lasts 5 hours in the evening. Tickets will cost "
           "from 50 to 1000 Euros. Preparation will be launched from Sep 1. Total festival budget 1M Euros.\"\n",
            {
                "date": "Mar 15 2024",
                "country": "Poland",
                "city": "Warsaw",
                "participants": "20000",
                "bands": [{"title": "AC/DC"}, {"title": "Guns N' Roses"}, {"title": "Deep Purple"}]
            },
        )
    ],
    many=False,
)

schedule = Object(
    id="schedule",
    description="Event schedule",
    attributes=[
        Text(id="date"),
        Text(id="concert_time"),
        Text(id="band"),
        Text(id="venue"),
        Text(id="ticket_price"),
        Number(id="participants"),
    ],
    examples=[
        (
            "| Dec 20 2023 | 6pm-11pm      | Aerosmith         | Arena   | 50-500             | 7000                      |",
            {
                "date": "Dec 20 2023",
                "concert_time": "6pm-11pm",
                "band": "Aerosmith",
                "venue": "Arena",
                "ticket_price": "50-500 EUR",
                "participants": 7000,
            },
        )
    ],
    many=True,
)

timeline = Object(
    id="timeline",
    description="Timeline",
    attributes=[
        Text(id="stage"),
        Text(id="date"),
        Text(id="task"),
        Text(id="deadline"),
        Text(id="responsible_person"),
    ],
    examples=[
        (
            "| Aug 1 2023  | Kick-off meeting and event planning discussion  | Event Manager      |  Aug 20 2023     |",
            {
                "stage": "Before start",
                "date": "Aug 1 2023",
                "task": "Kick-off meeting and event planning discussion",
                "deadline": "Aug 20 2023",
                "responsible_person": "Event manager",
            },
        )
    ],
    many=True,
)

contacts = Object(
    id="contacts",
    description="Contacts",
    attributes=[
        Text(id="category"),
        Text(id="title"),
        Text(id="contact_name"),
        Text(id="email"),
        Text(id="telephone"),
        Text(id="address"),
        Text(id="website"),
    ],
    examples=[
        (
            """### Band Contact Email:
                - AC/DC: acdc@music.com
                
                The contact information for Axica Berlin is as follows:
                - Telephone: +49 30 2000860
                - Address: Pariser Platz 3, 10117 Berlin, Germany
                - Website: www.axica.de""",
            [{
                "category": "Bands",
                "title": "AC/DC",
                "contact_name": "",
                "email": "acdc@acdc.com",
                "telephone": "",
                "address": "",
                "website": ""
            },
            {
                "category": "Venue",
                "title": "Axica Berlin",
                "contact_name": "",
                "email": "",
                "telephone": "+49 30 2000860",
                "address": "Pariser Platz 3, 10117 Berlin, Germany",
                "website": "www.axica.de"
            }
            ]
        ),
    ]
)

eventPlan = Object(
    id="event_plan",
    description=(
        "Professional event plan"
    ),
    attributes=[
        Text(
            id="overview",
            description="Event description",
            example="The festival will take place in Berlin from December 20 to 26, 2023. There will be 10 musical "
                    "groups in total: AC/DC, Guns N' Roses, Metallica, Led Zeppelin, Black Sabbath, Deep Purple, "
                    "Van Halen, Aerosmith, Iron Maiden, and Kiss. Metallica will perform at the end of the festival, "
                    "and the others will be spread out over the week. Each concert will last 5 hours in the evening, "
                    "and tickets will cost from 50 to 1000 Euros. The festival budget is 1M Euros."
        ),
        schedule,
        timeline,
        contacts
    ],
)