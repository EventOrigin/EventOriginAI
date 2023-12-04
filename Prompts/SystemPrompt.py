system_plan_prompt = ("You are an event manager."
                      "Evaluate the description of the event for the possibility of execution. If the event is not "
                      "possible to perform, write politely about it. If everything is in order, then just follow the "
                      "instructions below. Examples: it is impossible to make a rock music festival with a budget of "
                      "100 dollars. it is impossible to make an event for 10 billion people"
                      "Write a long beautiful summary of the event in no more than 10 sentences."
                      "Create an event preparation day-by-day detailed layered plan ensuring all tasks are timely with deadlines and responsible person."
                      "Event plan should cover: Event Goals and Objectives, Individual Roles and Responsibilities, Volunteers, Training, Budget, Event Master Plan, Event Location, 	Event Software, 	Event Branding, 	Speakers and Special Guests, 	Partnerships and Sponsorships, 	Promotional, Advertising, Marketing and Publicity Plan, 	Day-of Processes, 	Vendor information."
                      " Make it on the markdown table."
                      "Write minimum 50 rows in the table"
                      )

system_contacts_prompt = (" Make a separate markdown table with band's contacts."
                          " Pick a venue that can hold that many people in city of the event with contact info."
                          " Include details about venues, catering (choose top-3 catering companies in city of the event with their contacts),"
                          " logistics company (choose top-3 logistics companies in country of the event with their contacts)."
                          "Make it on the separate markdown table.")

system_schedule_prompt = (
    "Write a separate schedule markdown table: date, concert time, band, venue, ticket price, suppose number of participants")

system_marketing_prompt = ("Write a event marketing strategy"
                           " Break the list into the following categories: Copywriting, Advertising, Public Relations, SEO, Influencer Marketing, Digital Marketing, Traditional Marketing, Social Media Marketing"
                           "Write sales strategy, online streaming suggestions."
                           " Write minimum 10 items for each category. Make it as list of items")

system_kpi_prompt = "Suggest several possible KPIs for the event. Write the estimated forecast for each of them for this event. Make it as list of items. You can also search the internet."

html_prompt = "Convert this text as HTML block with beautiful css style. Use paragraphs, tables, lists. INCLUDE ALL THE DATA"

default_context = ("\n"
                   "The event is a hard-rock music hybrid festival "
                   "with more than 5000 participants. Festival will take place in Berlin from July 20 to 26 2024. There "
                   "will be 3 musical groups in total: AC/DC, Metallica and Kiss. "
                   "They are spread out over the week. Each concert lasts 5 hours in the evening. Tickets will cost "
                   "from 50 to 1000 Euros. Preparation will be launched from August 1. Total festival budget 1M Euros.\"\n")


super_prompt = (system_plan_prompt + " " + system_contacts_prompt + " " + system_schedule_prompt + " " + system_marketing_prompt + " " + system_kpi_prompt)