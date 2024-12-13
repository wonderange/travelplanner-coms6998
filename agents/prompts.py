from langchain.prompts import PromptTemplate


ZEROSHOT_REACT_INSTRUCTION = """Collect information for a query plan using interleaving 'Thought', 'Action', and 'Observation' steps. Ensure you gather valid information related to transportation, dining, attractions, and accommodation. All information should be written in Notebook, which will then be input into the Planner tool. Note that the nested use of tools is prohibited. 'Thought' can reason about the current situation, and 'Action' can have 8 different types:
(1) FlightSearch[Departure City, Destination City, Date]:
Description: A flight information retrieval tool.
Parameters:
Departure City: The city you'll be flying out from.
Destination City: The city you aim to reach.
Date: The date of your travel in YYYY-MM-DD format.
Example: FlightSearch[New York, London, 2022-10-01] would fetch flights from New York to London on October 1, 2022.

(2) GoogleDistanceMatrix[Origin, Destination, Mode]:
Description: Estimate the distance, time and cost between two cities.
Parameters:
Origin: The departure city of your journey.
Destination: The destination city of your journey.
Mode: The method of transportation. Choices include 'self-driving' and 'taxi'.
Example: GoogleDistanceMatrix[Paris, Lyon, self-driving] would provide driving distance, time and cost between Paris and Lyon.

(3) AccommodationSearch[City]:
Description: Discover accommodations in your desired city.
Parameter: City - The name of the city where you're seeking accommodation.
Example: AccommodationSearch[Rome] would present a list of hotel rooms in Rome.

(4) RestaurantSearch[City]:
Description: Explore dining options in a city of your choice.
Parameter: City – The name of the city where you're seeking restaurants.
Example: RestaurantSearch[Tokyo] would show a curated list of restaurants in Tokyo.

(5) AttractionSearch[City]:
Description: Find attractions in a city of your choice.
Parameter: City – The name of the city where you're seeking attractions.
Example: AttractionSearch[London] would return attractions in London.

(6) CitySearch[State]
Description: Find cities in a state of your choice.
Parameter: State – The name of the state where you're seeking cities.
Example: CitySearch[California] would return cities in California.

(7) NotebookWrite[Short Description]
Description: Writes a new data entry into the Notebook tool with a short description. This tool should be used immediately after FlightSearch, AccommodationSearch, AttractionSearch, RestaurantSearch or GoogleDistanceMatrix. Only the data stored in Notebook can be seen by Planner. So you should write all the information you need into Notebook.
Parameters: Short Description - A brief description or label for the stored data. You don't need to write all the information in the description. The data you've searched for will be automatically stored in the Notebook.
Example: NotebookWrite[Flights from Rome to Paris in 2022-02-01] would store the informatrion of flights from Rome to Paris in 2022-02-01 in the Notebook.

(8) Planner[Query]
Description: A smart planning tool that crafts detailed plans based on user input and the information stroed in Notebook.
Parameters: 
Query: The query from user.
Example: Planner[Give me a 3-day trip plan from Seattle to New York] would return a detailed 3-day trip plan.
You should use as many as possible steps to collect engough information to input to the Planner tool. 

Each action only calls one function once. Do not add any description in the action.

Query: {query}{scratchpad}"""



zeroshot_react_agent_prompt = PromptTemplate(
                        input_variables=["query", "scratchpad"],
                        template=ZEROSHOT_REACT_INSTRUCTION,
                        )

PLANNER_INSTRUCTION = """You are a proficient planner. Based on the provided information and query, please give me a detailed plan, including specifics such as flight numbers (e.g., F0123456), restaurant names, and accommodation names. Note that all the information in your plan should be derived from the provided data. You must adhere to the format given in the example. Additionally, all details should align with commonsense. The symbol '-' indicates that information is unnecessary. For example, in the provided sample, you do not need to plan after returning to the departure city. When you travel to two cities in one day, you should note it in the 'Current City' section as in the example (i.e., from A to B).

***** Example *****
Query: Could you create a travel plan for 7 people from Ithaca to Charlotte spanning 3 days, from March 8th to March 14th, 2022, with a budget of $30,200?
Travel Plan:
Day 1:
Current City: from Ithaca to Charlotte
Transportation: Flight Number: F3633413, from Ithaca to Charlotte, Departure Time: 05:38, Arrival Time: 07:46
Breakfast: Nagaland's Kitchen, Charlotte
Attraction: The Charlotte Museum of History, Charlotte
Lunch: Cafe Maple Street, Charlotte
Dinner: Bombay Vada Pav, Charlotte
Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

Day 2:
Current City: Charlotte
Transportation: -
Breakfast: Olive Tree Cafe, Charlotte
Attraction: The Mint Museum, Charlotte;Romare Bearden Park, Charlotte.
Lunch: Birbal Ji Dhaba, Charlotte
Dinner: Pind Balluchi, Charlotte
Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

Day 3:
Current City: from Charlotte to Ithaca
Transportation: Flight Number: F3786167, from Charlotte to Ithaca, Departure Time: 21:42, Arrival Time: 23:26
Breakfast: Subway, Charlotte
Attraction: Books Monument, Charlotte.
Lunch: Olive Tree Cafe, Charlotte
Dinner: Kylin Skybar, Charlotte
Accommodation: -

***** Example Ends *****

Given information: {text}
Query: {query}
Travel Plan:"""

