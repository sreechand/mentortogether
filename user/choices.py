
AC_STATE_CHOICES = (
    ( u'Activation', u'Activation' ),
    ( u'Pending', u'Pending' ),
    ( u'Approved', u'Approved' ),
    ( u'Banned', u'Banned' )
)

ACCOUNT_TYPE_CHOICES = (
    ( u'Mentor', u'Mentor' ),
    ( u'Mentee', u'Mentee' )
)

OCCUPATION_FUNCTIONALITY_AREAS = (
    u"Accounts / Finance / Tax / CS / Audit",
    u"Agent",
    u"Architecture / Interior Design",
    u"Banking / Insurance",
    u"Content / Journalism",
    u"Corporate Planning / Consulting",
    u"Engineering Design / R&D",
    u"Export / Import / Merchandising",
    u"Fashion / Garments / Merchandising",
    u"Guards / Security Services",
    u"Hotels / Restaurants",
    u"HR / Administration / IR",
    u"IT Software - Client Server",
    u"IT Software - Mainframe",
    u"IT Software - Middleware",
    u"IT Software - Mobile",
    u"IT Software - Other",
    u"IT Software - System Programming",
    u"IT Software - Telecom Software",
    u"IT Software - Application Programming / Maintenance",
    u"IT Software - DBA / Datawarehousing",
    u"IT Software - E-Commerce / Internet Technologies",
    u"IT Software - Embedded / EDA / VLSI / ASIC /Chip Des.",
    u"IT Software - ERP / CRM",
    u"IT Software - Network Administration / Security",
    u"IT Software - QA & Testing",
    u"IT Software - Systems / EDP / MIS",
    u"IT Hardware - / Telecom / Technical Staff / Support",
    u"ITES / BPO / KPO / Customer Service / Operations",
    u"Legal",
    u"Marketing / Advertising / MR / PR",
    u"Packaging",
    u"Pharma / Biotech / Healthcare / Medical / R&D",
    u"Production / Maintenance / Quality",
    u"Purchase / Logistics / Supply Chain",
    u"Research",
    u"Sales / BD",
    u"Secretary / Front Office / Data Entry",
    u"Self Employed / Consultants",
    u"Site Engineering / Project Management",
    u"Teaching / Education",
    u"Ticketing / Travel / Airlines",
    u"Top Management",
    u"TV / Films / Production",
    u"Web / Graphic Design / Visualiser",
    u"Other",
)

OCCUPATION_INDUSTRIES = (
    u"Accounting/Finance",
    u"Advertising/PR/MR/Events",
    u"Agriculture/Dairy",
    u"Architecture/Interior Designing",
    u"Auto/Auto Ancillary",
    u"Banking/Financial Services/Broking",
    u"BPO/ITES",
    u"Chemicals/PetroChemical/Plastic/Rubber",
    u"Construction/Engineering/Cement/Metals",
    u"Consumer Durables",
    u"Courier/Transportation/Freight",
    u"Defence/Government",
    u"Education/Teaching/Training",
    u"Export/Import",
    u"Fertilizers/Pesticides",
    u"FMCG/Foods/Beverage",
    u"Fresher/Trainee",
    u"Gems & Jewellery",
    u"Hotels/Restaurants/Airlines/Travel",
    u"Industrial Products/Heavy Machinery",
    u"Insurance",
    u"IT-Software/Software Services",
    u"IT-Hardware & Networking",
    u"Telcom/ISP",
    u"Legal",
    u"Media/Dotcom/Entertainment",
    u"Medical/Healthcare/Hospital",
    u"NGO/Social Services",
    u"Office Equipment/Automation",
    u"Oil and Gas/Power/Infrastructure/Energy",
    u"Paper",
    u"Pharma/Biotech/Clinical Research",
    u"Printing/Packaging",
    u"Recruitment",
    u"Retail",
    u"Security/Law Enforcement",
    u"Semiconductors/Electronics",
    u"Shipping/Marine",
    u"Textiles/Garments/Accessories",
    u"Tyres",
    u"Other",
)

