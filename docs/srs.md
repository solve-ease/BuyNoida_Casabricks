​
Preliminary Software Requirements
Specification (SRS)
CasaBricks – Interactive Property Listing
Website (Buy Noida)
​
1. Introduction
1.1 Purpose
This document defines the functional and non-functional requirements for the CasaBricks
(Buy Noida) property listing website.
The system will provide an interactive, AI-enhanced browsing experience for residential and
commercial properties located exclusively in Noida.
The objective is to:
• Replace traditional filter-heavy property search with a guided 3-question flow.
•
•
Improve poor-quality property images using an AI enhancement pipeline.
Present key property information using intuitive visual graphics instead of dense text.
​
1.2 Scope
The platform will:
• Display property listings restricted to Noida.
•
•Allow users to discover properties based on a short questionnaire instead of filters.
Use AI to enhance listing images (angle correction, lighting, clarity, composition).
•
•Display critical property information visually using charts, meters, and mini-maps.
Provide standard property inquiry and lead generation features.
​
1.3 Intended Audience
•
•
•
•
•
Business stakeholders
Product managers
Web Development team
AI engineering team
QA and operations teams
​
​
2. Overall Description
2.1 Product Perspective
The system will be a web-based property discovery platform consisting of:
•
•Frontend web application
Backend API services
•
•AI image enhancement pipeline
Property database
• Admin management panel
All components will work together to deliver a guided, visual-first property browsing
experience.
​​
​
2.2 User Classes
•
•
•
Visitors (buyers/renters)
Property Administrators (client-side admins)
System Administrators
​
2.3 Operating Environment
•
•
•
Web browsers (desktop and mobile)
Cloud-hosted backend
LLM-based AI services
​
3. Functional Requirements
​
3.1 Home Page
3.1.1 Visual Introduction
​​
The system shall display an aesthetic animated or interactive hero section on the
home page.
​
3.1.2 Guided Property Selection
​​
Instead of a traditional filter system:
• The system shall present users with three guided questions, such as:
•
•
•
Budget (slider-based input)
Property type (flat, villa, plot, commercial)
• Additional preference (BHK, purpose, or location zone)
The system shall generate property results based on these responses.
​
​
3.2 Property Listing Page
​
•
•
•
The system shall display only properties located in Noida.
The system shall not show traditional filter panels to the user.
The system shall rpesent properties as visual cards with :
• AI Enhanced Images
• Key Metrics
• Quick-view graphical indicators
​
3.3 Property Detail Page
​
3.3.1 AI Image Enhancement (Front View Only)
​
•The system shall generate only one AI-enhanced image per property,
representing the front exterior view of the property.
•The AI enhancement pipeline shall:
• Improve lighting and exposure
•
Correct perspective and camera angle distortion
​​
•
•
•
•
• Preserve the original architectural structure and layout
The system shall not generate AI-enhanced images for:
•
•Interior rooms
Floor plans
•
•Surrounding environment
Non-front-facing views
The system shall store:
• Original uploaded images
• One AI-enhanced front-facing image
The enhanced image shall be used primarily for:
•
•
•
Enhance sharpness and clarity
Property listing cards
Hero image on property detail page
• Visual consistency across the website
The primary purpose of the AI-enhanced image is to:
•
•Maintain aesthetic uniformity of the platform
Improve visual quality of poor photography
•Provide a clearer first impression of the property
​
3.3.2 AI Image Disclamer
​
•The system shall display a visible indicator (e.g., “AI Enhanced” label or asterisk)
on all AI-enhanced images.
•The system shall display a disclaimer text stating that:
“This image has been AI-enhanced for visual clarity and presentation. Actual
•
property appearance may vary.”
The disclaimer shall:
•
•Be visible on hover or tap
Be permanently visible on the property detail page
•Not be removable by the user
​
•
The system shall ensure that:
• Original (non-enhanced) images remain accessible to users
•
AI-enhanced images are not represented as real photographs
​
3.3.3 Visual Data Representation
The system shall present property information using graphical components:
​
a. Facing Direction Visualization:
•The System Shall display a compass style widget indicating house
facing direction
•The compass shall include:
• Heat Exposure Indicator (can be a meter).
​​
•Vastu Compatibility Meter.
•Natural Light Intensity Meter
​
​
b. Price vs Area Comparision
•
•
•
The system shall generate a chart comparing:
• Price per square foot of the selected property.
• Price per square foot of similar properties in the system.
The chart units shall be configurable by the user.
The chart shall visually highlight whether the property is:
• Below Average
•
•
Market Average
Above Average
​
​
c. Nearby Amenities Mini-Map
• The system shall display a mini-map for each property.
•
The mini-map shall show nearby:
• Schools
•
•Hospitals
Markets
•
•Metro Stations
Parks
​
3.4 Property Inquiry and Leads
​
•
The system shall allow users to:
• Submit Inquiry forms.
•
•
Request Callbacks.
Save properties for later viewing.
•​
The system shall store all inquiries in the backend.
•The system shall provide admin access to view leads.
​
3.5 Admin Panel
​
•
The system shall allow admins to:
•
•Add, update and remove property listings.
Upload Property images.
•
•Trigger AI image enhancement.​
View inquiries and leads.
​
​​
​
​
4. Non-Functional Requirements
4.1 Performance
•
•
Mobile and web apges shall load withing 3 seconds under nomal conditions..
Graphical Elements shall render withing 1 second of page load.
4.2 Scalability
•The system shall support horizontal scaling.
•The architecture shall support future growth in users and products.
4.3 Security
•
•All data shall be encrypted in transit and at rest.
Authentication and authorization mechanisms shall be implemented.
•The system shall comply with applicable data protection regulations.
4.4 Reliability and Availability
•
•
The system shall maintain 99% uptime.
Backup and failover mechanisms shall be implemented.
4.5 Usability
•The system shall be mobile first.
•The system shall minimize user effor by replacing filters with guided selection.
5. Assumptions and Constraints
•
•The platform only lists properties from Noida.
Image enhancement quality depends on the input image quality.
•
•LLM provider availability is assumed.
Client will provide:
•
•
Property Data
Initial Images
• ​ Guided Question Configuration
​