COT_PLANNER_INSTRUCTION = """You are a proficient planner. Based on the provided information and query, please give me a detailed plan, including specifics such as flight numbers (e.g., F0123456), restaurant names, and hotel names. Note that all the information in your plan should be derived from the provided data. You must adhere to the format given in the example. Additionally, all details should align with common sense. Attraction visits and meals are expected to be diverse. The symbol '-' indicates that information is unnecessary. For example, in the provided sample, you do not need to plan after returning to the departure city. When you travel to two cities in one day, you should note it in the 'Current City' section as in the example (i.e., from A to B). 

***** Example *****
Query: Could you create a travel plan for 7 people from Ithaca to Charlotte spanning 3 days, from March 8th to March 14th, 2022, with a budget of $30,200?
Travel Plan:
Day 1:
Current City: from Ithaca to Charlotte
Transportation: Flight Number: F3633413, from Ithaca to Charlotte, Departure Time: 05:38, Arrival Time: 07:46
Breakfast: Nagaland's Kitchen, Charlotte
Attraction: The Charlotte Museum of History, Charlotte
Lunch: Cafe Maple Street, Charlotte
Dinner: Bombay Vada Pav, Charlotte
Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

Day 2:
Current City: Charlotte
Transportation: -
Breakfast: Olive Tree Cafe, Charlotte
Attraction: The Mint Museum, Charlotte;Romare Bearden Park, Charlotte.
Lunch: Birbal Ji Dhaba, Charlotte
Dinner: Pind Balluchi, Charlotte
Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

Day 3:
Current City: from Charlotte to Ithaca
Transportation: Flight Number: F3786167, from Charlotte to Ithaca, Departure Time: 21:42, Arrival Time: 23:26
Breakfast: Subway, Charlotte
Attraction: Books Monument, Charlotte.
Lunch: Olive Tree Cafe, Charlotte
Dinner: Kylin Skybar, Charlotte
Accommodation: -

***** Example Ends *****

Given information: {text}
Query: {query}
Travel Plan: Let's think step by step. First, """

REACT_PLANNER_INSTRUCTION = """You are a proficient planner. Based on the provided information and query, please give me a detailed plan, including specifics such as flight numbers (e.g., F0123456), restaurant names, and hotel names. Note that all the information in your plan should be derived from the provided data. You must adhere to the format given in the example. Additionally, all details should align with common sense. Attraction visits and meals are expected to be diverse. The symbol '-' indicates that information is unnecessary. For example, in the provided sample, you do not need to plan after returning to the departure city. When you travel to two cities in one day, you should note it in the 'Current City' section as in the example (i.e., from A to B). Solve this task by alternating between Thought, Action, and Observation steps. The 'Thought' phase involves reasoning about the current situation. The 'Action' phase can be of two types:
(1) CostEnquiry[Sub Plan]: This function calculates the cost of a detailed sub plan, which you need to input the people number and plan in JSON format. The sub plan should encompass a complete one-day plan. An example will be provided for reference.
(2) Finish[Final Plan]: Use this function to indicate the completion of the task. You must submit a final, complete plan as an argument.
***** Example *****
Query: Could you create a travel plan for 7 people from Ithaca to Charlotte spanning 3 days, from March 8th to March 14th, 2022, with a budget of $30,200?
You can call CostEnquiry like CostEnquiry[{{"people_number": 7,"day": 1,"current_city": "from Ithaca to Charlotte","transportation": "Flight Number: F3633413, from Ithaca to Charlotte, Departure Time: 05:38, Arrival Time: 07:46","breakfast": "Nagaland's Kitchen, Charlotte","attraction": "The Charlotte Museum of History, Charlotte","lunch": "Cafe Maple Street, Charlotte","dinner": "Bombay Vada Pav, Charlotte","accommodation": "Affordable Spacious Refurbished Room in Bushwick!, Charlotte"}}]
You can call Finish like Finish[Day: 1
Current City: from Ithaca to Charlotte
Transportation: Flight Number: F3633413, from Ithaca to Charlotte, Departure Time: 05:38, Arrival Time: 07:46
Breakfast: Nagaland's Kitchen, Charlotte
Attraction: The Charlotte Museum of History, Charlotte
Lunch: Cafe Maple Street, Charlotte
Dinner: Bombay Vada Pav, Charlotte
Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

Day 2:
Current City: Charlotte
Transportation: -
Breakfast: Olive Tree Cafe, Charlotte
Attraction: The Mint Museum, Charlotte;Romare Bearden Park, Charlotte.
Lunch: Birbal Ji Dhaba, Charlotte
Dinner: Pind Balluchi, Charlotte
Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

Day 3:
Current City: from Charlotte to Ithaca
Transportation: Flight Number: F3786167, from Charlotte to Ithaca, Departure Time: 21:42, Arrival Time: 23:26
Breakfast: Subway, Charlotte
Attraction: Books Monument, Charlotte.
Lunch: Olive Tree Cafe, Charlotte
Dinner: Kylin Skybar, Charlotte
Accommodation: -]
***** Example Ends *****

You must use Finish to indict you have finished the task. And each action only calls one function once.
Given information: {text}
Query: {query}{scratchpad} """