EDUCATION_DEGREES = (
    u"BA",
    u"BA Hons",
    u"BAcc Hons",
    u"BCom",
    u"BCA",
    u"BEd",
    u"BEng",
    u"BEng Hons",
    u"BPharm",
    u"BPhil",
    u"BSc",
    u"BSc Hons",
    u"BTech",
    u"Diploma",
    u"Doctorat",
    u"Doktor",
    u"DPhil",
    u"DRS",
    u"EngD",
    u"LLB",
    u"LLM",
    u"LPC",
    u"MA",
    u"MA Hons",
    u"MASc",
    u"Master",
    u"MBA",
    u"MBBS",
    u"MCA",
    u"MChem",
    u"MComp",
    u"MD",
    u"MEng",
    u"MLitt",
    u"MMath",
    u"MPharm",
    u"MPhil",
    u"MPhys",
    u"MR",
    u"MSc",
    u"MSci",
    u"MTech",
    u"Other",
    u"PGCE",
    u"PGdip",
    u"PhD"
)

EDUCATION_MAJORS = (
    u"Accountancy",
    u"Actuarial Science",
    u"Agriculture",
    u"American Studies",
    u"Anatomy/Physiology/Genetics",
    u"Archaeology",
    u"Architecture",
    u"Art and Design",
    u"Arts",
    u"Biochemistry and Biological Chemistry",
    u"Biochemistry/Biophysics/Biotechnology",
    u"Biology",
    u"Botany",
    u"Building and Surveying",
    u"Business and Management",
    u"Chemistry",
    u"Cinematics - Film, TV, Photography",
    u"Classics",
    u"Combined Programmes",
    u"Computer Sciences and IT",
    u"Cultural/Ethnic Studies",
    u"Dentistry",
    u"Drama, Dance and Performance Arts",
    u"Development Studies",
    u"Econometrics",
    u"Economics",
    u"Education Studies",
    u"Engineering - Aeronautical",
    u"Engineering - Automotive",
    u"Engineering - Chemical",
    u"Engineering - Civil",
    u"Engineering - Electrical and Electronic",
    u"Engineering - General",
    u"Engineering - Mechanical and Production",
    u"English",
    u"Environmental Studies, Technology and Oceanography",
    u"European Studies and Languages",
    u"Finance",
    u"Food Science/Technology and Nutrition",
    u"General Science",
    u"Geography",
    u"Geological Sciences",
    u"Health Care and Therapies",
    u"History",
    u"History of Art",
    u"Hotel, Institutional and Recreation Management",
    u"Humanities and Social Sciences",
    u"Languages",
    u"Languages - African, Asian and Oriental",
    u"Languages - Celtic",
    u"Languages - Classical and Ancient",
    u"Languages - East European",
    u"Languages - French",
    u"Languages - German",
    u"Languages - Italian",
    u"Languages - Middle Eastern",
    u"Languages - Russian",
    u"Languages - Scandinavian",
    u"Languages - Spanish/Latin American",
    u"Law",
    u"Librarianship and Information Science",
    u"Linguistics and Literature",
    u"Marine Sciences and Technologies",
    u"Materials/Minerals Sciences and Technologies",
    u"Mathematics / Statistics",
    u"Media Studies - Communications, Journalism and Publishing",
    u"Medicine",
    u"Microbiology",
    u"Music",
    u"Neuro-Science",
    u"Nursing",
    u"Other",
    u"Pediatrics",
    u"Pharmacy and Pharmacology",
    u"Philosophy",
    u"Physics",
    u"Planning (Town and Country)",
    u"Politics",
    u"Psychology",
    u"Retail",
    u"Social Policy, Social Work and Administration",
    u"Sociology and Anthropology",
    u"Sports Science/Studies",
    u"Teacher Training",
    u"Telecommunications",
    u"Theology",
    u"Tourism",
    u"Women's Studies",
    u"Veterinary Science",
    u"Zoology",
)

