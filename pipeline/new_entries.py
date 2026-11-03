# New listings added in v2 — compact pipe format:
# title|org|category|city|type|mode|edu|salNum|salText|expYears|daysAgo|skills(;)|safe|verified|url|intern
NEW = r"""
Guitar Teacher (home tuition)|Self / direct parents|Music & Performing Arts|Your city|Gig|On-site|any|16000|₹600 / hour|0|1|Acoustic guitar;Music theory;Patience|1|0
Tabla Player – weddings & events|Freelance bookings|Music & Performing Arts|Your city|Gig|On-site|any|15000|₹3,000 / event|2|2|Tabla;Laya;Stage experience|1|0
Piano / Keyboard Teacher|Harmony Music School|Music & Performing Arts|Mumbai|Private|On-site|grad|22000|₹22,000/mo|0|3|Piano;Grade exams;Sight reading|1|1
Vocal Music Teacher (Hindustani)|Sangeet Academy|Music & Performing Arts|Varanasi|Private|On-site|grad|20000|₹20,000/mo|0|4|Hindustani vocal;Raag;Bhatkhande|1|1
Music Therapist|Healing Sounds Centre|Music & Performing Arts|Pune|Private|On-site|pg|30000|₹30,000/mo|1|6|Music therapy;Special needs;Empathy|1|1
Sound Engineer – live events|StageCraft Audio|Music & Performing Arts|Delhi|Private|On-site|dip|28000|₹28,000/mo|1|2|Mixing console;Mics;Live sound|1|1
Recording Studio Assistant|BlueWave Studio|Music & Performing Arts|Kolkata|Private|On-site|any|18000|₹18,000/mo|0|5|DAW basics;Mic setup;Cables|1|0
Dance Teacher – Bollywood|StepUp Dance Studio|Music & Performing Arts|Ahmedabad|Private|On-site|any|20000|₹20,000/mo|0|3|Choreography;Fitness;Kids batches|1|0
Event Anchor / Theatre Artist|EventCraft|Music & Performing Arts|Jaipur|Gig|On-site|any|20000|₹2,500 / event|0|4|Stage presence;Hindi;Improv|1|0
School Music Teacher|Vidya Public School|Music & Performing Arts|Bhopal|Private|On-site|grad|24000|₹24,000/mo|0|7|Music;B.Ed preferred;Choir|1|1

Videographer|Frame Studio|Film & Media|Jaipur|Private|On-site|any|22000|₹22,000/mo|0|2|Camera;Lighting;Editing|1|1
Content Writer|WordWorks Media|Film & Media|Remote|Private|Remote|grad|25000|₹25,000/mo|0|1|English writing;SEO;Research|1|1
Reporter – local news|Jan Sandesh Daily|Film & Media|Lucknow|Private|On-site|grad|22000|₹22,000/mo|0|4|Reporting;Hindi;Field work|1|0
Radio Jockey Assistant|Radio Mirchi Local|Film & Media|Indore|Private|On-site|grad|18000|₹18,000/mo|0|6|Voice;Scripting;Audio editing|1|1
Wedding Photographer (freelance)|Freelance bookings|Film & Media|Your city|Gig|On-site|any|24000|₹4,000 / day|1|3|DSLR;Portraits;Lightroom|1|0
Video Editor – YouTube channel|CreatorHub Media|Film & Media|Remote|Private|Remote|any|25000|₹25,000/mo|0|2|Premiere Pro;Reels;Thumbnails|1|1

2D Animator|AnimHouse|Animation & Gaming|Remote|Private|Remote|any|25000|₹25,000/mo|0|3|Toon Boom;Storyboard;Timing|1|1
3D Artist (Blender)|AnimHouse|Animation & Gaming|Remote|Private|Remote|any|30000|₹30,000/mo|1|4|Blender;Modelling;Texturing|1|1
VFX Compositor|PixelWorks VFX|Animation & Gaming|Mumbai|Private|On-site|grad|32000|₹32,000/mo|1|5|After Effects;Nuke;Rotoscopy|1|1
Game Tester (QA)|PlayForge Studios|Animation & Gaming|Bengaluru|Private|On-site|any|20000|₹20,000/mo|0|6|Game testing;Bug reports;Patience|1|1

Interior Designer|SpaceCraft Interiors|Architecture & Interior|Gurugram|Private|On-site|dip|28000|₹28,000/mo|0|2|AutoCAD;SketchUp;Site visits|1|1
Junior Architect|Studio Aakar|Architecture & Interior|Pune|Private|On-site|grad|30000|₹30,000/mo|0|3|B.Arch;AutoCAD;Working drawings|1|1
AutoCAD Draftsman|Skyline Infra Projects|Architecture & Interior|Noida|Private|On-site|dip|22000|₹22,000/mo|0|5|AutoCAD;Civil drawings;Revision|1|1
Interior Site Supervisor|SpaceCraft Interiors|Architecture & Interior|Gurugram|Private|On-site|dip|25000|₹25,000/mo|1|7|Site supervision;Carpentry;Finishes|1|0

Ayurveda Doctor (BAMS)|AyurCare Clinic|AYUSH|Nagpur|Private|On-site|pg|45000|₹45,000/mo|0|3|BAMS;Panchakarma;Consultation|1|1
Homeopathy Doctor (BHMS)|HomeoHeal Clinic|AYUSH|Bhopal|Private|On-site|pg|40000|₹40,000/mo|0|5|BHMS;Case taking;Counseling|1|1
Naturopathy Therapist|Wellness Retreat|AYUSH|Rishikesh|Private|On-site|dip|25000|₹25,000/mo|0|6|Naturopathy;Diet;Yoga|1|0
Panchakarma Technician|AyurCare Clinic|AYUSH|Nagpur|Private|On-site|dip|20000|₹20,000/mo|0|8|Massage;Steam;Therapy room|1|0
Yoga Instructor|YogaBharat Studio|Sports & Fitness|Your city|Gig|On-site|any|22000|₹700 / session|0|1|Hatha yoga;Pranayama;Group class|1|0

Dental Assistant / Hygienist|SmileCare Dental|Dentistry|Chennai|Private|On-site|dip|20000|₹20,000/mo|0|3|Dental assisting;Sterilisation;X-ray|1|1
Dental Receptionist|SmileCare Dental|Dentistry|Chennai|Private|On-site|12|15000|₹15,000/mo|0|6|Front desk;Appointments;Hindi/English|1|1

Veterinary Field Assistant|Animal Care Trust|Veterinary|Nashik|Private|On-site|dip|22000|₹22,000/mo|0|4|Animal handling;Vaccination;Field visits|1|0
Dairy Vet Assistant|Gokul Dairy|Veterinary|Kolhapur|Private|On-site|dip|20000|₹20,000/mo|0|7|Cattle health;AI;Records|1|1

Hospital Administrator|City Care Hospital|Public Health & Admin|Delhi|Private|On-site|pg|45000|₹45,000/mo|1|2|MHA;Roster;NABH|1|1
Medical Coder (CPC)|CodeMed Solutions|Public Health & Admin|Remote|Private|Remote|grad|28000|₹28,000/mo|0|3|ICD-10;CPT;Coding test|1|1
Pharmacovigilance Associate|Vitalis CRO|Public Health & Admin|Chennai|Private|Hybrid|pg|35000|₹35,000/mo|0|5|Case processing;Argus;MedDRA|1|1
Health Inspector|Municipal Corporation|Public Health & Admin|Pune|Government|On-site|grad|30000|₹30,000/mo|0|6|Sanitation;Field inspection;Report|1|1|https://www.ncs.gov.in

Lab Research Assistant|BioGen Labs|Biotechnology|Hyderabad|Private|On-site|pg|30000|₹30,000/mo|0|3|Cell culture;PCR;Lab safety|1|1
QC Microbiologist|NovaLife Pharma|Biotechnology|Hyderabad|Private|On-site|grad|28000|₹28,000/mo|0|4|Microbiology;Sterility test;GMP|1|1
Bioinformatics Trainee|HelixData Sciences|Biotechnology|Remote|Private|Remote|pg|32000|₹32,000/mo|0|6|Python;R;BLAST|1|0

Penetration Tester (Junior)|ShieldNet Labs|Cyber Security|Bengaluru|Private|Hybrid|grad|50000|₹6.0 LPA|0|2|Burp Suite;OWASP;Linux|1|1
Cyber Forensics Analyst|SecureTrace|Cyber Security|Delhi|Private|On-site|grad|46000|₹5.5 LPA|0|5|FTK;Chain of custody;Reporting|1|1

Cloud Support Associate|CloudNest Systems|IT & Data|Remote|Private|Remote|grad|38000|₹4.5 LPA|0|2|AWS;Linux;Ticketing|1|1
DevOps Trainee|Trellis Systems|IT & Data|Bengaluru|Private|Hybrid|grad|42000|₹5.0 LPA|0|3|Docker;CI/CD;Git|1|1
Mobile App Developer (Flutter)|AppWorks Studio|IT & Data|Remote|Private|Remote|any|42000|₹5.0 LPA|0|4|Flutter;Dart;Play Store|1|0
IT Support / Helpdesk|InfoBridge Services|IT & Data|Indore|Private|On-site|dip|18000|₹18,000/mo|0|6|Windows;Networking;Ticket handling|1|1
Data Science Trainee|Metricly Analytics|IT & Data|Remote|Private|Remote|grad|50000|₹6.0 LPA|0|7|Python;Pandas;ML basics|1|1
AI / ML Intern|Metricly Analytics|IT & Data|Remote|Internship|Remote|grad|15000|₹15,000 stipend|0|1|Python;Scikit-learn;Kaggle|1|1||paid

Drone Pilot – survey|SkyMap Surveys|Drone & Robotics|Jaipur|Private|On-site|dip|30000|₹30,000/mo|0|3|DGCA drone licence;Mapping;GPS|1|1
Robotics Technician|Automate India|Drone & Robotics|Pune|Private|On-site|dip|25000|₹25,000/mo|0|5|Sensors;Arduino;Assembly|1|1
PLC / Automation Engineer|Automate India|Drone & Robotics|Pune|Private|On-site|grad|38000|₹4.5 LPA|0|4|PLC;SCADA;Panel wiring|1|1
EV Technician|VoltAuto Services|Automotive|Bengaluru|Private|On-site|iti|22000|₹22,000/mo|0|6|Battery;BMS;EV safety|1|0
Solar Panel Installer|GreenVolt Energy|Engineering|Indore|Private|On-site|iti|20000|₹20,000/mo|0|7|Panel mounting;Wiring;Height work|1|1

Warehouse Supervisor|QuickShip|Logistics & Supply Chain|Gurugram|Private|On-site|grad|25000|₹25,000/mo|0|3|Inventory;WMS;Team handling|1|1
Delivery Fleet Coordinator|QuickShip|Logistics & Supply Chain|Bengaluru|Private|On-site|grad|26000|₹26,000/mo|0|4|Rostering;Fuel tracking;Excel|1|1
Truck Driver (HMV licence)|TransLink Logistics|Logistics & Supply Chain|Nagpur|Private|On-site|10|28000|₹28,000/mo|2|5|HMV licence;Long route;Fitness|1|1
Supply Chain Trainee|Metro Manufacturing|Logistics & Supply Chain|Pune|Private|On-site|grad|30000|₹3.6 LPA|0|8|Procurement;Excel;Vendor follow-up|1|1

Auto Mechanic (car)|ServicePro Garage|Automotive|Delhi|Private|On-site|iti|22000|₹22,000/mo|1|2|Engine;Diagnostics;Tools|1|1
Two-wheeler Mechanic|BikeCare|Automotive|Patna|Private|On-site|any|18000|₹18,000/mo|0|5|Servicing;Electricals;Punctuality|1|0
Service Advisor|ServicePro Garage|Automotive|Delhi|Private|On-site|grad|24000|₹24,000/mo|0|7|Customer handling;Job cards;Hindi|1|1

Hotel Front Desk Executive|Grand Palm Hotel|Hospitality & Travel|Goa|Private|On-site|grad|22000|₹22,000/mo|0|2|Front office;ID checks;English|1|1
Commi Chef|Grand Palm Hotel|Hospitality & Travel|Goa|Private|On-site|dip|20000|₹20,000/mo|0|3|Kitchen;Hygiene;Shift work|1|1
Housekeeping Supervisor|Grand Palm Hotel|Hospitality & Travel|Goa|Private|On-site|10|18000|₹18,000/mo|0|6|Team;Linen;Checklist|1|1
Travel Consultant|TripCraft Holidays|Hospitality & Travel|Mumbai|Private|On-site|grad|25000|₹25,000/mo|0|4|Itinerary;GDS;Sales|1|1
Local Tour Guide|City Tours Co|Hospitality & Travel|Jaipur|Gig|On-site|any|18000|₹1,200 / tour|0|8|History;Languages;Storytelling|1|0

Cabin Crew|SkyHigh Airways|Aviation|Delhi|Private|On-site|grad|45000|₹45,000/mo|0|3|Height 155cm+;Grooming;English|1|1
Airport Ground Staff|SkyHigh Airways|Aviation|Hyderabad|Private|On-site|12|22000|₹22,000/mo|0|4|Boarding;Baggage;Shift|1|1
Aircraft Maintenance Trainee (AME)|AeroMech Services|Aviation|Chennai|Private|On-site|dip|28000|₹28,000/mo|0|7|AME module;Tools;Safety|1|0

Salon Hair Stylist|Glamour Studio|Beauty & Wellness|Chandigarh|Private|On-site|any|20000|₹20,000/mo|1|2|Cutting;Colour;Blow dry|1|1
Spa Therapist|Wellness Retreat|Beauty & Wellness|Rishikesh|Private|On-site|dip|22000|₹22,000/mo|0|4|Massage;Aroma;Hygiene|1|1
Barber|Glamour Studio|Beauty & Wellness|Chandigarh|Private|On-site|any|18000|₹18,000/mo|1|5|Haircut;Beard;Razors|1|0
Nail Artist|Glamour Studio|Beauty & Wellness|Chandigarh|Private|On-site|any|18000|₹18,000/mo|0|8|Gel nails;Art;Hygiene|1|0

Gym Trainer|FitZone Gym|Sports & Fitness|Delhi|Private|On-site|any|22000|₹22,000/mo|0|2|Certification;Form;Client handling|1|1
Cricket Coach|Victory Sports Academy|Sports & Fitness|Nagpur|Private|On-site|any|25000|₹25,000/mo|2|5|Coaching;Nets;Fitness|1|1
Swimming Instructor|AquaFit Club|Sports & Fitness|Kochi|Private|On-site|any|20000|₹20,000/mo|0|6|Lifesaving;Freestyle;Kids|1|0
Sports Physiotherapist|FitZone Gym|Sports & Fitness|Delhi|Private|On-site|grad|30000|₹30,000/mo|0|4|BPT;Taping;Rehab|1|1

Horticulture Supervisor|GreenFields Farms|Agriculture|Nashik|Private|On-site|dip|22000|₹22,000/mo|0|3|Nursery;Grafting;Irrigation|1|1
Fisheries Field Assistant|AquaFarm Co-op|Agriculture|Kochi|Private|On-site|dip|20000|₹20,000/mo|0|6|Pond mgmt;Feed;Water testing|1|0
Soil Testing Technician|KrishiConnect|Agriculture|Indore|Private|On-site|dip|20000|₹20,000/mo|0|7|Soil kit;Sampling;Reports|1|1

Environment Field Assistant|GreenEarth Foundation|Environment|Dehradun|Private|On-site|grad|22000|₹22,000/mo|0|4|Survey;Data;Field work|1|1
Forest Guard|State Forest Department|Environment|Your state|Government|On-site|12|22000|₹22,000/mo|0|5|Physical test;Forest law;Patrolling|1|1|https://www.ncs.gov.in

Field Social Worker|Aarogya Foundation|Social Work & NGO|Patna|Private|On-site|grad|24000|₹24,000/mo|0|3|Community work;Documentation;Empathy|1|1
NGO Project Coordinator|GreenEarth Foundation|Social Work & NGO|Dehradun|Private|On-site|pg|32000|₹32,000/mo|1|5|MSW;Donor reports;Team|1|1

Clinical Psychology Assistant|MindCare Clinic|Psychology & Counselling|Pune|Private|On-site|pg|30000|₹30,000/mo|0|2|M.A./M.Sc;Assessment;Ethics|1|1
Career Counsellor|PathFinder Guidance|Psychology & Counselling|Remote|Private|Remote|grad|25000|₹25,000/mo|0|4|Counselling;Course mapping;Listening|1|0
School Counsellor|Vidya Public School|Psychology & Counselling|Bhopal|Private|On-site|pg|30000|₹30,000/mo|0|7|RCI / M.A.;Adolescents;Confidentiality|1|1

Dietician|HealthFirst Hospital|Nutrition & Dietetics|Delhi|Private|On-site|pg|32000|₹32,000/mo|0|3|M.Sc Nutrition;Diet plans;Ward rounds|1|1
Nutritionist (clinic)|Wellness Retreat|Nutrition & Dietetics|Rishikesh|Private|On-site|grad|25000|₹25,000/mo|0|6|Diet counselling;Body comp;Follow-up|1|0

Legal Associate|Chambers of R. Menon|Law|Delhi|Private|On-site|grad|30000|₹30,000/mo|0|3|LLB;Drafting;Litigation support|1|1
Paralegal – Corporate|Vertex Legal LLP|Law|Mumbai|Private|Hybrid|grad|25000|₹25,000/mo|0|6|LLB;Compliance;Contract review|1|1
Company Secretary Trainee|Nexus Advisory|Law|Mumbai|Private|On-site|pg|28000|₹28,000/mo|0|8|CS Executive;ROC filing;Minutes|1|0
Legal Content Writer|LawDocs|Law|Remote|Private|Remote|grad|25000|₹25,000/mo|0|9|Legal writing;Research;English|1|0

Tally Operator|Shah & Associates|Commerce & Accounts|Surat|Private|On-site|12|16000|₹16,000/mo|0|4|Tally;Vouchers;Excel|1|1
Audit Assistant|Nexus Advisory|Commerce & Accounts|Mumbai|Private|On-site|grad|22000|₹22,000/mo|0|5|Audit;Excel;Documentation|1|1
CA Articleship (IPCC cleared)|Shah & Associates|Commerce & Accounts|Surat|Internship|On-site|grad|12000|₹12,000 stipend|0|2|Accounts;Tax;Articleship|1|1||paid

Insurance Advisor|LifeSecure Insurance|Banking & Insurance|Your city|Private|On-site|any|18000|₹18,000/mo + commission|0|3|Selling;Trust;Local network|0|1
Loan Processing Officer|FinServe NBFC|Banking & Insurance|Jaipur|Private|On-site|grad|24000|₹24,000/mo|0|5|KYC;Documents;Credit basics|1|1
Microfinance Field Officer|FinServe NBFC|Banking & Insurance|Patna|Private|On-site|grad|22000|₹22,000/mo|0|7|Field visits;Groups;Collection|1|1

Digital Marketing Executive|BrandLoom|Sales & Marketing|Remote|Private|Remote|grad|25000|₹25,000/mo|0|2|Meta Ads;SEO;Analytics|1|1
Field Sales Officer (FMCG)|DailyGoods Distributors|Sales & Marketing|Kanpur|Private|On-site|any|20000|₹20,000/mo + incentive|0|4|Route sales;Retailers;Two-wheeler|1|1
Telecaller|InfoBridge Services|BPO & Customer Support|Indore|Private|On-site|12|15000|₹15,000/mo|0|3|Hindi;Calling;CRM|1|1
Customer Support Executive (voice)|TalkBridge|BPO & Customer Support|Hyderabad|Private|On-site|12|18000|₹18,000/mo|0|2|English;Night shift allowance;Typing|1|1
Chat Support (remote)|TalkBridge|BPO & Customer Support|Remote|Private|Remote|any|16000|₹16,000/mo|0|5|Typing 40wpm;English;Patience|1|1
BPO Team Leader|TalkBridge|BPO & Customer Support|Hyderabad|Private|On-site|grad|30000|₹30,000/mo|2|8|Team handling;SLA;Reports|1|1

Recruitment Consultant|PeopleBridge Services|HR|Gurugram|Private|On-site|grad|26000|₹26,000/mo|0|3|Sourcing;Screening;Follow-up|1|1
Payroll Executive|PeopleBridge Services|HR|Gurugram|Private|Hybrid|grad|24000|₹24,000/mo|0|6|PF/ESI;Excel;Attendance|1|1

Event Coordinator|EventCraft|Event Management|Jaipur|Private|On-site|grad|24000|₹24,000/mo|0|2|Vendor calls;Logistics;Site visits|1|1
Wedding Planner Assistant|EventCraft|Event Management|Jaipur|Private|On-site|any|20000|₹20,000/mo|0|4|Decor;Coordination;Travel|1|0
Sound & Light Technician|StageCraft Audio|Event Management|Delhi|Private|On-site|any|22000|₹22,000/mo|0|6|Speakers;DMX;Setup|1|0

Pre-Primary Teacher (KG)|Little Steps Playschool|Teaching|Pune|Private|On-site|12|16000|₹16,000/mo|0|2|NTT;Kids care;Activity planning|1|1
Special Educator|Vidya Public School|Teaching|Bhopal|Private|On-site|pg|28000|₹28,000/mo|0|5|RCI registration;IEP;Patience|1|1
PET / Sports Teacher|Vidya Public School|Teaching|Bhopal|Private|On-site|grad|22000|₹22,000/mo|0|7|BPEd;Ground drills;Discipline|1|1

Food Technologist Trainee|FreshFoods Pvt Ltd|Food & Dairy|Pune|Private|On-site|grad|28000|₹28,000/mo|0|3|FSSAI;QA;Lab tests|1|1
Dairy Plant Operator|Gokul Dairy|Food & Dairy|Kolhapur|Private|On-site|dip|20000|₹20,000/mo|0|6|Pasteuriser;CIP;Hygiene|1|1
Bakery Assistant|CakeHouse|Food & Dairy|Kochi|Private|On-site|any|16000|₹16,000/mo|0|8|Baking;Decorating;Shift|1|0

Fashion Designer Assistant|Label Meera|Fashion & Textile|Mumbai|Private|On-site|grad|24000|₹24,000/mo|0|3|Illustration;Pattern;Sampling|1|1
Textile Designer|WeaveWorks|Fashion & Textile|Surat|Private|On-site|grad|30000|₹30,000/mo|0|5|Prints;CAD;Fabric knowledge|1|1
Jewellery Designer|GoldCraft Jewellers|Fashion & Textile|Jaipur|Private|On-site|dip|26000|₹26,000/mo|0|7|CAD;Sketching;Stones|1|0

Anganwadi Worker|ICDS (Women & Child Dev)|Government|Your district|Government|On-site|10|12000|₹12,000/mo|0|2|10th pass;Local resident;Community|1|1|https://www.ncs.gov.in
ASHA Worker|National Health Mission|Government|Your district|Government|On-site|10|10000|₹10,000/mo|0|3|10th pass;Village link;Health work|1|1|https://nhm.gov.in
Gram Panchayat Clerk|Gram Panchayat|Government|Your district|Government|On-site|12|18000|₹18,000/mo|0|4|12th pass;Typing;Local language|1|1|https://www.ncs.gov.in
Postman / MTS|India Post|Government|All India|Government|On-site|10|20000|₹20,000/mo|0|5|10th pass;Cycling route;Exam|1|1|https://www.indiapost.gov.in
Court Clerk|District Court|Government|Your district|Government|On-site|grad|22000|₹22,000/mo|0|6|Graduate;Typing;Court procedure|1|1|https://www.ncs.gov.in
Railway NTPC (Ticket Collector)|Railway Recruitment Board|Government|All India|Government|On-site|12|22000|₹22,000/mo|0|4|12th pass;CBT;Medical|1|1|https://www.rrbcdg.gov.in
Home Guard|State Home Department|Defence & Police|Your district|Government|On-site|10|15000|₹15,000/mo|0|7|10th pass;Physical;Local duty|1|1|https://www.ncs.gov.in

Mason (Raj Mistri)|Site contractor|Gig & Local|Your city|Gig|On-site|any|24000|₹900/day|2|1|Brickwork;Plaster;Level|1|0
Gardener (Mali)|Home service|Gig & Local|Your city|Gig|On-site|any|14000|₹500/visit|0|2|Pruning;Watering;Pots|1|0
Cook / Maharaj (home)|Direct households|Gig & Local|Your city|Gig|On-site|any|22000|₹800/day|1|3|Cooking;Hygiene;Menu|1|0
Personal Driver|Direct family|Gig & Local|Delhi|Gig|On-site|10|22000|₹22,000/mo|1|4|LMV licence;Punctual;Local routes|1|1
Packer / Mover|MoveEasy|Gig & Local|Mumbai|Gig|On-site|any|20000|₹700/day|0|5|Lifting;Packing;Team|1|0
Tiffin Service Cook|Self / direct customers|Gig & Local|Pune|Gig|On-site|any|20000|₹20,000/mo|0|6|Bulk cooking;Delivery;Hygiene|1|0
Car Wash Attendant|ServicePro Garage|Gig & Local|Delhi|Gig|On-site|any|14000|₹14,000/mo|0|7|Washing;Polishing;Punctuality|1|0
Farm Labour (seasonal)|Local farms|Gig & Local|Your district|Gig|On-site|any|12000|₹450/day|0|8|Sowing;Harvest;Outdoor|1|0
"""