REFLECTION_HEADER = 'You have attempted to give a sub plan before and failed. The following reflection(s) give a suggestion to avoid failing to answer the query in the same way you did previously. Use them to improve your strategy of correctly planning.\n'

REFLECT_INSTRUCTION = """You are an advanced reasoning agent that can improve based on self refection. You will be given a previous reasoning trial in which you were given access to an automatic cost calculation environment, a travel query to give plan and relevant information. Only the selection whose name and city match the given information will be calculated correctly. You were unsuccessful in creating a plan because you used up your set number of reasoning steps. In a few sentences, Diagnose a possible reason for failure and devise a new, concise, high level plan that aims to mitigate the same failure. Use complete sentences.  

Given information: {text}

Previous trial:
Query: {query}{scratchpad}

Reflection:"""

REACT_REFLECT_PLANNER_INSTRUCTION = """You are a proficient planner. Based on the provided information and query, please give me a detailed plan, including specifics such as flight numbers (e.g., F0123456), restaurant names, and hotel names. Note that all the information in your plan should be derived from the provided data. You must adhere to the format given in the example. Additionally, all details should align with common sense. Attraction visits and meals are expected to be diverse. The symbol '-' indicates that information is unnecessary. For example, in the provided sample, you do not need to plan after returning to the departure city. When you travel to two cities in one day, you should note it in the 'Current City' section as in the example (i.e., from A to B). Solve this task by alternating between Thought, Action, and Observation steps. The 'Thought' phase involves reasoning about the current situation. The 'Action' phase can be of two types:
(1) CostEnquiry[Sub Plan]: This function calculates the cost of a detailed sub plan, which you need to input the people number and plan in JSON format. The sub plan should encompass a complete one-day plan. An example will be provided for reference.
(2) Finish[Final Plan]: Use this function to indicate the completion of the task. You must submit a final, complete plan as an argument.
***** Example *****
Query: Could you create a travel plan for 7 people from Ithaca to Charlotte spanning 3 days, from March 8th to March 14th, 2022, with a budget of $30,200?
You can call CostEnquiry like CostEnquiry[{{"people_number": 7,"day": 1,"current_city": "from Ithaca to Charlotte","transportation": "Flight Number: F3633413, from Ithaca to Charlotte, Departure Time: 05:38, Arrival Time: 07:46","breakfast": "Nagaland's Kitchen, Charlotte","attraction": "The Charlotte Museum of History, Charlotte","lunch": "Cafe Maple Street, Charlotte","dinner": "Bombay Vada Pav, Charlotte","accommodation": "Affordable Spacious Refurbished Room in Bushwick!, Charlotte"}}]
You can call Finish like Finish[Day: 1
Current City: from Ithaca to Charlotte
Transportation: Flight Number: F3633413, from Ithaca to Charlotte, Departure Time: 05:38, Arrival Time: 07:46
Breakfast: Nagaland's Kitchen, Charlotte
Attraction: The Charlotte Museum of History, Charlotte
Lunch: Cafe Maple Street, Charlotte
Dinner: Bombay Vada Pav, Charlotte
Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

Day 2:
Current City: Charlotte
Transportation: -
Breakfast: Olive Tree Cafe, Charlotte
Attraction: The Mint Museum, Charlotte;Romare Bearden Park, Charlotte.
Lunch: Birbal Ji Dhaba, Charlotte
Dinner: Pind Balluchi, Charlotte
Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

Day 3:
Current City: from Charlotte to Ithaca
Transportation: Flight Number: F3786167, from Charlotte to Ithaca, Departure Time: 21:42, Arrival Time: 23:26
Breakfast: Subway, Charlotte
Attraction: Books Monument, Charlotte.
Lunch: Olive Tree Cafe, Charlotte
Dinner: Kylin Skybar, Charlotte
Accommodation: -]
***** Example Ends *****

{reflections}

You must use Finish to indict you have finished the task. And each action only calls one function once.
Given information: {text}
Query: {query}{scratchpad} """

