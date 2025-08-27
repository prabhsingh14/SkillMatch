# SkillMatch: AI-Powered Job Matching Platform

**SkillMatch** is an intelligent job matching platform that connects candidates with employers through advanced AI-driven matching algorithms, resume parsing, and personalized learning recommendations.

## 🚀 Features

### For Candidates
- **Smart Resume Upload & Parsing**: PDF resume analysis with automatic skill extraction
- **OTP & Google Authentication**: Secure login with email OTP or Google OAuth
- **AI-Powered Job Matching**: Intelligent matching based on skills, experience, location, and salary preferences
- **Personalized Learning Paths**: YouTube-based skill development recommendations for missing competencies
- **Match Explanations**: AI-generated explanations of why candidates match specific jobs

### For Employers
- **Company Profile Management**: Complete company profile setup and management
- **Job Posting & Management**: Create, update, and manage job listings
- **Intelligent Candidate Matching**: Find the best candidates using AI-powered matching algorithms
- **Recruiter Intelligence Dashboard**: 
  - Candidate pool analytics
  - Application metrics and insights
  - AI-generated summaries of shortlisted candidates
- **Auto Job Description Parsing**: Extract skills and requirements from job descriptions

### Platform Features
- **External Job Integration**: Fetch jobs from Indian API for expanded opportunities
- **Real-time Analytics**: Dashboard metrics for hiring performance
- **Role-based Access Control**: Separate interfaces for candidates, employers, and admins
- **Scalable Architecture**: Built with Django REST Framework for high performance

## 🛠️ Technology Stack

**Backend:**
- **Django & Django REST Framework**: Robust API development
- **PostgreSQL**: Primary database for data persistence
- **OpenAI GPT**: AI-powered matching explanations and summaries
- **PyPDF2**: Resume text extraction and parsing
- **JWT Authentication**: Secure token-based authentication
- **Cache**: Performance optimization

**External Integrations:**
- **Google OAuth**: Social authentication
- **YouTube API**: Learning resource recommendations
- **Indian Jobs API**: External job data aggregation
- **Email Services**: OTP delivery system

**Key Libraries:**
- `djangorestframework-simplejwt`: JWT token management
- `requests`: External API integration
- `python-decouple`: Environment configuration
- `django-cors-headers`: Cross-origin resource sharing

## Architecture
![Uploading architecture.png…]()


## 📁 Project Structure

```
skillmatch/
├── accounts/          # User management & authentication
├── candidates/        # Candidate profiles & resume handling
├── company/           # Employer profiles & job management
├── applications/      # Job applications & matching logic
├── core/             # Shared models & external job fetching
├── explanations/     # AI-powered match explanations
├── learning/         # Personalized learning paths
└── utils/         # Helper functions & utilities
```

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis (optional, for caching)

### Environment Variables
Create a `.env` file in the project root:

```env
#Security
DEBUG=True
SECRET_KEY=your-secret-key

#Database
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=your-db-host
DB_PORT=your-db-port

#Email
EMAIL_HOST=email-host
EMAIL_PORT=email-port
EMAIL_HOST_USER=your-email-user
EMAIL_HOST_PASSWORD=your-email-password

#Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-secret

#IndianAPI Jobs
INDIANAPI_JOBS_KEY=your-indianapi-jobs-key

#YouTube - for suggesting learning resources
YOUTUBE_API_KEY=your-youtube-api-key

#OpenAI API - for AI-based features
OPENAI_API_KEY=your-openai-key
```

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/skillmatch.git
   cd skillmatch
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## 🔗 API Endpoints

### Authentication
- `POST /api/accounts/users/send-otp/` - Send OTP for login
- `POST /api/accounts/users/verify-otp/` - Verify OTP and login
- `POST /api/accounts/users/google-login/` - Google OAuth login
- `POST /api/accounts/users/logout/` - User logout

### Candidates
- `POST /api/candidates/resumes/upload/` - Upload resume
- `POST /api/candidates/resumes/parse/` - Auto-parse resume
- `GET /api/candidates/resumes/` - List candidate resumes

### Employers
- `POST /api/company/create/` - Create company profile
- `POST /api/company/jobs/create/` - Create job posting
- `GET /api/company/jobs/` - List company jobs
- `GET /api/company/dashboard/metrics/` - Dashboard analytics

### Matching
- `POST /api/applications/match/jobs/` - Find matching jobs for candidate
- `POST /api/applications/match/candidates/` - Find matching candidates for job

### Learning
- `GET /api/learning/candidates/learning-path/` - Get personalized learning path

## 🧠 AI-Powered Matching Algorithm

The matching system uses a weighted scoring algorithm:

- **Skills Match (50%)**: Overlap between candidate skills and job requirements
- **Experience (25%)**: Years of experience vs. job requirements
- **Location (15%)**: Geographic preference alignment
- **Salary (10%)**: Salary expectation vs. job offering

Match scores range from 0-100, providing quantifiable compatibility metrics.

## 📊 Key Features Deep Dive

### Resume Parsing Engine
- Extracts text from PDF resumes using PyPDF2
- Identifies skills using keyword matching from a comprehensive skill database
- Automatically estimates years of experience using regex pattern matching

### Intelligent Dashboard
- Real-time metrics on application conversion rates
- AI-generated summaries of shortlisted candidates using GPT models
- Performance analytics for hiring pipeline optimization

### Learning Path Generation
- Identifies skill gaps between candidates and desired positions
- Curates YouTube learning resources for skill development
- Creates ordered learning sequences for systematic improvement

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 📞 Contact

**Your Name** - prabhsingh1407@gmail.com

**Project Link**: [https://github.com/prabhsingh14/SkillMatch](https://github.com/prabhsingh14/SkillMatch)

---

*Built with Django REST Framework and powered by AI for the future of recruitment.*