NEW_WORKERS = r"""
Ravi Sharma|Guitar Teacher|Kothrud, Pune|12|₹600 / hour|0|Acoustic & electric guitar;Chords for beginners;Hindi songs|4.9|180|98••• ••441
Ustad Imran Khan|Tabla Player|Old City, Hyderabad|20|₹3,000 / event|0|Wedding programmes;Laya;Accompanist|4.9|320|99••• ••217
Sister Anita|Piano / Keyboard Teacher|Bandra, Mumbai|9|₹700 / hour|0|Trinity grade prep;Kids;Keyboard|4.8|140|90••• ••663
Vikram Rathore|Wedding Photographer|Jaipur|8|₹4,000 / day|0|Candid;Album;Drone add-on|4.7|260|88••• ••105
Sundar Mistri|Mason (Raj Mistri)|Bhopal|22|₹900 / day|0|Brickwork;Plaster;Tile|4.5|410|93••• ••772
Lakshmi Bai|Cook / Maharaj|Pune|16|₹800 / day|1|Gujarati & Maharashtrian thali;Party cooking|4.8|520|70••• ••316
Rafiq Bhai|Barber|Chandigarh|11|₹150 / cut|0|Home visit haircut;Beard;Kids|4.6|900|96••• ••438
Anjali Nair|Dance Teacher|Kochi|6|₹500 / class|0|Bollywood;Kids batches;Wedding choreography|4.9|95|78••• ••221
"""