GREEDY_SEARCH_PROMPT = """You are a trip planner using a "Greedy Search" strategy to create travel plans. Based on 
the provided information and query, please give me a detailed plan, including specifics such as flight numbers (e.g., 
F0123456), restaurant names, and accommodation names. Note that all the information in your plan should be derived 
from the provided data. You must adhere to the format given in the example. Additionally, all details should align 
with commonsense. The symbol '-' indicates that information is unnecessary. For example, in the provided sample, 
you do not need to plan after returning to the departure city. When you travel to two cities in one day, you should 
note it in the 'Current City' section as in the example (i.e., from A to B). 

Follow these instructions:

### 1. Transportation:
- For each leg of the trip, retrieve transportation options from the available data.
- Compare the costs of flights, self-driving, and taxis for the specified origin, destination, and date.
- Select the mode with the lowest cost. If multiple options have the same cost, prioritize in this order: flights, self-driving, taxis.
- When selecting flights:
  - Retrieve flight information for the origin and destination cities on the travel date from the flight dataset.
  - Choose the flight with the lowest price and include its flight number, departure time, arrival time, and cost in the plan.
- When selecting self-driving or taxi options:
  - Use the distance and cost data to calculate and compare self-driving and taxi costs.
  - If no valid options are available for all modes, use `'-'` in the plan as a last resort.
  - For days where no inter-city transportation is required, use a placeholder: `'-'`.
- Note the transportation details in the plan, including:
  - Mode of transportation.
  - Origin and destination cities.
  - Duration, distance, and cost (if applicable).

### 2. Meals:
- Retrieve restaurants for each city from the database.
- Sort the restaurants by average cost (ascending) and select the least expensive option for breakfast, lunch, and dinner.
- Try to avoid restaurant being repeated on the same day or across multiple meals.
- If no valid restaurant information is available after all attempts, use `'-'` as a last resort.

### 3. Attractions:
- Retrieve attractions for each city from the database.
- Randomly select one or more attractions from the available list, ensuring variety across days.
- Ensure no attraction is repeated in the same city over the trip duration.
- If no valid attraction information is available after all attempts, use `'-'` as a last resort.

### 4. Accommodations:
- Retrieve accommodations for each city from the database.
- Sort by price (ascending) and select the least expensive option meeting the constraints (e.g., room type, occupancy).
- Reuse accommodations across consecutive days in the same city when possible to reduce costs.
- If no valid accommodation is available after all attempts, use `'-'` as a last resort.

### 5. Daily Plan:
- For each day of the trip:
  - Specify the city where the traveler is staying or transitioning to.
  - Include the transportation details for that day.
  - List breakfast, lunch, and dinner options.
  - Highlight the attraction(s) to visit.
  - Add accommodation details, unless it is the final day of the trip.
- Ensure logical consistency and a cost-effective approach across all components.

### 6. Fallback Strategy:
- Use `'-'` for any component only after all database-driven options have been exhausted.
- Prioritize valid options from the database to avoid excessive `'-'` placeholders.

***** Example *****

Query: Please design a travel plan departing from Las Vegas and heading to Stockton for 3 days, from March 3rd to March 5th, 2022, for one person, with a budget of $1,400.

Travel Plan:
Day 1:
Current City: from Las Vegas to Stockton
Transportation: Flight Number: F3576711, from Las Vegas to Stockton, Departure Time: 06:01, Arrival Time: 07:28
Breakfast: Biaggi's Ristorante Italiano, Stockton
Attraction: Louis Park, Stockton; Buckley Cove Park, Stockton
Lunch: Twin Brothers, Stockton
Dinner: Muffins, Stockton
Accommodation: Private Apt 2BR/1Bath/Kitchen/Parking in OUR HOME, Stockton

Day 2:
Current City: Stockton
Transportation: -
Breakfast: The Blue Tandoor, Stockton
Attraction: Shumway Oak Grove Regional Park, Stockton; Mexican Heritage Center & Gallery, Stockton
Lunch: Nand Bhai Chholey Bhature, Stockton
Dinner: Wok On Fire, Stockton
Accommodation: Private Apt 2BR/1Bath/Kitchen/Parking in OUR HOME, Stockton

Day 3:
Current City: from Stockton to Las Vegas
Transportation: Flight Number: F3576850, from Stockton to Las Vegas, Departure Time: 13:42, Arrival Time: 15:03
Breakfast: Dimsum & Co., Stockton
Attraction: Wat Dhammararam Buddhist Temple, Stockton
Lunch: High Street Kitchen & Bar, Stockton
Dinner: Ovenstory Pizza, Stockton
Accommodation: -

***** Example Ends *****

### Implementation Notes:
- Ensure all decisions align with the user's constraints (e.g., transportation mode, accommodation type).
- Provide a complete plan for all days of the trip, ensuring every day includes all components.
- Avoid repetitive attractions and restaurants while maintaining cost-effectiveness.
- Use `'-'` only when no valid data is available after exhaustive attempts.
- All decisions in this plan are derived from the "Greedy Search" strategy:
  - Transportation was selected based on minimum cost, using a flight in both legs of the trip.
  - Meals were selected by choosing the least expensive available restaurant for each city.
  - Attractions were chosen randomly from the available options to ensure variety.
  - Accommodation was the least expensive option for the city.

Query: {query}
Given information: {text}
Travel Plan:"""

