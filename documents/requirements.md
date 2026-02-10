# Requirements

## Description of the process adopted for requirements elicitation
## Mockup(s) of the app (just most relevant ones)

## User Stories

### Persona 1: The Daily Commuter
 
Name: Sean O'Connor
 
Background: 28 years old, IT Consultant working in Dublin City Centre, living in Rathmines.

User Story: As a time-pressed commuter, I want to see real-time bike and dock availability directly on the map so that I don't waste time walking to an empty station.
 
Goals: Cycles from home to the office every morning to avoid morning rush hour traffic. Needs to quickly locate stations that definitely have bikes available.

### Persona 2: The One-Time Tourist
 
Name: Maria Garcia
 
Background: 24 years old, a backpacker from Spain spending the weekend in Dublin.

User Story: As a short-term tourist, I want to buy a "One-Day Pass" via mobile payment so that I can use the system immediately without a long-term subscription.
 
Goals: Wants to cycle to explore Phoenix Park and sightseeing spots along the river. Wants to pay once or pay-per-day and does not want to register for a long-term membership.

### Persona 3: The Budget Student
 
Name: Liam Byrne
 
Background: 19 years old, First-year student (Fresher) at UCD.

User Story: As a budget-conscious student, I want to see my account balance and active discounts on my dashboard so that I can manage my cycling expenses.
 
Goals: Wants to save money. Mainly uses the bikes to commute across campus or to travel from his apartment to the supermarket.

## Acceptance Criteria

### Standard Login Validation

Given: button on the upper right corner:

If not login yet, show “Login/Sign up”

    If press ‘login’, let user input email and password
    If press ‘Sign up’, let user input email, password and confirm pass word
        If email has been registered, report to user
        If len(password) <8 or only digits, report to user
        If confirmed password is not the same, report
        If no problem, automatically go to login page
    If they enter their registered email and password and tap "Login",
        Then the system shall verify the credentials and redirect the user to the Map Home Page.
            If they provide a valid email and create a password
                Then the system shall create their account and display a "Welcome" onboarding message.
            Else let user reenter


        

