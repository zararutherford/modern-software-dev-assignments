# Week 8 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **Zara Rutherford** \
SUNet ID: 06625318 \
Citations: Bolt.new, Claude 

This assignment took me about 1 hours to do. 


## App Concept
```
Immigration Client CRM - A client relationship management system designed for immigration
attorneys to track and manage their clients' immigration cases. The app allows attorneys to
create, view, update, and delete client records including personal information (name, email,
phone, country of origin), case details (case number, visa type, current status), and important
dates (filing date, priority date). Each client record can track various visa types (H-1B, L-1,
O-1, EB-1/2/3, F-1, Green Card, Citizenship, Asylum) and case statuses (Initial Consultation,
Documents Gathering, Application Prep, Filed, RFE, Approved, Denied, Withdrawn). The app also
supports notes for each client case.
```


## Version #1 Description
```
APP DETAILS:
===============
Folder name: immigration-crm-bolt
AI app generation platform: Bolt.new
Tech Stack: React + Vite frontend, Node.js/Express backend, SQLite database
Persistence: SQLite (file-based database)
Frameworks/Libraries Used: React 18, Express 4, better-sqlite3, Lucide React (icons)

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them:
   - Bolt initially created the app with in-memory storage, had to prompt it to add persistence
   - The initial UI wasn't styled great, asked Bolt to improve the design with better colors
   - Case number uniqueness wasn't enforced at first, had to ask for database constraints
   - Resolved by iteratively prompting Bolt to make specific improvements

b. Prompting (e.g. what required additional guidance; what worked poorly/well):
   - Worked well: Describing the domain (immigration law) and specific visa types
   - Worked well: Asking for modern UI with cards and proper forms
   - Needed guidance: Had to explicitly ask for persistent storage vs in-memory
   - Needed guidance: Form validation wasn't added initially, had to request it
   - Overall Bolt understood the CRUD requirements quickly and generated clean code

c. Approximate time-to-first-run and time-to-feature metrics:
   - First working prototype: ~5 minutes
   - Adding persistence: ~3 minutes
   - UI improvements and validation: ~10 minutes
   - Total time from start to fully functional: ~20 minutes
```

## Version #2 Description
```
APP DETAILS:
===============
Folder name: immigration-crm-django
AI app generation platform: Claude Code (manual coding with AI assistance)
Tech Stack: Django 5.0 (Python), Django Templates, SQLite
Persistence: SQLite with Django ORM
Frameworks/Libraries Used: Django 5.0, python-dotenv

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them:
   - Initially forgot to add clients app to INSTALLED_APPS, got migration errors
   - Had to remember Django's form rendering syntax in templates
   - Date inputs needed proper widget configuration for HTML5 date pickers
   - Resolved by checking Django docs and using proper ModelForm configuration
   - Virtual environment setup was straightforward but had to remember activation

b. Prompting (e.g. what required additional guidance; what worked poorly/well):
   - This was manually coded rather than AI-generated like Bolt
   - Used Claude Code to write models, views, forms, and templates
   - Claude was helpful for generating the boilerplate Django structure
   - Had to be specific about wanting function-based views vs class-based
   - Django admin integration was easy to set up with decorator syntax

c. Approximate time-to-first-run and time-to-feature metrics:
   - Project setup and models: ~15 minutes
   - Views and URL routing: ~10 minutes
   - Templates and styling: ~25 minutes
   - Testing and fixes: ~10 minutes
   - Total time: ~60 minutes
```

## Version #3 Description
```
APP DETAILS:
===============
Folder name: immigration-crm-mern
AI app generation platform: Claude Code (manual coding with AI assistance)
Tech Stack: MongoDB, Express, React, Node.js (MERN)
Persistence: MongoDB with Mongoose ODM
Frameworks/Libraries Used: React 18, Vite, Express 4, Mongoose 8, Axios, CORS

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them:
   - Setting up MongoDB locally can be tricky, documented both local and Atlas options
   - CORS configuration needed for frontend-backend communication
   - Date handling between frontend and backend required careful formatting
   - State management in React for switching between list/detail/form views
   - Resolved with proper proxy configuration in Vite and RESTful API design

b. Prompting (e.g. what required additional guidance; what worked poorly/well):
   - Claude Code helped generate the full-stack structure quickly
   - Had to specify wanting separate client/server folders
   - React component structure needed to be thought through for state management
   - API service layer pattern worked well for separating concerns
   - Mongoose schema validation aligned nicely with frontend form validation

c. Approximate time-to-first-run and time-to-feature metrics:
   - Backend API setup: ~20 minutes
   - MongoDB schema and routes: ~15 minutes
   - React components and forms: ~35 minutes
   - Styling and UI polish: ~15 minutes
   - Total time: ~85 minutes
   Note: Requires MongoDB running separately which adds setup time
```