PRIORITIZE_ROOM_RULES_PLANNER_INSTRUCTION = """You are a proficient planner. Based on the provided information and query, please give me a detailed plan, including specifics such as flight numbers (e.g., F0123456), restaurant names, and accommodation names. Note that all the information in your plan should be derived from the provided data. You must adhere to the format given in the example. Additionally, all details should align with commonsense. The symbol '-' indicates that information is unnecessary. For example, in the provided sample, you do not need to plan after returning to the departure city. When you travel to two cities in one day, you should note it in the 'Current City' section as in the example (i.e., from A to B).

If it is impossible to meet all the constraints in the query exactly as specified, use the following hierarchy to guide your decision-making:
1. Non-negotiable constraint: Constraints related to house rules should always be satisfied
2. High priority constraint: Strive to budget constraint unless doing so would violate the non-negotiable constraint
3. Lower priority constraints: Other constraints such as room type can be relaxed to accommodate the above

***** Example *****
Query: Could you create a travel plan for 7 people from Ithaca to Charlotte spanning 3 days, from March 8th to March 14th, 2022, with a budget of $30,200?
Travel Plan:
Day 1:
Current City: from Ithaca to Charlotte
Transportation: Flight Number: F3633413, from Ithaca to Charlotte, Departure Time: 05:38, Arrival Time: 07:46
Breakfast: Nagaland's Kitchen, Charlotte
Attraction: The Charlotte Museum of History, Charlotte
Lunch: Cafe Maple Street, Charlotte
Dinner: Bombay Vada Pav, Charlotte
Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

Day 2:
Current City: Charlotte
Transportation: -
Breakfast: Olive Tree Cafe, Charlotte
Attraction: The Mint Museum, Charlotte;Romare Bearden Park, Charlotte.
Lunch: Birbal Ji Dhaba, Charlotte
Dinner: Pind Balluchi, Charlotte
Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

Day 3:
Current City: from Charlotte to Ithaca
Transportation: Flight Number: F3786167, from Charlotte to Ithaca, Departure Time: 21:42, Arrival Time: 23:26
Breakfast: Subway, Charlotte
Attraction: Books Monument, Charlotte.
Lunch: Olive Tree Cafe, Charlotte
Dinner: Kylin Skybar, Charlotte
Accommodation: -

***** Example Ends *****

Given information: {text}
Query: {query}
Travel Plan:"""

ALLOW_BUDGET_OVERRUN_PROMPT = """You are a proficient planner. Based on the provided information and query, please give me a detailed plan, including specifics such as flight numbers (e.g., F0123456), restaurant names, and accommodation names. Note that all the information in your plan should be derived from the provided data. You must adhere to the format given in the example. Additionally, all details should align with commonsense. The symbol '-' indicates that information is unnecessary. For example, in the provided sample, you do not need to plan after returning to the departure city. When you travel to two cities in one day, you should note it in the 'Current City' section as in the example (i.e., from A to B).

If it is impossible to meet all the constraints in the query exactly as specified, use the following hierarchy to guide your decision-making:
Aim to stay as close to the budget as possible but allow a slight budget overrun (up to 10%) if it helps to meet other constraints. 

***** Example *****
Query: Could you create a travel plan for 7 people from Ithaca to Charlotte spanning 3 days, from March 8th to March 14th, 2022, with a budget of $30,200?
Travel Plan:
Day 1:
Current City: from Ithaca to Charlotte
Transportation: Flight Number: F3633413, from Ithaca to Charlotte, Departure Time: 05:38, Arrival Time: 07:46
Breakfast: Nagaland's Kitchen, Charlotte
Attraction: The Charlotte Museum of History, Charlotte
Lunch: Cafe Maple Street, Charlotte
Dinner: Bombay Vada Pav, Charlotte
Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

Day 2:
Current City: Charlotte
Transportation: -
Breakfast: Olive Tree Cafe, Charlotte
Attraction: The Mint Museum, Charlotte;Romare Bearden Park, Charlotte.
Lunch: Birbal Ji Dhaba, Charlotte
Dinner: Pind Balluchi, Charlotte
Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

Day 3:
Current City: from Charlotte to Ithaca
Transportation: Flight Number: F3786167, from Charlotte to Ithaca, Departure Time: 21:42, Arrival Time: 23:26
Breakfast: Subway, Charlotte
Attraction: Books Monument, Charlotte.
Lunch: Olive Tree Cafe, Charlotte
Dinner: Kylin Skybar, Charlotte
Accommodation: -

***** Example Ends *****

Given information: {text}
Query: {query}
Travel Plan:
"""