CAREER_INTERESTS = (
    u'Applied Arts - Animation',
    u'Applied Arts - Fine Arts',
    u'Applied Arts - Fashion designing',
    u'Applied Arts - Performing Arts',
    u'Commerce - Chartered Accountant',
    u'Commerce - Banking',
    u'Commerce - Insurance',
    u'Engineering - Architecture',
    u'Engineering - Computers',
    u'Engineering - Chemical',
    u'Engineering - Civil',
    u'Engineering - Electrical',
    u'Engineering - Electronics',
    u'Engineering - Information Technology',
    u'Education - Teaching',
    u'Government - Civil Services',
    u'Government - IPS',
    u'Government - State Civil Services',
    u'Government - Railways',
    u'Health and Medicine - Dentistry',
    u'Health and Medicine - Medicine',
    u'Health and Medicine - Nursing',
    u'Health and Medicine - Pharmacy',
    u'Health and Medicine - Veterinary Sciences',
    u'Law',
    u'Management And Business - Entrepreneur',
    u'Management And Business - Sales and Marketing',
    u'Military',
    u'Sports',
    u'Social sciences - Counselling',
    u'Sociel sciences - Social Workers',
    u'Services - Event Management',
    u'Services - Hospitality and Tourism',
    u'Services - Hospital Management',
    u'Services - Journalism',
    u'Services - Media and Entertainment',
)

MENTOR_MATCH_PREFS = (
    u"Academic (1st), Career (2nd)",
    u"Career(1st), Academic(2nd)"
)

# ---------------------------------------------------------------------
# Mentee Educational Courses at various levels
MenteePUCCourses = (
    u"Arts",
    u"Science",
    u"Commerce"
)
MenteePUCCourseChoices = [(course, course) for course in MenteePUCCourses]

MenteeDegreeCourses = (
    u"BCom",
    u"BSc",
    u"BA",
    u"BE"
)
MenteeDegreeCourseChoices = [(course, course) for course in MenteeDegreeCourses]

# ---------------------------------------------------------------------
# School Choices
Schools = (
    ( u"Balakiya Bala Mandir" ),
)
SchoolChoices = [ (school, school) for school in Schools ]

# ---------------------------------------------------------------------
# Grade Choices
GradeChoices = (
    ( 8,  u"Secondary School Std. 8" ),
    ( 9,  u"Secondary School Std. 9" ),
    ( 10, u"Secondary School Std. 10" ),
    ( 11, u"Pre-University College - 1st Yr" ),
    ( 12, u"Pre-University College - 2nd Yr" ),
    ( 13, u"College Degree - 1st Yr" ),
    ( 14, u"College Degree - 2nd Yr" ),
    ( 15, u"College Degree - 3rd Yr" ),
    ( 16, u"College Degree - 4th Yr" ),
)

# ---------------------------------------------------------------------
# Mentor Roles For Mentees: List of possible roles that a Mentor can 
# play.
MentorRoles = (
    u"Improve Spoken and Written English",
    u"Improve Computer Skills",
    u"Broaden Knowledge of Academic and Career Choices",
    u"Impart Training on Communication Skills",
    u"Impart Training on Decision Making and Critical Thinking Skills",
    u"Impart Training on Self Esteeem, Self Awareness and Goal-setting Skills",
    u"Impart Training on Managing Time and Stress",
    u"Other"
)
MentorRoleChoices = [(r, r) for r in MentorRoles]



MENTOR_MATCH_PREF_CHOICES = [ ( x,x ) for x in MENTOR_MATCH_PREFS ]

OCCUPATION_FUNCTIONALITY_AREA_CHOICES = [ ( x,x ) for x in OCCUPATION_FUNCTIONALITY_AREAS ]

OCCUPATION_INDUSTRY_CHOICES = [ ( x,x ) for x in OCCUPATION_INDUSTRIES ]

EDUCATION_DEGREE_CHOICES = [ ( x,x ) for x in EDUCATION_DEGREES ]

EDUCATION_MAJOR_CHOICES = [ ( x,x ) for x in EDUCATION_MAJORS ]

PREUNIV_DISCIPLINE_CHOICES = ( ( u'Science', u'Science' ),
                               ( u'Arts', u'Arts' ),
                               ( u'Commerce', u'Commerce' ) )
   
CAREER_INTEREST_CHOICES = [ (x,x) for x in CAREER_INTERESTS ] 

SKILL_SCORE_CHOICES = ( ( 1, u'1' ),
                        ( 2, u'2' ),
                        ( 3, u'3' ),
                        ( 4, u'4' ),
                        ( 5, u'5' ) )


GENDER_CHOICES = ( ( u'Male', u'Male' ),
                   ( u'Female', u'Female' ) )

ROLE_CHOICES = ( ( u'mentor', u'Mentor' ),
                 ( u'mentee', u'Mentee' ),
                 ( u'subscriber', u'subscriber' ) )