NEW_COURSES = r"""
Justin Guitar|Free, structured guitar lessons from beginner to intermediate — one of the best free music resources anywhere.|Completely free, no certificate (your playing is the proof).|https://www.justinguitar.com|Music
Berklee Intro to Music Production (Coursera)|Music production basics from Berklee College of Music — the audit option is free.|Free to audit; certificate costs money.|https://www.coursera.org/learn/music-production|Music
NIELIT|Government IT courses and O/A/B/C level certifications recognised for many government jobs.|Course fees are low but not always free; O/A level exams are paid.|https://www.nielit.gov.in|Government IT
eGyanKosh (IGNOU)|Free study material and video lectures for IGNOU and school-level subjects.|Free to read and download.|https://egyankosh.ac.in|All levels
"""

NEW_REVIEWS = r"""
Harmony Music School, Mumbai|Piano Teacher|4.5|2023–now|Students are genuinely interested and fees are shared fairly. Sunday off is respected.|Evening batches run late; travel between two branches is on you.|1
StageCraft Audio, Delhi|Sound Engineer|3.5|2022–2023|Learned live sound fast — big weddings, big consoles, real experience.|Wedding season means 16-hour days with no overtime pay.|1
Grand Palm Hotel, Goa|Front Desk|2.5|2024|Training was good and the property is clean.|Guests' complaints get taken out on staff. Two female colleagues left after repeated rude behaviour by a senior.|0
"""