ALLOW_BUDGET_OVERRUN_AGGRESSIVE_PROMPT = """
You are a proficient planner. Based on the provided information and query, please give me a detailed plan, including specifics such as flight numbers (e.g., F0123456), restaurant names, and accommodation names. Note that all the information in your plan should be derived from the provided data. You must adhere to the format given in the example. Additionally, all details should align with commonsense. The symbol '-' indicates that information is unnecessary. For example, in the provided sample, you do not need to plan after returning to the departure city. When you travel to two cities in one day, you should note it in the 'Current City' section as in the example (i.e., from A to B).

Additional Instruction on Budget:
Prioritize meeting all constraints (e.g., budget, room types, transporations, etc). If it is not possible to satisfy all constraints within the given budget, you may exceed the budget by up to 75%, but only do so when it is absolutely necessary to fulfill the other required conditions.

***** Example *****
Query: Could you create a travel plan for 7 people from Ithaca to Charlotte spanning 3 days, from March 8th to March 14th, 2022, with a budget of $30,200?
Travel Plan:
Day 1:
Current City: from Ithaca to Charlotte
Transportation: Flight Number: F3633413, from Ithaca to Charlotte, Departure Time: 05:38, Arrival Time: 07:46
Breakfast: Nagaland's Kitchen, Charlotte
Attraction: The Charlotte Museum of History, Charlotte
Lunch: Cafe Maple Street, Charlotte
Dinner: Bombay Vada Pav, Charlotte
Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

Day 2:
Current City: Charlotte
Transportation: -
Breakfast: Olive Tree Cafe, Charlotte
Attraction: The Mint Museum, Charlotte;Romare Bearden Park, Charlotte.
Lunch: Birbal Ji Dhaba, Charlotte
Dinner: Pind Balluchi, Charlotte
Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

Day 3:
Current City: from Charlotte to Ithaca
Transportation: Flight Number: F3786167, from Charlotte to Ithaca, Departure Time: 21:42, Arrival Time: 23:26
Breakfast: Subway, Charlotte
Attraction: Books Monument, Charlotte.
Lunch: Olive Tree Cafe, Charlotte
Dinner: Kylin Skybar, Charlotte
Accommodation: -

***** Example Ends *****

Given information: {text}
Query: {query}
Travel Plan:
"""

HEURISTIC_PLANNER_PROMPT = """You are a proficient planner. Based on the provided information and query, please give 
me a detailed plan, including specifics such as flight numbers (e.g., F0123456), restaurant names, and accommodation 
names. Note that all the information in your plan should be derived from the provided data. You must adhere to the 
format given in the example. Do not include intermediary steps, explanations, or any process details. Additionally, 
all details should align with commonsense. The symbol '-' indicates that information is unnecessary. For example, 
in the provided sample, you do not need to plan after returning to the departure city. When you travel to two cities 
in one day, you should note it in the 'Current City' section as in the example (i.e., from A to B). 

Utilize a heuristic, forward-looking strategy inspired by recent research on hierarchical reasoning (e.g., 
Tree-of-Thoughts) and best industry practices for complex planning with large language models. Your goal is to 
produce a feasible travel plan that meets all constraints, including budget, accommodations, transportation modes, 
room type and rules, cuisines, and commonsense constraints such as logical city routes and non-repetitive attractions 
or restaurants. 

Follow this strategy:

1. Global Reasoning: Before detailing each day, form a rough global plan. Assess transportation and accommodation 
costs against the budget and minimum nights stay requirements. If certain transportation modes are too expensive, 
consider cheaper alternatives (e.g., self-driving instead of flight) early. If room rules or cuisines are specified, 
ensure the chosen accommodations and dining options can fulfill these constraints from the start. 

2. Heuristic Selection: Start by picking key cost-intensive components (accommodations, long-distance transportation) 
that fit the constraints. If something appears too costly, choose more economical restaurants or shorter taxi routes 
to maintain overall budget feasibility. 

3. Forward-Looking Constraint Handling: Anticipate downstream issues. For example, if a particular day has fewer 
accommodation options meeting the rules, secure a compliant accommodation first so you do not have to revise the 
entire plan later. If certain cuisines are requested, ensure the chosen city’s restaurants support these preferences, 
so you do not need last-minute changes. 

4. Validate All Components: Once you have a global outline, fill in daily transportation, meals, attractions, 
and accommodations. Ensure that no attraction or restaurant is repeated, that the daily plan matches the current 
city, and that you remain within budget. If you encounter a constraint violation, refine earlier choices before 
presenting the final plan. 

5. Use '-' only if no suitable data is available after considering all options. 

**Important Note:**: Ensure every day includes all components, strictly following the example format.

***** Example *****
Query: Could you create a travel plan for 7 people from Ithaca to Charlotte spanning 3 days, from March 8th to March 14th, 2022, with a budget of $30,200?
Travel Plan:
Day 1:
Current City: from Ithaca to Charlotte
Transportation: Flight Number: F3633413, from Ithaca to Charlotte, Departure Time: 05:38, Arrival Time: 07:46
Breakfast: Nagaland's Kitchen, Charlotte
Attraction: The Charlotte Museum of History, Charlotte
Lunch: Cafe Maple Street, Charlotte
Dinner: Bombay Vada Pav, Charlotte
Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

Day 2:
Current City: Charlotte
Transportation: -
Breakfast: Olive Tree Cafe, Charlotte
Attraction: The Mint Museum, Charlotte; Romare Bearden Park, Charlotte.
Lunch: Birbal Ji Dhaba, Charlotte
Dinner: Pind Balluchi, Charlotte
Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

Day 3:
Current City: from Charlotte to Ithaca
Transportation: Flight Number: F3786167, from Charlotte to Ithaca, Departure Time: 21:42, Arrival Time: 23:26
Breakfast: Subway, Charlotte
Attraction: Books Monument, Charlotte.
Lunch: Olive Tree Cafe, Charlotte
Dinner: Kylin Skybar, Charlotte
Accommodation: -
***** Example Ends *****

Given information: {text}
Query: {query}
Travel Plan:"""

BACKTRACKING_PLANNER_PROMPT = """You are a proficient planner. Based on the provided information and query, 
please give me a detailed plan, including specifics such as flight numbers (e.g., F0123456), restaurant names, 
and accommodation names. Note that all the information in your plan should be derived from the provided data. You 
must adhere to the format given in the example and only present the **final refined travel plan**. Do not include 
intermediary steps, explanations, or any process details. Additionally, all details should align with commonsense. 
The symbol '-' indicates that information is unnecessary. For example, in the provided sample, you do not need to 
plan after returning to the departure city. When you travel to two cities in one day, you should note it in the 
'Current City' section as in the example (i.e., from A to B).

Utilize an iterative refinement and backtracking strategy inspired by leading research in large language model 
reasoning (e.g., Reflexion, iterative structured planning). Your goal is to produce a feasible travel plan that meets 
all constraints, including budget, accommodations, transportation modes, room type and rules, cuisines, 
and commonsense constraints such as logical city routes and non-repetitive attractions or restaurants. 

Follow this strategy:

1. Initial Draft: First, construct a complete preliminary plan without worrying if some constraints are slightly 
violated. Include the cities, transportation, accommodations, meals, and attractions as per the user’s query. 

2. Constraint Check: Compare the preliminary plan against all constraints:
   - Budget: If exceeded, reduce costs by choosing cheaper accommodations, less expensive restaurants, or more cost-effective transportation.
   - Room Rules and Types: If violated, pick alternative accommodations that fulfill these requirements.
   - Transportation and Route: If transportation between chosen cities or times is unavailable or illogical, adjust transportation modes or departure/arrival times within the given cities and dates.
   - Cuisine and Commonsense Constraints: If requested cuisines aren’t met, select suitable restaurants. If attractions or restaurants repeat unnecessarily, pick new ones to ensure variety and adherence to commonsense.

3. Backtracking: Modify earlier choices to fix any issues, one by one. For example, if the minimum nights stay is not 
met, swap to a different accommodation that satisfies the requirement even if it changes daily costs. Repeat this 
refinement until all constraints are met or no further improvements are possible. 

4. Finalize: Provide the final revised plan after all necessary adjustments. Use '-' only if no suitable data is 
available even after revisions. 

**Important Note:**: Ensure every day includes all components, strictly following the example format.

***** Example *****
Query: Could you create a travel plan for 7 people from Ithaca to Charlotte spanning 3 days, from March 8th to March 14th, 2022, with a budget of $30,200?
Travel Plan:
Day 1:
Current City: from Ithaca to Charlotte
Transportation: Flight Number: F3633413, from Ithaca to Charlotte, Departure Time: 05:38, Arrival Time: 07:46
Breakfast: Nagaland's Kitchen, Charlotte
Attraction: The Charlotte Museum of History, Charlotte
Lunch: Cafe Maple Street, Charlotte
Dinner: Bombay Vada Pav, Charlotte
Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

Day 2:
Current City: Charlotte
Transportation: -
Breakfast: Olive Tree Cafe, Charlotte
Attraction: The Mint Museum, Charlotte; Romare Bearden Park, Charlotte.
Lunch: Birbal Ji Dhaba, Charlotte
Dinner: Pind Balluchi, Charlotte
Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

Day 3:
Current City: from Charlotte to Ithaca
Transportation: Flight Number: F3786167, from Charlotte to Ithaca, Departure Time: 21:42, Arrival Time: 23:26
Breakfast: Subway, Charlotte
Attraction: Books Monument, Charlotte.
Lunch: Olive Tree Cafe, Charlotte
Dinner: Kylin Skybar, Charlotte
Accommodation: -
***** Example Ends *****

Given information: {text}
Query: {query}
Travel Plan:"""

BACKTRACKING_WITH_PRIORITIZATION_PROMPT = """You are a proficient planner. Based on the provided information and query, 
please give me a detailed plan, including specifics such as flight numbers (e.g., F0123456), restaurant names, 
and accommodation names. Note that all the information in your plan should be derived from the provided data. You 
must adhere to the format given in the example and only present the **final refined travel plan**. Do not include 
intermediary steps, explanations, or any process details. Additionally, all details should align with commonsense. 
The symbol '-' indicates that information is unnecessary. For example, in the provided sample, you do not need to 
plan after returning to the departure city. When you travel to two cities in one day, you should note it in the 
'Current City' section as in the example (i.e., from A to B).

Utilize an iterative refinement and backtracking strategy inspired by leading research in large language model 
reasoning (e.g., Reflexion, iterative structured planning). Your goal is to produce a feasible travel plan that meets 
all constraints, including budget, accommodations, transportation modes, room type and rules, cuisines, 
and commonsense constraints such as logical city routes and non-repetitive attractions or restaurants. 

Follow this strategy:

1. Initial Draft: First, construct a complete preliminary plan without worrying if some constraints are slightly 
violated. Include the cities, transportation, accommodations, meals, and attractions as per the user’s query. 

2. Check constraints and backtracking to adjust: Compare the preliminary plan against all constraints and adjust based on hierarchy defined below.
   - Room Rules and Types: If violated, pick alternative accommodations that fulfill these requirements.
   - Transportations: If transportation mode does not meet requirements, adjust transportation modes.
   - Cuisines: If requested cuisine types are not included, find existing restaurants with duplicated cuisine types and replace them with the restaurants of the requested cuisines.
   - Budget: If exceeded, reduce costs by choosing cheaper accommodations, less expensive restaurants, or more cost-effective transportation. *Only* do this if it does not compromise on the aforementioned constraints, as they have higher priority. If needed, you may exceed budget by at most 75%. 

3. Finalize: Provide the final revised plan after all necessary adjustments. Use '-' only if no suitable data is 
available even after revisions. 

**Important Note:**: Ensure every day includes all components, strictly following the example format.

***** Example *****
Query: Could you create a travel plan for 7 people from Ithaca to Charlotte spanning 3 days, from March 8th to March 14th, 2022, with a budget of $30,200?
Travel Plan:
Day 1:
Current City: from Ithaca to Charlotte
Transportation: Flight Number: F3633413, from Ithaca to Charlotte, Departure Time: 05:38, Arrival Time: 07:46
Breakfast: Nagaland's Kitchen, Charlotte
Attraction: The Charlotte Museum of History, Charlotte
Lunch: Cafe Maple Street, Charlotte
Dinner: Bombay Vada Pav, Charlotte
Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

Day 2:
Current City: Charlotte
Transportation: -
Breakfast: Olive Tree Cafe, Charlotte
Attraction: The Mint Museum, Charlotte; Romare Bearden Park, Charlotte.
Lunch: Birbal Ji Dhaba, Charlotte
Dinner: Pind Balluchi, Charlotte
Accommodation: Affordable Spacious Refurbished Room in Bushwick!, Charlotte

Day 3:
Current City: from Charlotte to Ithaca
Transportation: Flight Number: F3786167, from Charlotte to Ithaca, Departure Time: 21:42, Arrival Time: 23:26
Breakfast: Subway, Charlotte
Attraction: Books Monument, Charlotte.
Lunch: Olive Tree Cafe, Charlotte
Dinner: Kylin Skybar, Charlotte
Accommodation: -
***** Example Ends *****

Given information: {text}
Query: {query}
Travel Plan:
"""


planner_agent_prompt = PromptTemplate(
                        input_variables=["text","query"],
                        template = PLANNER_INSTRUCTION,
                        )

cot_planner_agent_prompt = PromptTemplate(
                        input_variables=["text","query"],
                        template = COT_PLANNER_INSTRUCTION,
                        )

react_planner_agent_prompt = PromptTemplate(
                        input_variables=["text","query", "scratchpad"],
                        template = REACT_PLANNER_INSTRUCTION,
                        )

reflect_prompt = PromptTemplate(
                        input_variables=["text", "query", "scratchpad"],
                        template = REFLECT_INSTRUCTION,
                        )

react_reflect_planner_agent_prompt = PromptTemplate(
                        input_variables=["text", "query", "reflections", "scratchpad"],
                        template = REACT_REFLECT_PLANNER_INSTRUCTION,
                        )

greedy_search_prompt = PromptTemplate(
                        input_variables=["text","query"],
                        template = GREEDY_SEARCH_PROMPT,
                        )

prioritize_room_rules_agent_prompt = PromptTemplate(
                        input_variables=["text","query"],
                        template = PRIORITIZE_ROOM_RULES_PLANNER_INSTRUCTION,
                        )

allow_budget_overrun_prompt = PromptTemplate(
                        input_variables=["text","query"],
                        template = ALLOW_BUDGET_OVERRUN_PROMPT,
                        )

allow_budget_overrun_aggressive_prompt = PromptTemplate(
                        input_variables=["text","query"],
                        template = ALLOW_BUDGET_OVERRUN_AGGRESSIVE_PROMPT,
                        )

heuristic_planner_agent_prompt = PromptTemplate(
                        input_variables=["text","query"],
                        template = HEURISTIC_PLANNER_PROMPT,
                    )

backtracking_planner_agent_prompt = PromptTemplate(
                        input_variables=["text","query"],
                        template = BACKTRACKING_PLANNER_PROMPT,
                    )

backtracking_with_prioritization_prompt = PromptTemplate(
                        input_variables=["text","query"],
                        template = BACKTRACKING_WITH_PRIORITIZATION_PROMPT
                    )